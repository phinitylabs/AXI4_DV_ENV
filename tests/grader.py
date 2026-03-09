#!/usr/bin/env python3
"""
AXI4 Memory Data Integrity SVA Benchmark - Grading Engine (HARD MODE)

This grader verifies that the agent-written SVA assertions:
1. Compile successfully with Verilator
2. Pass (no errors) on the golden (bug-free) DUT
3. Detect bugs in mutant designs (mutation testing)
4. Have proper structural quality (assertion patterns)

Focus: Memory data integrity - read after write, address mapping, timing
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
    has_tracking_logic: bool = False
    has_assert_property: bool = False
    has_property_blocks: bool = False
    assertion_count: int = 0
    has_data_check: bool = False
    has_timing_check: bool = False
    has_reference_model: bool = False
    uses_error: bool = False
    structural_score: int = 0


@dataclass
class GradeResult:
    """Final grading result."""
    phase1_compiled: bool = False
    phase2_negative_passed: bool = False
    phase3_mutation: Optional[MutationResult] = None
    phase4_structural: Optional[StructuralResult] = None
    golden_output: str = ""   # Stored from Phase 2 for differential comparison
    passed: bool = False
    error_message: str = ""


class AXI4MemorySVAGrader:
    """
    Grader for AXI4 Memory SVA assertion generation benchmark.
    """

    # Thresholds (HARD MODE)
    MUTATION_MIN = 3  # Must kill 3 out of 4 mutants
    MIN_ASSERTIONS = 3  # Minimum assertion count
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
        """Run command and return exit code, stdout, stderr."""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.build_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)

    def _compile(self, extra_sources: list[Path] = None) -> tuple[bool, str]:
        """Compile testbench with Verilator."""
        sources = extra_sources if extra_sources else self.source_files
        source_args = [str(f) for f in sources]
        
        cmd = [
            "verilator", "--binary", "-j", "0",
            "--timing", "--assert",
            "-Wno-fatal", "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC",
            "-o", "sim"
        ] + source_args + [str(self.tb_path)]

        code, stdout, stderr = self._run_command(cmd, timeout=self.TIMEOUT_SECONDS)
        
        if code != 0:
            return False, f"Compilation failed:\n{stderr}"
        return True, ""

    def _run_simulation(self) -> tuple[bool, str, str]:
        """Run compiled simulation."""
        sim_path = self.build_dir / "obj_dir" / "sim"
        if not sim_path.exists():
            sim_path = self.build_dir / "sim"
        if not sim_path.exists():
            return False, "", "Simulation binary not found"
        
        code, stdout, stderr = self._run_command(
            [str(sim_path)],
            timeout=self.TIMEOUT_SECONDS
        )
        
        return code == 0, stdout, stderr

    def _count_errors(self, output: str) -> int:
        """Count error markers in combined stdout+stderr."""
        return sum(len(re.findall(p, output, re.IGNORECASE)) for p in ERROR_MARKERS)

    def _is_mutant_killed(self, golden_out: str, mutant_out: str, mutant_exit: int) -> bool:
        """
        Differential kill detection (ungameable).
        Mutant is KILLED only if golden has 0 errors AND mutant has errors or nonzero exit.
        """
        return (
            self._count_errors(golden_out) == 0
            and (self._count_errors(mutant_out) > 0 or mutant_exit != 0)
        )

    def _phase1_compile(self, result: GradeResult) -> bool:
        """Phase 1: Check if testbench compiles."""
        print("\n[Phase 1] Compilation Check...")
        
        success, error_msg = self._compile()
        if not success:
            result.error_message = f"Phase 1 FAILED: {error_msg}"
            print(f"  FAILED: {error_msg[:100]}...")
            return False
        
        print("  PASSED")
        result.phase1_compiled = True
        return True

    def _phase2_negative_test(self, result: GradeResult) -> bool:
        """Phase 2: Run on golden DUT. Gate: 0 error markers. Also stores golden output."""
        print("\n[Phase 2] Negative Test (Golden DUT)...")

        success, stdout, stderr = self._run_simulation()
        golden_output = stdout + stderr
        result.golden_output = golden_output  # Saved for Phase 3 differential

        n_errors = self._count_errors(golden_output)
        if n_errors > 0:
            result.error_message = (
                f"Phase 2 FAILED: {n_errors} error marker(s) on golden DUT (false positives)"
            )
            print(f"  FAILED: {n_errors} false positive(s)")
            return False

        print("  PASSED (no false positives)")
        result.phase2_negative_passed = True
        return True

    def _phase3_mutation_testing(self, result: GradeResult) -> bool:
        """Phase 3: Differential mutation testing. Each .sv replaces axi4_memory.sv."""
        print("\n[Phase 3] Mutation Testing...")
        
        mutation_result = MutationResult()
        
        if not self.mutants_dir.exists():
            result.error_message = "Phase 3 FAILED: No mutants directory"
            print("  FAILED: No mutants found")
            return False
        
        mutant_files = list(self.mutants_dir.glob("*.sv"))
        mutation_result.total_mutants = len(mutant_files)
        
        if mutation_result.total_mutants == 0:
            result.error_message = "Phase 3 FAILED: No mutant files"
            print("  FAILED: No mutant files")
            return False
        
        for mutant_file in mutant_files:
            mutant_name = mutant_file.stem
            
            # Create temp directory for this mutant
            mutant_build = Path(tempfile.mkdtemp())
            
            try:
                # Copy all sources except the original memory
                mutant_sources = []
                for src in self.source_files:
                    if 'memory' not in src.name.lower():
                        mutant_sources.append(src)
                mutant_sources.append(mutant_file)
                
                # Compile with mutant
                source_args = [str(f) for f in mutant_sources]
                cmd = [
                    "verilator", "--binary", "-j", "0",
                    "--timing", "--assert",
                    "-Wno-fatal", "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC",
                    "-o", "sim"
                ] + source_args + [str(self.tb_path)]
                
                code, _, stderr = self._run_command(cmd, cwd=mutant_build, timeout=30)

                if code != 0:
                    # Compile failure counts as killed
                    mutation_result.killed_mutants += 1
                    mutation_result.killed_list.append(f"{mutant_name}(compile_fail)")
                    print(f"    {mutant_name}: KILLED (compile fail)")
                    continue

                # Run simulation
                sim_path = mutant_build / "obj_dir" / "sim"
                if not sim_path.exists():
                    sim_path = mutant_build / "sim"

                code, stdout, stderr = self._run_command(
                    [str(sim_path)], cwd=mutant_build, timeout=30
                )
                mutant_output = stdout + stderr

                # Differential comparison: kill only if golden is clean AND mutant has errors
                if self._is_mutant_killed(result.golden_output, mutant_output, code):
                    mutation_result.killed_mutants += 1
                    mutation_result.killed_list.append(mutant_name)
                    print(f"    {mutant_name}: KILLED")
                else:
                    mutation_result.survived_list.append(mutant_name)
                    print(f"    {mutant_name}: survived")
                    
            finally:
                shutil.rmtree(mutant_build, ignore_errors=True)
        
        result.phase3_mutation = mutation_result
        
        print(f"  Mutants Killed: {mutation_result.killed_mutants}/{mutation_result.total_mutants}")
        print(f"  Killed: {mutation_result.killed_list}")
        print(f"  Survived: {mutation_result.survived_list}")
        
        if mutation_result.killed_mutants < self.MUTATION_MIN:
            result.error_message = (
                f"Phase 3 FAILED: Only {mutation_result.killed_mutants} mutants killed, "
                f"need {self.MUTATION_MIN}"
            )
            return False
        
        return True

    def _phase4_structural_quality(self, result: GradeResult) -> bool:
        """Phase 4: Check assertion structure and quality."""
        print("\n[Phase 4] Structural Quality Check...")
        
        struct_result = StructuralResult()
        
        try:
            tb_content = self.tb_path.read_text()
        except Exception as e:
            result.error_message = f"Phase 4 FAILED: Cannot read testbench: {e}"
            return False
        
        # Check for tracking/reference model (agent must implement this)
        struct_result.has_tracking_logic = bool(re.search(
            r'(expected|reference|shadow|model|track)',
            tb_content, re.IGNORECASE
        ))
        
        struct_result.has_reference_model = bool(re.search(
            r'(expected_mem|shadow_mem|ref_mem|expected_data)',
            tb_content, re.IGNORECASE
        ))
        
        # Check for assertion patterns
        struct_result.has_assert_property = bool(re.search(
            r'assert\s+property', tb_content, re.IGNORECASE
        ))
        
        struct_result.has_property_blocks = bool(re.search(
            r'property\s+\w+', tb_content
        ))
        
        # Count assertions (SVA or immediate)
        sva_assertions = re.findall(r'assert\s+property\s*\([^)]+\)', tb_content)
        immediate_assertions = re.findall(r'\$error\s*\(', tb_content)
        struct_result.assertion_count = len(sva_assertions) + len(immediate_assertions)
        
        # Check for data integrity checks
        struct_result.has_data_check = bool(re.search(
            r'(rd_data\s*===?|===?\s*rd_data|expected.*==|==.*expected)',
            tb_content, re.IGNORECASE
        ))
        
        # Check for timing checks
        struct_result.has_timing_check = bool(re.search(
            r'(rd_valid.*rd_en|rd_en.*rd_valid|\|->|\|=>)',
            tb_content
        ))
        
        # Check for $error usage
        struct_result.uses_error = bool(re.search(
            r'\$error\s*\(',
            tb_content
        ))
        
        # Calculate score
        struct_result.structural_score = sum([
            struct_result.has_tracking_logic,
            struct_result.has_reference_model,
            struct_result.has_assert_property or struct_result.uses_error,
            struct_result.has_property_blocks,
            struct_result.assertion_count >= 2,
            struct_result.assertion_count >= 3,
            struct_result.has_data_check,
            struct_result.has_timing_check,
        ])
        
        result.phase4_structural = struct_result
        
        print(f"  Has tracking logic: {struct_result.has_tracking_logic}")
        print(f"  Has reference model: {struct_result.has_reference_model}")
        print(f"  Has assert property: {struct_result.has_assert_property}")
        print(f"  Has property blocks: {struct_result.has_property_blocks}")
        print(f"  Assertion/check count: {struct_result.assertion_count}")
        print(f"  Has data integrity check: {struct_result.has_data_check}")
        print(f"  Has timing check: {struct_result.has_timing_check}")
        print(f"  Uses $error: {struct_result.uses_error}")
        print(f"  Structural score: {struct_result.structural_score}/8")
        
        # Require reference model
        if not struct_result.has_reference_model:
            result.error_message = (
                "Phase 4 FAILED: Must implement a reference model "
                "(expected_mem, shadow_mem, etc.) to track expected data"
            )
            return False
        
        if struct_result.assertion_count < self.MIN_ASSERTIONS:
            result.error_message = (
                f"Phase 4 FAILED: Only {struct_result.assertion_count} assertions/checks, "
                f"need at least {self.MIN_ASSERTIONS}"
            )
            return False
        
        if not struct_result.uses_error:
            result.error_message = "Phase 4 FAILED: Must use $error() to report failures"
            return False
        
        return True

    def grade(self) -> GradeResult:
        """Run all grading phases."""
        result = GradeResult()
        
        print("=" * 60)
        print("AXI4 Memory SVA Assertion Benchmark - Grading (HARD MODE)")
        print("=" * 60)
        print(f"Requirements:")
        print(f"  - Kill {self.MUTATION_MIN}/4 mutants")
        print(f"  - At least {self.MIN_ASSERTIONS} assertions/checks")
        print(f"  - Must implement reference model (expected_mem)")
        print(f"  - Must use $error() for failures")
        print("=" * 60)
        
        if not self._phase1_compile(result):
            return result
        
        if not self._phase2_negative_test(result):
            return result
        
        if not self._phase3_mutation_testing(result):
            return result
        
        if not self._phase4_structural_quality(result):
            return result
        
        result.passed = True
        return result


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Grade AXI4 memory SVA")
    parser.add_argument("--tb", default="verif/axi4_memory_tb.sv", help="Testbench path")
    parser.add_argument("--sources", default="sources", help="Sources directory")
    parser.add_argument("--mutants", default="tests/mutants", help="Mutants directory")
    parser.add_argument("--build", default=None, help="Build directory")

    args = parser.parse_args()

    grader = AXI4MemorySVAGrader(
        tb_path=args.tb,
        sources_dir=args.sources,
        mutants_dir=args.mutants,
        build_dir=args.build
    )

    result = grader.grade()
    exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
