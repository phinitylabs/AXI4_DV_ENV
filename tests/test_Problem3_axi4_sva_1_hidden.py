"""
Weighted Grading for AXI4 SVA Assertion Generation (Problem 3)

This grader uses weighted scoring:
- Prerequisites (Compilation, No False Positives) must pass or grade = 0
- Other metrics contribute proportionally to a weighted score
- Final grade = 1 if total_score >= threshold (60%), else 0

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


# =======================================================================
# WEIGHTED GRADING CONFIGURATION
# =======================================================================

WEIGHTS = {
    "compilation": 0.15,          # Prerequisite - must pass
    "no_false_positives": 0.20,   # Prerequisite - must pass
    "mutation": 0.40,             # Proportional scoring
    "structural": 0.25,           # Binary
}

PASS_THRESHOLD = 0.60  # 60% - easiest task (higher threshold)


def test_weighted_grade():
    """Weighted Grading for SVA Assertion Generation (Problem 3)"""
    proj_path = Path(__file__).resolve().parent.parent
    
    grader = AXI4SVAGrader(
        tb_path=str(proj_path / "verif" / "axi4_slave_tb.sv"),
        sources_dir=str(proj_path / "sources"),
        mutants_dir=str(proj_path / "tests" / "mutants"),
        build_dir=str(proj_path / "build")
    )
    
    result = grader.grade()
    
    print("\n" + "=" * 70)
    print("WEIGHTED GRADING - Problem 3 (SVA Assertion Generation)")
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
    
    # PREREQUISITE 2: No False Positives (20%)
    print("\n[PREREQUISITE 2] No False Positives Check...")
    if not result.phase2_negative_passed:
        print(f"  FAILED: {result.error_message}")
        pytest.fail(f"Prerequisite failed: No False Positives - {result.error_message[:100]}")
    scores["no_false_positives"] = WEIGHTS["no_false_positives"]
    print(f"  PASSED (+{WEIGHTS['no_false_positives']*100:.0f}%)")
    
    # METRIC 3: Mutation Testing (40% - proportional)
    print("\n[METRIC 3] Mutation Testing Check...")
    if result.phase3_mutation:
        killed = result.phase3_mutation.killed_mutants
        total = result.phase3_mutation.total_mutants
        mutation_ratio = killed / total if total > 0 else 0
        scores["mutation"] = WEIGHTS["mutation"] * mutation_ratio
        print(f"  Mutants Killed: {killed}/{total} ({mutation_ratio*100:.1f}%)")
        print(f"  Contribution: {WEIGHTS['mutation']*100:.0f}% x {mutation_ratio*100:.1f}% = +{scores['mutation']*100:.1f}%")
        print(f"  Killed: {result.phase3_mutation.killed_list}")
        print(f"  Survived: {result.phase3_mutation.survived_list}")
    else:
        scores["mutation"] = 0
        print("  Mutation data not available (+0%)")
    
    # METRIC 4: Structural Quality (25% - binary)
    print("\n[METRIC 4] Structural Quality Check...")
    if result.phase4_structural:
        has_enough_assertions = result.phase4_structural.assertion_count >= 5
        no_illegal_patterns = len(result.phase4_structural.illegal_patterns) == 0
        
        print(f"  Assertion Count: {result.phase4_structural.assertion_count} (need >= 5)")
        print(f"  Illegal Patterns: {result.phase4_structural.illegal_patterns}")
        
        if has_enough_assertions and no_illegal_patterns:
            scores["structural"] = WEIGHTS["structural"]
            print(f"  PASSED (+{WEIGHTS['structural']*100:.0f}%)")
        else:
            scores["structural"] = 0
            if not has_enough_assertions:
                print(f"  FAILED: Not enough assertions (+0%)")
            else:
                print(f"  FAILED: Illegal patterns detected (+0%)")
    else:
        scores["structural"] = 0
        print("  Structural data not available (+0%)")
    
    # FINAL SCORE
    total_score = sum(scores.values())
    
    print("\n" + "=" * 70)
    print("SCORE BP¥AKDOWN:")
    for metric, score in scores.items():
        print(f"  {metric}: {score*100:.1f}%")
    print(f"  TOTAL: {total_score*100:.1f}% (Threshold: {PASS_THRESHOLD*100:.0f}%)")
    print("=" * 70)
    
    result_str = "PASS" if total_score >= PASS_THRESHOLD else "FAIL"
    print(f"RESULT: {result_str}")
    
    assert total_score >= PASS_THRESHOLD, f"Score {total_score*100:.1f}% < {PASS_THRESHOLD*100:.0f}%"
