"""
Hidden test for AXI4 SVA Assertion Generation Problem.

This test validates that the agent-written assertions:
1. Compile successfully
2. Pass on golden DUT (no false positives)
3. Detect bugs in mutant designs (kill mutants)
4. Have proper structural quality
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from grader import AXI4SVAGrader


def test_axi4_sva_assertions():
    """Main test for AXI4 SVA assertion generation benchmark."""
    
    proj_path = Path(__file__).resolve().parent.parent
    
    grader = AXI4SVAGrader(
        tb_path=str(proj_path / "verif" / "axi4_slave_tb.sv"),
        sources_dir=str(proj_path / "sources"),
        mutants_dir=str(proj_path / "tests" / "mutants"),
        build_dir=str(proj_path / "build")
    )
    
    result = grader.grade()
    
    # Phase 1: Compilation
    assert result.phase1_compiled, f"Phase 1 FAILED: {result.error_message}"
    
    # Phase 2: Negative test (no false positives on golden DUT)
    assert result.phase2_negative_passed, f"Phase 2 FAILED: {result.error_message}"
    
    # Phase 3: Mutation testing (must kill at least 5 mutants)
    if result.phase3_mutation:
        assert result.phase3_mutation.killed_mutants >= 2, (
            f"Phase 3 FAILED: Only {result.phase3_mutation.killed_mutants} mutants killed, "
            f"need at least 5. Survived: {result.phase3_mutation.survived_list}"
        )
    
    # Phase 4: Structural checks (at least 5 assertions, no cheating)
    if result.phase4_structural:
        assert result.phase4_structural.assertion_count >= 2, (
            f"Phase 4 FAILED: Only {result.phase4_structural.assertion_count} assertions found, "
            f"need at least 5"
        )
        assert len(result.phase4_structural.illegal_patterns) == 0, (
            f"Phase 4 FAILED: Suspicious patterns found: {result.phase4_structural.illegal_patterns}"
        )
    
    print("ALL PHASES PASSED!")

