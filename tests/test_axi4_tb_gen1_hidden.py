"""
Hidden test for AXI4 Testbench Generation Problem.
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from grader import AXI4TBGrader


def test_axi4_testbench_generation():
    proj_path = Path(__file__).resolve().parent.parent
    
    grader = AXI4TBGrader(
        tb_path=str(proj_path / "verif" / "axi4_slave_tb.sv"),
        sources_dir=str(proj_path / "sources"),
        mutants_dir=str(proj_path / "tests" / "mutants"),
        build_dir=str(proj_path / "build")
    )
    
    result = grader.grade()
    
    assert result.phase1_compiled, f"Phase 1 FAILED: {result.error_message}"
    assert result.phase2_negative_passed, f"Phase 2 FAILED: {result.error_message}"
    
    if result.phase3_coverage:
        assert result.phase3_coverage.line_coverage >= 0.60
    
    if result.phase4_mutation:
        assert result.phase4_mutation.killed_mutants >= 5
    
    print("ALL PHASES PASSED!")
