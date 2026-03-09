"""
AXI4 Read Channel Complete Verification — Three-Pillar Grading

Industry-standard TB quality metrics:
  Pillar 1 (30%): Code Coverage   — Verilator --coverage-line → coverage.dat
  Pillar 2 (30%): Functional Coverage — axi4_coverage.sv COVERAGE_BINS_HIT
  Pillar 3 (15%): Differential Mutation Testing — golden vs mutant output

Weights:
  Compilation:          10%
  No False Positives:   15%
  Code Coverage:        30%
  Functional Coverage:  30%
  Mutation Testing:     15%

Pass Threshold: 60%
"""

import os
import pytest
from grader import AXI4ReadChannelGrader


WEIGHTS = {
    "compilation":         0.10,
    "no_false_positives":  0.15,
    "code_coverage":       0.30,
    "functional_coverage": 0.30,
    "mutation":            0.15,
}

PASS_THRESHOLD = 0.60


testbench_path = os.getenv("TESTBENCH_PATH", "verif/axi4_read_channel_tb.sv")
sources_dir    = os.getenv("SOURCES_DIR", "sources")
mutants_dir    = os.getenv("MUTANTS_DIR", "tests/mutants")


class TestAXI4ReadChannelVerification:
    """Three-pillar grading for AXI4 read channel TB + assertions."""

    def test_axi4_read_channel_verification(self):
        if not os.path.exists(testbench_path):
            pytest.fail(f"Testbench not found: {testbench_path}")

        grader = AXI4ReadChannelGrader(
            tb_path=testbench_path,
            sources_dir=sources_dir,
            mutants_dir=mutants_dir,
        )
        result = grader.grade()

        # ---- Score each pillar ----

        # Pillar 0a: Compilation (10%)
        s_compile = 1.0 if result.phase1_compiled else 0.0

        # Pillar 0b: No false positives (15%)
        s_no_fp = 1.0 if result.phase2_negative_passed else 0.0

        # Pillar 1: Code Coverage (30%) — from coverage.dat line %
        s_line_cov = 0.0
        if result.phase3_coverage:
            s_line_cov = result.phase3_coverage.line_coverage

        # Pillar 2: Functional Coverage (30%) — from axi4_coverage.sv bins
        s_func_cov = 0.0
        if result.phase3_coverage:
            s_func_cov = result.phase3_coverage.functional_coverage

        # Pillar 3: Mutation score (15%) — differential comparison
        s_mutation = 0.0
        if result.phase4_mutation:
            s_mutation = result.phase4_mutation.score

        # ---- Weighted total ----
        total_score = (
            s_compile         * WEIGHTS["compilation"]
            + s_no_fp         * WEIGHTS["no_false_positives"]
            + s_line_cov      * WEIGHTS["code_coverage"]
            + s_func_cov      * WEIGHTS["functional_coverage"]
            + s_mutation      * WEIGHTS["mutation"]
        )

        print("\n" + "=" * 60)
        print("GRADING SUMMARY — Three-Pillar Model")
        print("=" * 60)
        print(f"  Compilation:           {s_compile:.0%}  (weight {WEIGHTS['compilation']:.0%})")
        print(f"  No False Positives:    {s_no_fp:.0%}  (weight {WEIGHTS['no_false_positives']:.0%})")
        print(f"  Code Coverage:         {s_line_cov:.0%}  (weight {WEIGHTS['code_coverage']:.0%})")
        print(f"  Functional Coverage:   {s_func_cov:.0%}  (weight {WEIGHTS['functional_coverage']:.0%})")
        print(f"  Mutation Testing:      {s_mutation:.0%}  (weight {WEIGHTS['mutation']:.0%})")
        print("-" * 60)
        print(f"  TOTAL SCORE:  {total_score:.1%}")
        print(f"  THRESHOLD:    {PASS_THRESHOLD:.0%}")
        print("=" * 60)

        if not result.phase1_compiled:
            pytest.fail(f"Compilation failed: {result.error_message}")

        if total_score < PASS_THRESHOLD:
            pytest.fail(
                f"Score {total_score:.1%} < threshold {PASS_THRESHOLD:.0%}. "
                f"{result.error_message}"
            )
