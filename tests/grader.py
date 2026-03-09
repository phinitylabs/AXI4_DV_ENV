#!/usr/bin/env python3
"""
AXI4 Testbench Generation Benchmark - Grading Engine

5-Phase Grading:
1. Compilation Check - TB compiles with Verilator
2. Negative Test - TB produces 0 errors on golden DUT
3. Coverage Analysis - Line coverage on core modules
4. Mutation Testing - Bug detection on 10 mutants
5. Quality Checks - Anti-cheating and structural validation

Pass = All phases pass
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
    r'FAILED:\s*[1-9]',  # Test task failure (not "FAILED: 0" summary lines)
    r'\[ERROR\]',        # Alternative error format
]


@dataclass
class CoverageResult:
    """Coverage analysis results."""
    line_coverage: float = 0.0
    branch_coverage: float = 0.0
    per_module: dict = field(default_factory=dict)
    coverpoints_hit: list = field(default_factory=list)


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
    has_write_task: bool = False
    has_read_task: bool = False
    illegal_hierarchical_refs: list = field(default_factory=list)
    has_force_release: bool = False
    lazy_strategy_detected: bool = False
    structural_score: int = 0


@dataclass
class GradeResult:
    """Final grading result."""
    # Phase results
    phase1_compiled: bool = False
    phase2_negative_passed: bool = False
    phase3_coverage: Optional[CoverageResult] = None
    phase4_mutation: Optional[MutationResult] = None
    phase5_quality: Optional[QualityResult] = None
    
    # Overall
    passed: bool = False
    error_message: str = ""
    golden_output: str = ""

    # Detailed metrics for analysis
    simulation_cycles: int = 0
    simulation_time_ms: int = 0
    error_tags_found: list = field(default_factory=list)


class AXI4TBGrader:
    """
    Comprehensive testbench grader for AXI4 slave design.
    """
    
    # Thresholds
    COVERAGE_LINE_MIN = 0.60        # 60% line coverage
    COVERAGE_FUNCTIONAL_MIN = 10    # 10 out of 12 coverpoints
    MUTATION_MIN = 5                # 5 out of 10 mutants killed
    TIMEOUT_SECONDS = 60
    MAX_CYCLES = 100_000
    
    # Core modules to measure coverage on
    CORE_MODULES = [
        "axi4_slave_top",
        "axi4_write_channel",
        "axi4_read_channel", 
        "axi4_memory",
        "axi4_decoder"
    ]
    
    # Functional coverpoints (embedded in simulation)
    COVERPOINTS = [
        "cp_burst_single",
        "cp_burst_incr",
        "cp_burst_wrap",
        "cp_burst_fixed",
        "cp_burst_max",
        "cp_strobe_full",
        "cp_strobe_partial",
        "cp_addr_zero",
        "cp_addr_boundary",
        "cp_decode_error",
        "cp_write_response",
        "cp_read_response"
    ]
    
    # Allowed DUT port signals (not internal hierarchy)
    ALLOWED_DUT_SIGNALS = {
        "aclk", "aresetn",
        "awid", "awaddr", "awlen", "awsize", "awburst", "awvalid", "awready",
        "wdata", "wstrb", "wlast", "wvalid", "wready",
        "bid", "bresp", "bvalid", "bready",
        "arid", "araddr", "arlen", "arsize", "arburst", "arvalid", "arready",
        "rid", "rdata", "rresp", "rlast", "rvalid", "rready"
    }
    
    def __init__(
        self,
        tb_path: str,
        sources_dir: str,
        mutants_dir: str,
        build_dir: Optional[str] = None
    ):
        # Convert all paths to absolute paths
        self.tb_path = Path(tb_path).resolve()
        self.sources_dir = Path(sources_dir).resolve()
        self.mutants_dir = Path(mutants_dir).resolve()
        self.build_dir = Path(build_dir).resolve() if build_dir else Path(tempfile.mkdtemp())
        
        # Get list of source files (absolute paths)
        # Package must come first for proper compilation order
        self.source_files = self._get_ordered_sources()
    
    def _get_ordered_sources(self) -> list[Path]:
        """
        Get source files in correct compilation order.
        Package files must come first, then other modules.
        """
        all_files = list(self.sources_dir.glob("*.sv"))
        
        # Separate package files and regular files
        pkg_files = [f for f in all_files if 'pkg' in f.name.lower()]
        other_files = [f for f in all_files if 'pkg' not in f.name.lower()]
        
        # Sort each group
        pkg_files.sort()
        other_files.sort()
        
        # Package files first
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
                cwd=cwd,  # Run from current directory, use absolute paths
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
        coverage: bool = True,
        output_name: str = "Vtb",
        obj_dir: Optional[Path] = None
    ) -> list[str]:
        """Build Verilator compilation command."""
        if obj_dir is None:
            obj_dir = self.build_dir / "obj_dir"
        
        # Ensure obj_dir exists
        obj_dir.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            "verilator",
            "--cc",
            "--exe",
            "--build",
            "-j", "0",
            "--timing",
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
        
        if coverage:
            cmd.extend(["--coverage-line", "--coverage-toggle"])
        
        # Add source files (package first)
        for src in sources:
            cmd.append(str(src))
        
        # Add testbench
        cmd.append(str(tb_path))
        
        # Add C++ main wrapper
        sim_main = self.tb_path.parent / "sim_main.cpp"
        if sim_main.exists():
            cmd.append(str(sim_main))
        
        return cmd
    
    # =========================================================================
    # Phase 1: Compilation Check
    # =========================================================================
    def phase1_compile(self) -> tuple[bool, str]:
        """
        Check if testbench compiles with Verilator.
        Returns (success, error_message).
        """
        if not self.tb_path.exists():
            return False, f"Testbench file not found: {self.tb_path}"
        
        # Ensure build directory exists
        self.build_dir.mkdir(parents=True, exist_ok=True)
        obj_dir = self.build_dir / "obj_dir"
        obj_dir.mkdir(parents=True, exist_ok=True)
        
        # Debug: print source files
        print(f"  Source files ({len(self.source_files)}):")
        for f in self.source_files:
            print(f"    - {f}")
        print(f"  Testbench: {self.tb_path}")
        
        cmd = self._get_verilator_cmd(
            self.source_files,
            self.tb_path,
            coverage=True,
            output_name="Vtb_golden",
            obj_dir=obj_dir
        )
        
        # Debug: print command
        print(f"  Command: {' '.join(cmd)}")
        
        returncode, stdout, stderr = self._run_command(cmd, timeout=120)
        
        if returncode != 0:
            # Extract meaningful error
            combined = stdout + stderr
            error_lines = [l for l in combined.split('\n') if 'Error' in l or 'error' in l]
            error_msg = '\n'.join(error_lines[:5]) if error_lines else combined[:500]
            return False, f"Compilation failed:\n{error_msg}"
        
        return True, ""
    
    # =========================================================================
    # Phase 2: Negative Test (Run on Golden DUT)
    # =========================================================================
    def phase2_negative_test(self) -> tuple[bool, str, int, str]:
        """
        Run testbench against golden (bug-free) DUT.
        Must produce 0 errors.
        Returns (success, error_message, error_count, sim_output).
        """
        # Run simulation
        obj_dir = self.build_dir / "obj_dir"
        exe_path = obj_dir / "Vtb_golden"
        if not exe_path.exists():
            # Check alternative paths
            alt_paths = [
                self.build_dir / "Vtb_golden",
                obj_dir / "Vaxi4_slave_tb",
            ]
            for alt in alt_paths:
                if alt.exists():
                    exe_path = alt
                    break
            else:
                return False, f"Executable not found at {exe_path} - compile first", -1, ""
        
        returncode, stdout, stderr = self._run_command(
            [str(exe_path)],
            cwd=self.build_dir,  # Run from build_dir so coverage.dat is written there
            timeout=self.TIMEOUT_SECONDS
        )
        
        # Store simulation output for functional coverage parsing
        sim_output = stdout + stderr
        
        # Check for timeout
        if returncode == -1:
            return False, "Simulation timeout (possible infinite loop)", -1, sim_output
        
        n_errors = self._count_errors(sim_output)
        if n_errors > 0:
            return False, f"Testbench reported {n_errors} errors on golden DUT (false positives)", n_errors, sim_output

        return True, "", 0, sim_output
    
    # =========================================================================
    # Phase 3: Coverage Analysis
    # =========================================================================
    def phase3_coverage(self, sim_output: str = "") -> CoverageResult:
        """
        Parse Verilator coverage data and calculate metrics.
        """
        result = CoverageResult()
        
        coverage_file = self.build_dir / "coverage.dat"
        if not coverage_file.exists():
            # Try to find it
            for f in self.build_dir.rglob("coverage.dat"):
                coverage_file = f
                break
        
        if not coverage_file.exists():
            return result
        
        # Parse coverage.dat (Verilator format)
        try:
            total_lines = 0
            covered_lines = 0
            module_stats = {}
            
            with open(coverage_file, 'r') as f:
                content = f.read()
            
            # Simple parsing - count coverage points
            # Verilator coverage.dat format: C 'path_info' <hit_count>
            # The hit count is the last element after splitting
            for line in content.split('\n'):
                if line.startswith('C'):
                    parts = line.split()
                    if len(parts) >= 2:
                        # Extract hit count (last element)
                        try:
                            hits = int(parts[-1])
                            total_lines += 1
                            if hits > 0:
                                covered_lines += 1
                        except (ValueError, IndexError):
                            pass
            
            if total_lines > 0:
                result.line_coverage = covered_lines / total_lines
            
        except Exception as e:
            print(f"Coverage parsing error: {e}")
        
        # Parse functional coverage from simulation output
        if sim_output:
            result.coverpoints_hit = self._parse_functional_coverage(sim_output)
        
        return result
    
    def _parse_functional_coverage(self, sim_output: str) -> list[str]:
        """Extract which coverpoints were hit from simulation output."""
        hit_coverpoints = []
        
        for cp in self.COVERPOINTS:
            # Look for coverage markers in output
            if f"COVERPOINT_HIT:{cp}" in sim_output or f"[{cp}]" in sim_output:
                hit_coverpoints.append(cp)
        
        return hit_coverpoints
    
    # =========================================================================
    # Phase 4: Mutation Testing
    # =========================================================================
    def phase4_mutation(self, golden_output: str = "") -> MutationResult:
        """
        Run testbench against each mutant and check if bugs are detected.
        """
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
        """
        Compile and run TB against a mutant.
        Returns True if TB detects the bug (kills the mutant).
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
            coverage=False,
            output_name=f"Vtb_{mutant_name}",
            obj_dir=mutant_build
        )
        
        returncode, stdout, stderr = self._run_command(cmd, timeout=60)
        
        if returncode != 0:
            # Compilation failed - mutant might have syntax error
            # Consider this as "killed" since it's detectable
            return True
        
        # Run simulation
        exe_path = mutant_build / f"Vtb_{mutant_name}"
        returncode, stdout, stderr = self._run_command(
            [str(exe_path)],
            timeout=self.TIMEOUT_SECONDS
        )
        
        mutant_output = stdout + stderr

        if returncode == -1:  # Timeout - possible hang due to bug
            return True

        return self._is_mutant_killed(golden_output, mutant_output, returncode)
    
    # =========================================================================
    # Phase 5: Quality Checks
    # =========================================================================
    def phase5_quality(self) -> QualityResult:
        """
        Check testbench quality and anti-cheating measures.
        """
        result = QualityResult()
        
        if not self.tb_path.exists():
            return result
        
        with open(self.tb_path, 'r') as f:
            tb_content = f.read()
        
        # Structural checks
        result.has_clock_gen = bool(re.search(
            r'forever\s+#\s*\d+\s+\w+\s*=\s*~?\s*\w+|always\s+#\s*\d+\s+\w+\s*=\s*~?\s*\w+',
            tb_content
        ))
        
        result.has_reset_seq = bool(re.search(
            r'aresetn\s*<=?\s*[01\'bh]|aresetn\s*=\s*[01\'bh]',
            tb_content
        ))
        
        result.has_dut_instance = bool(re.search(
            r'axi4_slave_top\s+\w+\s*\(',
            tb_content
        ))
        
        result.has_write_task = bool(re.search(
            r'task\s+(automatic\s+)?(\w*write\w*|axi_write|wr_txn)',
            tb_content, re.IGNORECASE
        ))
        
        result.has_read_task = bool(re.search(
            r'task\s+(automatic\s+)?(\w*read\w*|axi_read|rd_txn)',
            tb_content, re.IGNORECASE
        ))
        
        # Anti-cheat: Check for illegal hierarchical references
        # Pattern: dut.u_something.signal or dut.internal_signal
        hier_refs = re.findall(r'dut\.(\w+)(?:\.(\w+))?', tb_content)
        for ref in hier_refs:
            top_signal = ref[0]
            sub_signal = ref[1] if len(ref) > 1 and ref[1] else None
            
            if sub_signal:  # Hierarchical reference like dut.u_write.state
                result.illegal_hierarchical_refs.append(f"dut.{top_signal}.{sub_signal}")
            elif top_signal not in self.ALLOWED_DUT_SIGNALS:
                # Direct reference to non-port signal
                if not top_signal.startswith('u_'):  # Skip submodule names in instantiation
                    result.illegal_hierarchical_refs.append(f"dut.{top_signal}")
        
        # Check for force/release
        result.has_force_release = bool(re.search(
            r'\b(force|release)\s+',
            tb_content
        ))
        
        # Lazy strategy detection: $error before any stimulus
        # This is a simplified check
        first_error_pos = tb_content.find('$error')
        first_write_pos = tb_content.find('awvalid')
        if first_error_pos != -1 and first_write_pos != -1:
            if first_error_pos < first_write_pos:
                result.lazy_strategy_detected = True
        
        # Calculate structural score
        checks = [
            result.has_clock_gen,
            result.has_reset_seq,
            result.has_dut_instance,
            result.has_write_task,
            result.has_read_task,
            len(result.illegal_hierarchical_refs) == 0,
            not result.has_force_release,
            not result.lazy_strategy_detected
        ]
        result.structural_score = sum(checks)
        
        return result
    
    # =========================================================================
    # Main Grading Pipeline
    # =========================================================================
    def grade(self) -> GradeResult:
        """
        Run complete grading pipeline.
        Returns GradeResult with pass/fail and detailed metrics.
        """
        result = GradeResult()
        
        print("=" * 60)
        print("AXI4 Testbench Generation Benchmark - Grading")
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
        result.phase2_negative_passed, error_msg, error_count, sim_output = self.phase2_negative_test()
        if not result.phase2_negative_passed:
            result.error_message = f"Phase 2 FAILED: {error_msg}"
            print(f"  FAILED: {error_msg}")
            return result
        result.golden_output = sim_output
        print("  PASSED (0 errors on golden DUT)")

        # Phase 3: Coverage
        print("\n[Phase 3] Coverage Analysis...")
        result.phase3_coverage = self.phase3_coverage(sim_output)
        print(f"  Line Coverage: {result.phase3_coverage.line_coverage:.1%}")
        func_cov_hit = len(result.phase3_coverage.coverpoints_hit)
        func_cov_total = len(self.COVERPOINTS)
        print(f"  Functional Coverage: {func_cov_hit}/{func_cov_total} coverpoints")

        # Phase 4: Mutation Testing
        print("\n[Phase 4] Mutation Testing...")
        result.phase4_mutation = self.phase4_mutation(golden_output=sim_output)
        print(f"  Mutants Killed: {result.phase4_mutation.killed_mutants}/{result.phase4_mutation.total_mutants}")
        print(f"  Killed: {result.phase4_mutation.killed_list}")
        print(f"  Survived: {result.phase4_mutation.survived_list}")
        
        # Phase 5: Quality Checks
        print("\n[Phase 5] Quality Checks...")
        result.phase5_quality = self.phase5_quality()
        print(f"  Structural Score: {result.phase5_quality.structural_score}/8")
        print(f"  Clock Gen: {result.phase5_quality.has_clock_gen}")
        print(f"  Reset Seq: {result.phase5_quality.has_reset_seq}")
        print(f"  DUT Instance: {result.phase5_quality.has_dut_instance}")
        print(f"  Write Task: {result.phase5_quality.has_write_task}")
        print(f"  Read Task: {result.phase5_quality.has_read_task}")
        
        if result.phase5_quality.illegal_hierarchical_refs:
            print(f"  WARNING: Illegal hierarchical refs: {result.phase5_quality.illegal_hierarchical_refs}")
        elif result.phase5_quality.has_force_release:
            print("  WARNING: force/release detected")
        else:
            print("  PASSED")

        result.passed = True
        print("\n" + "=" * 60)
        print("RESULT: All phases complete (see weighted score for pass/fail)")
        print("=" * 60)
        
        return result


def main():
    """CLI entry point for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AXI4 TB Grader")
    parser.add_argument("--tb", default="verif/axi4_slave_tb.sv", help="Testbench path")
    parser.add_argument("--sources", default="sources", help="Sources directory")
    parser.add_argument("--mutants", default="tests/mutants", help="Mutants directory")
    parser.add_argument("--build", default=None, help="Build directory")
    args = parser.parse_args()
    
    grader = AXI4TBGrader(
        tb_path=args.tb,
        sources_dir=args.sources,
        mutants_dir=args.mutants,
        build_dir=args.build
    )
    
    result = grader.grade()
    
    # Exit with appropriate code
    exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()

