#!/usr/bin/env python3
"""
Run Hidden Tests Against a Testbench

This script simulates how HUD runs the hidden tests from the test branch
against an agent-generated testbench.

Usage:
    python3 run_hidden_tests.py                          # Test golden TB
    python3 run_hidden_tests.py verif/my_tb.sv           # Test custom TB
    python3 run_hidden_tests.py -v                       # Verbose output
    SIM=verilator python3 run_hidden_tests.py            # Force Verilator

This mimics running:
    pytest tests/test_axi4_slave_sva_hidden.py
"""

import os
import sys
import subprocess
import shutil

def get_available_simulator():
    """Get available simulator with fallback."""
    sim = os.getenv("SIM", "verilator").lower()
    if sim == "verilator" and not shutil.which("verilator"):
        return "icarus"
    return sim

def run_tests(testbench_path: str, verbose: bool = False):
    """Run the hidden tests against the specified testbench."""
    
    # Set environment variables
    env = os.environ.copy()
    env["TESTBENCH_PATH"] = testbench_path
    env["SIM"] = get_available_simulator()
    env["DUT_PATH"] = "sources/axi4_top.sv sources/axi4_master.sv sources/axi4_slave.sv sources/axi4_interrupt.sv"
    env["DESIGN_ROOT"] = "."
    env["REQUIRE_ASSERTIONS"] = "true"
    env["ENABLE_BUG_INJECTION"] = "true"
    env["ENABLE_PROTOCOL_COVERAGE"] = "true"
    
    print("=" * 70)
    print("RUNNING HIDDEN TESTS")
    print("=" * 70)
    print(f"Testbench: {testbench_path}")
    print(f"Simulator: {env['SIM']}")
    print(f"Test File: tests/test_axi4_slave_sva_hidden.py")
    print("=" * 70)
    
    # Check if testbench exists
    if not os.path.exists(testbench_path):
        print(f"\n❌ ERROR: Testbench not found: {testbench_path}")
        print("   Make sure the golden testbench exists in verif/ directory")
        return 1
    
    # Check if test file exists
    test_file = "tests/test_axi4_slave_sva_hidden.py"
    if not os.path.exists(test_file):
        print(f"\n❌ ERROR: Test file not found: {test_file}")
        print("   Make sure you're on the test branch")
        return 1
    
    # Build pytest command
    pytest_args = [
        sys.executable, "-m", "pytest",
        test_file,
        "-v",  # Verbose
        "--tb=short",  # Short traceback
        "-x",  # Stop on first failure (optional, remove for full run)
    ]
    
    if verbose:
        pytest_args.append("-s")  # Show print statements
    
    print(f"\nRunning: {' '.join(pytest_args)}\n")
    print("-" * 70)
    
    # Run pytest
    result = subprocess.run(
        pytest_args,
        env=env,
        cwd=os.path.dirname(os.path.abspath(__file__)) or ".",
    )
    
    print("-" * 70)
    
    if result.returncode == 0:
        print("\n✅ ALL TESTS PASSED")
    else:
        print(f"\n❌ TESTS FAILED (exit code: {result.returncode})")
    
    return result.returncode


def run_specific_test(testbench_path: str, test_name: str, verbose: bool = False):
    """Run a specific test."""
    
    env = os.environ.copy()
    env["TESTBENCH_PATH"] = testbench_path
    env["SIM"] = get_available_simulator()
    env["DUT_PATH"] = "sources/axi4_top.sv sources/axi4_master.sv sources/axi4_slave.sv sources/axi4_interrupt.sv"
    env["DESIGN_ROOT"] = "."
    env["REQUIRE_ASSERTIONS"] = "true"
    env["ENABLE_BUG_INJECTION"] = "true"
    env["ENABLE_PROTOCOL_COVERAGE"] = "true"
    
    test_file = "tests/test_axi4_slave_sva_hidden.py"
    
    pytest_args = [
        sys.executable, "-m", "pytest",
        f"{test_file}::{test_name}",
        "-v",
        "--tb=short",
    ]
    
    if verbose:
        pytest_args.append("-s")
    
    print(f"Running test: {test_name}")
    print("-" * 50)
    
    result = subprocess.run(pytest_args, env=env)
    
    return result.returncode


def main():
    # Parse arguments
    testbench_path = "verif/axi4_top_tb_golden.sv"  # Default
    verbose = False
    specific_test = None
    
    args = sys.argv[1:]
    for arg in args:
        if arg in ["-v", "--verbose"]:
            verbose = True
        elif arg.startswith("--test="):
            specific_test = arg.split("=")[1]
        elif arg in ["-h", "--help"]:
            print(__doc__)
            print("\nAvailable tests:")
            print("  test_testbench_file_exists")
            print("  test_testbench_has_assertions")
            print("  test_protocol_coverage")
            print("  test_testbench_compiles")
            print("  test_testbench_simulates")
            print("  test_assertions_execute")
            print("  test_bug_detection")
            print("  test_comprehensive_grade")
            print("  test_quick_assertion_check")
            print("\nExample: python3 run_hidden_tests.py --test=test_comprehensive_grade -v")
            return 0
        elif not arg.startswith("-"):
            testbench_path = arg
    
    # Run tests
    if specific_test:
        return run_specific_test(testbench_path, specific_test, verbose)
    else:
        return run_tests(testbench_path, verbose)


if __name__ == "__main__":
    sys.exit(main())

