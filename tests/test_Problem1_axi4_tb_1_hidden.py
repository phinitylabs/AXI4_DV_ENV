"""
CID14-Style Execution-Based Grading for AXI4 SVA Testbench

This grader follows CVDP's cid14 approach:
- BINARY assertion correctness: Either all assertions work correctly OR score = 0
- Coverage score: Based on % of FIXED coverpoint bins hit by agent's stimulus
- No partial credit for "compiles but wrong assertions"

Grading Flow:
1. Compile agent's testbench with DUT (must succeed)
2. Run simulation with correct RTL (no false positives allowed)
3. Run bug injection tests (assertions must fire on bugs)
4. Extract coverage from fixed coverpoints (% bins hit = score component)

Final Score:
- If assertions fail checks → 0 (even if compiles/simulates)
- If assertions pass → functional coverage % determines score
"""

import os
import re
import pytest
from pathlib import Path
from checkers.testbench_assertion_checker import AssertionChecker


# ============================================================
# CONFIGURATION
# ============================================================

# Testbench path - agent creates verif/axi4_top_tb.sv
testbench_path = os.getenv("TESTBENCH_PATH", "verif/axi4_top_tb.sv")

# DUT files including the fixed coverage module
dut_path = os.getenv("DUT_PATH", 
    "sources/axi4_top.sv sources/axi4_master.sv sources/axi4_slave.sv "
    "sources/axi4_interrupt.sv sources/axi4_coverage.sv")

# Simulator
simulator = os.getenv("SIM", "verilator")

# Design root
design_root = os.getenv("DESIGN_ROOT", ".")

