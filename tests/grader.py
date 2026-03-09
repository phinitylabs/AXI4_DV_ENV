#!/usr/bin/env python3
"""
AXI4 SVA Assertion Generation Benchmark - Grading Engine

This grader verifies that the agent-written SVA assertions:
1. Compile successfully with Verilator
2. Pass (no errors) on the golden (bug-free) DUT
3. Detect bugs in mutant designs (mutation testing)
4. Have proper structural quality (anti-cheat checks)

Grading Phases:
1. Compilation Check - TB with assertions compiles with Verilator
2. Negative Test - Assertions PASS on golden DUT (no false positives)
3. Mutation Testing - Assertions detect bugs in mutant designs
4. Structural Checks - Verify assertions exist and follow best practices
"""

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# === Differential error detection markers (ungameable) ===
ERROR_MARKERS = [
    r'%Error',           # Verilator $error() stderr prefix
    r'ASSERTION FAILED', # Standard SVA failure message
    r'TESTBENCH FAILED', # End-of-sim summary
    r'\$fatal',          # $fatal() in output
    r'FAILED:',          # Test task failure
    r'\[ERROR\]',        # Alternative error format
]


@dataclass
class MutationResult:
    """Mutation testing results."""
    total_mutants: int = 0
    killed_mutants: int = 0
    killed_list: list = field(default_factory=list)
    survived_list: list = field(default_factory=list)

    @property
    def score(self) -> float:
        if self.total_mutants == 0:
            return 0.0
        return self.killed_mutants / self.total_mutants


@dataclass
class StructuralResult:
    """Structural quality check results."""
    has_assert_property: bool = False
    has_property_blocks: bool = False
    assertion_count: int = 0
    has_valid_stability: bool = False
    has_resp_check: bool = False
    has_timing_check: bool = False
    has_error_messages: bool = False
    illegal_patterns: list = field(default_factory=list)
    structural_score: int = 0


@dataclass
class GradeResult:
    """Final grading result."""
    # Phase results
    phase1_compiled: bool = False
    phase2_negative_passed: bool = False
    phase3_mutation: Optional[MutationResult] = None
    phase4_structural: Optional[StructuralResult] = None

    # Overall
    golden_output: str = ""
    passed: bool = False
    error_message: str = ""


