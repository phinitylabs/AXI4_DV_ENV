#!/usr/bin/env python3
"""
AXI4 Read Channel Complete Verification Benchmark - Grading Engine

This grader verifies that the agent-written testbench AND assertions:
1. Compile successfully with Verilator
2. Pass (no errors) on the golden (bug-free) DUT
3. Detect bugs in mutant designs (mutation testing)
4. Have proper structural quality (TB coverage + assertion patterns)

Focus: Combined testbench and assertion verification for read channel
"""

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


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
    # Assertion quality
    has_assert_property: bool = False
    has_property_blocks: bool = False
    assertion_count: int = 0
    has_rlast_check: bool = False
    has_handshake_check: bool = False
    # Testbench quality
    has_test_tasks: bool = False
    has_read_stimulus: bool = False
    has_burst_test: bool = False
    test_count: int = 0
    structural_score: int = 0


@dataclass
class GradeResult:
    """Final grading result."""
    phase1_compiled: bool = False
    phase2_negative_passed: bool = False
    phase3_mutation: Optional[MutationResult] = None
    phase4_structural: Optional[StructuralResult] = None
    passed: bool = False
    error_message: str = ""


class AXI4ReadChannelGrader:
    """
    Grader for AXI4 Read Channel complete verification benchmark.
    """

    # Thresholds
    MUTATION_MIN = 2  # Minimum mutants that must be killed
    MIN_ASSERTIONS = 2  # Minimum assertion count
    MIN_TESTS = 2  # Minimum test count
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
            "-o", "sim",
        ] + source_args + [str(self.tb_path)]

        code, stdout, stderr = self._run_command(cmd, timeout=self.TIMEOUT_SECONDS)
        
        if code != 0:
            return False, f"Compilation failed:\n{stderr}"
        return True, ""

    def _run_simulation(self) -> tuple[bool, str, str]:
        """Run compiled simulation."""
        sim_path = self.build_dir / "sim"
        if not sim_path.exists():
            return False, "", "Simulation binary not found"
        
        code, stdout, stderr = self._run_command(
            [str(sim_path)],
            timeout=self.TIMEOUT_SECONDS
        )
        
        return code == 0, stdout, stderr

    def _check_for_errors(self, output: str) -> list[str]:
        """Check simulation output for error messages."""
        errors = []
        error_patterns = [
            r'\[ERROR\]',
            r'FAIL:',
            r'\$error',
            r'Assertion failed',
            r'ASSERTION FAILED',
            r'TESTBENCH FAILED'
        ]
        for pattern in error_patterns:
            matches = re.findall(pattern, output, re.IGNORECASE)
            errors.extend(matches)
        return errors

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
        """Phase 2: Run on golden DUT, should pass."""
        print("\n[Phase 2] Negative Test (Golden DUT)...")
        
        success, stdout, stderr = self._run_simulation()
        output = stdout + stderr
        errors = self._check_for_errors(output)
        
        if errors:
            result.error_message = f"Phase 2 FAILED: Errors on golden DUT: {errors[:3]}"
            print(f"  FAILED: Found errors on golden DUT")
            return False
        
        print("  PASSED (no false positives)")
        result.phase2_negative_passed = True
        return True

    def _phase3_mutation_testing(self, result: GradeResult) -> bool:
        """Phase 3: Run on mutant DUTs, should detect bugs."""
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
                # Copy all sources except the original read channel
                mutant_sources = []
                for src in self.source_files:
                    if 'read_channel' not in src.name.lower():
                        mutant_sources.append(src)
                mutant_sources.append(mutant_file)
                
                # Compile with mutant
                source_args = [str(f) for f in mutant_sources]
                cmd = [
                    "verilator", "--binary", "-j", "0",
                    "--timing", "--assert",
                    "-Wno-fatal", "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC",
                    "-o", "sim",
                ] + source_args + [str(self.tb_path)]
                
                code, _, stderr = self._run_command(cmd, cwd=mutant_build, timeout=30)
                
                if code != 0:
                    # Compilation failed - skip this mutant (don't count as killed)
                    print(f"    {mutant_name}: Compilation failed, skipping")
                    mutation_result.total_mutants -= 1
                    continue
                
                # Run simulation
                sim_path = mutant_build / "obj_dir" / "sim"
                code, stdout, stderr = self._run_command(
                    [str(sim_path)],
                    cwd=mutant_build,
                    timeout=30
                )
                
                output = stdout + stderr
                errors = self._check_for_errors(output)
                
                # Count as killed if simulation detected errors OR exited non-zero
                if errors or code != 0:
                    mutation_result.killed_mutants += 1
                    mutation_result.killed_list.append(mutant_name)
                    print(f"    {mutant_name}: KILLED (errors: {errors[:2] if errors else ['exit=' + str(code)]})")
                else:
                    mutation_result.survived_list.append(mutant_name)
                    print(f"    {mutant_name}: SURVIVED")
                    
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
        """Phase 4: Check both TB and assertion quality."""
        print("\n[Phase 4] Structural Quality Check...")
        
        struct_result = StructuralResult()
        
        try:
            tb_content = self.tb_path.read_text()
        except Exception as e:
            result.error_message = f"Phase 4 FAILED: Cannot read testbench: {e}"
            return False
        
        # Check assertion patterns
        struct_result.has_assert_property = bool(re.search(
            r'assert\s+property', tb_content, re.IGNORECASE
        ))
        
        struct_result.has_property_blocks = bool(re.search(
            r'property\s+\w+', tb_content
        ))
        
        # Count assertions
        assertions = re.findall(r'assert\s+property\s*\([^)]+\)', tb_content)
        struct_result.assertion_count = len(assertions)
        
        # Check for specific assertion types
        struct_result.has_rlast_check = bool(re.search(
            r'rlast|last.*beat|final.*beat', tb_content, re.IGNORECASE
        ))
        
        struct_result.has_handshake_check = bool(re.search(
            r'rvalid.*rready|handshake|valid.*ready', tb_content, re.IGNORECASE
        ))
        
        # Check testbench patterns
        test_tasks = re.findall(r'task\s+(?:automatic\s+)?test_\w+', tb_content)
        struct_result.test_count = len(test_tasks)
        struct_result.has_test_tasks = struct_result.test_count > 0
        
        struct_result.has_read_stimulus = bool(re.search(
            r'arvalid\s*=|araddr\s*=', tb_content
        ))
        
        struct_result.has_burst_test = bool(re.search(
            r'arlen\s*=\s*[1-9]|burst|BURST_INCR', tb_content
        ))
        
        # Calculate score (10 points total)
        struct_result.structural_score = sum([
            struct_result.has_assert_property,
            struct_result.has_property_blocks,
            struct_result.assertion_count >= 2,
            struct_result.has_rlast_check,
            struct_result.has_handshake_check,
            struct_result.has_test_tasks,
            struct_result.has_read_stimulus,
            struct_result.has_burst_test,
            struct_result.test_count >= 2,
            struct_result.assertion_count >= 3,
        ])
        
        result.phase4_structural = struct_result
        
        print(f"  Assertions: {struct_result.assertion_count}")
        print(f"  Tests: {struct_result.test_count}")
        print(f"  Has RLAST check: {struct_result.has_rlast_check}")
        print(f"  Has handshake check: {struct_result.has_handshake_check}")
        print(f"  Has burst test: {struct_result.has_burst_test}")
        print(f"  Structural score: {struct_result.structural_score}/10")
        
        # Check minimums
        if struct_result.assertion_count < self.MIN_ASSERTIONS:
            result.error_message = (
                f"Phase 4 FAILED: Only {struct_result.assertion_count} assertions, "
                f"need at least {self.MIN_ASSERTIONS}"
            )
            return False
        
        if struct_result.test_count < self.MIN_TESTS:
            result.error_message = (
                f"Phase 4 FAILED: Only {struct_result.test_count} tests, "
                f"need at least {self.MIN_TESTS}"
            )
            return False
        
        return True

    def grade(self) -> GradeResult:
        """Run all grading phases."""
        result = GradeResult()
        
        print("=" * 60)
        print("AXI4 Read Channel Complete Verification - Grading")
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
    
    parser = argparse.ArgumentParser(description="Grade AXI4 read channel TB+SVA")
    parser.add_argument("--tb", default="verif/axi4_read_channel_tb.sv", help="Testbench path")
    parser.add_argument("--sources", default="sources", help="Sources directory")
    parser.add_argument("--mutants", default="tests/mutants", help="Mutants directory")
    parser.add_argument("--build", default=None, help="Build directory")

    args = parser.parse_args()

    grader = AXI4ReadChannelGrader(
        tb_path=args.tb,
        sources_dir=args.sources,
        mutants_dir=args.mutants,
        build_dir=args.build
    )

    result = grader.grade()
    exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()

