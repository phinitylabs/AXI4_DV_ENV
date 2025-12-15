"""
Enhanced Test Runner for Grading Generated Testbenches with Assertions.

VERILATOR-BASED GRADING SYSTEM
==============================

This comprehensive test runner uses Verilator as the default simulator for:
- Better SystemVerilog support
- Stricter syntax checking
- Proper SVA (SystemVerilog Assertions) evaluation
- Built-in coverage capabilities (line, toggle, branch)

Test Workflow:
1. Compiles and simulates testbench with Verilator --binary
2. Verifies REQUIRED assertions execute (from prompt) by checking logs
3. Checks protocol coverage (AXI4 channels)
4. Analyzes code coverage using Verilator's coverage instrumentation
5. Tests bug detection capability (functional correctness)
6. Calculates weighted final score

Grading Breakdown (8 categories, 100% total):
- Compilation: 5%
- Simulation: 5%
- Required Assertions (from prompt): 15%
- Functional Correctness: 10%
- Protocol Coverage: 10%
- Assertion Execution: 10%
- Code Coverage (Verilator): 15%  <-- NEW
- Bug Detection (Functional): 30%

Simulator: Verilator (default) or Icarus (fallback)
"""

import os
import pytest
from pathlib import Path
from checkers.testbench_assertion_checker import grade_generated_testbench, AssertionChecker
from checkers.protocol_coverage_checker import (
    AXI4ProtocolCoverageChecker,
    check_protocol_coverage,
    format_coverage_report,
)
from checkers.bug_injection_tester import (
    AXI4BugInjectionTester,
    test_bug_detection,
    format_bug_detection_report,
)
from checkers.assertion_requirement_checker import (
    AssertionRequirementChecker,
    check_required_assertions,
    format_assertion_requirement_report,
    REQUIRED_ASSERTIONS,
)
from checkers.targeted_bug_injection import (
    TargetedBugInjectionTester,
    format_targeted_bug_report,
    TARGETED_BUGS,
)
from checkers.functional_correctness_checker import (
    FunctionalCorrectnessChecker,
    format_functional_correctness_report,
)
from checkers.verilator_coverage_checker import (
    VerilatorCoverageChecker,
    analyze_verilator_coverage,
    format_coverage_report as format_verilator_coverage_report,
)

# Fetch environment variables
# Testbench path - agent creates verif/axi4_top_tb.sv
# For grading, we check both possible names (agent-created and golden reference)
_default_tb = "verif/axi4_top_tb.sv"
if not os.path.exists(_default_tb):
    _default_tb = "verif/axi4_top_tb_golden.sv"  # Fallback to golden for testing
testbench_path = os.getenv("TESTBENCH_PATH", _default_tb)
dut_path = os.getenv("DUT_PATH", "sources/axi4_top.sv sources/axi4_master.sv sources/axi4_slave.sv sources/axi4_interrupt.sv")
simulator = os.getenv("SIM", "verilator")
require_assertions = os.getenv("REQUIRE_ASSERTIONS", "true").lower() == "true"
enable_bug_injection = os.getenv("ENABLE_BUG_INJECTION", "true").lower() == "true"
enable_protocol_coverage = os.getenv("ENABLE_PROTOCOL_COVERAGE", "true").lower() == "true"

# Design root for bug injection
design_root = os.getenv("DESIGN_ROOT", ".")

# DUT files as list for bug injection
dut_files_list = [
    "sources/axi4_top.sv",
    "sources/axi4_master.sv",
    "sources/axi4_slave.sv",
    "sources/axi4_interrupt.sv",
]


# Helper to check if testbench exists (underscore prefix to avoid pytest collection)
def _testbench_exists():
    """Check if testbench file exists (with path resolution)."""
    checker = AssertionChecker(testbench_path, dut_path)
    return os.path.exists(checker.testbench_path)


def _require_testbench():
    """
    Fail the test if testbench doesn't exist.
    
    IMPORTANT: We use pytest.fail() instead of pytest.skip() because:
    - A missing testbench is a FAILURE (agent didn't create submission)
    - pytest.skip() would be treated as "pass" by the validation framework
    - This ensures validation correctly identifies missing submissions
    """
    if not _testbench_exists():
        pytest.fail(f"Testbench file not found: {testbench_path} - agent must create this file")


