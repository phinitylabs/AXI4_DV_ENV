#!/usr/bin/env python3
"""
AXI4 Decoder Testbench Generation Benchmark - Grading Engine (HARD MODE)

This grader verifies that the agent-written testbench:
1. Compiles successfully with Verilator
2. Passes on the golden (bug-free) DUT
3. Detects bugs in mutant designs (mutation testing)
4. Achieves sufficient line coverage
5. Has proper structural quality (covers all scenarios)

Focus: Address decoder verification - valid range, invalid range, boundaries
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
# Verilator prefixes $error() output with "%Error" in stderr.
# $fatal() causes these same markers plus a nonzero exit.
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
class CoverageResult:
    """Coverage analysis results."""
    line_coverage: float = 0.0
    toggle_coverage: float = 0.0
    passed: bool = False


@dataclass
class StructuralResult:
    """Structural quality check results."""
    has_valid_test: bool = False
    has_invalid_test: bool = False
    has_boundary_low_test: bool = False
    has_boundary_high_test: bool = False
    has_deassert_test: bool = False
    test_count: int = 0
    uses_error: bool = False
    structural_score: int = 0


@dataclass
class GradeResult:
    """Final grading result."""
    phase1_compiled: bool = False
    phase2_negative_passed: bool = False
    phase3_mutation: Optional[MutationResult] = None
    phase4_coverage: Optional[CoverageResult] = None
    phase5_structural: Optional[StructuralResult] = None
    golden_output: str = ""   # Stored from Phase 2 for differential comparison
    passed: bool = False
    error_message: str = ""


class AXI4DecoderTBGrader:
    """
    Grader for AXI4 Decoder testbench generation benchmark.
    """

    # Thresholds (HARD MODE)
    MUTATION_MIN = 3  # Must kill 3 out of 4 mutants
    MIN_TESTS = 4  # Minimum test count
    MIN_LINE_COVERAGE = 0.80  # 80% line coverage required
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

    def _compile(self, extra_sources: list[Path] = None, coverage: bool = False) -> tuple[bool, str]:
        """Compile testbench with Verilator."""
        sources = extra_sources if extra_sources else self.source_files
        source_args = [str(f) for f in sources]
        
        cmd = [
            "verilator", "--binary", "-j", "0",
            "--timing", "--assert",
            "-Wno-fatal", "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC",
            "-o", "sim"
        ]
        
        if coverage:
            cmd.extend(["--coverage", "--coverage-line"])
        
        cmd.extend(source_args)
        cmd.append(str(self.tb_path))

        code, stdout, stderr = self._run_command(cmd, timeout=self.TIMEOUT_SECONDS)
        
        if code != 0:
            return False, f"Compilation failed:\n{stderr}"
        return True, ""

    def _run_simulation(self, coverage: bool = False) -> tuple[bool, str, str]:
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

    def _parse_coverage_dat(self, cov_file: Path) -> float:
        """Parse Verilator coverage.dat. Returns line coverage fraction."""
        if not cov_file.exists():
            return 0.0
        info_file = cov_file.parent / "coverage.info"
        ret = subprocess.run(
            ["verilator_coverage", "--write-info", str(info_file), str(cov_file)],
            capture_output=True, text=True,
        )
        if ret.returncode == 0 and info_file.exists():
            total, hit = 0, 0
            for line in info_file.read_text().splitlines():
                if line.startswith("DA:"):
                    parts = line[3:].split(",")
                    if len(parts) >= 2:
                        total += 1
                        try:
                            if int(parts[1]) > 0:
                                hit += 1
                        except ValueError:
                            pass
            return hit / total if total > 0 else 0.0
        # Fallback: direct C-line parsing
        total, hit = 0, 0
        for line in cov_file.read_text().splitlines():
            if line.startswith("C "):
                total += 1
                try:
                    if int(line.strip().split()[-1]) > 0:
                        hit += 1
                except (ValueError, IndexError):
                    pass
        return hit / total if total > 0 else 0.0

    def _parse_functional_coverage(self, stdout: str) -> float:
        """Parse COVERAGE_BINS_HIT=N from axi4_coverage.sv stdout."""
        m = re.search(r"COVERAGE_BINS_HIT=(\d+)", stdout)
        if not m:
            return 0.0
        bins_hit = int(m.group(1))
        total_m = re.search(r"COVERAGE_BINS_TOTAL=(\d+)", stdout)
        total = int(total_m.group(1)) if total_m else 24
        return min(bins_hit / total, 1.0)

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
            print(f"  FAILED: {n_errors} false positive(s) on golden DUT")
            return False

        # Also collect functional coverage from this run
        func_cov = self._parse_functional_coverage(stdout)
        if func_cov > 0:
            print(f"  Functional Coverage: {func_cov*100:.1f}%")

        print("  PASSED (no false positives)")
        result.phase2_negative_passed = True
        return True

    def _phase3_mutation_testing(self, result: GradeResult) -> bool:
        """Phase 3: Differential mutation testing. Each .sv replaces axi4_decoder.sv."""
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
                # Copy all sources except the original decoder
                mutant_sources = []
                for src in self.source_files:
                    if 'decoder' not in src.name.lower():
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

    def _phase4_coverage(self, result: GradeResult) -> bool:
        """Phase 4: Check code coverage."""
        print("\n[Phase 4] Coverage Analysis...")
        
        coverage_result = CoverageResult()
        
        # Recompile with coverage
        cov_build = Path(tempfile.mkdtemp())
        
        try:
            source_args = [str(f) for f in self.source_files]
            cmd = [
                "verilator", "--binary", "-j", "0",
                "--timing", "--assert", "--coverage-line",
                "-Wno-fatal", "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC",
                "-Mdir", str(cov_build),
                "-o", "sim"
            ] + source_args + [str(self.tb_path)]

            code, _, stderr = self._run_command(cmd, cwd=cov_build, timeout=60)

            if code != 0:
                print("  SKIPPED: Could not compile with coverage")
                coverage_result.passed = True
                result.phase4_coverage = coverage_result
                return True

            sim_path = cov_build / "sim"
            self._run_command([str(sim_path)], cwd=cov_build, timeout=60)
            
            # Parse coverage results using proper verilator_coverage parsing
            cov_file = cov_build / "coverage.dat"
            coverage_result.line_coverage = self._parse_coverage_dat(cov_file)
            
            coverage_result.passed = coverage_result.line_coverage >= self.MIN_LINE_COVERAGE
            
            print(f"  Line Coverage: {coverage_result.line_coverage * 100:.1f}%")
            print(f"  Required: {self.MIN_LINE_COVERAGE * 100:.1f}%")
            
        finally:
            shutil.rmtree(cov_build, ignore_errors=True)
        
        result.phase4_coverage = coverage_result
        
        # Coverage is required for testbench generation
        if not coverage_result.passed and coverage_result.line_coverage > 0:
            result.error_message = (
                f"Phase 4 FAILED: Line coverage {coverage_result.line_coverage*100:.1f}% "
                f"below minimum {self.MIN_LINE_COVERAGE*100:.1f}%"
            )
            return False
        
        return True

    def _phase5_structural_quality(self, result: GradeResult) -> bool:
        """Phase 5: Check testbench structure and quality."""
        print("\n[Phase 5] Structural Quality Check...")
        
        struct_result = StructuralResult()
        
        try:
            tb_content = self.tb_path.read_text()
        except Exception as e:
            result.error_message = f"Phase 5 FAILED: Cannot read testbench: {e}"
            return False
        
        # Check for specific test patterns
        # Valid address test (0x0000-0xFFFF range)
        struct_result.has_valid_test = bool(re.search(
            r'(addr\s*[=<]\s*.*0x[0-9a-fA-F]{1,4}[^0-9a-fA-F].*valid\s*[=<]\s*1|'
            r'valid\s*[=<]\s*1.*addr\s*[=<]\s*.*0x[0-9a-fA-F]{1,4}[^0-9a-fA-F])',
            tb_content, re.IGNORECASE | re.DOTALL
        ))
        
        # Invalid address test (above 0xFFFF)
        struct_result.has_invalid_test = bool(re.search(
            r'(0x[1-9a-fA-F][0-9a-fA-F]{4,}|0x0001_?0000)',
            tb_content, re.IGNORECASE
        ))
        
        # Boundary tests
        struct_result.has_boundary_low_test = bool(re.search(
            r'(0x0+[^1-9a-fA-F]|BASE_ADDR\s*\+?\s*0)',
            tb_content, re.IGNORECASE
        ))
        
        struct_result.has_boundary_high_test = bool(re.search(
            r'(0x[fF]{4}|ADDR_RANGE)',
            tb_content, re.IGNORECASE
        ))
        
        struct_result.has_deassert_test = bool(re.search(
            r'valid\s*[=<]+\s*0',
            tb_content
        ))
        
        # Check for $error usage
        struct_result.uses_error = bool(re.search(
            r'\$error\s*\(',
            tb_content
        ))
        
        # Count test tasks
        test_tasks = re.findall(r'task\s+(?:automatic\s+)?test_\w+', tb_content)
        struct_result.test_count = len(test_tasks)
        
        # Calculate score
        struct_result.structural_score = sum([
            struct_result.has_valid_test,
            struct_result.has_invalid_test,
            struct_result.has_boundary_low_test,
            struct_result.has_boundary_high_test,
            struct_result.has_deassert_test,
            struct_result.uses_error,
            struct_result.test_count >= 3,
            struct_result.test_count >= 5,
        ])
        
        result.phase5_structural = struct_result
        
        print(f"  Valid addr test: {struct_result.has_valid_test}")
        print(f"  Invalid addr test: {struct_result.has_invalid_test}")
        print(f"  Boundary low test: {struct_result.has_boundary_low_test}")
        print(f"  Boundary high test: {struct_result.has_boundary_high_test}")
        print(f"  Deassert test: {struct_result.has_deassert_test}")
        print(f"  Uses $error: {struct_result.uses_error}")
        print(f"  Test count: {struct_result.test_count}")
        print(f"  Structural score: {struct_result.structural_score}/8")
        
        if struct_result.test_count < self.MIN_TESTS:
            result.error_message = (
                f"Phase 5 FAILED: Only {struct_result.test_count} tests, "
                f"need at least {self.MIN_TESTS}"
            )
            return False
        
        if not struct_result.uses_error:
            result.error_message = "Phase 5 FAILED: Tests must use $error() to report failures"
            return False
        
        return True

    def grade(self) -> GradeResult:
        """Run all grading phases."""
        result = GradeResult()
        
        print("=" * 60)
        print("AXI4 Decoder Testbench Benchmark - Grading (HARD MODE)")
        print("=" * 60)
        print(f"Requirements:")
        print(f"  - Kill {self.MUTATION_MIN}/4 mutants")
        print(f"  - At least {self.MIN_TESTS} test tasks")
        print(f"  - Must use $error() for failures")
        print("=" * 60)
        
        # Phase 1: Compilation
        if not self._phase1_compile(result):
            return result
        
        # Phase 2: Negative test
        if not self._phase2_negative_test(result):
            return result
        
        # Phase 3: Mutation testing
        if not self._phase3_mutation_testing(result):
            return result
        
        # Phase 4: Coverage (informational)
        self._phase4_coverage(result)
        
        # Phase 5: Structural quality
        if not self._phase5_structural_quality(result):
            return result
        
        result.passed = True
        return result


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Grade AXI4 decoder testbench")
    parser.add_argument("--tb", default="verif/axi4_decoder_tb.sv", help="Testbench path")
    parser.add_argument("--sources", default="sources", help="Sources directory")
    parser.add_argument("--mutants", default="tests/mutants", help="Mutants directory")
    parser.add_argument("--build", default=None, help="Build directory")

    args = parser.parse_args()

    grader = AXI4DecoderTBGrader(
        tb_path=args.tb,
        sources_dir=args.sources,
        mutants_dir=args.mutants,
        build_dir=args.build
    )

    result = grader.grade()
    exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
