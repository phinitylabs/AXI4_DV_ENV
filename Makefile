# =============================================================================
# AXI4 System-Level Testbench Generation Benchmark - Makefile
# =============================================================================

# Simulator selection
SIM ?= verilator

# Directories
SRC_DIR = sources
VERIF_DIR = verif
BUILD_DIR = build
TESTS_DIR = tests
MUTANTS_DIR = $(TESTS_DIR)/mutants

# Source files
SOURCES = $(wildcard $(SRC_DIR)/*.sv)

# Testbench
TB = $(VERIF_DIR)/axi4_top_tb.sv
SIM_MAIN = $(VERIF_DIR)/sim_main.cpp
TOP = axi4_top_tb

# Verilator settings
VERILATOR_FLAGS = --cc --exe --build -j 0 \
    --timing \
    -Wno-fatal \
    -Wno-WIDTHEXPAND \
    -Wno-WIDTHTRUNC \
    -Wno-TIMESCALEMOD \
    -Wno-INITIALDLY \
    -Wno-UNSIGNED \
    --top-module $(TOP)

VERILATOR_COV_FLAGS = --coverage-line --coverage-toggle

# =============================================================================
# Targets
# =============================================================================

.PHONY: all compile run grade clean help test lint

all: run

# Create build directory
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Get absolute path to project root
PROJECT_ROOT := $(shell pwd)

# Compile with Verilator
compile: $(BUILD_DIR)
	@echo "=== Compiling with Verilator ==="
	verilator $(VERILATOR_FLAGS) $(VERILATOR_COV_FLAGS) \
		--Mdir $(BUILD_DIR)/obj_dir \
		-o Vtb \
		$(addprefix $(PROJECT_ROOT)/,$(SOURCES)) \
		$(PROJECT_ROOT)/$(TB) \
		$(PROJECT_ROOT)/$(SIM_MAIN)
	@echo "=== Compilation successful ==="

# Run simulation
run: compile
	@echo ""
	@echo "=== Running Simulation ==="
	cd $(BUILD_DIR) && ./obj_dir/Vtb
	@echo ""
	@echo "=== Simulation Complete ==="

# Run full grading (pytest)
grade: $(BUILD_DIR)
	@echo "=== Running Full Grading ==="
	python3 -m pytest $(TESTS_DIR)/test_Problem5_axi4_top_tb_hidden.py -v -s

# Run grader directly (without pytest)
grade-direct: $(BUILD_DIR)
	@echo "=== Running Direct Grading ==="
	python3 $(TESTS_DIR)/grader.py --tb $(TB) --sources $(SRC_DIR) --mutants $(MUTANTS_DIR) --build $(BUILD_DIR)

# Run all pytest tests
test:
	python3 -m pytest $(TESTS_DIR)/ -v

# List mutants
mutants:
	@echo "=== Available Mutants ==="
	@ls -1 $(MUTANTS_DIR)/

# Lint check (Verilator only, no build)
lint: $(BUILD_DIR)
	@echo "=== Running Lint Check ==="
	verilator --lint-only -Wall \
		-Wno-WIDTHEXPAND \
		-Wno-WIDTHTRUNC \
		$(SOURCES) $(TB) 2>&1 || true
	@echo "=== Lint Check Complete ==="

# Clean build artifacts
clean:
	rm -rf $(BUILD_DIR)
	rm -f *.vcd
	rm -rf obj_dir
	rm -rf __pycache__
	rm -rf $(TESTS_DIR)/__pycache__
	rm -rf .pytest_cache

# Help
help:
	@echo "AXI4 System-Level Testbench Generation Benchmark"
	@echo ""
	@echo "Targets:"
	@echo "  make          - Compile and run simulation"
	@echo "  make compile  - Compile only"
	@echo "  make run      - Compile and run"
	@echo "  make grade    - Run full 5-phase grading"
	@echo "  make test     - Run all pytest tests"
	@echo "  make mutants  - List available mutants"
	@echo "  make lint     - Run Verilator lint check"
	@echo "  make clean    - Remove build artifacts"
	@echo ""
	@echo "Environment:"
	@echo "  SIM=verilator - Use Verilator (default)"
	@echo ""
	@echo "Prerequisites:"
	@echo "  - Verilator (apt install verilator)"
	@echo "  - Python 3.10+ with pytest"