def _get_checker():
    """Get a configured AssertionChecker instance."""
    checker = AssertionChecker(testbench_path, dut_path)
    checker.simulator = simulator
    return checker


# ============================================================
# REQUIRED ASSERTIONS TEST (Log-based verification)
# This test verifies the SPECIFIC assertions from the prompt
# ============================================================

@pytest.mark.parametrize("test", range(1))
def test_required_assertions_present(test):
    """
    Test that the testbench implements the REQUIRED assertions from the prompt.
    Weight: 20%
    
    This test:
    1. Compiles and runs the testbench against golden RTL
    2. Parses the simulation log for assertion messages
    3. Verifies that required protocol checks are executed
    
    Required assertions (from prompt):
    - VALID signal stability (AWVALID, WVALID, ARVALID, BVALID, RVALID)
    - LAST signal correctness (WLAST, RLAST)
    - Response code validation (BRESP, RRESP)
    - Timing relationships (write response after data, read data after address)
    """
    _require_testbench()
    
    checker = _get_checker()
    
    # First compile and simulate to generate logs
    print(f"\n=== Required Assertions Verification ===")
    print(f"Testbench: {checker.testbench_path}")
    print(f"Simulator: {checker.simulator}")
    
    compile_success, compile_error = checker.compile_testbench()
    if not compile_success:
        pytest.fail(f"Testbench must compile to verify assertions: {compile_error}")
    
    sim_success, sim_log = checker.run_simulation()
    if not sim_success:
        pytest.fail(f"Testbench must simulate to verify assertions: {sim_log[:200]}")
    
    # Read simulation log
    sim_log_content = ""
    if os.path.exists(checker.sim_log_path):
        with open(checker.sim_log_path, 'r') as f:
            sim_log_content = f.read()
    
    # Check required assertions
    req_checker = AssertionRequirementChecker(checker.testbench_path)
    req_checker.set_simulation_log(sim_log_content)
    
    score, details = req_checker.get_score()
    
    # Print report
    print(format_assertion_requirement_report(details))
    
    # Count verified assertions
    verified = details["verified_assertions"]
    total = details["total_assertions"]
    
    print(f"Required Assertions: {verified}/{total} verified")
    print(f"Score: {score:.1f}%")
    
    # Must verify at least 50% of required assertions
    min_required = total * 0.5
    assert verified >= min_required, \
        f"Must verify at least {int(min_required)} required assertions, only verified {verified}/{total}"
    
    assert score >= 50.0, \
        f"Required assertions score {score:.1f}% below 50% minimum"


# ============================================================
# PROTOCOL COVERAGE TEST
# ============================================================

@pytest.mark.parametrize("test", range(1))
def test_protocol_coverage(test):
    """
    Test that checks AXI4 protocol coverage in testbench.
    Weight: 20%
    
    Checks:
    - All 5 AXI4 channels monitored (AW, W, B, AR, R)
    - Required protocol checks present (handshakes, VALID stability, etc.)
    """
    _require_testbench()
    
    if not enable_protocol_coverage:
        pytest.skip("Protocol coverage checking disabled")
    
    checker = _get_checker()
    coverage_checker = AXI4ProtocolCoverageChecker(checker.testbench_path)
    
    score, details = coverage_checker.get_coverage_grade()
    
    # Print report
    print("\n" + format_coverage_report(details))
    
    # Assertions
    assert details["channels_covered"] >= 3, \
        f"Must cover at least 3 AXI4 channels, found {details['channels_covered']}"
    
    assert details["checks_found"] >= 5, \
        f"Must have at least 5 protocol checks, found {details['checks_found']}"
    
    # Required checks should be present for a good testbench
    required_ratio = details["required_checks_found"] / max(details["required_checks_total"], 1)
    assert required_ratio >= 0.5, \
        f"Must have at least 50% of required protocol checks, found {required_ratio*100:.0f}%"
    
    assert score >= 50.0, \
        f"Protocol coverage score {score:.1f}% below 50%"


# ============================================================
# COMPILATION AND SIMULATION TESTS
# ============================================================

