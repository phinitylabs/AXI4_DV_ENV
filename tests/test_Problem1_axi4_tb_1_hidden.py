"""
Weighted Grading for AXI4 Testbench + Assertion Generation

This grader uses weighted scoring:
- Prerequisites (Compilation, Simulation) must pass or grade = 0
- Other metrics contribute proportionally to a weighted score
- Final grade = 1 if total_score >= threshold (40%), else 0

Weights:
- Compilation: 15% (prerequisite)
- Simulation: 15% (prerequisite)
- No False Positives: 20%
- Assertions Active: 10%
- Coverage: 15% (proportional)
- Bug Injection: 25% (proportional)

Pass Threshold: 40%
"""

import os
import re
import pytest
from pathlib import Path
from checkers.testbench_assertion_checker import AssertionChecker


WEIGHTS = {
    "compilation": 0.15,
    "simulation": 0.15,
    "no_false_positives": 0.20,
    "assertions_active": 0.10,
    "coverage": 0.15,
    "bug_injection": 0.25,
}

PASS_THRESHOLD = 0.40

testbench_path = os.getenv("TESTBENCH_PATH", "verif/axi4_top_tb.sv")
dut_path = os.getenv("DUT_PATH", 
    "sources/axi4_top.sv sources/axi4_master.sv sources/axi4_slave.sv "
    "sources/axi4_interrupt.sv sources/axi4_coverage.sv")
simulator = os.getenv("SIM", "verilator")
design_root = os.getenv("DESIGN_ROOT", ".")

dut_files_list = [
    "sources/axi4_top.sv",
    "sources/axi4_master.sv",
    "sources/axi4_slave.sv",
    "sources/axi4_interrupt.sv",
    "sources/axi4_coverage.sv",
]


def _testbench_exists():
    checker = AssertionChecker(testbench_path, dut_path)
    return os.path.exists(checker.testbench_path)


def _require_testbench():
    if not _testbench_exists():
        pytest.fail(f"Testbench file not found: {testbench_path}")


def _get_checker():
    checker = AssertionChecker(testbench_path, dut_path)
    checker.simulator = simulator
    return checker


def _parse_coverage_from_log(log_content: str) -> dict:
    result = {"bins_hit": 0, "bins_total": 24, "coverage_percent": 0.0, "found": False}
    
    match = re.search(r"COVERAGE_BINS_HIT=(\d+)", log_content)
    if match:
        result["bins_hit"] = int(match.group(1))
        result["found"] = True
    
    match = re.search(r"COVERAGE_BINS_TOTAL=(\d+)", log_content)
    if match:
        result["bins_total"] = int(match.group(1))
    
    match = re.search(r"COVERAGE_PERCENT=([\d.]+)", log_content)
    if match:
        result["coverage_percent"] = float(match.group(1))
    elif result["bins_total"] > 0:
        result["coverage_percent"] = (result["bins_hit"] * 100.0) / result["bins_total"]
    
    return result


def _check_assertion_behavior(log_content: str) -> dict:
    result = {"has_assertion_passes": False, "has_assertion_failures": False, "pass_count": 0, "failure_count": 0}
    
    pass_matches = re.findall(r"ASSERTION.*PASSED", log_content, re.IGNORECASE)
    result["pass_count"] = len(pass_matches)
    result["has_assertion_passes"] = len(pass_matches) > 0
    
    fail_matches = re.findall(r"ASSERTION.*FAILED", log_content, re.IGNORECASE)
    result["failure_count"] = len(fail_matches)
    result["has_assertion_failures"] = len(fail_matches) > 0
    
    return result


def _run_bug_injection(checker) -> dict:
    from checkers.targeted_bug_injection import TargetedBugInjectionTester
    tester = TargetedBugInjectionTester(
        testbench_path=checker.testbench_path,
        design_root=design_root,
        dut_files=dut_files_list,
        simulator=simulator,
    )
    score, results = tester.get_grade()
    return results


