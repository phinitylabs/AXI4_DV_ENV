"""
Weighted Grading for AXI4 Burst Boundary SVA Assertion Generation

Weights:
- Compilation: 15%
- No False Positives: 20%
- Mutation Testing: 40%
- Structural Quality: 25%

Pass Threshold: 60%
"""

import os
import pytest
from pathlib import Path
from grader import AXI4BurstSVAGrader


WEIGHTS = {
    "compilation": 0.15,
    "no_false_positives": 0.20,
    "mutation": 0.40,
    "structural": 0.25,
}

PASS_THRESHOLD = 0.60


testbench_path = os.getenv("TESTBENCH_PATH", "verif/axi4_slave_tb.sv")
sources_dir = os.getenv("SOURCES_DIR", "sources")
mutants_dir = os.getenv("MUTANTS_DIR", "tests/mutants")
design_root = os.getenv("DESIGN_ROOT", ".")


def _get_grader():
    return AXI4BurstSVAGrader(
        tb_path=testbench_path,
        sources_dir=sources_dir,
        mutants_dir=mutants_dir
    )


def _testbench_exists():
    return os.path.exists(testbench_path)


def _require_testbench():
    if not _testbench_exists():
        pytest.fail(f"Testbench file not found: {testbench_path}")


class TestAXI4BurstSVAGeneration:
    """Test class for AXI4 Burst Boundary SVA generation grading."""

    def test_axi4_burst_sva_generation(self):
        """Main grading test for burst boundary assertions."""
        _require_testbench()
        
        grader = _get_grader()
        result = grader.grade()
        
        # Calculate weighted score
        scores = {}
        
        # Phase 1: Compilation (15%)
        scores["compilation"] = 1.0 if result.phase1_compiled else 0.0
        
        # Phase 2: No False Positives (20%)
        scores["no_false_positives"] = 1.0 if result.phase2_negative_passed else 0.0
        
        # Phase 3: Mutation Testing (40%)
        if result.phase3_mutation:
            scores["mutation"] = result.phase3_mutation.score
        else:
            scores["mutation"] = 0.0
        
        # Phase 4: Structural Quality (25%)
        if result.phase4_structural:
            scores["structural"] = result.phase4_structural.structural_score / 8.0
        else:
            scores["structural"] = 0.0
        
        # Calculate total weighted score
        total_score = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)
        
        print("\n" + "=" * 60)
        print("GRADING SUMMARY")
        print("=" * 60)
        print(f"  Compilation:      {scores['compilation']:.0%} (weight: {WEIGHTS['compilation']:.0%})")
        print(f"  No False Positives: {scores['no_false_positives']:.0%} (weight: {WEIGHTS['no_false_positives']:.0%})")
        print(f"  Mutation Testing: {scores['mutation']:.0%} (weight: {WEIGHTS['mutation']:.0%})")
        print(f"  Structural:       {scores['structural']:.0%} (weight: {WEIGHTS['structural']:.0%})")
        print("-" * 60)
        print(f"  TOTAL SCORE:      {total_score:.1%}")
        print(f"  PASS THRESHOLD:   {PASS_THRESHOLD:.0%}")
        print("=" * 60)
        
        # Check if prerequisites passed
        if not result.phase1_compiled:
            pytest.fail(f"Compilation failed: {result.error_message}")
        
        if not result.phase2_negative_passed:
            pytest.fail(f"False positives detected: {result.error_message}")
        
        # Check total score against threshold
        if total_score < PASS_THRESHOLD:
            pytest.fail(
                f"Total score {total_score:.1%} below threshold {PASS_THRESHOLD:.0%}. "
                f"Details: {result.error_message}"
            )
        
        print(f"\nPASSED with score: {total_score:.1%}")