@pytest.mark.parametrize("test", range(1))
def test_testbench_compiles(test):
    """
    Test that generated testbench compiles successfully.
    Weight: 10%
    """
    _require_testbench()
    
    checker = _get_checker()
    
    print(f"\n=== Compilation Check ===")
    print(f"Testbench: {checker.testbench_path}")
    print(f"Simulator: {checker.simulator}")
    if checker.dut_path:
        print(f"DUT: {checker.dut_path}")
    
    compile_success, compile_error = checker.compile_testbench()
    
    if compile_success:
        print("Compilation: PASS")
    else:
        print(f"Compilation: FAIL")
        print(f"Error: {compile_error}")
    
    assert compile_success, f"Testbench compilation failed: {compile_error}"


@pytest.mark.parametrize("test", range(1))
def test_testbench_simulates(test):
    """
    Test that generated testbench simulates successfully.
    Weight: 10%
    """
    _require_testbench()
    
    checker = _get_checker()
    
    # First compile
    compile_success, compile_error = checker.compile_testbench()
    if not compile_success:
        pytest.skip(f"Testbench must compile first: {compile_error}")
    
    # Then simulate
    sim_success, sim_log = checker.run_simulation()
    
    print(f"\n=== Simulation Check ===")
    if sim_success:
        print("Simulation: PASS")
        print(f"Log length: {len(sim_log)} characters")
    else:
        print(f"Simulation: FAIL")
        print(f"Error: {sim_log[:500]}")
    
    assert sim_success, f"Testbench simulation failed: {sim_log[:200]}"


@pytest.mark.parametrize("test", range(1))
def test_assertions_execute(test):
    """
    Test that assertions in testbench are executed during simulation.
    Weight: 15%
    """
    _require_testbench()
    
    checker = _get_checker()
    
    # Compile and simulate
    compile_success, compile_error = checker.compile_testbench()
    if not compile_success:
        pytest.skip(f"Testbench must compile first: {compile_error}")
    
    sim_success, sim_log = checker.run_simulation()
    if not sim_success:
        pytest.skip(f"Testbench must simulate first: {sim_log[:200]}")
    
    # Check assertions in log
    log_check = checker.check_assertions_in_log()
    
    print(f"\n=== Assertion Execution Check ===")
    print(f"Assertions Executed: {log_check['assertions_executed']}")
    print(f"Assertion Passes: {log_check['assertion_passes']}")
    print(f"Assertion Failures: {log_check['assertion_failures']}")
    
    if require_assertions:
        assert log_check['assertions_executed'], \
            "Assertions were not executed during simulation"
        
        # Assertions should have been evaluated (passes or failures)
        total_assertions = log_check['assertion_passes'] + log_check['assertion_failures']
        assert total_assertions > 0, \
            "No assertion activity detected in simulation log"


# ============================================================
# FUNCTIONAL CORRECTNESS TEST (Testbench works with correct RTL)
# ============================================================

@pytest.mark.parametrize("test", range(1))
def test_functional_correctness(test):
    """
    Test that the testbench is functionally correct with CORRECT RTL.
    
    This verifies:
    1. NO FALSE POSITIVES: Assertions don't fail on correct RTL
    2. TRANSACTIONS OCCUR: Write and read transactions happen
    3. ALL CHANNELS ACTIVE: All 5 AXI channels are exercised
    4. SIMULATION COMPLETES: Simulation finishes properly
    
    A testbench that fails on correct RTL is buggy!
    """
    _require_testbench()
    
    checker = _get_checker()
    
    # Compile and simulate against correct RTL
    compile_success, compile_error = checker.compile_testbench()
    if not compile_success:
        pytest.fail(f"Testbench must compile: {compile_error}")
    
    sim_success, sim_log = checker.run_simulation()
    if not sim_success:
        pytest.fail(f"Testbench must simulate: {sim_log[:200]}")
    
    # Read simulation log
    sim_log_content = ""
    if os.path.exists(checker.sim_log_path):
        with open(checker.sim_log_path, 'r') as f:
            sim_log_content = f.read()
    
    # Check functional correctness
    print(f"\n=== Functional Correctness Check ===")
    print(f"Verifying testbench works correctly with CORRECT RTL...")
    
    fc_checker = FunctionalCorrectnessChecker(sim_log_content)
    score, details = fc_checker.get_score()
    
    # Print report
    print(format_functional_correctness_report(details))
    
    # Assertions
    # Should have some assertion passes
    assert details["assertion_passes"] > 0, \
        "No assertions passed - testbench may not have working assertions"
    
    # Transactions should occur
    assert details["transactions_occur"], \
        "No transactions observed - testbench does not exercise DUT"
    
    # Simulation should complete
    assert details["simulation_completes"], \
        "Simulation did not complete properly"
    
    # Score should be reasonable
    assert score >= 50.0, \
        f"Functional correctness score {score:.1f}% below 50% minimum"
    
    print(f"\nFunctional Correctness Score: {score:.1f}%")


