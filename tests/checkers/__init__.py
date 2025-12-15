"""
Checkers module for DV task grading.

Contains checkers for:
1. Testbench Assertion Checker - Basic assertion detection and simulation
2. Protocol Coverage Checker - AXI4 protocol rule coverage
3. Bug Injection Tester - Functional correctness via bug detection
4. Verilator Coverage Checker - RTL coverage metrics using Verilator
5. Assertion Requirement Checker - Verifies specific required assertions from prompt
"""
from .testbench_assertion_checker import AssertionChecker, grade_generated_testbench
from .protocol_coverage_checker import AXI4ProtocolCoverageChecker, check_protocol_coverage
from .bug_injection_tester import AXI4BugInjectionTester, test_bug_detection
from .verilator_coverage_checker import (
    VerilatorCoverageChecker,
    analyze_verilator_coverage,
    format_coverage_report as format_verilator_coverage_report,
)
from .assertion_requirement_checker import (
    AssertionRequirementChecker,
    check_required_assertions,
    format_assertion_requirement_report,
    REQUIRED_ASSERTIONS,
)
from .targeted_bug_injection import (
    TargetedBugInjectionTester,
    format_targeted_bug_report,
    TARGETED_BUGS,
)
from .functional_correctness_checker import (
    FunctionalCorrectnessChecker,
    check_functional_correctness,
    format_functional_correctness_report,
)

__all__ = [
    # Testbench Assertion Checker
    "AssertionChecker",
    "grade_generated_testbench",
    # Protocol Coverage
    "AXI4ProtocolCoverageChecker",
    "check_protocol_coverage",
    # Bug Injection
    "AXI4BugInjectionTester",
    "test_bug_detection",
    # Verilator Coverage
    "VerilatorCoverageChecker",
    "analyze_verilator_coverage",
    "format_verilator_coverage_report",
    # Assertion Requirements
    "AssertionRequirementChecker",
    "check_required_assertions",
    "format_assertion_requirement_report",
    "REQUIRED_ASSERTIONS",
    # Targeted Bug Injection
    "TargetedBugInjectionTester",
    "format_targeted_bug_report",
    "TARGETED_BUGS",
    # Functional Correctness
    "FunctionalCorrectnessChecker",
    "check_functional_correctness",
    "format_functional_correctness_report",
]
