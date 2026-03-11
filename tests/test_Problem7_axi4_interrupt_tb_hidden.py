"""
Weighted Grading for AXI4 Interrupt Controller TB+Assertion Generation

Three-pillar model (code coverage dominant):
- Compilation: 15%
- No False Positives: 15%
- Line Coverage: 40%
- Mutation Testing: 20%
- Quality Checks: 10%

Pass Threshold: 60%
"""

import os
import pytest
from pathlib import Path
from grader import AXI4InterruptTBGrader


WEIGHTS = {
    "compilation": 0.15,
    "negative_test": 0.15,
    "line_coverage": 0.40,
    "mutation": 0.20,
    "quality": 0.10,
}

PASS_THRESHOLD = 0.60


testbench_path = os.getenv("TESTBENCH_PATH", "verif/axi4_top_tb.sv")
sources_dir = os.getenv("SOURCES_DIR", "sources")
mutants_dir = os.getenv("MUTANTS_DIR", "tests/mutants")
design_root = os.getenv("DESIGN_ROOT", ".")


def _get_grader():
    return AXI4InterruptTBGrader(
        tb_path=testbench_path,
        sources_dir=sources_dir,
        mutants_dir=mutants_dir
    )


def _testbench_exists():
    return os.path.exists(testbench_path)


def _require_testbench():
    if not _testbench_exists():
        pytest.fail(f"Testbench file not found: {testbench_path}")


class TestAXI4InterruptTBGeneration:
    """Test class for AXI4 Interrupt TB+Assertion generation grading."""

    def test_axi4_interrupt_tb_generation(self):
        """Main grading test for interrupt testbench."""
        _require_testbench()
        
        grader = _get_grader()
        result = grader.grade()
        
        # Calculate weighted score
        scores = {}
        
        # Phase 1: Compilation (15%)
        scores["compilation"] = 1.0 if result.phase1_compiled else 0.0
        
        # Phase 2: Negative Test (15%)
        scores["negative_test"] = 1.0 if result.phase2_negative_passed else 0.0
        
        # Phase 3: Line Coverage (20%)
        if result.phase3_coverage:
            cov_min = grader.COVERAGE_LINE_MIN
            if result.phase3_coverage.line_coverage >= cov_min:
                scores["line_coverage"] = 1.0
            else:
                scores["line_coverage"] = result.phase3_coverage.line_coverage / cov_min
        else:
            scores["line_coverage"] = 0.0
        
        # Phase 4: Mutation Testing (30%)
        if result.phase4_mutation:
            scores["mutation"] = result.phase4_mutation.score
        else:
            scores["mutation"] = 0.0
        
        # Phase 5: Quality Checks (20%)
        if result.phase5_quality:
            scores["quality"] = result.phase5_quality.structural_score / 6.0
            # Penalize hierarchical references heavily
            if result.phase5_quality.illegal_hierarchical_refs:
                scores["quality"] = 0.0
        else:
            scores["quality"] = 0.0
        
        # Calculate total weighted score
        total_score = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)
        
        print("\n" + "=" * 60)
        print("GRADING SUMMARY")
        print("=" * 60)
        print(f"  Compilation:      {scores['compilation']:.0%} (weight: {WEIGHTS['compilation']:.0%})")
        print(f"  Negative Test:    {scores['negative_test']:.0%} (weight: {WEIGHTS['negative_test']:.0%})")
        print(f"  Line Coverage:    {scores['line_coverage']:.0%} (weight: {WEIGHTS['line_coverage']:.0%})")
        print(f"  Mutation Testing: {scores['mutation']:.0%} (weight: {WEIGHTS['mutation']:.0%})")
        print(f"  Quality:          {scores['quality']:.0%} (weight: {WEIGHTS['quality']:.0%})")
        print("-" * 60)
        print(f"  TOTAL SCORE:      {total_score:.1%}")
        print(f"  PASS THRESHOLD:   {PASS_THRESHOLD:.0%}")
        print("=" * 60)
        
        # Check if prerequisites passed
        if not result.phase1_compiled:
            pytest.fail(f"Compilation failed: {result.error_message}")
        
        if not result.phase2_negative_passed:
            pytest.fail(f"Errors on golden DUT: {result.error_message}")
        
        # Require assertions - this is a hard prerequisite
        if result.phase5_quality and not result.phase5_quality.has_assertions:
            pytest.fail("No SVA assertions found in testbench - assertions are required")
        
        # Require at least 1 mutant killed - ensures assertions actually detect bugs
        if result.phase4_mutation and result.phase4_mutation.killed_mutants < 1:
            pytest.fail(
                f"No mutants killed ({result.phase4_mutation.killed_mutants}/{result.phase4_mutation.total_mutants}). "
                "Assertions must detect at least one bug."
            )
        
        # Check total score against threshold
        if total_score < PASS_THRESHOLD:
            pytest.fail(
                f"Total score {total_score:.1%} below threshold {PASS_THRESHOLD:.0%}. "
                f"Details: {result.error_message}"
            )
        
        print(f"\nPASSED with score: {total_score:.1%}")