# ============================================================
# TARGETED BUG INJECTION TEST (Testbench catches specific bugs)
# ============================================================

@pytest.mark.parametrize("test", range(1))
def test_bug_detection(test):
    """
    Test that testbench catches SPECIFIC bugs related to prompt requirements.
    Weight: 25%
    
    This tests if the agent's assertions catch the RIGHT bugs:
    - Each bug targets a specific requirement from the prompt
    - Full credit (1.0): Bug caught with the CORRECT assertion
    - Partial credit (0.5): Bug caught with ANY assertion
    - No credit (0.0): Bug not caught
    
    Example:
    - Prompt says: "AWVALID must remain stable until AWREADY"
    - We inject bug: AWVALID becomes unstable
    - Expected: Assertion about AWVALID stability should fail
    """
    _require_testbench()
    
    if not enable_bug_injection:
        pytest.skip("Bug injection testing disabled")
    
    checker = _get_checker()
    
    # First verify testbench works with correct RTL
    compile_success, _ = checker.compile_testbench()
    if not compile_success:
        pytest.skip("Testbench must compile with correct RTL first")
    
    sim_success, _ = checker.run_simulation()
    if not sim_success:
        pytest.skip("Testbench must simulate with correct RTL first")
    
    # Now test TARGETED bug detection
    print(f"\n=== Targeted Bug Injection Testing ===")
    print(f"Testing if assertions catch SPECIFIC bugs from prompt requirements...")
    
    tester = TargetedBugInjectionTester(
        testbench_path=checker.testbench_path,
        design_root=design_root,
        dut_files=dut_files_list,
        simulator=simulator,
    )
    
    score, results = tester.get_grade()
    
    # Print detailed report
    print("\n" + format_targeted_bug_report(results))
    
    # Assertions
    assert results["total_bugs"] > 0, \
        "Bug injection test setup failed - no bugs tested"
    
    # Must catch at least some bugs
    caught = results["fully_caught"] + results["partially_caught"]
    assert caught > 0, \
        f"Testbench caught 0 bugs - must catch at least 1"
    
    # Minimum 30% detection score for passing
    assert score >= 30.0, \
        f"Bug detection score {score:.1f}% below 30% minimum"
    
    print(f"\nTargeted Bug Detection Score: {score:.1f}%")
    print(f"  Fully caught (correct assertion): {results['fully_caught']}")
    print(f"  Partially caught (any assertion): {results['partially_caught']}")
    print(f"  Missed: {results['missed']}")


# ============================================================
# CODE COVERAGE TEST (Verilator-based coverage analysis)
# ============================================================

@pytest.mark.parametrize("test", range(1))
def test_code_coverage(test):
    """
    Test that the testbench achieves adequate code coverage on the DUT.
    Weight: 15%
    
    Uses Verilator's built-in coverage instrumentation to measure:
    - Line coverage: Which lines of DUT code are executed
    - Toggle coverage: Which signals are toggled during simulation
    - Branch coverage: Which branches are taken in conditional statements
    
    This ensures the testbench actually exercises the DUT thoroughly,
    not just checking a few trivial cases.
    """
    _require_testbench()
    
    checker = _get_checker()
    
    # First verify testbench compiles and simulates
    compile_success, compile_error = checker.compile_testbench()
    if not compile_success:
        pytest.skip(f"Testbench must compile first: {compile_error}")
    
    sim_success, _ = checker.run_simulation()
    if not sim_success:
        pytest.skip("Testbench must simulate first")
    
    print(f"\n=== Code Coverage Analysis (Verilator) ===")
    print(f"Testbench: {checker.testbench_path}")
    print(f"Analyzing coverage on DUT files...")
    
    # Run coverage analysis
    cov_checker = VerilatorCoverageChecker(
        testbench_path=checker.testbench_path,
        dut_files=dut_files_list,
        design_root=design_root,
    )
    
    score, details = cov_checker.get_coverage_grade()
    
    # Print report
    print(format_verilator_coverage_report(details))
    
    print(f"Coverage Score: {score:.1f}%")
    print(f"  Line Coverage: {details['line_coverage']:.1f}%")
    print(f"  Toggle Coverage: {details['toggle_coverage']:.1f}%")
    print(f"  Branch Coverage: {details['branch_coverage']:.1f}%")
    
    # Assertions - require minimum coverage
    # Note: These are lenient thresholds since not all code can be covered
    assert score >= 20.0, \
        f"Code coverage score {score:.1f}% below 20% minimum"
    
    # At least some line coverage is required
    assert details['line_coverage'] >= 10.0, \
        f"Line coverage {details['line_coverage']:.1f}% too low - testbench must exercise DUT"


