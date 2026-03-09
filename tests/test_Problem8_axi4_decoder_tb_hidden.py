"""
AXI4 Decoder Testbench Generation — Three-Pillar Grading (HARD MODE)

Industry-standard TB quality metrics:
  Pillar 1 (25%): Code Coverage   — Verilator --coverage-line → coverage.dat
  Pillar 2 (25%): Functional Coverage — axi4_coverage.sv COVERAGE_BINS_HIT
  Pillar 3 (20%): Differential Mutation Testing — golden vs mutant output

Weights:
  Compilation:          10%
  No False Positives:   20%
  Code Coverage:        25%
  Functional Coverage:  25%
  Mutation Testing:     20%

Pass Threshold: 60%
Hard requirement: must kill at least 3/4 mutants via differential comparison
"""

import os
import pytest
from grader import AXI4DecoderTBGrader


WEIGHTS = {
    "compilation":         0.10,
    "no_false_positives":  0.20,
    "code_coverage":       0.25,
    "functional_coverage": 0.25,
    "mutation":            0.20,
}

PASS_THRESHOLD = 0.60
MIN_MUTANTS_KILLED = 3


testbench_path = os.getenv("TESTBENCH_PATH", "verif/axi4_decoder_tb.sv")
sources_dir    = os.getenv("SOURCES_DIR", "sources")
mutants_dir    = os.getenv("MUTANTS_DIR", "tests/mutants")


class TestAXI4DecoderTBGeneration:
    """Three-pillar grading for AXI4 decoder testbench generation (HARD MODE)."""

    def test_axi4_decoder_tb_generation(self):
        if not os.path.exists(testbench_path):
            pytest.fail(f"Testbench not found: {testbench_path}")

        grader = AXI4DecoderTBGrader(
            tb_path=testbench_path,
            sources_dir=sources_dir,
            mutants_dir=mutants_dir,
        )
        result = grader.grade()

        # ---- Score each pillar ----
        s_compile  = 1.0 if result.phase1_compiled else 0.0
        s_no_fp    = 1.0 if result.phase2_negative_passed else 0.0

        # Pillar 1: Code Coverage from coverage.dat
        s_line_cov = 0.0
        if result.phase4_coverage:
            s_line_cov = result.phase4_coverage.line_coverage

        # Pillar 2: Functional Coverage from axi4_coverage.sv (if present)
        s_func_cov = 0.0
        # Extracted from golden_output stored in result (if coverage module used)
        if result.golden_output:
            import re
            m = re.search(r"COVERAGE_BINS_HIT=(\d+)", result.golden_output)
            if m:
                bins_hit = int(m.group(1))
                total_m = re.search(r"COVERAGE_BINS_TOTAL=(\d+)", result.golden_output)
                total = int(total_m.group(1)) if total_m else 24
                s_func_cov = min(bins_hit / total, 1.0)

        # Pillar 3: Mutation score (differential)
        s_mutation = 0.0
        if result.phase3_mutation:
            s_mutation = result.phase3_mutation.score

        total_score = (
            s_compile         * WEIGHTS["compilation"]
            + s_no_fp         * WEIGHTS["no_false_positives"]
            + s_line_cov      * WEIGHTS["code_coverage"]
            + s_func_cov      * WEIGHTS["functional_coverage"]
            + s_mutation      * WEIGHTS["mutation"]
        )

        print("\n" + "=" * 60)
        print("GRADING SUMMARY — Three-Pillar Model (HARD MODE)")
        print("=" * 60)
        print(f"  Compilation:           {s_compile:.0%}  (weight {WEIGHTS['compilation']:.0%})")
        print(f"  No False Positives:    {s_no_fp:.0%}  (weight {WEIGHTS['no_false_positives']:.0%})")
        print(f"  Code Coverage:         {s_line_cov:.0%}  (weight {WEIGHTS['code_coverage']:.0%})")
        print(f"  Functional Coverage:   {s_func_cov:.0%}  (weight {WEIGHTS['functional_coverage']:.0%})")
        print(f"  Mutation Testing:      {s_mutation:.0%}  (weight {WEIGHTS['mutation']:.0%})")
        print("-" * 60)
        print(f"  TOTAL SCORE:  {total_score:.1%}")
        print(f"  THRESHOLD:    {PASS_THRESHOLD:.0%}")
        print(f"  MIN MUTANTS:  {MIN_MUTANTS_KILLED}/4")
        print("=" * 60)

        if not result.phase1_compiled:
            pytest.fail(f"Compilation failed: {result.error_message}")

        # Hard requirement: differential kill gate
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
