#!/bin/bash
# Convert test4 problem to HUD format and push to GitHub
# This script creates the three branches and pushes them

set -e

PROBLEM_ID="axi4_slave_sva"
GITHUB_REPO="https://github.com/praveensaravanan30/test4"

echo "=========================================="
echo "Converting to HUD Format"
echo "Problem ID: $PROBLEM_ID"
echo "GitHub Repo: $GITHUB_REPO"
echo "=========================================="

# Step 1: Create HUD directory structure
echo ""
echo "[1/12] Creating HUD directory structure..."
mkdir -p sources
mkdir -p tests/checkers
mkdir -p verif
mkdir -p docs
echo "  ✓ Created directories"

# Step 2: Copy golden RTL to sources/
echo ""
echo "[2/12] Copying golden RTL to sources/..."
if [ -d "harness/patch/rtl" ]; then
    cp -f harness/patch/rtl/*.sv sources/ 2>/dev/null || true
    echo "  ✓ Copied RTL files to sources/"
else
    echo "  ⚠ Warning: harness/patch/rtl/ not found, using rtl/ instead"
    cp -f rtl/*.sv sources/ 2>/dev/null || true
fi

# Step 3: Copy grading scripts to tests/
echo ""
echo "[3/12] Setting up tests/ directory..."
if [ -f "harness/patch/tests/pytest_testbench_assertions.py" ]; then
    cp -f harness/patch/tests/pytest_testbench_assertions.py tests/test_axi4_slave_sva_hidden.py
    echo "  ✓ Copied pytest_testbench_assertions.py to tests/test_axi4_slave_sva_hidden.py"
    
    # Update paths in test file for axi4_slave task
    # Change testbench path to verif/axi4_slave_tb.sv
    sed -i 's|verif/agent_tb.sv|verif/axi4_slave_tb.sv|g' tests/test_axi4_slave_sva_hidden.py
    # Change DUT path to sources/axi4_slave.sv (single module for slave task)
    sed -i 's|DUT_PATH.*rtl/axi4_top.sv.*rtl/axi4_interrupt.sv|DUT_PATH", "sources/axi4_slave.sv|g' tests/test_axi4_slave_sva_hidden.py
    sed -i 's|rtl/axi4_slave.sv|sources/axi4_slave.sv|g' tests/test_axi4_slave_sva_hidden.py
    echo "  ✓ Updated paths to use sources/ and verif/axi4_slave_tb.sv"
fi

# Step 4: Copy checkers
echo ""
echo "[4/12] Setting up tests/checkers/..."
if [ -f "harness/patch/tests/checkers/testbench_assertion_checker.py" ]; then
    cp -f harness/patch/tests/checkers/testbench_assertion_checker.py tests/checkers/
    echo "  ✓ Copied testbench_assertion_checker.py"
    
    # Update checker to include sources/ in search paths
    if ! grep -q '"sources"' tests/checkers/testbench_assertion_checker.py; then
        sed -i 's|"rtl",|"rtl",\n            "sources",  # HUD format|' tests/checkers/testbench_assertion_checker.py
        echo "  ✓ Updated checker to support sources/ path"
    fi
fi

# Create __init__.py
cat > tests/checkers/__init__.py << 'EOF'
"""
Checkers module for DV task grading.
"""
from .testbench_assertion_checker import AssertionChecker, grade_generated_testbench
__all__ = ["AssertionChecker", "grade_generated_testbench"]
EOF
echo "  ✓ Created __init__.py"

# Step 5: Create pyproject.toml if not exists
echo ""
echo "[5/12] Checking pyproject.toml..."
if [ ! -f "pyproject.toml" ]; then
    cat > pyproject.toml << 'EOF'
[project]
name = "axi4-slave-sva"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "pytest>=7.0.0",
    "pytest-xdist>=3.0.0",
]
EOF
    echo "  ✓ Created pyproject.toml"
else
    echo "  ✓ pyproject.toml already exists"
fi

# Step 6: Create README if not exists
echo ""
echo "[6/12] Checking README.md..."
if [ ! -f "README.md" ]; then
    cat > README.md << 'EOF'
# AXI4 Slave SVA Task

## Task Description

Create a SystemVerilog testbench for the AXI4 slave module with assertions.

The agent should create `verif/axi4_slave_tb.sv` that:
1. Instantiates the DUT (`sources/axi4_slave.sv`)
2. Contains assertions to verify AXI4 behavior
3. Provides test stimulus
4. Compiles and simulates successfully

## Directory Structure

- `sources/` - RTL files (golden implementation)
- `verif/` - Testbench directory (agent creates testbench here)
- `tests/` - Hidden grading scripts
- `docs/` - Documentation

## Running Tests

```bash
pytest tests/test_axi4_slave_sva_hidden.py -v
```
EOF
    echo "  ✓ Created README.md"
else
    echo "  ✓ README.md already exists"
fi

# Step 7: Initialize git if not done
echo ""
echo "[7/12] Setting up git repository..."
if [ ! -d ".git" ]; then
    git init
    git config user.email "praveensaravanan30@users.noreply.github.com" || true
    git config user.name "Praveen Saravanan" || true
    echo "  ✓ Initialized git repository"
else
    echo "  ✓ Git repository already exists"
fi

# Step 8: Create baseline branch
echo ""
echo "[8/12] Creating baseline branch..."
git checkout -b ${PROBLEM_ID}_baseline 2>/dev/null || {
    echo "  Branch exists, checking it out..."
    git checkout ${PROBLEM_ID}_baseline
}

# Remove tests directory (CRITICAL for baseline)
rm -rf tests/
echo "  ✓ Removed tests/ directory"

# Ensure verif/ is empty
rm -rf verif/
mkdir -p verif
echo "  ✓ Created empty verif/ directory"

# Add files (sources, docs, pyproject.toml, README, empty verif)
git add sources/*.sv 2>/dev/null || true
git add docs/ 2>/dev/null || true
git add pyproject.toml README.md 2>/dev/null || true
git add verif/ 2>/dev/null || true

# Commit
git commit -m "Baseline: Golden RTL in sources/, empty verif/, no tests" || echo "  (No changes to commit)"
echo "  ✓ Created baseline branch"

# Step 9: Create test branch
echo ""
echo "[9/12] Creating test branch..."
git checkout -b ${PROBLEM_ID}_test 2>/dev/null || {
    echo "  Branch exists, checking it out..."
    git checkout ${PROBLEM_ID}_test
}

# Restore tests directory structure
mkdir -p tests/checkers

# Copy checkers if needed
if [ -f "harness/patch/tests/checkers/testbench_assertion_checker.py" ]; then
    cp -f harness/patch/tests/checkers/testbench_assertion_checker.py tests/checkers/ 2>/dev/null || true
fi

# Update checker
if [ -f "tests/checkers/testbench_assertion_checker.py" ] && ! grep -q '"sources"' tests/checkers/testbench_assertion_checker.py; then
    sed -i 's|"rtl",|"rtl",\n            "sources",  # HUD format|' tests/checkers/testbench_assertion_checker.py
fi

# Create __init__.py
cat > tests/checkers/__init__.py << 'EOF'
"""
Checkers module for DV task grading.
"""
from .testbench_assertion_checker import AssertionChecker, grade_generated_testbench
__all__ = ["AssertionChecker", "grade_generated_testbench"]
EOF

# Copy test file
if [ -f "harness/patch/tests/pytest_testbench_assertions.py" ]; then
    cp -f harness/patch/tests/pytest_testbench_assertions.py tests/test_axi4_slave_sva_hidden.py
    # Update paths for axi4_slave task
    sed -i 's|verif/agent_tb.sv|verif/axi4_slave_tb.sv|g' tests/test_axi4_slave_sva_hidden.py
    sed -i 's|DUT_PATH.*rtl/axi4_top.sv.*rtl/axi4_interrupt.sv|DUT_PATH", "sources/axi4_slave.sv|g' tests/test_axi4_slave_sva_hidden.py
    sed -i 's|rtl/axi4_slave.sv|sources/axi4_slave.sv|g' tests/test_axi4_slave_sva_hidden.py
fi

git add tests/
git commit -m "Test branch: Add hidden grading tests" || echo "  (No changes to commit)"
echo "  ✓ Created test branch"

# Step 10: Create golden branch
echo ""
echo "[10/12] Creating golden branch..."
git checkout ${PROBLEM_ID}_baseline
git checkout -b ${PROBLEM_ID}_golden 2>/dev/null || {
    echo "  Branch exists, checking it out..."
    git checkout ${PROBLEM_ID}_golden
}

# Verify no tests directory
if [ -d "tests" ]; then
    rm -rf tests/
    echo "  ✓ Removed tests/ directory from golden"
fi

# For DV tasks, golden branch should have golden testbench in verif/
# Check for slave-specific golden testbench
if [ -f "harness/patch/tests/axi4_slave_tb_golden.sv" ]; then
    cp harness/patch/tests/axi4_slave_tb_golden.sv verif/axi4_slave_tb_golden.sv
    echo "  ✓ Added golden testbench to verif/"
else
    echo "  ⚠ Note: No axi4_slave_tb_golden.sv found, leaving verif/ empty"
    echo "  (You may want to create a golden testbench for axi4_slave)"
fi

git add sources/ docs/ pyproject.toml README.md verif/ 2>/dev/null || true
git commit -m "Golden: Golden RTL + golden testbench, no tests" || echo "  (No changes to commit)"
echo "  ✓ Created golden branch"

# Step 11: Set up GitHub remote
echo ""
echo "[11/12] Setting up GitHub remote..."
git remote remove origin 2>/dev/null || true
git remote add origin ${GITHUB_REPO} 2>/dev/null || {
    echo "  Remote already exists, updating URL..."
    git remote set-url origin ${GITHUB_REPO}
}
echo "  ✓ GitHub remote configured"

# Step 12: Push to GitHub
echo ""
echo "[12/12] Pushing branches to GitHub..."
echo "  This will push:"
echo "    - ${PROBLEM_ID}_baseline"
echo "    - ${PROBLEM_ID}_test"
echo "    - ${PROBLEM_ID}_golden"
echo ""
read -p "  Push to GitHub now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push -u origin ${PROBLEM_ID}_baseline || echo "  ⚠ Failed to push baseline"
    git push -u origin ${PROBLEM_ID}_test || echo "  ⚠ Failed to push test"
    git push -u origin ${PROBLEM_ID}_golden || echo "  ⚠ Failed to push golden"
    echo "  ✓ Pushed to GitHub"
else
    echo "  Skipped push. Run manually:"
    echo "    git push -u origin ${PROBLEM_ID}_baseline"
    echo "    git push -u origin ${PROBLEM_ID}_test"
    echo "    git push -u origin ${PROBLEM_ID}_golden"
fi

# Summary
echo ""
echo "=========================================="
echo "Conversion Complete!"
echo "=========================================="
echo ""
echo "Branches created:"
git branch | grep ${PROBLEM_ID} || echo "  (No branches found)"
echo ""
echo "Directory structure:"
echo "  sources/ - Golden RTL (all branches)"
echo "  verif/ - Empty in baseline/test, golden testbench in golden"
echo "  tests/ - Only in test branch (grading scripts)"
echo "  docs/ - Documentation"
echo ""
echo "Note: harness/ directory is NOT pushed to GitHub"
echo ""
echo "To push manually:"
echo "  git push -u origin ${PROBLEM_ID}_baseline"
echo "  git push -u origin ${PROBLEM_ID}_test"
echo "  git push -u origin ${PROBLEM_ID}_golden"
echo ""