# ============================================================
# COMPREHENSIVE GRADING TEST
# ============================================================

@pytest.mark.parametrize("test", range(1))
def test_comprehensive_grade(test):
    """
    Comprehensive test that grades the entire testbench with weighted scoring.
    
    Score Breakdown (8 categories, 100% total):
    - Compilation: 5%
    - Simulation: 5%
    - Required Assertions: 15%
    - Functional Correctness: 10%
    - Protocol Coverage: 10%
    - Assertion Execution: 10%
    - Code Coverage: 15%  (NEW: Verilator-based coverage)
    - Bug Detection: 30%
    
    Pass threshold: 60% overall
    """
    _require_testbench()
    
    checker = _get_checker()
    
    scores = {}
    weights = {
        "compilation": 5,
        "simulation": 5,
        "required_assertions": 15,
        "functional_correctness": 10,
        "protocol_coverage": 10,
        "assertion_execution": 10,
        "code_coverage": 15,  # NEW: Verilator coverage
        "bug_detection": 30,
    }
    
    print("\n" + "=" * 60)
    print("COMPREHENSIVE TESTBENCH GRADING")
    print("=" * 60)
    
    # 1. Compilation (10%) - Do this first
    compile_success, compile_error = checker.compile_testbench()
    scores["compilation"] = 100.0 if compile_success else 0.0
    print(f"\n1. Compilation: {scores['compilation']:.0f}/100 (weight: {weights['compilation']}%)")
    
    # 2. Simulation (10%)
    if compile_success:
        sim_success, sim_log = checker.run_simulation()
        scores["simulation"] = 100.0 if sim_success else 0.0
    else:
        scores["simulation"] = 0.0
        sim_success = False
    print(f"\n2. Simulation: {scores['simulation']:.0f}/100 (weight: {weights['simulation']}%)")
    
    # Read simulation log (used by multiple checks)
    sim_log_content = ""
    if sim_success and os.path.exists(checker.sim_log_path):
        with open(checker.sim_log_path, 'r') as f:
            sim_log_content = f.read()
    
    # 3. Required Assertions (15%) - Check from simulation log
    if sim_success:
        req_checker = AssertionRequirementChecker(checker.testbench_path)
        req_checker.set_simulation_log(sim_log_content)
        req_score, req_details = req_checker.get_score()
        scores["required_assertions"] = req_score
        print(f"\n3. Required Assertions: {scores['required_assertions']:.0f}/100 (weight: {weights['required_assertions']}%)")
        print(f"   Verified: {req_details['verified_assertions']}/{req_details['total_assertions']}")
    else:
        scores["required_assertions"] = 0.0
        print(f"\n3. Required Assertions: SKIPPED (simulation failed)")
    
    # 4. Functional Correctness (15%) - Testbench works with correct RTL
    if sim_success:
        fc_checker = FunctionalCorrectnessChecker(sim_log_content)
        fc_score, fc_details = fc_checker.get_score()
        scores["functional_correctness"] = fc_score
        print(f"\n4. Functional Correctness: {scores['functional_correctness']:.0f}/100 (weight: {weights['functional_correctness']}%)")
        print(f"   No False Positives: {'✓' if fc_details['no_false_positives'] else '✗'}")
        print(f"   Transactions Occur: {'✓' if fc_details['transactions_occur'] else '✗'}")
        print(f"   All Channels Active: {'✓' if fc_details['all_channels_active'] else '✗'}")
    else:
        scores["functional_correctness"] = 0.0
        print(f"\n4. Functional Correctness: SKIPPED (simulation failed)")
    
    # 5. Protocol Coverage (15%)
    if enable_protocol_coverage:
        coverage_checker = AXI4ProtocolCoverageChecker(checker.testbench_path)
        cov_score, cov_details = coverage_checker.get_coverage_grade()
        scores["protocol_coverage"] = cov_score
        print(f"\n5. Protocol Coverage: {scores['protocol_coverage']:.0f}/100 (weight: {weights['protocol_coverage']}%)")
        print(f"   Channels: {cov_details['channels_covered']}/5")
        print(f"   Checks: {cov_details['checks_found']}/{cov_details['checks_possible']}")
    else:
        scores["protocol_coverage"] = 50.0
        print(f"\n5. Protocol Coverage: SKIPPED (using default 50)")
    
    # 6. Assertion Execution (10%)
    if sim_success:
        log_check = checker.check_assertions_in_log()
        if log_check['assertions_executed'] > 0:
            exec_score = min(100, 50 + log_check['assertion_passes'] * 2)
            scores["assertion_execution"] = exec_score
        else:
            scores["assertion_execution"] = 0.0
        print(f"\n6. Assertion Execution: {scores['assertion_execution']:.0f}/100 (weight: {weights['assertion_execution']}%)")
        print(f"   Executed: {log_check['assertions_executed']}, Passes: {log_check['assertion_passes']}")
    else:
        scores["assertion_execution"] = 0.0
        print(f"\n6. Assertion Execution: SKIPPED (simulation failed)")
    
    # 7. Code Coverage (15%) - Verilator-based DUT coverage
    if compile_success and sim_success:
        try:
            cov_checker = VerilatorCoverageChecker(
                testbench_path=checker.testbench_path,
                dut_files=dut_files_list,
                design_root=design_root,
            )
            cov_score, cov_details = cov_checker.get_coverage_grade()
            scores["code_coverage"] = cov_score
            print(f"\n7. Code Coverage: {scores['code_coverage']:.0f}/100 (weight: {weights['code_coverage']}%)")
            print(f"   Line: {cov_details['line_coverage']:.1f}%, Toggle: {cov_details['toggle_coverage']:.1f}%, Branch: {cov_details['branch_coverage']:.1f}%")
        except Exception as e:
            scores["code_coverage"] = 0.0
            print(f"\n7. Code Coverage: ERROR ({str(e)[:50]})")
    else:
        scores["code_coverage"] = 0.0
        print(f"\n7. Code Coverage: SKIPPED (simulation failed)")
    
    # 8. Targeted Bug Detection (30%) - Most important!
    if enable_bug_injection and compile_success and sim_success:
        tester = TargetedBugInjectionTester(
            testbench_path=checker.testbench_path,
            design_root=design_root,
            dut_files=dut_files_list,
            simulator=simulator,
        )
        bug_score, bug_results = tester.get_grade()
        scores["bug_detection"] = bug_score
        print(f"\n8. Targeted Bug Detection: {scores['bug_detection']:.0f}/100 (weight: {weights['bug_detection']}%)")
        print(f"   Fully caught (correct assertion): {bug_results['fully_caught']}/{bug_results['total_bugs']}")
        print(f"   Partially caught (any assertion): {bug_results['partially_caught']}/{bug_results['total_bugs']}")
        print(f"   Missed: {bug_results['missed']}/{bug_results['total_bugs']}")
    else:
        scores["bug_detection"] = 0.0
        print(f"\n8. Targeted Bug Detection: SKIPPED (prerequisite failed)")
    
    # Calculate weighted total
    total_score = sum(
        scores[key] * weights[key] / 100
        for key in weights.keys()
    )
    
    print("\n" + "=" * 60)
    print(f"FINAL SCORE: {total_score:.1f}/100")
    print("=" * 60)
    
    # Score breakdown
    print("\nScore Breakdown:")
    for key in weights.keys():
        contribution = scores[key] * weights[key] / 100
        print(f"  {key}: {scores[key]:.0f} × {weights[key]}% = {contribution:.1f}")
    
    # Pass/Fail
    pass_threshold = 60.0
    passed = total_score >= pass_threshold
    
    print(f"\nResult: {'PASS' if passed else 'FAIL'} (threshold: {pass_threshold}%)")
    print("=" * 60)
    
    # Assertions
    assert total_score >= pass_threshold, \
        f"Overall score {total_score:.1f}% below {pass_threshold}% threshold"
