"""
Weighted Grading for AXI4 SVA Assertion Generation (Problem 4)

Weights:
- Compilation: 15% (prerequisite)
- No False Positives: 20% (prerequisite)
- Mutation Testing: 40% (proportional)
- Structural Quality: 25% (binary)

Pass Threshold: 60%
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from grader import AXI4SVAGrader


WEIGHTS = {
    "compilation": 0.15,
    "no_false_positives": 0.20,
    "mutation": 0.40,
    "structural": 0.25,
}

PASS_THRESHOLD = 0.60


def test_weighted_grade():
    """Weighted Grading for SVA Assertion Generation (Problem 4)"""
    proj_path = Path(__file__).resolve().parent.parent
    
    grader = AXI4SVAGrader(
        tb_path=str(proj_path / "verif" / "axi4_slave_tb.sv"),
        sources_dir=str(proj_path / "sources"),
        mutants_dir=str(proj_path / "tests" / "mutants"),
        build_dir=str(proj_path / "build")
    )
    
    result = grader.grade()
    
    print("\n" + "=" * 70)
    print("WEIGHTED GRADING - Problem 4 (axi4_slave SVA Assertion Generation)")
    print(f"Pass Threshold: {PASS_THRESHOLD*100:.0f}%")
    print("=" * 70)
    
    scores = {}
    
    if not result.phase1_compiled:
        pytest.fail(f"Prerequisite failed: Compilation - {result.error_message[:100]}")
    scores["compilation"] = WEIGHTS["compilation"]
    
    if not result.phase2_negative_passed:
        pytest.fail(f"Prerequisite failed: No False Positives - {result.error_message[:100]}")
    scores["no_false_positives"] = WEIGHTS["no_false_positives"]
    
    if result.phase3_mutation:
        killed = result.phase3_mutation.killed_mutants
        total = result.phase3_mutation.total_mutants
        mutation_ratio = killed / total if total > 0 else 0
        scores["mutation"] = WEIGHTS["mutation"] * mutation_ratio
    else:
        scores["mutation"] = 0
    
    if result.phase4_structural:
        has_enough_assertions = result.phase4_structural.assertion_count >= 5
        no_illegal_patterns = len(result.phase4_structural.illegal_patterns) == 0
        if has_enough_assertions and no_illegal_patterns:
            scores["structural"] = WEIGHTS["structural"]
        else:
            scores["structural"] = 0
    else:
        scores["structural"] = 0
    
    total_score = sum(scores.values())
    
    print("SCORE BREAKDOWN:")
    for metric, score in scores.items():
        print(f"  {metric}: {score*100:.1f}%")
    print(f"  TOTAL: {total_score*100:.1f}% (Threshold: {PASS_THRESHOLD*100:.0f}%)")
    
    assert total_score >= PASS_THRESHOLD, f"Score {total_score*100:.1f}% < {PASS_THRESHOLD*100:.0f}%"
