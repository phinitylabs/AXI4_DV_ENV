"""
Weighted Grading for AXI4 Testbench Generation (Problem 2)

Three-pillar model (code coverage dominant, no functional coverage for P2):
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


# =======================================================================
# WEIGHTED GRADING CONFIGURATION
# =======================================================================

WEIGHTS = {
    "compilation": 0.15,       # Prerequisite - must pass
    "negative_test": 0.15,     # Prerequisite - must pass
    "line_coverage": 0.40,     # Proportional scoring - primary quality signal
    "mutation": 0.20,          # Differential kill detection
    "quality": 0.10,           # Structural checks
}

PASS_THRESHOLD = 0.60  # 60% - must achieve good coverage


def test_weighted_grade():
    """Weighted Grading for TB Generation (Problem 2)"""
    proj_path = Path(__file__).resolve().parent.parent
    
    grader = AXI4TBGrader(
        tb_path=str(proj_path / "verif" / "axi4_slave_tb.sv"),
        sources_dir=str(proj_path / "sources"),
        mutants_dir=str(proj_path / "tests" / "mutants"),
        build_dir=str(proj_path / "build")
    )
    
    result = grader.grade()
    
    print("\n" + "=" * 70)
    print("WEIGHTED GRADING - Problem 2 (TB Generation)")
    print(f"Pass Threshold: {PASS_THRESHOLD*100:.0f}%")
    print("=" * 70)
    
    scores = {}
    
    # PREREQUISITE 1: Compilation (15%)
    print("\n[PREREQUISITE 1] Compilation Check...")
    if not result.phase1_compiled:
        print(f"  FAILED: {result.error_message}")
        pytest.fail(f"Prerequisite failed: Compilation - {result.error_message[:100]}")
    scores["compilation"] = WEIGHTS["compilation"]
    print(f"  PASSED (+{WEIGHTS['compilation']*100:.0f}%)")
    
    # PREREQUISITE 2: Negative Test (15%)
    print("\n[PREREQUISITE 2] Negative Test Check...")
    if not result.phase2_negative_passed:
        print(f"  FAILED: {result.error_message}")
        pytest.fail(f"Prerequisite failed: Negative Test - {result.error_message[:100]}")
    scores["negative_test"] = WEIGHTS["negative_test"]
    print(f"  PASSED (+{WEIGHTS['negative_test']*100:.0f}%)")
    
    # METRIC 3: Line Coverage (25% - proportional)
    print("\n[METRIC 3] Line Coverage Check...")
    if result.phase3_coverage:
        coverage_ratio = result.phase3_coverage.line_coverage
        scores["line_coverage"] = WEIGHTS["line_coverage"] * coverage_ratio
        print(f"  Line Coverage: {coverage_ratio*100:.1f}%")
        print(f"  Contribution: {WEIGHTS['line_coverage']*100:.0f}% x {coverage_ratio*100:.1f}% = +{scores['line_coverage']*100:.1f}%")
    else:
        scores["line_coverage"] = 0
        print("  Coverage data not available (+0%)")
    
    # METRIC 4: Mutation Testing (30% - proportional)
    print("\n[METRIC 4] Mutation Testing Check...")
    if result.phase4_mutation:
        killed = result.phase4_mutation.killed_mutants
        total = result.phase4_mutation.total_mutants
        mutation_ratio = killed / total if total > 0 else 0
        scores["mutation"] = WEIGHTS["mutation"] * mutation_ratio
        print(f"  Mutants Killed: {killed}/{total} ({mutation_ratio*100:.1f}%)")
        print(f"  Contribution: {WEIGHTS['mutation']*100:.0f}% x {mutation_ratio*100:.1f}% = +{scores['mutation']*100:.1f}%")
    else:
        scores["mutation"] = 0
        print("  Mutation data not available (+0%)")
    
    # METRIC 5: Quality Checks (15% - binary)
    print("\n[METRIC 5] Quality Checks...")
    if result.phase5_quality:
        # Check for illegal patterns
        if not result.phase5_quality.illegal_hierarchical_refs and not result.phase5_quality.has_force_release:
            scores["quality"] = WEIGHTS["quality"]
            print(f"  PASSED: No illegal patterns (+{WEIGHTS['quality']*100:.0f}%)")
        else:
            scores["quality"] = 0
            print("  FAILED: Illegal patterns detected (+0%)")
    else:
        scores["quality"] = 0
        print("  Quality data not available (+0%)")
    
    # FINAL SCORE
    total_score = sum(scores.values())
    
    print("\n" + "=" * 70)
    print("SCORE BREAKDOWN:")
    for metric, score in scores.items():
        print(f"  {metric}: {score*100:.1f}%")
    print(f"  TOTAL: {total_score*100:.1f}% (Threshold: {PASS_THRESHOLD*100:.0f}%)")
    print("=" * 70)
    
    result_str = "PASS" if total_score >= PASS_THRESHOLD else "FAIL"
    print(f"RESULT: {result_str}")
    
    assert total_score >= PASS_THRESHOLD, f"Score {total_score*100:.1f}% < {PASS_THRESHOLD*100:.0f}%"
