"""
AXI4 Memory SVA Assertion Benchmark — Differential Grading (HARD MODE)

SVA-only problem: agent adds assertions to a pre-written testbench.
TB stimulus is fixed, so mutation testing is the primary quality metric.

Weights:
  Compilation:          15%
  No False Positives:   20%
  Mutation Testing:     40%   (differential comparison — ungameable)
  Structural Quality:   25%

Pass Threshold: 60%
Hard requirement: must kill at least 3/4 mutants via differential comparison.
"""

import os
import pytest
from grader import AXI4MemorySVAGrader


WEIGHTS = {
    "compilation":        0.15,
    "no_false_positives": 0.20,
    "mutation":           0.40,
    "structural":         0.25,
}

PASS_THRESHOLD = 0.60
MIN_MUTANTS_KILLED = 3


testbench_path = os.getenv("TESTBENCH_PATH", "verif/axi4_memory_tb.sv")
sources_dir    = os.getenv("SOURCES_DIR", "sources")
mutants_dir    = os.getenv("MUTANTS_DIR", "tests/mutants")


class TestAXI4MemorySVAGeneration:
    """Differential grading for AXI4 memory SVA assertions (HARD MODE)."""

    def test_axi4_memory_sva_generation(self):
        if not os.path.exists(testbench_path):
            pytest.fail(f"Testbench not found: {testbench_path}")

        grader = AXI4MemorySVAGrader(
            tb_path=testbench_path,
            sources_dir=sources_dir,
            mutants_dir=mutants_dir,
        )
        result = grader.grade()

        s_compile  = 1.0 if result.phase1_compiled else 0.0
        s_no_fp    = 1.0 if result.phase2_negative_passed else 0.0
        s_mutation = result.phase3_mutation.score if result.phase3_mutation else 0.0
        s_struct   = (
            min(result.phase4_structural.structural_score / 8.0, 1.0)
            if result.phase4_structural else 0.0
        )

        total_score = (
            s_compile  * WEIGHTS["compilation"]
            + s_no_fp  * WEIGHTS["no_false_positives"]
            + s_mutation * WEIGHTS["mutation"]
            + s_struct * WEIGHTS["structural"]
        )

        print("\n" + "=" * 60)
        print("GRADING SUMMARY — Differential Model (HARD MODE)")
        print("=" * 60)
        print(f"  Compilation:           {s_compile:.0%}  (weight {WEIGHTS['compilation']:.0%})")
        print(f"  No False Positives:    {s_no_fp:.0%}  (weight {WEIGHTS['no_false_positives']:.0%})")
        print(f"  Mutation Testing:      {s_mutation:.0%}  (weight {WEIGHTS['mutation']:.0%})")
        print(f"  Structural Quality:    {s_struct:.0%}  (weight {WEIGHTS['structural']:.0%})")
        print("-" * 60)
        print(f"  TOTAL SCORE:  {total_score:.1%}")
        print(f"  THRESHOLD:    {PASS_THRESHOLD:.0%}")
        print(f"  MIN MUTANTS:  {MIN_MUTANTS_KILLED}/4")
        print("=" * 60)

        if not result.phase1_compiled:
            pytest.fail(f"Compilation failed: {result.error_message}")

        if result.phase3_mutation and result.phase3_mutation.killed_mutants < MIN_MUTANTS_KILLED:
            pytest.fail(
                f"Must kill at least {MIN_MUTANTS_KILLED} mutants (differential). "
                f"Killed: {result.phase3_mutation.killed_mutants}. "
                f"Survived: {result.phase3_mutation.survived_list}"
            )

        if total_score < PASS_THRESHOLD:
            pytest.fail(
                f"Score {total_score:.1%} < threshold {PASS_THRESHOLD:.0%}. "
                f"{result.error_message}"
            )
