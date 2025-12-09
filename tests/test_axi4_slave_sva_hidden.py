"""
Enhanced Test Runner for Grading Generated Testbenches with Assertions.

This comprehensive test runner:
1. Checks if testbench has assertions (basic)
2. Checks protocol coverage (AXI4 channels)
3. Compiles and simulates testbench
4. Verifies assertions execute
5. Tests bug detection capability (functional correctness)
6. Calculates weighted final score

Grading Breakdown:
- Basic Assertions: 15%
- Protocol Coverage: 25%
- Compilation: 10%
- Simulation: 10%
- Assertion Execution: 15%
- Bug Detection (Functional): 25%
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

# Fetch environment variables
testbench_path = os.getenv("TESTBENCH_PATH", "verif/axi4_top_tb.sv")
dut_path = os.getenv("DUT_PATH", "sources/axi4_top.sv sources/axi4_master.sv sources/axi4_slave.sv sources/axi4_interrupt.sv")
simulator = os.getenv("SIM", "icarus")
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


# Helper to check if testbench exists
def testbench_exists():
    """Check if testbench file exists (with path resolution)."""
    checker = AssertionChecker(testbench_path, dut_path)
    return os.path.exists(checker.testbench_path)


# ============================================================
# BASIC TESTS
# ============================================================

@pytest.mark.parametrize("test", range(1))
def test_testbench_has_assertions(test):
    """
    Test that checks if generated testbench has assertions.
    Weight: 15%
    """
    if not testbench_exists():
        pytest.skip(f"Testbench file not found: {testbench_path}")
    
    checker = AssertionChecker(testbench_path, dut_path)
    checker.simulator = simulator
    
    # Check assertions in code
    code_check = checker.check_assertions_in_code()
    
    print(f"\n=== Assertion Code Check ===")
    print(f"Testbench: {checker.testbench_path}")
    print(f"Has Assertions: {code_check['has_assertions']}")
    print(f"Assertion Count: {code_check['assertion_count']}")
    print(f"Assertion Types: {code_check['assertion_types']}")
    print(f"Locations: {code_check['assertion_locations']}")
    
    # Check if file was found
    if not code_check['valid']:
        pytest.skip(f"Could not read testbench file: {checker.testbench_path}")
    
    if require_assertions:
        assert code_check['has_assertions'], \
            f"No assertions found in testbench. Found {code_check['assertion_count']} assertions."


# ============================================================
# PROTOCOL COVERAGE TEST
# ============================================================

@pytest.mark.parametrize("test", range(1))
def test_protocol_coverage(test):
    """
    Test that checks AXI4 protocol coverage in testbench.
    Weight: 25%
    
    Checks:
    - All 5 AXI4 channels monitored (AW, W, B, AR, R)
    - Required protocol checks present (handshakes, VALID stability, etc.)
    """
    if not testbench_exists():
        pytest.skip(f"Testbench file not found: {testbench_path}")
    
    if not enable_protocol_coverage:
        pytest.skip("Protocol coverage checking disabled")
    
    checker = AssertionChecker(testbench_path, dut_path)
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
    if not testbench_exists():
        pytest.skip(f"Testbench file not found: {testbench_path}")
    
    checker = AssertionChecker(testbench_path, dut_path)
    checker.simulator = simulator
    
    print(f"\n=== Compilation Check ===")
    print(f"Testbench: {checker.testbench_path}")
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
    if not testbench_exists():
        pytest.skip(f"Testbench file not found: {testbench_path}")
    
    checker = AssertionChecker(testbench_path, dut_path)
    checker.simulator = simulator
    
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
    if not testbench_exists():
        pytest.skip(f"Testbench file not found: {testbench_path}")
    
    checker = AssertionChecker(testbench_path, dut_path)
    checker.simulator = simulator
    
    # Compile and simulate
    compile_success, compile_error = checker.compile_testbench()
    if not compile_success:
        pytest.skip(f"Testbench must compile first: {compile_error}")
    
    sim_success, sim_log = checker.run_simulation()
    if not sim_success:
        pytest.skip(f"Testbench must simulate first: {sim_log[:200]}")
    
    # Check assertions in log (checker will look in log directory)
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
# BUG INJECTION TEST (FUNCTIONAL CORRECTNESS)
# ============================================================

@pytest.mark.parametrize("test", range(1))
def test_bug_detection(test):
    """
    Test that testbench can detect injected bugs (functional correctness).
    Weight: 25%
    
    This is the most important test for DV quality:
    - Injects known bugs into RTL
    - Verifies testbench catches them via assertion failures
    - A good testbench should catch at least 50% of bugs
    """
    if not testbench_exists():
        pytest.skip(f"Testbench file not found: {testbench_path}")
    
    if not enable_bug_injection:
        pytest.skip("Bug injection testing disabled")
    
    checker = AssertionChecker(testbench_path, dut_path)
    
    # First verify testbench works with correct RTL
    compile_success, _ = checker.compile_testbench()
    if not compile_success:
        pytest.skip("Testbench must compile with correct RTL first")
    
    sim_success, _ = checker.run_simulation()
    if not sim_success:
        pytest.skip("Testbench must simulate with correct RTL first")
    
    # Now test bug detection
    print(f"\n=== Bug Injection Testing ===")
    print(f"Testing testbench's ability to catch protocol violations...")
    
    tester = AXI4BugInjectionTester(
        testbench_path=checker.testbench_path,
        design_root=design_root,
        dut_files=dut_files_list,
        simulator=simulator,
    )
    
    score, details = tester.get_bug_detection_grade()
    
    # Print report
    print("\n" + format_bug_detection_report(details))
    
    # Assertions
    assert details["total_bugs"] > 0, \
        "Bug injection test setup failed - no bugs tested"
    
    assert details["bugs_caught"] > 0, \
        f"Testbench caught 0 bugs - must catch at least 1"
    
    # Minimum 30% detection rate for passing
    # (Lowered from 50% to be more lenient initially)
    assert score >= 30.0, \
        f"Bug detection rate {score:.1f}% below 30% minimum"
    
    print(f"\nBug Detection Score: {score:.1f}%")


# ============================================================
# COMPREHENSIVE GRADING TEST
# ============================================================

@pytest.mark.parametrize("test", range(1))
def test_comprehensive_grade(test):
    """
    Comprehensive test that grades the entire testbench with weighted scoring.
    
    Score Breakdown:
    - Basic Assertions: 15%
    - Protocol Coverage: 25%
    - Compilation: 10%
    - Simulation: 10%
    - Assertion Execution: 15%
    - Bug Detection: 25%
    
    Pass threshold: 60% overall
    """
    if not testbench_exists():
        pytest.skip(f"Testbench file not found: {testbench_path}")
    
    checker = AssertionChecker(testbench_path, dut_path)
    checker.simulator = simulator
    
    scores = {}
    weights = {
        "assertions": 15,
        "protocol_coverage": 25,
        "compilation": 10,
        "simulation": 10,
        "assertion_execution": 15,
        "bug_detection": 25,
    }
    
    print("\n" + "=" * 60)
    print("COMPREHENSIVE TESTBENCH GRADING")
    print("=" * 60)
    
    # 1. Basic Assertions (15%)
    code_check = checker.check_assertions_in_code()
    if code_check['has_assertions'] and code_check['assertion_count'] >= 5:
        scores["assertions"] = 100.0
    elif code_check['has_assertions']:
        scores["assertions"] = min(code_check['assertion_count'] * 20, 100)
    else:
        scores["assertions"] = 0.0
    print(f"\n1. Basic Assertions: {scores['assertions']:.0f}/100 (weight: {weights['assertions']}%)")
    print(f"   Found {code_check['assertion_count']} assertions")
    
    # 2. Protocol Coverage (25%)
    if enable_protocol_coverage:
        coverage_checker = AXI4ProtocolCoverageChecker(checker.testbench_path)
        cov_score, cov_details = coverage_checker.get_coverage_grade()
        scores["protocol_coverage"] = cov_score
        print(f"\n2. Protocol Coverage: {scores['protocol_coverage']:.0f}/100 (weight: {weights['protocol_coverage']}%)")
        print(f"   Channels: {cov_details['channels_covered']}/5")
        print(f"   Checks: {cov_details['checks_found']}/{cov_details['checks_possible']}")
    else:
        scores["protocol_coverage"] = 50.0  # Default if disabled
        print(f"\n2. Protocol Coverage: SKIPPED (using default 50)")
    
    # 3. Compilation (10%)
    compile_success, compile_error = checker.compile_testbench()
    scores["compilation"] = 100.0 if compile_success else 0.0
    print(f"\n3. Compilation: {scores['compilation']:.0f}/100 (weight: {weights['compilation']}%)")
    
    # 4. Simulation (10%)
    if compile_success:
        sim_success, sim_log = checker.run_simulation()
        scores["simulation"] = 100.0 if sim_success else 0.0
    else:
        scores["simulation"] = 0.0
    print(f"\n4. Simulation: {scores['simulation']:.0f}/100 (weight: {weights['simulation']}%)")
    
    # 5. Assertion Execution (15%)
    if scores["simulation"] > 0:
        log_check = checker.check_assertions_in_log()
        if log_check['assertions_executed'] > 0:
            # Bonus for more assertions executed
            exec_score = min(100, 50 + log_check['assertion_passes'] * 5)
            scores["assertion_execution"] = exec_score
        else:
            scores["assertion_execution"] = 0.0
    else:
        scores["assertion_execution"] = 0.0
    print(f"\n5. Assertion Execution: {scores['assertion_execution']:.0f}/100 (weight: {weights['assertion_execution']}%)")
    
    # 6. Bug Detection (25%)
    if enable_bug_injection and compile_success and scores["simulation"] > 0:
        tester = AXI4BugInjectionTester(
            testbench_path=checker.testbench_path,
            design_root=design_root,
            dut_files=dut_files_list,
            simulator=simulator,
        )
        bug_score, bug_details = tester.get_bug_detection_grade()
        scores["bug_detection"] = bug_score
        print(f"\n6. Bug Detection: {scores['bug_detection']:.0f}/100 (weight: {weights['bug_detection']}%)")
        print(f"   Bugs caught: {bug_details['bugs_caught']}/{bug_details['total_bugs']}")
    else:
        scores["bug_detection"] = 0.0
        print(f"\n6. Bug Detection: SKIPPED (prerequisite failed)")
    
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


# ============================================================
# QUICK CHECK (for fast iteration)
# ============================================================

def test_quick_assertion_check():
    """
    Quick test to just check if assertions exist (no compilation).
    Useful for fast feedback.
    """
    if not testbench_exists():
        pytest.skip(f"Testbench file not found: {testbench_path}")
    
    checker = AssertionChecker(testbench_path, dut_path)
    code_check = checker.check_assertions_in_code()
    
    print(f"\nQuick Check: {code_check['assertion_count']} assertions found")
    print(f"Testbench: {checker.testbench_path}")
    
    if not code_check['valid']:
        pytest.skip(f"Could not read testbench file: {checker.testbench_path}")
    
    if require_assertions:
        assert code_check['has_assertions'], "No assertions found in testbench"