def test_weighted_grade():
    """Weighted Grading for TB + Assertion Generation (Problem 1)"""
    _require_testbench()
    checker = _get_checker()
    
    print("\n" + "=" * 70)
    print("WEIGHTED GRADING - Problem 1 (TB + Assertion Generation)")
    print(f"Pass Threshold: {PASS_THRESHOLD*100:.0f}%")
    print("=" * 70)
    
    scores = {}
    
    # PREREQUISITE 1: Compilation
    print("\n[PREREQUISITE 1] Compilation Check...")
    compile_success, compile_error = checker.compile_testbench()
    if not compile_success:
        pytest.fail(f"Prerequisite failed: Compilation - {compile_error[:100]}")
    scores["compilation"] = WEIGHTS["compilation"]
    print(f"  PASSED (+{WEIGHTS['compilation']*100:.0f}%)")
    
    # PREREQUISITE 2: Simulation
    print("\n[PREREQUISITE 2] Simulation Check...")
    sim_success, sim_log = checker.run_simulation()
    if not sim_success:
        pytest.fail(f"Prerequisite failed: Simulation - {sim_log[:100]}")
    scores["simulation"] = WEIGHTS["simulation"]
    print(f"  PASSED (+{WEIGHTS['simulation']*100:.0f}%)")
    
    sim_log_content = ""
    if os.path.exists(checker.sim_log_path):
        with open(checker.sim_log_path, "r") as f:
            sim_log_content = f.read()
    
    assertion_check = _check_assertion_behavior(sim_log_content)
    
    # METRIC 3: No False Positives
    print("\n[METRIC 3] No False Positives Check...")
    if not assertion_check["has_assertion_failures"]:
        scores["no_false_positives"] = WEIGHTS["no_false_positives"]
        print(f"  PASSED (+{WEIGHTS['no_false_positives']*100:.0f}%)")
    else:
        scores["no_false_positives"] = 0
        print(f"  FAILED: {assertion_check['failure_count']} false positives (+0%)")
    
    # METRIC 4: Assertions Active
    print("\n[METRIC 4] Assertions Active Check...")
    if assertion_check["has_assertion_passes"]:
        scores["assertions_active"] = WEIGHTS["assertions_active"]
        print(f"  PASSED (+{WEIGHTS['assertions_active']*100:.0f}%)")
    else:
        scores["assertions_active"] = 0
        print("  FAILED: No assertion passes (+0%)")
    
    # METRIC 5: Coverage (proportional)
    print("\n[METRIC 5] Coverage Check...")
    coverage = _parse_coverage_from_log(sim_log_content)
    if coverage["found"] and coverage["bins_total"] > 0:
        coverage_ratio = coverage["bins_hit"] / coverage["bins_total"]
        scores["coverage"] = WEIGHTS["coverage"] * coverage_ratio
        print(f"  Bins: {coverage['bins_hit']}/{coverage['bins_total']} = +{scores['coverage']*100:.1f}%")
    else:
        scores["coverage"] = 0
        print("  Coverage not found (+0%)")
    
    # METRIC 6: Bug Injection (proportional)
    print("\n[METRIC 6] Bug Injection Check...")
    try:
        bug_results = _run_bug_injection(checker)
        caught = bug_results.get("fully_caught", 0) + bug_results.get("partially_caught", 0)
        total = bug_results.get("total_bugs", 1)
        bug_ratio = caught / total if total > 0 else 0
        scores["bug_injection"] = WEIGHTS["bug_injection"] * bug_ratio
        print(f"  Bugs: {caught}/{total} = +{scores['bug_injection']*100:.1f}%")
    except Exception as e:
        scores["bug_injection"] = 0
        print(f"  Failed: {e} (+0%)")
    
    # FINAL SCORE
    total_score = sum(scores.values())
    
    print("\n" + "=" * 70)
    print("SCORE BEEDKOWN:")
    for metric, score in scores.items():
        print(f"  {metric}: {score*100:.1f}%")
    print(f"  TOTAL: {total_score*100:.1f}% (Threshold: {PASS_THRESHOLD*100:.0f}%)")
    print("=" * 70)
    
    result = "PASS" if total_score >= PASS_THRESHOLD else "FAIL"
    print(f"RESULT: {result}")
    
    assert total_score >= PASS_THRESHOLD, f"Score {total_score*100:.1f}% < {PASS_THRESHOLD*100:.0f}%"