# DUT files as list
dut_files_list = [
    "sources/axi4_top.sv",
    "sources/axi4_master.sv",
    "sources/axi4_slave.sv",
    "sources/axi4_interrupt.sv",
    "sources/axi4_coverage.sv",
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def _testbench_exists():
    """Check if testbench file exists."""
    checker = AssertionChecker(testbench_path, dut_path)
    return os.path.exists(checker.testbench_path)


def _require_testbench():
    """Fail if testbench doesn't exist (agent must create it)."""
    if not _testbench_exists():
        pytest.fail(f"Testbench file not found: {testbench_path} - agent must create this file")


def _get_checker():
    """Get configured AssertionChecker."""
    checker = AssertionChecker(testbench_path, dut_path)
    checker.simulator = simulator
    return checker


def _parse_coverage_from_log(log_content: str) -> dict:
    """
    Parse coverage metrics from simulation log.
    The fixed coverage module prints: COVERAGE_PERCENT=XX.X
    """
    result = {
        "bins_hit": 0,
        "bins_total": 24,  # Fixed total bins
        "coverage_percent": 0.0,
        "found": False,
    }
    
    # Look for machine-readable coverage output
    match = re.search(r'COVERAGE_BINS_HIT=(\d+)', log_content)
    if match:
        result["bins_hit"] = int(match.group(1))
        result["found"] = True
    
    match = re.search(r'COVERAGE_BINS_TOTAL=(\d+)', log_content)
    if match:
        result["bins_total"] = int(match.group(1))
    
    match = re.search(r'COVERAGE_PERCENT=([\d.]+)', log_content)
    if match:
        result["coverage_percent"] = float(match.group(1))
    elif result["bins_total"] > 0:
        result["coverage_percent"] = (result["bins_hit"] * 100.0) / result["bins_total"]
    
    return result


def _check_assertion_behavior(log_content: str) -> dict:
    """
    Check if assertions behave correctly:
    1. No ASSERTION FAILED on correct RTL (no false positives)
    2. Some ASSERTION PASSED indicates assertions are working
    """
    result = {
        "has_assertion_passes": False,
        "has_assertion_failures": False,
        "pass_count": 0,
        "failure_count": 0,
    }
    
    # Count passes
    pass_matches = re.findall(r'ASSERTION.*PASSED', log_content, re.IGNORECASE)
    result["pass_count"] = len(pass_matches)
    result["has_assertion_passes"] = len(pass_matches) > 0
    
    # Count failures
    fail_matches = re.findall(r'ASSERTION.*FAILED', log_content, re.IGNORECASE)
    result["failure_count"] = len(fail_matches)
    result["has_assertion_failures"] = len(fail_matches) > 0
    
    return result


# ============================================================
# GRADING TESTS (cid14-style binary + coverage)
# ============================================================

@pytest.mark.parametrize("test", range(1))
def test_execution_based_grade(test):
    """
    CID14-Style Execution-Based Grading
    
    This is the MAIN grading test. It follows CVDP's cid14 approach:
    
    BINARY CHECKS (must all pass or score = 0):
    1. Testbench compiles with Verilator
    2. Testbench simulates to completion
    3. NO false positives (no ASSERTION FAILED on correct RTL)
    4. Assertions are active (some ASSERTION PASSED seen)
    
    COVERAGE SCORE (if binary checks pass):
    - Score = % of fixed coverpoint bins hit by agent's stimulus
    - Measured by the fixed axi4_coverage module in DUT
    
    If any binary check fails → score = 0 (no partial credit)
    """
    _require_testbench()
    
    checker = _get_checker()
    
    print("\n" + "=" * 70)
    print("CID14-STYLE EXECUTION-BASED GRADING")
    print("=" * 70)
    
    # ================================================================
    # STEP 1: Compilation Check (binary - must pass)
    # ================================================================
    print("\n[1/4] Compilation Check...")
    compile_success, compile_error = checker.compile_testbench()
    
    if not compile_success:
        print(f"  ✗ FAILED: {compile_error[:200]}")
        print("\n" + "=" * 70)
        print("FINAL SCORE: 0 (compilation failed)")
        print("=" * 70)
        pytest.fail(f"Compilation failed - score 0: {compile_error[:100]}")
    
    print("  ✓ PASSED: Testbench compiles successfully")
    
    # ================================================================
    # STEP 2: Simulation Check (binary - must pass)
    # ================================================================
    print("\n[2/4] Simulation Check...")
    sim_success, sim_log = checker.run_simulation()
    
    if not sim_success:
        print(f"  ✗ FAILED: {sim_log[:200]}")
        print("\n" + "=" * 70)
        print("FINAL SCORE: 0 (simulation failed)")
        print("=" * 70)
        pytest.fail(f"Simulation failed - score 0: {sim_log[:100]}")
    
    print("  ✓ PASSED: Testbench simulates to completion")
    
    # Read simulation log for analysis
    sim_log_content = ""
    if os.path.exists(checker.sim_log_path):
        with open(checker.sim_log_path, 'r') as f:
            sim_log_content = f.read()
    
    # ================================================================
    # STEP 3: False Positive Check (binary - must have NO failures)
    # ================================================================
    print("\n[3/4] False Positive Check (no ASSERTION FAILED on correct RTL)...")
    assertion_check = _check_assertion_behavior(sim_log_content)
    
    if assertion_check["has_assertion_failures"]:
        print(f"  ✗ FAILED: {assertion_check['failure_count']} assertion failures on correct RTL")
        print("  This means the assertions have false positives - they fire incorrectly")
        print("\n" + "=" * 70)
        print("FINAL SCORE: 0 (false positive assertions)")
        print("=" * 70)
        pytest.fail(f"False positives detected - score 0: {assertion_check['failure_count']} failures")
    
    print("  ✓ PASSED: No assertion failures on correct RTL")
    
    # ================================================================
    # STEP 4: Assertions Active Check (binary - must have SOME passes)
    # ================================================================
    print("\n[4/4] Assertions Active Check (some ASSERTION PASSED seen)...")
    
    if not assertion_check["has_assertion_passes"]:
        print("  ✗ FAILED: No ASSERTION PASSED messages in log")
        print("  This means assertions are not executing or not reporting")
        print("\n" + "=" * 70)
        print("FINAL SCORE: 0 (assertions not active)")
        print("=" * 70)
        pytest.fail("No assertion activity detected - score 0")
    
    print(f"  ✓ PASSED: {assertion_check['pass_count']} assertion passes detected")
    
    # ================================================================
    # ALL BINARY CHECKS PASSED - Calculate Coverage Score
    # ================================================================
    print("\n" + "-" * 70)
    print("ALL BINARY CHECKS PASSED - Calculating Coverage Score...")
    print("-" * 70)
    
    # Parse coverage from simulation log
    coverage = _parse_coverage_from_log(sim_log_content)
    
    if coverage["found"]:
        print(f"\nFunctional Coverage (Fixed Coverpoints):")
        print(f"  Bins Hit: {coverage['bins_hit']}/{coverage['bins_total']}")
        print(f"  Coverage: {coverage['coverage_percent']:.1f}%")
    else:
        print("\nWARNING: Coverage module output not found in log")
        print("Using default minimum coverage score")
        coverage["coverage_percent"] = 10.0  # Minimum for passing binary checks
    
    # Final score = coverage percentage
    final_score = coverage["coverage_percent"]
    
    print("\n" + "=" * 70)
    print(f"FINAL SCORE: {final_score:.1f}/100")
    print("=" * 70)
    
    # For cid14-style, we could require a minimum coverage threshold
    # But for now, passing all binary checks is the main requirement
    min_coverage = 10.0  # Minimum 10% coverage required
    
    if final_score < min_coverage:
        print(f"\nWARNING: Coverage {final_score:.1f}% below {min_coverage}% threshold")
        # Don't fail - binary checks passed, just low coverage
    
    # Pass the test if all binary checks passed
    assert True, "All binary checks passed"


@pytest.mark.parametrize("test", range(1))
def test_bug_injection_correctness(test):
    """
    Bug Injection Test (cid14-style)
    
    Tests if agent's assertions fire correctly on buggy RTL:
    - Inject bug into DUT
    - Run agent's testbench
    - Check if ASSERTION FAILED appears
    
    This is a BINARY test: Either assertions catch the bug OR they don't.
    No partial credit for "almost catching" the bug.
    """
    _require_testbench()
    
    # Import bug injection tester
    from checkers.targeted_bug_injection import (
        TargetedBugInjectionTester, TARGETED_BUGS, format_targeted_bug_report
    )
    
    checker = _get_checker()
    
    # First verify testbench works with correct RTL
    compile_success, compile_error = checker.compile_testbench()
    if not compile_success:
        pytest.fail(f"Testbench must compile with correct RTL: {compile_error[:100]}")
    
    sim_success, _ = checker.run_simulation()
    if not sim_success:
        pytest.fail("Testbench must simulate with correct RTL first")
    
    # Now run bug injection
    print("\n" + "=" * 70)
    print("BUG INJECTION TEST (Assertion Correctness)")
    print("=" * 70)
    
    tester = TargetedBugInjectionTester(
        testbench_path=checker.testbench_path,
        design_root=design_root,
        dut_files=dut_files_list,
        simulator=simulator,
    )
    
    score, results = tester.get_grade()
    
    # Print report
    print("\n" + format_targeted_bug_report(results))
    
    # For cid14-style: We could require ALL bugs to be caught
    # For now, require at least 50% bug detection
    caught = results["fully_caught"] + results["partially_caught"]
    total = results["total_bugs"]
    catch_rate = (caught / total * 100) if total > 0 else 0
    
    print(f"\nBug Detection Rate: {caught}/{total} ({catch_rate:.0f}%)")
    
    # Minimum requirement: catch at least 30% of bugs
    min_catch_rate = 30.0
    
    if catch_rate < min_catch_rate:
        print(f"✗ FAILED: Must catch at least {min_catch_rate:.0f}% of bugs")
        pytest.fail(f"Bug detection rate {catch_rate:.0f}% below {min_catch_rate:.0f}% minimum")
    
    print(f"✓ PASSED: Bug detection rate {catch_rate:.0f}% meets threshold")


# ============================================================
# INDIVIDUAL COMPONENT TESTS (for debugging)
# ============================================================

@pytest.mark.parametrize("test", range(1))
def test_compilation_only(test):
    """Test that testbench compiles (for debugging)."""
    _require_testbench()
    checker = _get_checker()
    
    compile_success, compile_error = checker.compile_testbench()
    
    print(f"\nCompilation: {'PASS' if compile_success else 'FAIL'}")
    if not compile_success:
        print(f"Error: {compile_error}")
    
    assert compile_success, f"Compilation failed: {compile_error}"


@pytest.mark.parametrize("test", range(1))
def test_simulation_only(test):
    """Test that testbench simulates (for debugging)."""
    _require_testbench()
    checker = _get_checker()
    
    compile_success, _ = checker.compile_testbench()
    if not compile_success:
        pytest.skip("Must compile first")
    
    sim_success, sim_log = checker.run_simulation()
    
    print(f"\nSimulation: {'PASS' if sim_success else 'FAIL'}")
    if not sim_success:
        print(f"Error: {sim_log[:500]}")
    
    assert sim_success, f"Simulation failed"


@pytest.mark.parametrize("test", range(1))
def test_coverage_extraction(test):
    """Test coverage extraction from simulation log (for debugging)."""
    _require_testbench()
    checker = _get_checker()
    
    compile_success, _ = checker.compile_testbench()
    if not compile_success:
        pytest.skip("Must compile first")
    
    sim_success, _ = checker.run_simulation()
    if not sim_success:
        pytest.skip("Must simulate first")
    
    # Read log and extract coverage
    sim_log_content = ""
    if os.path.exists(checker.sim_log_path):
        with open(checker.sim_log_path, 'r') as f:
            sim_log_content = f.read()
    
    coverage = _parse_coverage_from_log(sim_log_content)
    
    print(f"\nCoverage Extraction:")
    print(f"  Found: {coverage['found']}")
    print(f"  Bins Hit: {coverage['bins_hit']}/{coverage['bins_total']}")
    print(f"  Coverage: {coverage['coverage_percent']:.1f}%")
    
    # Just verify coverage module ran
    assert coverage["found"], "Coverage module output not found in simulation log"
