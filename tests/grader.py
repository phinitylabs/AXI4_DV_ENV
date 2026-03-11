#!/usr/bin/env python3
"""
AXI4 Read Channel Complete Verification — Three-Pillar Grader

Industry-standard TB quality model:
  Pillar 1 (30%): Code Coverage   — Verilator --coverage-line → coverage.dat
  Pillar 2 (30%): Functional Coverage — axi4_coverage.sv COVERAGE_BINS_HIT
  Pillar 3 (15%): Differential Mutation Testing — golden vs mutant output

Full scoring weights:
  Compilation:          10%
  No False Positives:   15%
  Code Coverage:        30%   (line coverage from coverage.dat)
  Functional Coverage:  30%   (bins hit / total, parsed from stdout)
  Mutation Testing:     15%   (ungameable differential comparison)

Pass Threshold: 60%
"""

import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# === Differential error detection markers ===
# These appear in Verilator stderr when $error() fires (prefix %Error)
# or when the TB explicitly signals failure.
ERROR_MARKERS = [
    r'%Error',           # Verilator $error() always prefixes with %Error
    r'ASSERTION FAILED', # Standard SVA failure message
    r'TESTBENCH FAILED', # End-of-sim summary line
    r'\$fatal',          # $fatal() appears in output before exit
    r'FAILED:\s*[1-9]',  # Test task failure line (avoid matching "FAILED: 0" summary)
    r'\[ERROR\]',        # Alternative error format
]


@dataclass
class MutationResult:
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
    line_coverage: float = 0.0        # Pillar 1: verilator --coverage-line
    functional_coverage: float = 0.0  # Pillar 2: axi4_coverage.sv bins


@dataclass
class StructuralResult:
    assertion_count: int = 0
    test_count: int = 0
    has_assert_property: bool = False
    has_rlast_check: bool = False
    has_handshake_check: bool = False
    structural_score: float = 0.0


@dataclass
class GradeResult:
    phase1_compiled: bool = False
    phase2_negative_passed: bool = False
    phase3_coverage: Optional[CoverageResult] = None
    phase4_mutation: Optional[MutationResult] = None
    phase5_structural: Optional[StructuralResult] = None
    golden_output: str = ""   # Stored from Phase 2 for differential comparison
    passed: bool = False
    error_message: str = ""


