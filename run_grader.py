#!/usr/bin/env python3
"""
AXI4 Testbench Grader Script

Run this script to grade a testbench against the AXI4 design.

Usage:
    python3 run_grader.py                              # Grade golden testbench
    python3 run_grader.py verif/my_testbench.sv        # Grade custom testbench
    SIM=verilator python3 run_grader.py                # Force Verilator
    SIM=icarus python3 run_grader.py                   # Force Icarus

Environment Variables:
    SIM             - Simulator to use (verilator, icarus). Default: verilator (with fallback)
    TESTBENCH_PATH  - Path to testbench file
    VERBOSE         - Set to 1 for detailed output
"""

import os
import sys
import shutil

# Add the tests directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

from checkers.testbench_assertion_checker import AssertionChecker
from checkers.protocol_coverage_checker import AXI4ProtocolCoverageChecker, format_coverage_report
from checkers.bug_injection_tester import AXI4BugInjectionTester, format_bug_detection_report
from checkers.assertion_requirement_checker import (
    AssertionRequirementChecker,
    format_assertion_requirement_report,
)
from checkers.targeted_bug_injection import (
    TargetedBugInjectionTester,
    format_targeted_bug_report,
)
from checkers.functional_correctness_checker import (
    FunctionalCorrectnessChecker,
    format_functional_correctness_report,
)


def get_simulator():
    """Get the simulator to use, with automatic fallback."""
    sim = os.getenv("SIM", "verilator").lower()
    
    if sim == "verilator" and not shutil.which("verilator"):
        print("⚠️  Verilator not found, falling back to Icarus Verilog")
        return "icarus"
    
    if sim == "icarus" and not shutil.which("iverilog"):
        print("⚠️  Icarus Verilog not found, trying Verilator")
        return "verilator"
    
    return sim


