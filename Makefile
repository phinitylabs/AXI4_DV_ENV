# =============================================================================
# AXI4 SVA Assertion Generation Benchmark - Makefile
# =============================================================================

# Directories
SRC_DIR = sources
VERIF_DIR = verif
BUILD_DIR = build
TESTS_DIR = tests
MUTANTS_DIR = $(TESTS_DIR)/mutants

# Source files - Package MUST come first
PKG_FILE = $(SRC_DIR)/axi4_pkg.sv
OTHER_SOURCES = $(filter-out $(PKG_FILE), $(wildcard $(SRC_DIR)/*.sv))
SOURCES = $(PKG_FILE) $(OTHER_SOURCES)

# Testbench
TB = $(VERIF_DIR)/axi4_slave_tb.sv
SIM_MAIN = $(VERIF_DIR)/sim_main.cpp
TOP = axi4_slave_tb

# Verilator settings
VERILATOR_FLAGS = --cc --exe --build -j 0 \
    --timing \
    --assert \
    -Wno-fatal \
    -Wno-WIDTHEXPAND \
    -Wno-WIDTHTRUNC \
    -Wno-TIMESCALEMOD \
    -Wno-INITIALDLY \
    -Wno-UNSIGNED \
    --top-module $(TOP)

# =============================================================================
# Targets
# =============================================================================

.PHONY: all compile run grade clean help lint

all: run

# Create build directory
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Get absolute path to project root
PROJECT_ROOT := $(shell pwd)

# Compile with Verilator
compile: $(BUILD_DIR)
	@echo "=== Compiling with Verilator ==="
	verilator $(VERILATOR_FLAGS) \
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

# Run grading
grade: $(BUILD_DIR)
	@echo "=== Running Grading ==="
	python3 -m pytest $(TESTS_DIR)/test_problem3_axi4_sva_hidden.py -v -s

# Run grader directly
grade-direct: $(BUILD_DIR)
	@echo "=== Running Direct Grading ==="
	python3 $(TESTS_DIR)/grader.py --tb $(TB) --sources $(SRC_DIR) --mutants $(MUTANTS_DIR) --build $(BUILD_DIR)

# Lint check only (no build)
lint: $(BUILD_DIR)
	@echo "=== Running Lint Check ==="
	verilator --lint-only -Wall \
	    -Wno-WIDTHEXPAND \
	    -Wno-WIDTHTRUNC \
	    $(SOURCES) $(TB) 2>&1 || true
	@echo "=== Lint Check Complete ==="

# List mutants
mutants:
	@echo "=== Available Mutants ==="
	@ls -1 $(MUTANTS_DIR)/

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
	@echo "AXI4 SVA Assertion Generation Benchmark"
	@echo ""
	@echo "Targets:"
	@echo "  make         - Compile and run simulation"
	@echo "  make compile - Compile only"
	@echo "  make run     - Compile and run"
	@echo "  make grade   - Run full grading (pytest)"
	@echo "  make lint    - Run Verilator lint check"
	@echo "  make mutants - List available mutants"
	@echo "  make clean   - Remove build artifacts"
	@echo ""
	@echo "Prerequisites:"
	@echo "  - Verilator (apt install verilator)"
	@echo "  - Python 3.10+ with pytest"

