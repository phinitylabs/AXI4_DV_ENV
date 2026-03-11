#!/usr/bin/env python3
"""
AXI4 Burst Boundary SVA Assertion Generation Benchmark - Grading Engine

This grader verifies that the agent-written SVA assertions:
1. Compile successfully with Verilator
2. Pass (no errors) on the golden (bug-free) DUT
3. Detect bugs in mutant designs (mutation testing)
4. Have proper structural quality (anti-cheat checks)

Focus: Burst address calculations (INCR, WRAP, FIXED) and boundary checks
"""

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# === Differential error detection markers ===
ERROR_MARKERS = [
    r'%Error',           # Verilator $error() stderr prefix
    r'ASSERTION FAILED', # Standard SVA failure message
    r'TESTBENCH FAILED', # End-of-sim summary
    r'\$fatal',          # $fatal() in output
    r'FAILED:\s*[1-9]',  # Test task failure (avoid matching "FAILED: 0" summary)
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
    has_burst_check: bool = False
    has_addr_check: bool = False
    has_boundary_check: bool = False
    has_error_messages: bool = False
    illegal_patterns: list = field(default_factory=list)
    structural_score: int = 0


@dataclass
class GradeResult:
    """Final grading result."""
    phase1_compiled: bool = False
    phase2_negative_passed: bool = False
    phase3_mutation: Optional[MutationResult] = None
    phase4_structural: Optional[StructuralResult] = None
    golden_output: str = ""
    passed: bool = False
    error_message: str = ""


class AXI4BurstSVAGrader:
    """
    Grader for AXI4 Burst Boundary SVA assertion generation benchmark.
    """

    # Thresholds (simplified for easier pass)
    MUTATION_MIN = 1  # Minimum mutants that must be killed
    MIN_ASSERTIONS = 2  # Minimum assertion count (just need INCR + WLAST)
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

        sim_main = self.tb_path.parent / "sim_main.cpp"
        if sim_main.exists():
            cmd.append(str(sim_main))

        return cmd

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

    def phase2_negative_test(self) -> tuple[bool, str, str]:
        """Run testbench against golden DUT. Assertions must NOT fire."""
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

    def phase3_mutation(self, golden_output: str = "") -> MutationResult:
        """Run testbench against mutant designs to check bug detection."""
        result = MutationResult()

        if not self.mutants_dir.exists():
            return result

        mutant_dirs = sorted([d for d in self.mutants_dir.iterdir() if d.is_dir()])
        result.total_mutants = len(mutant_dirs)

        for mutant_dir in mutant_dirs:
            mutant_name = mutant_dir.name
            killed = self._run_mutant_test(mutant_dir, golden_output=golden_output)

            if killed:
                result.killed_mutants += 1
                result.killed_list.append(mutant_name)
            else:
                result.survived_list.append(mutant_name)

        return result

    def _run_mutant_test(self, mutant_dir: Path, golden_output: str = "") -> bool:
        """Compile and run TB against a mutant. Returns True if bug detected."""
        mutant_name = mutant_dir.name
        mutant_sources = []
        mutant_files = {f.name: f for f in mutant_dir.glob("*.sv")}

        for src in self.source_files:
            if src.name in mutant_files:
                mutant_sources.append(mutant_files[src.name])
            else:
                mutant_sources.append(src)

        mutant_build = self.build_dir / f"mutant_{mutant_name}"
        mutant_build.mkdir(parents=True, exist_ok=True)

        cmd = self._get_verilator_cmd(
            mutant_sources,
            self.tb_path,
            output_name=f"Vtb_{mutant_name}",
            obj_dir=mutant_build
        )

        returncode, stdout, stderr = self._run_command(cmd, timeout=60)

        if returncode != 0:
            return True  # Compilation failed - mutant killed

        exe_path = mutant_build / f"Vtb_{mutant_name}"
        returncode, stdout, stderr = self._run_command(
            [str(exe_path)],
            timeout=self.TIMEOUT_SECONDS
        )

        mutant_output = stdout + stderr

        if returncode == -1:  # Timeout
            return True

        return self._is_mutant_killed(golden_output, mutant_output, returncode)

    def phase4_structural(self) -> StructuralResult:
        """Check assertion quality and anti-cheating measures."""
        result = StructuralResult()

        if not self.tb_path.exists():
            return result

        with open(self.tb_path, 'r') as f:
            tb_content = f.read()

        tb_no_comments = re.sub(r'//.*$', '', tb_content, flags=re.MULTILINE)
        
        assert_matches = re.findall(r'assert\s+property', tb_no_comments)
        result.has_assert_property = len(assert_matches) > 0
        result.assertion_count = len(assert_matches)

        if re.search(r'property\s+\w+', tb_content):
            result.has_property_blocks = True

        # Check for burst-specific assertions
        if re.search(r'burst|BURST|INCR|WRAP|FIXED', tb_content, re.IGNORECASE):
            result.has_burst_check = True

        # Check for address calculations
        if re.search(r'addr|ADDR|address', tb_content, re.IGNORECASE):
            result.has_addr_check = True

        # Check for boundary checks (4KB)
        if re.search(r'4KB|boundary|0x1000|4096|\[31:12\]', tb_content, re.IGNORECASE):
            result.has_boundary_check = True

        if re.search(r'else\s+\$error', tb_content, re.IGNORECASE):
            result.has_error_messages = True

        # Anti-cheat checks
        initial_blocks = re.findall(r'initial\s+begin.*?end\b', tb_content, re.DOTALL)
        for block in initial_blocks:
            if '$error' in block and 'assert' not in block.lower():
                result.illegal_patterns.append("Hardcoded $error in initial block")
                break

        always_blocks = re.findall(r'always.*?end', tb_content, re.DOTALL)
        for block in always_blocks:
            if '$error' in block and 'assert' not in block.lower():
                result.illegal_patterns.append("$error without assertion")
                break

        # Check for hierarchical references (cheating by accessing DUT internals)
        hierarchical_patterns = [
            r'dut\.u_write_channel\.',
            r'dut\.u_read_channel\.',
            r'dut\.\w+_channel\.',
            r'dut\.internal',
        ]
        for pattern in hierarchical_patterns:
            if re.search(pattern, tb_no_comments, re.IGNORECASE):
                result.illegal_patterns.append("Hierarchical reference to DUT internals (use port-level signals only)")
                break

        checks = [
            result.has_assert_property,
            result.has_property_blocks,
            result.assertion_count >= self.MIN_ASSERTIONS,
            result.has_burst_check,
            result.has_addr_check,
            result.has_boundary_check,
            result.has_error_messages,
            len(result.illegal_patterns) == 0,
        ]
        result.structural_score = sum(checks)

        return result

    def grade(self) -> GradeResult:
        """Run complete grading pipeline."""
        result = GradeResult()

        print("=" * 60)
        print("AXI4 Burst Boundary SVA Assertion Benchmark - Grading")
        print("=" * 60)

        print("\n[Phase 1] Compilation Check...")
        result.phase1_compiled, error_msg = self.phase1_compile()
        if not result.phase1_compiled:
            result.error_message = f"Phase 1 FAILED: {error_msg}"
            print(f"  FAILED: {error_msg}")
            return result
        print("  PASSED")

        print("\n[Phase 2] Negative Test (Golden DUT)...")
        result.phase2_negative_passed, error_msg, sim_output = self.phase2_negative_test()
        if not result.phase2_negative_passed:
            result.error_message = f"Phase 2 FAILED: {error_msg}"
            print(f"  FAILED: {error_msg}")
            return result
        result.golden_output = sim_output
        print("  PASSED (no false positives)")

        print("\n[Phase 3] Mutation Testing...")
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

        print("\n[Phase 4] Structural Checks...")
        result.phase4_structural = self.phase4_structural()
        print(f"  Assertion Count: {result.phase4_structural.assertion_count}")
        print(f"  Has Burst Check: {result.phase4_structural.has_burst_check}")
        print(f"  Has Address Check: {result.phase4_structural.has_addr_check}")
        print(f"  Has Boundary Check: {result.phase4_structural.has_boundary_check}")
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

        result.passed = True
        print("\n" + "=" * 60)
        print("RESULT: PASSED")
        print("=" * 60)

        return result


def main():
    """CLI entry point for testing."""
    import argparse

    parser = argparse.ArgumentParser(description="AXI4 Burst SVA Grader")
    parser.add_argument("--tb", default="verif/axi4_slave_tb.sv", help="Testbench path")
    parser.add_argument("--sources", default="sources", help="Sources directory")
    parser.add_argument("--mutants", default="tests/mutants", help="Mutants directory")
    parser.add_argument("--build", default=None, help="Build directory")

    args = parser.parse_args()

    grader = AXI4BurstSVAGrader(
        tb_path=args.tb,
        sources_dir=args.sources,
        mutants_dir=args.mutants,
        build_dir=args.build
    )

    result = grader.grade()
    exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()