def grade_testbench(testbench_path: str, verbose: bool = False):
    """
    Grade a testbench with comprehensive scoring.
    
    Returns:
        Tuple of (total_score, detailed_scores)
    """
    # DUT files
    dut_path = "sources/axi4_top.sv sources/axi4_master.sv sources/axi4_slave.sv sources/axi4_interrupt.sv"
    dut_files = [
        "sources/axi4_top.sv",
        "sources/axi4_master.sv", 
        "sources/axi4_slave.sv",
        "sources/axi4_interrupt.sv",
    ]
    
    # Get simulator
    simulator = get_simulator()
    
    print("=" * 70)
    print("AXI4 TESTBENCH GRADER")
    print("=" * 70)
    print(f"Testbench: {testbench_path}")
    print(f"Simulator: {simulator}")
    print("=" * 70)
    
    # Check testbench exists
    if not os.path.exists(testbench_path):
        print(f"\n❌ ERROR: Testbench not found: {testbench_path}")
        return 0, {}
    
    # Initialize checker
    checker = AssertionChecker(testbench_path, dut_path, simulator=simulator)
    
    scores = {}
    weights = {
        "compilation": 10,
        "simulation": 10,
        "required_assertions": 15,
        "functional_correctness": 15,
        "protocol_coverage": 15,
        "assertion_execution": 10,
        "bug_detection": 25,
    }
    
    # ================================================================
    # 1. Compilation Check (10%) - Do this first
    # ================================================================
    print("\n" + "-" * 50)
    print("1. COMPILATION CHECK (10%)")
    print("-" * 50)
    
    compile_success, compile_error = checker.compile_testbench()
    scores["compilation"] = 100.0 if compile_success else 0.0
    
    if compile_success:
        print(f"   ✓ Compilation PASSED")
    else:
        print(f"   ✗ Compilation FAILED")
        if verbose:
            print(f"   Error: {compile_error[:300]}")
    print(f"   Score: {scores['compilation']:.0f}/100")
    
    # ================================================================
    # 2. Simulation Check (10%)
    # ================================================================
    print("\n" + "-" * 50)
    print("2. SIMULATION CHECK (10%)")
    print("-" * 50)
    
    if compile_success:
        sim_success, sim_log = checker.run_simulation(timeout=60)
        scores["simulation"] = 100.0 if sim_success else 0.0
        
        if sim_success:
            print(f"   ✓ Simulation PASSED")
        else:
            print(f"   ✗ Simulation FAILED")
            if verbose:
                print(f"   Error: {sim_log[:300]}")
    else:
        scores["simulation"] = 0.0
        sim_success = False
        print(f"   ⊘ Skipped (compilation failed)")
    print(f"   Score: {scores['simulation']:.0f}/100")
    
    # Read simulation log (used by multiple checks)
    sim_log_content = ""
    if sim_success and os.path.exists(checker.sim_log_path):
        with open(checker.sim_log_path, 'r') as f:
            sim_log_content = f.read()
    
    # ================================================================
    # 3. Required Assertions Check (15%) - From simulation log
    # ================================================================
    print("\n" + "-" * 50)
    print("3. REQUIRED ASSERTIONS CHECK (15%)")
    print("-" * 50)
    
    if sim_success:
        req_checker = AssertionRequirementChecker(checker.testbench_path)
        req_checker.set_simulation_log(sim_log_content)
        req_score, req_details = req_checker.get_score()
        scores["required_assertions"] = req_score
        
        print(f"   Verified: {req_details['verified_assertions']}/{req_details['total_assertions']} assertions")
        print(f"   Score: {scores['required_assertions']:.0f}/100")
        
        if verbose:
            print(format_assertion_requirement_report(req_details))
    else:
        scores["required_assertions"] = 0.0
        print(f"   ⊘ Skipped (simulation failed)")
        print(f"   Score: 0/100")
    
    # ================================================================
    # 4. Functional Correctness (15%) - TB works with correct RTL
    # ================================================================
    print("\n" + "-" * 50)
    print("4. FUNCTIONAL CORRECTNESS (15%)")
    print("-" * 50)
    
    if sim_success:
        fc_checker = FunctionalCorrectnessChecker(sim_log_content)
        fc_score, fc_details = fc_checker.get_score()
        scores["functional_correctness"] = fc_score
        
        print(f"   No False Positives: {'✓' if fc_details['no_false_positives'] else '✗'}")
        print(f"   Transactions Occur: {'✓' if fc_details['transactions_occur'] else '✗'} ({fc_details['write_transactions']} write, {fc_details['read_transactions']} read)")
        print(f"   All Channels Active: {'✓' if fc_details['all_channels_active'] else '✗'}")
        print(f"   Score: {scores['functional_correctness']:.0f}/100")
        
        if verbose:
            print(format_functional_correctness_report(fc_details))
    else:
        scores["functional_correctness"] = 0.0
        print(f"   ⊘ Skipped (simulation failed)")
        print(f"   Score: 0/100")
    
    # ================================================================
    # 5. Protocol Coverage Check (15%)
    # ================================================================
    print("\n" + "-" * 50)
    print("5. PROTOCOL COVERAGE CHECK (15%)")
    print("-" * 50)
    
    coverage_checker = AXI4ProtocolCoverageChecker(checker.testbench_path)
    cov_score, cov_details = coverage_checker.get_coverage_grade()
    scores["protocol_coverage"] = cov_score
    
    print(f"   Channels Covered: {cov_details['channels_covered']}/5")
    print(f"   Protocol Checks: {cov_details['checks_found']}/{cov_details['checks_possible']}")
    print(f"   Required Checks: {cov_details['required_checks_found']}/{cov_details['required_checks_total']}")
    print(f"   Score: {scores['protocol_coverage']:.0f}/100")
    
    if verbose:
        print("\n   Detailed Coverage:")
        for channel, covered in cov_details.get('channel_details', {}).items():
            status = "✓" if covered else "✗"
            print(f"      {status} {channel}")
    
    # ================================================================
    # 6. Assertion Execution Check (10%)
    # ================================================================
    print("\n" + "-" * 50)
    print("6. ASSERTION EXECUTION CHECK (10%)")
    print("-" * 50)
    
    if sim_success:
        log_check = checker.check_assertions_in_log()
        
        print(f"   Assertions Executed: {log_check['assertions_executed']}")
        print(f"   Assertion Passes: {log_check['assertion_passes']}")
        print(f"   Assertion Failures: {log_check['assertion_failures']}")
        
        if log_check['assertions_executed'] > 0:
            # Score based on execution plus bonus for passes
            exec_score = min(100, 50 + log_check['assertion_passes'] * 2)
            scores["assertion_execution"] = exec_score
        else:
            scores["assertion_execution"] = 0.0
    else:
        scores["assertion_execution"] = 0.0
        print(f"   ⊘ Skipped (simulation failed)")
    print(f"   Score: {scores['assertion_execution']:.0f}/100")
    
    # ================================================================
    # 7. Targeted Bug Detection (25%) - Most important!
    # ================================================================
    print("\n" + "-" * 50)
    print("7. TARGETED BUG DETECTION (25%)")
    print("-" * 50)
    
    if compile_success and sim_success:
        print("   Running targeted bug injection tests...")
        print("   (Testing if assertions catch SPECIFIC bugs from requirements)")
        
        tester = TargetedBugInjectionTester(
            testbench_path=checker.testbench_path,
            design_root=".",
            dut_files=dut_files,
            simulator=simulator,
        )
        
        bug_score, bug_results = tester.get_grade()
        scores["bug_detection"] = bug_score
        
        print(f"   Fully caught (correct assertion): {bug_results['fully_caught']}/{bug_results['total_bugs']}")
        print(f"   Partially caught (any assertion): {bug_results['partially_caught']}/{bug_results['total_bugs']}")
        print(f"   Missed: {bug_results['missed']}/{bug_results['total_bugs']}")
        
        if verbose:
            print(format_targeted_bug_report(bug_results))
    else:
        scores["bug_detection"] = 0.0
        print(f"   ⊘ Skipped (compilation/simulation failed)")
    print(f"   Score: {scores['bug_detection']:.0f}/100")
    
    # ================================================================
    # FINAL SCORE
    # ================================================================
    print("\n" + "=" * 70)
    print("FINAL SCORE")
    print("=" * 70)
    
    total_score = sum(
        scores[key] * weights[key] / 100
        for key in weights.keys()
    )
    
    print("\nScore Breakdown:")
    print("-" * 40)
    for key in weights.keys():
        contribution = scores[key] * weights[key] / 100
        bar = "█" * int(scores[key] / 10) + "░" * (10 - int(scores[key] / 10))
        print(f"  {key:20} {bar} {scores[key]:5.0f} × {weights[key]:2}% = {contribution:5.1f}")
    
    print("-" * 40)
    print(f"  {'TOTAL':20} {'':11} {total_score:18.1f}/100")
    print("=" * 70)
    
    # Pass/Fail determination
    pass_threshold = 60.0
    if total_score >= 80:
        grade = "EXCELLENT"
        emoji = "🌟"
    elif total_score >= pass_threshold:
        grade = "PASS"
        emoji = "✅"
    elif total_score >= 40:
        grade = "NEEDS IMPROVEMENT"
        emoji = "⚠️"
    else:
        grade = "FAIL"
        emoji = "❌"
    
    print(f"\nResult: {emoji} {grade} ({total_score:.1f}/100)")
    print("=" * 70)
    
    return total_score, scores


def main():
    # Get testbench path from command line or environment
    if len(sys.argv) > 1:
        testbench_path = sys.argv[1]
    else:
        testbench_path = os.getenv("TESTBENCH_PATH", "verif/axi4_top_tb_golden.sv")
    
    # Check for verbose flag
    verbose = os.getenv("VERBOSE", "0") == "1" or "-v" in sys.argv or "--verbose" in sys.argv
    
    # Run grader
    score, _ = grade_testbench(testbench_path, verbose=verbose)
    
    # Exit with appropriate code
    sys.exit(0 if score >= 60 else 1)


if __name__ == "__main__":
    main()