class AXI4SVAGrader:
    """
    Grader for AXI4 SVA assertion generation benchmark.
    """

    # Thresholds
    MUTATION_MIN = 5  # Minimum mutants that must be killed
    MIN_ASSERTIONS = 5  # Minimum assertion count
    TIMEOUT_SECONDS = 60

    def __init__(
        self,
        tb_path: str,
        sources_dir: str,
        mutants_dir: str,
        build_dir: Optional[str] = None
    ):
        self.tb_path = Path(tb_path).resolve()
        self.sources_dir = Path(sources_dir).resolve()
        self.mutants_dir = Path(mutants_dir).resolve()
        self.build_dir = Path(build_dir).resolve() if build_dir else Path(tempfile.mkdtemp())

        # Get ordered source files (package first)
        self.source_files = self._get_ordered_sources()

    def _get_ordered_sources(self) -> list[Path]:
        """Get source files in correct compilation order."""
        all_files = list(self.sources_dir.glob("*.sv"))
        pkg_files = [f for f in all_files if 'pkg' in f.name.lower()]
        other_files = [f for f in all_files if 'pkg' not in f.name.lower()]
        pkg_files.sort()
        other_files.sort()
        return pkg_files + other_files

    def _run_command(
        self,
        cmd: list,
        cwd: Optional[Path] = None,
        timeout: int = 60
    ) -> tuple[int, str, str]:
        """Run a command and return (returncode, stdout, stderr)."""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "TIMEOUT"
        except Exception as e:
            return -2, "", str(e)

    def _count_errors(self, output: str) -> int:
        return sum(len(re.findall(p, output, re.IGNORECASE)) for p in ERROR_MARKERS)

    def _is_mutant_killed(self, golden_out: str, mutant_out: str, mutant_exit: int) -> bool:
        return (
            self._count_errors(golden_out) == 0
            and (self._count_errors(mutant_out) > 0 or mutant_exit != 0)
        )

    def _get_verilator_cmd(
        self,
        sources: list[Path],
        tb_path: Path,
        output_name: str = "Vtb",
        obj_dir: Optional[Path] = None
    ) -> list[str]:
        """Build Verilator compilation command."""
        if obj_dir is None:
            obj_dir = self.build_dir / "obj_dir"

        obj_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            "verilator",
            "--cc", "--exe", "--build",
            "-j", "1",
            "--timing",
            "--assert",
            "-Wno-fatal",
            "-Wno-WIDTHEXPAND",
            "-Wno-WIDTHTRUNC",
            "-Wno-TIMESCALEMOD",
            "-Wno-INITIALDLY",
            "-Wno-UNSIGNED",
            "--top-module", "axi4_slave_tb",
            "-o", output_name,
            "-Mdir", str(obj_dir),
        ]

        for src in sources:
            cmd.append(str(src))

        cmd.append(str(tb_path))

        # Add C++ main wrapper if exists
        sim_main = self.tb_path.parent / "sim_main.cpp"
        if sim_main.exists():
            cmd.append(str(sim_main))

        return cmd

    # =========================================================================
    # Phase 1: Compilation Check
    # =========================================================================
    def phase1_compile(self) -> tuple[bool, str]:
        """Check if testbench with assertions compiles."""
        if not self.tb_path.exists():
            return False, f"Testbench file not found: {self.tb_path}"

        self.build_dir.mkdir(parents=True, exist_ok=True)
        obj_dir = self.build_dir / "obj_dir"
        obj_dir.mkdir(parents=True, exist_ok=True)

        cmd = self._get_verilator_cmd(
            self.source_files,
            self.tb_path,
            output_name="Vtb_golden",
            obj_dir=obj_dir
        )

        returncode, stdout, stderr = self._run_command(cmd, timeout=120)

        if returncode != 0:
            combined = stdout + stderr
            error_lines = [l for l in combined.split('\n') if 'Error' in l or 'error' in l]
            error_msg = '\n'.join(error_lines[:5]) if error_lines else combined[:500]
            return False, f"Compilation failed:\n{error_msg}"

        return True, ""

    # =========================================================================
    # Phase 2: Negative Test (Run on Golden DUT)
    # =========================================================================
    def phase2_negative_test(self) -> tuple[bool, str, str]:
        """
        Run testbench against golden (bug-free) DUT.
        Assertions must NOT fire (no false positives).
        """
        obj_dir = self.build_dir / "obj_dir"
        exe_path = obj_dir / "Vtb_golden"

        if not exe_path.exists():
            return False, "Executable not found - compile first", ""

        returncode, stdout, stderr = self._run_command(
            [str(exe_path)],
            cwd=self.build_dir,
            timeout=self.TIMEOUT_SECONDS
        )

        sim_output = stdout + stderr

        if returncode == -1:
            return False, "Simulation timeout (possible infinite loop)", sim_output

        n_errors = self._count_errors(sim_output)
        if n_errors > 0:
            return False, f"Assertions fired on golden DUT ({n_errors} false positives)", sim_output

        return True, "", sim_output

    # =========================================================================
    # Phase 3: Mutation Testing (differential)
    # =========================================================================
    def phase3_mutation(self, golden_output: str = "") -> MutationResult:
        """Run testbench against mutant designs to check bug detection."""
        result = MutationResult()

        if not self.mutants_dir.exists():
            return result

        mutant_dirs = sorted([d for d in self.mutants_dir.iterdir() if d.is_dir()])
        result.total_mutants = len(mutant_dirs)

        for mutant_dir in mutant_dirs:
            mutant_name = mutant_dir.name
            killed = self._run_mutant_test(mutant_dir, golden_output)

            if killed:
                result.killed_mutants += 1
                result.killed_list.append(mutant_name)
            else:
                result.survived_list.append(mutant_name)

        return result

    def _run_mutant_test(self, mutant_dir: Path, golden_output: str = "") -> bool:
        """
        Compile and run TB against a mutant.
        Returns True if assertions detect the bug (kill the mutant).
        """
        mutant_name = mutant_dir.name

        # Build source list with mutant files overriding golden
        mutant_sources = []
        mutant_files = {f.name: f for f in mutant_dir.glob("*.sv")}

        for src in self.source_files:
            if src.name in mutant_files:
                mutant_sources.append(mutant_files[src.name])
            else:
                mutant_sources.append(src)

        # Create temp build directory for this mutant
        mutant_build = self.build_dir / f"mutant_{mutant_name}"
        mutant_build.mkdir(parents=True, exist_ok=True)

        # Compile with mutant
        cmd = self._get_verilator_cmd(
            mutant_sources,
            self.tb_path,
            output_name=f"Vtb_{mutant_name}",
            obj_dir=mutant_build
        )

        returncode, stdout, stderr = self._run_command(cmd, timeout=60)

        if returncode != 0:
            # Compilation failed - mutant might have syntax error
            return True

        # Run simulation
        exe_path = mutant_build / f"Vtb_{mutant_name}"
        returncode, stdout, stderr = self._run_command(
            [str(exe_path)],
            timeout=self.TIMEOUT_SECONDS
        )

        mutant_output = stdout + stderr

        if returncode == -1:  # Timeout = deadlock = bug detected
            return True

        return self._is_mutant_killed(golden_output, mutant_output, returncode)

    # =========================================================================
    # Phase 4: Structural Checks
    # =========================================================================
    def phase4_structural(self) -> StructuralResult:
        """Check assertion quality and anti-cheating measures."""
        result = StructuralResult()

        if not self.tb_path.exists():
            return result

        with open(self.tb_path, 'r') as f:
            tb_content = f.read()

        # Remove single-line comments for analysis
        tb_no_comments = re.sub(r'//.*$', '', tb_content, flags=re.MULTILINE)
        
        # Check for assert property statements (excluding comments)
        assert_matches = re.findall(r'assert\s+property', tb_no_comments)
        result.has_assert_property = len(assert_matches) > 0
        result.assertion_count = len(assert_matches)

        # Check for property blocks (excluding comments)
        property_matches = re.findall(r'property\s+\w+', tb_no_comments)
        result.has_property_blocks = len(property_matches) > 0

        # Check for VALID stability assertions
        valid_patterns = [r'awvalid.*stable', r'wvalid.*stable', r'arvalid.*stable',
                         r'bvalid.*stable', r'rvalid.*stable', r'\|=>\s*\w*valid']
        for pattern in valid_patterns:
            if re.search(pattern, tb_content, re.IGNORECASE):
                result.has_valid_stability = True
                break

        # Check for response code checks
        if re.search(r'bresp|rresp', tb_content, re.IGNORECASE):
            result.has_resp_check = True

        # Check for timing/sequence checks
        if re.search(r'\|->|\|=>', tb_content):
            result.has_timing_check = True

        # Check for error messages in assertions
        if re.search(r'else\s+\$error', tb_content, re.IGNORECASE):
            result.has_error_messages = True

        # Anti-cheat: Check for suspicious patterns
        # 1. Hardcoded $error in initial block (not in assertions)
        # Look for initial blocks containing $error directly (not in assert property)
        initial_blocks = re.findall(r'initial\s+begin.*?end\b', tb_content, re.DOTALL)
        for block in initial_blocks:
            # Skip if the block contains $finish, $display, etc. but not hardcoded $error
            if '$error' in block and 'assert' not in block.lower():
                result.illegal_patterns.append("Hardcoded $error in initial block")
                break

        # 2. $error in always block without assertion
        always_blocks = re.findall(r'always.*?end', tb_content, re.DOTALL)
        for block in always_blocks:
            if '$error' in block and 'assert' not in block.lower():
                result.illegal_patterns.append("$error without assertion")
                break

        # Calculate structural score
        checks = [
            result.has_assert_property,
            result.has_property_blocks,
            result.assertion_count >= self.MIN_ASSERTIONS,
            result.has_valid_stability,
            result.has_resp_check,
            result.has_timing_check,
            result.has_error_messages,
            len(result.illegal_patterns) == 0,
        ]
        result.structural_score = sum(checks)

        return result

    # =========================================================================
    # Main Grading Pipeline
    # =========================================================================
    def grade(self) -> GradeResult:
        """Run complete grading pipeline."""
        result = GradeResult()

        print("=" * 60)
        print("AXI4 SVA Assertion Generation Benchmark - Grading")
        print("=" * 60)

        # Phase 1: Compilation
        print("\n[Phase 1] Compilation Check...")
        result.phase1_compiled, error_msg = self.phase1_compile()
        if not result.phase1_compiled:
            result.error_message = f"Phase 1 FAILED: {error_msg}"
            print(f"  FAILED: {error_msg}")
            return result
        print("  PASSED")

        # Phase 2: Negative Test
        print("\n[Phase 2] Negative Test (Golden DUT)...")
        result.phase2_negative_passed, error_msg, sim_output = self.phase2_negative_test()
        if not result.phase2_negative_passed:
            result.error_message = f"Phase 2 FAILED: {error_msg}"
            print(f"  FAILED: {error_msg}")
            return result
        print("  PASSED (no false positives)")

        # Phase 3: Mutation Testing
        print("\n[Phase 3] Mutation Testing...")
        result.golden_output = sim_output
        result.phase3_mutation = self.phase3_mutation(golden_output=sim_output)
        print(f"  Mutants Killed: {result.phase3_mutation.killed_mutants}/{result.phase3_mutation.total_mutants}")
        print(f"  Killed: {result.phase3_mutation.killed_list}")
        print(f"  Survived: {result.phase3_mutation.survived_list}")

        if result.phase3_mutation.killed_mutants < self.MUTATION_MIN:
            result.error_message = (
                f"Phase 3 FAILED: Only {result.phase3_mutation.killed_mutants} mutants killed, "
                f"need {self.MUTATION_MIN}"
            )
            print(f"  FAILED: {result.error_message}")
            return result
        print("  PASSED")

        # Phase 4: Structural Checks
        print("\n[Phase 4] Structural Checks...")
        result.phase4_structural = self.phase4_structural()
        print(f"  Assertion Count: {result.phase4_structural.assertion_count}")
        print(f"  Has Property Blocks: {result.phase4_structural.has_property_blocks}")
        print(f"  Has VALID Stability: {result.phase4_structural.has_valid_stability}")
        print(f"  Has Response Check: {result.phase4_structural.has_resp_check}")
        print(f"  Has Timing Check: {result.phase4_structural.has_timing_check}")
        print(f"  Structural Score: {result.phase4_structural.structural_score}/8")

        if result.phase4_structural.illegal_patterns:
            result.error_message = (
                f"Phase 4 FAILED: Suspicious patterns found: "
                f"{result.phase4_structural.illegal_patterns}"
            )
            print(f"  FAILED: {result.error_message}")
            return result

        if result.phase4_structural.assertion_count < self.MIN_ASSERTIONS:
            result.error_message = (
                f"Phase 4 FAILED: Only {result.phase4_structural.assertion_count} assertions, "
                f"need at least {self.MIN_ASSERTIONS}"
            )
            print(f"  FAILED: {result.error_message}")
            return result
        print("  PASSED")

        # All phases passed!
        result.passed = True
        print("\n" + "=" * 60)
        print("RESULT: PASSED")
        print("=" * 60)

        return result


def main():
    """CLI entry point for testing."""
    import argparse

    parser = argparse.ArgumentParser(description="AXI4 SVA Grader")
    parser.add_argument("--tb", default="verif/axi4_slave_tb.sv", help="Testbench path")
    parser.add_argument("--sources", default="sources", help="Sources directory")
    parser.add_argument("--mutants", default="tests/mutants", help="Mutants directory")
    parser.add_argument("--build", default=None, help="Build directory")

    args = parser.parse_args()

    grader = AXI4SVAGrader(
        tb_path=args.tb,
        sources_dir=args.sources,
        mutants_dir=args.mutants,
        build_dir=args.build
    )

    result = grader.grade()
    exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()

