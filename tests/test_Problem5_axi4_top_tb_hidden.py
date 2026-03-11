"""
Weighted Grading for AXI4 System-Level Testbench Generation (Problem 5)

Three-pillar model (code coverage dominant):
- Compilation: 15% (prerequisite)
- No False Positives: 15% (prerequisite)
- Line Coverage: 40% (proportional - primary quality signal)
- Mutation Testing: 20% (differential kill detection)
- Quality Checks: 10% (structural checks)

Pass Threshold: 60%
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from grader import AXI4TBGrader


WEIGHTS = {
    "compilation": 0.15,
    "negative_test": 0.15,
    "line_coverage": 0.40,
    "mutation": 0.20,
    "quality": 0.10,
}

PASS_THRESHOLD = 0.60


def test_weighted_grade():
    """Weighted Grading for System-Level TB Generation (Problem 5)"""
    proj_path = Path(__file__).resolve().parent.parent
    
    grader = AXI4TBGrader(
        tb_path=str(proj_path / "verif" / "axi4_top_tb.sv"),
        sources_dir=str(proj_path / "sources"),
        mutants_dir=str(proj_path / "tests" / "mutants"),
        build_dir=str(proj_path / "build")
    )
    
    result = grader.grade()
    
    print("\n" + "=" * 70)
    print("WEIGHTED GRADING - Problem 5 (axi4_top System-Level TB Generation)")
    print(f"Pass Threshold: {PASS_THRESHOLD*100:.0f}%")
    print("=" * 70)
    
    scores = {}
    
    if not result.phase1_compiled:
        pytest.fail(f"Prerequisite failed: Compilation - {result.error_message[:100]}")
    scores["compilation"] = WEIGHTS["compilation"]
    
    if not result.phase2_negative_passed:
        pytest.fail(f"Prerequisite failed: Negative Test - {result.error_message[:100]}")
    scores["negative_test"] = WEIGHTS["negative_test"]
    
    if result.phase3_coverage:
        coverage_ratio = result.phase3_coverage.line_coverage
        scores["line_coverage"] = WEIGHTS["line_coverage"] * coverage_ratio
    else:
        scores["line_coverage"] = 0
    
    if result.phase4_mutation:
        killed = result.phase4_mutation.killed_mutants
        total = result.phase4_mutation.total_mutants
        mutation_ratio = killed / total if total > 0 else 0
        scores["mutation"] = WEIGHTS["mutation"] * mutation_ratio
    else:
        scores["mutation"] = 0
    
    if result.phase5_quality:
        if not result.phase5_quality.illegal_hierarchical_refs and not result.phase5_quality.has_force_release:
            scores["quality"] = WEIGHTS["quality"]
        else:
            scores["quality"] = 0
    else:
        scores["quality"] = 0
    
    total_score = sum(scores.values())
    
    print("SCORE BREAKDOWN:")
    for metric, score in scores.items():
        print(f"  {metric}: {score*100:.1f}%")
    print(f"  TOTAL: {total_score*100:.1f}% (Threshold: {PASS_THRESHOLD*100:.0f}%)")
    
    assert total_score >= PASS_THRESHOLD, f"Score {total_score*100:.1f}% < {PASS_THRESHOLD*100:.0f}%"
