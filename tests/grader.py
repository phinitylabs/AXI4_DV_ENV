#!/usr/bin/env python3
"""
AXI4 Interrupt Controller TB+Assertion Generation Benchmark - Grading Engine

5-Phase Grading:
1. Compilation Check - TB compiles with Verilator
2. Negative Test - TB produces 0 errors on golden DUT
3. Coverage Analysis - Line coverage on interrupt module
4. Mutation Testing - Bug detection on interrupt mutants
5. Quality Checks - Anti-cheating and structural validation
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
    r'FAILED:',          # Test task failure
    r'\[ERROR\]',        # Alternative error format
]


@dataclass
class CoverageResult:
    """Coverage analysis results."""
    line_coverage: float = 0.0
    per_module: dict = field(default_factory=dict)


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
class QualityResult:
    """Quality and anti-cheat check results."""
    has_clock_gen: bool = False
    has_reset_seq: bool = False
    has_dut_instance: bool = False
    has_interrupt_test: bool = False
    has_assertions: bool = False
    illegal_hierarchical_refs: list = field(default_factory=list)
    structural_score: int = 0


@dataclass
class GradeResult:
    """Final grading result."""
    phase1_compiled: bool = False
    phase2_negative_passed: bool = False
    phase3_coverage: Optional[CoverageResult] = None
    phase4_mutation: Optional[MutationResult] = None
    phase5_quality: Optional[QualityResult] = None
    passed: bool = False
    error_message: str = ""
    golden_output: str = ""


class AXI4InterruptTBGrader:
    """
    Grader for AXI4 Interrupt Controller TB+Assertion benchmark.
    """
    
    COVERAGE_LINE_MIN = 0.30
    MUTATION_MIN = 3
    TIMEOUT_SECONDS = 60
    MAX_CYCLES = 100_000
    
    CORE_MODULES = ["axi4_top", "axi4_interrupt"]
    
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
        obj_dir: Optional[Path] = None,
        coverage: bool = False
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
            "--top-module", "axi4_top_tb",
            "-o", output_name,
            "-Mdir", str(obj_dir),
        ]
        
        if coverage:
            cmd.extend(["--coverage-line", "--coverage-toggle"])
        
        for src in sources:
            cmd.append(str(src))
        cmd.append(str(tb_path))
        
        sim_main = self.tb_path.parent / "sim_main.cpp"
        if sim_main.exists():
            cmd.append(str(sim_main))
        
        return cmd
    
    def phase1_compile(self) -> tuple[bool, str]:
        """Check if testbench compiles."""
        if not self.tb_path.exists():
            return False, f"Testbench file not found: {self.tb_path}"
        
        self.build_dir.mkdir(parents=True, exist_ok=True)
        obj_dir = self.build_dir / "obj_dir"
        obj_dir.mkdir(parents=True, exist_ok=True)
        
        cmd = self._get_verilator_cmd(
            self.source_files,
            self.tb_path,
            output_name="Vtb_golden",
            obj_dir=obj_dir,
            coverage=True
        )
        
        returncode, stdout, stderr = self._run_command(cmd, timeout=120)
        
        if returncode != 0:
            combined = stdout + stderr
            error_lines = [l for l in combined.split('\n') if 'Error' in l or 'error' in l]
            error_msg = '\n'.join(error_lines[:5]) if error_lines else combined[:500]
            return False, f"Compilation failed:\n{error_msg}"
        
        return True, ""
    
    def phase2_negative_test(self) -> tuple[bool, str, str]:
        """Run testbench against golden DUT."""
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
            return False, f"Errors detected on golden DUT ({n_errors} false positives)", sim_output

        return True, "", sim_output
    
    def phase3_coverage(self) -> CoverageResult:
        """Analyze line coverage."""
        result = CoverageResult()
        
        coverage_file = self.build_dir / "coverage.dat"
        if not coverage_file.exists():
            return result
        
        try:
            with open(coverage_file, 'r') as f:
                content = f.read()

            total_lines = 0
            covered_lines = 0

            # Verilator coverage.dat format: C 'path_info' <hit_count>
            for line in content.split('\n'):
                if line.startswith('C '):
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            hits = int(parts[-1])
                            total_lines += 1
                            if hits > 0:
                                covered_lines += 1
                        except (ValueError, IndexError):
                            pass

            if total_lines > 0:
                result.line_coverage = covered_lines / total_lines

        except Exception:
            pass
        
        return result
    
    def phase4_mutation(self, golden_output: str = "") -> MutationResult:
        """Run testbench against mutant designs."""
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
        """Compile and run TB against a mutant."""
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
            cwd=mutant_build,
            timeout=self.TIMEOUT_SECONDS
        )
        
        mutant_output = stdout + stderr

        if returncode == -1:  # Timeout
            return True

        return self._is_mutant_killed(golden_output, mutant_output, returncode)
    
    def phase5_quality(self) -> QualityResult:
        """Check testbench quality and anti-cheat measures."""
        result = QualityResult()
        
        if not self.tb_path.exists():
            return result
        
        with open(self.tb_path, 'r') as f:
            tb_content = f.read()
        
        # Check for clock generation
        if re.search(r'forever\s+#', tb_content) or re.search(r'clk\s*=\s*~\s*clk', tb_content):
            result.has_clock_gen = True
        
        # Check for reset sequence
        if re.search(r'resetn?\s*=\s*[01]', tb_content, re.IGNORECASE):
            result.has_reset_seq = True
        
        # Check for DUT instantiation
        if re.search(r'axi4_top\s+\w+\s*\(', tb_content):
            result.has_dut_instance = True
        
        # Check for interrupt testing
        if re.search(r'interrupt_req|interrupt_ack', tb_content):
            result.has_interrupt_test = True
        
        # Check for assertions
        if re.search(r'assert\s+property', tb_content):
            result.has_assertions = True
        
        # Check for illegal hierarchical references
        hier_patterns = [
            r'dut\.\w+\.\w+',  # dut.submodule.signal
            r'\.u_interrupt\.',
            r'\.state\b',
        ]
        
        for pattern in hier_patterns:
            matches = re.findall(pattern, tb_content)
            result.illegal_hierarchical_refs.extend(matches)
        
        # Calculate structural score
        checks = [
            result.has_clock_gen,
            result.has_reset_seq,
            result.has_dut_instance,
            result.has_interrupt_test,
            result.has_assertions,
            len(result.illegal_hierarchical_refs) == 0,
        ]
        result.structural_score = sum(checks)
        
        return result
    
    def grade(self) -> GradeResult:
        """Run complete grading pipeline."""
        result = GradeResult()
        
        print("=" * 60)
        print("AXI4 Interrupt Controller TB+Assertion Benchmark - Grading")
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

        print("\n[Phase 3] Coverage Analysis...")
        result.phase3_coverage = self.phase3_coverage()
        print(f"  Line Coverage: {result.phase3_coverage.line_coverage:.1%}")

        print("\n[Phase 4] Mutation Testing...")
        result.phase4_mutation = self.phase4_mutation(golden_output=sim_output)
        print(f"  Mutants Killed: {result.phase4_mutation.killed_mutants}/{result.phase4_mutation.total_mutants}")
        print(f"  Killed: {result.phase4_mutation.killed_list}")
        print(f"  Survived: {result.phase4_mutation.survived_list}")
        
        if result.phase4_mutation.killed_mutants < self.MUTATION_MIN:
            result.error_message = f"Phase 4: Only {result.phase4_mutation.killed_mutants} mutants killed, need {self.MUTATION_MIN}"
            print(f"  WARNING: {result.error_message}")
        
        print("\n[Phase 5] Quality Checks...")
        result.phase5_quality = self.phase5_quality()
        print(f"  Clock Generation: {result.phase5_quality.has_clock_gen}")
        print(f"  Reset Sequence: {result.phase5_quality.has_reset_seq}")
        print(f"  DUT Instance: {result.phase5_quality.has_dut_instance}")
        print(f"  Interrupt Tests: {result.phase5_quality.has_interrupt_test}")
        print(f"  Assertions: {result.phase5_quality.has_assertions}")
        print(f"  Hierarchical Refs: {result.phase5_quality.illegal_hierarchical_refs}")
        print(f"  Structural Score: {result.phase5_quality.structural_score}/6")
        
        if result.phase5_quality.illegal_hierarchical_refs:
            print(f"  WARNING: Illegal hierarchical refs: {result.phase5_quality.illegal_hierarchical_refs}")
        else:
            print("  PASSED")

        result.passed = True
        print("\n" + "=" * 60)
        print("RESULT: All phases complete (see weighted score for pass/fail)")
        print("=" * 60)
        
        return result


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AXI4 Interrupt TB Grader")
    parser.add_argument("--tb", default="verif/axi4_top_tb.sv", help="Testbench path")
    parser.add_argument("--sources", default="sources", help="Sources directory")
    parser.add_argument("--mutants", default="tests/mutants", help="Mutants directory")
    parser.add_argument("--build", default=None, help="Build directory")
    
    args = parser.parse_args()
    
    grader = AXI4InterruptTBGrader(
        tb_path=args.tb,
        sources_dir=args.sources,
        mutants_dir=args.mutants,
        build_dir=args.build
    )
    
    result = grader.grade()
    exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()