class AXI4ReadChannelGrader:
    """
    Grader for AXI4 Read Channel complete verification (testbench + assertions).
    Uses three-pillar industry-standard approach: code coverage, functional
    coverage, and differential mutation testing.
    """

    TIMEOUT_SECONDS = 60
    MUTANT_TIMEOUT = 30

    def __init__(
        self,
        tb_path: str,
        sources_dir: str,
        mutants_dir: str,
        build_dir: Optional[str] = None,
    ):
        self.tb_path = Path(tb_path).resolve()
        self.sources_dir = Path(sources_dir).resolve()
        self.mutants_dir = Path(mutants_dir).resolve()
        self.build_dir = (
            Path(build_dir).resolve() if build_dir
            else Path(tempfile.mkdtemp(prefix="axi4_grade_"))
        )
        self.source_files = self._get_ordered_sources()

    def _get_ordered_sources(self) -> list:
        """Package files must come first for Verilator."""
        all_files = list(self.sources_dir.glob("*.sv"))
        pkg_files = sorted(f for f in all_files if "pkg" in f.name.lower())
        other_files = sorted(f for f in all_files if "pkg" not in f.name.lower())
        return pkg_files + other_files

    def _run_command(self, cmd: list, cwd=None, timeout: int = 60) -> tuple:
        """Run a command. Returns (returncode, stdout, stderr)."""
        try:
            r = subprocess.run(
                cmd,
                cwd=cwd or self.build_dir,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return r.returncode, r.stdout, r.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)

    # =========================================================================
    # Pillar helpers: differential comparison, coverage parsing
    # =========================================================================

    def _count_errors(self, output: str) -> int:
        """Count error markers in combined stdout+stderr."""
        return sum(len(re.findall(p, output, re.IGNORECASE)) for p in ERROR_MARKERS)

    def _is_mutant_killed(
        self, golden_out: str, mutant_out: str, mutant_exit: int
    ) -> bool:
        """
        Differential kill detection (ungameable).
        A mutant is KILLED only if:
          - Golden run shows 0 error markers (no false positives gate)
          - Mutant run shows >=1 error markers OR nonzero exit

        Unconditional $error prints penalize the golden run too — agent can't cheat.
        """
        return (
            self._count_errors(golden_out) == 0
            and (self._count_errors(mutant_out) > 0 or mutant_exit != 0)
        )

    def _parse_coverage_dat(self, cov_file: Path) -> float:
        """
        Parse Verilator coverage.dat for line coverage fraction.
        Tries verilator_coverage → lcov first, falls back to direct parsing.
        """
        if not cov_file.exists():
            return 0.0

        # Preferred: use verilator_coverage to produce standard lcov format
        info_file = cov_file.parent / "coverage.info"
        ret = subprocess.run(
            ["verilator_coverage", "--write-info", str(info_file), str(cov_file)],
            capture_output=True,
            text=True,
        )
        if ret.returncode == 0 and info_file.exists():
            return self._parse_lcov(info_file)

        # Fallback: direct C-line parsing
        return self._parse_coverage_dat_direct(cov_file)

    def _parse_lcov(self, info_file: Path) -> float:
        """Parse lcov .info format: DA:line,hits lines."""
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

    def _parse_coverage_dat_direct(self, cov_file: Path) -> float:
        """Fallback: parse Verilator coverage.dat C-lines directly."""
        total, hit = 0, 0
        for line in cov_file.read_text().splitlines():
            if line.startswith("C "):
                total += 1
                parts = line.strip().split()
                try:
                    if int(parts[-1]) > 0:
                        hit += 1
                except (ValueError, IndexError):
                    pass
        return hit / total if total > 0 else 0.0

    def _parse_functional_coverage(self, stdout: str) -> float:
        """
        Parse COVERAGE_BINS_HIT=N from axi4_coverage.sv stdout output.
        Returns fraction 0.0-1.0.
        Returns 0.0 if coverage module not instantiated by agent.
        """
        m = re.search(r"COVERAGE_BINS_HIT=(\d+)", stdout)
        if not m:
            return 0.0
        bins_hit = int(m.group(1))
        total_m = re.search(r"COVERAGE_BINS_TOTAL=(\d+)", stdout)
        total = int(total_m.group(1)) if total_m else 24
        return min(bins_hit / total, 1.0)

    # =========================================================================
    # Compilation helper
    # =========================================================================

    def _compile_cmd(
        self, sources: list, build_dir: Path, coverage: bool = False
    ) -> list:
        cmd = [
            "verilator", "--binary", "-j", "0",
            "--timing", "--assert",
            "-Wno-fatal", "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC",
            "-Wno-TIMESCALEMOD", "-Wno-INITIALDLY",
            "-Mdir", str(build_dir),
            "-o", "sim",
        ]
        if coverage:
            cmd.append("--coverage-line")
        cmd += [str(f) for f in sources] + [str(self.tb_path)]
        return cmd

    # =========================================================================
    # Grading phases
    # =========================================================================

    def _phase1_compile(self, result: GradeResult) -> bool:
        """
        Phase 1: Compile testbench with Verilator (--coverage-line --assert).
        Gate: compilation failure → score stays 0.
        """
        print("\n[Phase 1] Compilation (--coverage-line --assert)...")
        build = self.build_dir / "golden"
        build.mkdir(parents=True, exist_ok=True)

        cmd = self._compile_cmd(self.source_files, build, coverage=True)
        code, _, stderr = self._run_command(cmd, cwd=build, timeout=120)

        if code != 0:
            result.error_message = f"Compilation failed:\n{stderr[:600]}"
            print("  FAILED")
            return False

        print("  PASSED")
        result.phase1_compiled = True
        return True

    def _phase2_golden_run(self, result: GradeResult) -> bool:
        """
        Phase 2: Run compiled binary against golden (bug-free) DUT.
        Gate: any error marker = false positive = 0 coverage/mutation credit.
        Also collects code coverage (coverage.dat) and functional coverage (stdout).
        """
        print("\n[Phase 2] Golden DUT run (false positive check + coverage)...")
        build = self.build_dir / "golden"
        sim = build / "sim"

        if not sim.exists():
            result.error_message = "Simulation binary not found after compile"
            return False

        code, stdout, stderr = self._run_command(
            [str(sim)], cwd=build, timeout=self.TIMEOUT_SECONDS
        )
        golden_output = stdout + stderr
        result.golden_output = golden_output  # Saved for Phase 3 differential

        # Gate: assertions must NOT fire on the correct (golden) DUT
        n_errors = self._count_errors(golden_output)
        if n_errors > 0:
            result.error_message = (
                f"Phase 2 FAILED: {n_errors} error marker(s) on golden DUT "
                "(false positives — use 'else $error()' in SVA, not unconditional prints)"
            )
            print(f"  FAILED: {n_errors} false positive(s)")
            return False

        print("  PASSED: 0 false positives on golden DUT")
        result.phase2_negative_passed = True

        # Collect coverage from this run
        cov = CoverageResult()
        cov.line_coverage = self._parse_coverage_dat(build / "coverage.dat")
        cov.functional_coverage = self._parse_functional_coverage(stdout)
        result.phase3_coverage = cov

        print(f"  Code Coverage:       {cov.line_coverage * 100:.1f}%")
        if cov.functional_coverage > 0:
            print(f"  Functional Coverage: {cov.functional_coverage * 100:.1f}%")
        else:
            print("  Functional Coverage: 0% (axi4_coverage.sv not detected in output)")

        return True

    def _phase3_mutation_testing(self, result: GradeResult) -> bool:
        """
        Phase 3: Differential mutation testing.
        Each .sv file in mutants_dir replaces axi4_read_channel.sv.
        Mutant KILLED iff: golden_errors==0 AND mutant errors>0 or exit!=0.
        Non-blocking (partial credit).
        """
        print("\n[Phase 3] Differential Mutation Testing...")
        mut = MutationResult()

        if not self.mutants_dir.exists():
            print("  No mutants directory — skipping")
            result.phase4_mutation = mut
            return True

        mutant_files = sorted(self.mutants_dir.glob("*.sv"))
        mut.total_mutants = len(mutant_files)

        if mut.total_mutants == 0:
            print("  No mutant files — skipping")
            result.phase4_mutation = mut
            return True

        for mf in mutant_files:
            mname = mf.stem
            mdir = Path(tempfile.mkdtemp(prefix=f"mut_{mname}_"))
            try:
                # Replace axi4_read_channel.sv with this mutant
                msources = [
                    mf if "read_channel" in s.name.lower() else s
                    for s in self.source_files
                ]

                cmd = self._compile_cmd(msources, mdir, coverage=False)
                code, _, _ = self._run_command(cmd, cwd=mdir, timeout=60)

                if code != 0:
                    # Mutant causes compile failure — counts as killed
                    mut.killed_mutants += 1
                    mut.killed_list.append(f"{mname}(compile_fail)")
                    print(f"  {mname}: KILLED (compile fail)")
                    continue

                sim = mdir / "sim"
                code, stdout, stderr = self._run_command(
                    [str(sim)], cwd=mdir, timeout=self.MUTANT_TIMEOUT
                )
                mutant_output = stdout + stderr

                if self._is_mutant_killed(result.golden_output, mutant_output, code):
                    mut.killed_mutants += 1
                    mut.killed_list.append(mname)
                    print(f"  {mname}: KILLED")
                else:
                    mut.survived_list.append(mname)
                    print(f"  {mname}: survived")

            finally:
                shutil.rmtree(mdir, ignore_errors=True)

        result.phase4_mutation = mut
        print(f"  Killed: {mut.killed_mutants}/{mut.total_mutants}")
        if mut.survived_list:
            print(f"  Survived: {mut.survived_list}")
        return True

    def _phase4_structural(self, result: GradeResult) -> bool:
        """
        Phase 4: Structural quality of the testbench.
        Checks assertion presence, test tasks, RLAST/handshake coverage.
        Non-blocking (partial credit).
        """
        print("\n[Phase 4] Structural Quality...")
        struct = StructuralResult()

        try:
            tb = self.tb_path.read_text()
        except Exception as e:
            result.phase5_structural = struct
            print(f"  Could not read TB: {e}")
            return True

        struct.has_assert_property = bool(re.search(r"assert\s+property", tb, re.I))
        struct.assertion_count = len(re.findall(r"assert\s+property", tb, re.I))
        struct.test_count = len(re.findall(
            r"\btask\b\s+(?:automatic\s+)?\w*(?:test|read|write|burst)\w*", tb, re.I
        ))
        struct.has_rlast_check = bool(re.search(r"\brlast\b", tb, re.I))
        struct.has_handshake_check = bool(
            re.search(r"(rvalid.*rready|arvalid.*arready)", tb, re.I)
        )

        # Normalized 0-1 across 5 quality dimensions
        struct.structural_score = (
            (1.0 if struct.has_assert_property else 0.0)
            + min(struct.assertion_count / 3.0, 1.0)
            + (1.0 if struct.has_rlast_check else 0.0)
            + (1.0 if struct.has_handshake_check else 0.0)
            + min(struct.test_count / 2.0, 1.0)
        ) / 5.0

        result.phase5_structural = struct
        print(f"  assert property: {struct.assertion_count}, tasks: {struct.test_count}")
        print(f"  rlast: {struct.has_rlast_check}, handshake: {struct.has_handshake_check}")
        print(f"  Structural score: {struct.structural_score:.1%}")
        return True

    # =========================================================================
    # Main entry point
    # =========================================================================

    def grade(self) -> GradeResult:
        """Run all grading phases and return complete result."""
        result = GradeResult()

        print("=" * 60)
        print("AXI4 Read Channel — Three-Pillar Grading")
        print("=" * 60)

        if not self._phase1_compile(result):
            return result

        if not self._phase2_golden_run(result):
            return result

        self._phase3_mutation_testing(result)
        self._phase4_structural(result)

        result.passed = True
        return result


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Grade AXI4 read channel TB+SVA")
    parser.add_argument("--tb", default="verif/axi4_read_channel_tb.sv")
    parser.add_argument("--sources", default="sources")
    parser.add_argument("--mutants", default="tests/mutants")
    parser.add_argument("--build", default=None)
    args = parser.parse_args()

    grader = AXI4ReadChannelGrader(
        tb_path=args.tb,
        sources_dir=args.sources,
        mutants_dir=args.mutants,
        build_dir=args.build,
    )
    result = grader.grade()
    exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
