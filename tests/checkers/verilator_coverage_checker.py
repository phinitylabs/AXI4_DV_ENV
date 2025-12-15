"""
Verilator Coverage Checker for DV Task Grading.

This module provides coverage analysis using Verilator's built-in coverage features:
- Line coverage
- Toggle coverage  
- Branch coverage (requires --coverage-branch)

Verilator generates coverage data that can be analyzed to assess testbench quality.

Usage:
    checker = VerilatorCoverageChecker(testbench_path, dut_files)
    score, details = checker.get_coverage_grade()
"""

import os
import re
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class CoverageData:
    """Coverage data extracted from Verilator coverage reports."""
    line_coverage: float = 0.0
    toggle_coverage: float = 0.0
    branch_coverage: float = 0.0
    total_lines: int = 0
    covered_lines: int = 0
    total_toggles: int = 0
    covered_toggles: int = 0
    total_branches: int = 0
    covered_branches: int = 0
    coverage_files: List[str] = field(default_factory=list)


class VerilatorCoverageChecker:
    """
    Analyzes testbench coverage using Verilator.
    
    This checker compiles and runs the testbench with Verilator's coverage
    instrumentation enabled, then parses the coverage report to grade the testbench.
    """
    
    def __init__(
        self,
        testbench_path: str,
        dut_files: List[str],
        design_root: str = ".",
    ):
        """
        Initialize the Verilator coverage checker.
        
        Args:
            testbench_path: Path to the testbench file
            dut_files: List of DUT source files
            design_root: Root directory of the design
        """
        self.testbench_path = testbench_path
        self.dut_files = dut_files
        self.design_root = design_root
        self.temp_dir = None
        self.coverage_data = None
        
    def _setup_temp_directory(self) -> str:
        """Create temporary directory for compilation."""
        self.temp_dir = tempfile.mkdtemp(prefix="verilator_cov_")
        return self.temp_dir
    
    def _cleanup_temp_directory(self):
        """Remove temporary directory."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None
    
    def _compile_with_coverage(self) -> Tuple[bool, str]:
        """
        Compile testbench with Verilator coverage enabled.
        
        Returns:
            Tuple of (success, error_message)
        """
        if not self.temp_dir:
            self._setup_temp_directory()
        
        output_dir = os.path.join(self.temp_dir, "obj_dir")
        coverage_dir = os.path.join(self.temp_dir, "coverage")
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(coverage_dir, exist_ok=True)
        
        # Collect source files
        source_files = []
        for dut_file in self.dut_files:
            src_path = os.path.join(self.design_root, dut_file)
            if os.path.exists(src_path):
                source_files.append(src_path)
            elif os.path.exists(dut_file):
                source_files.append(dut_file)
        
        if os.path.exists(self.testbench_path):
            source_files.append(self.testbench_path)
        else:
            return False, f"Testbench not found: {self.testbench_path}"
        
        # Get testbench module name
        tb_name = os.path.splitext(os.path.basename(self.testbench_path))[0]
        
        # Verilator compilation command with coverage
        cmd = [
            "verilator",
            "--binary",
            "--timing",
            "--coverage",  # Enable coverage instrumentation
            "--coverage-line",  # Line coverage
            "--coverage-toggle",  # Toggle coverage
            "-Wno-fatal",
            "-Wno-WIDTHEXPAND",
            "-Wno-WIDTHTRUNC",
            "-Wno-TIMESCALEMOD",
            "-Wno-STMTDLY",
            "-Wno-INITIALDLY",
            "--trace",
            "--top-module", tb_name,
            "-o", f"{output_dir}/Vtb",
            "--Mdir", output_dir,
        ] + source_files
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180,  # Coverage builds take longer
            )
            
            if result.returncode != 0:
                return False, result.stderr
            return True, ""
        except subprocess.TimeoutExpired:
            return False, "Verilator compilation timed out"
        except FileNotFoundError:
            return False, "Verilator not found in PATH"
        except Exception as e:
            return False, str(e)
    
    def _run_simulation(self, timeout: int = 120) -> Tuple[bool, str]:
        """
        Run simulation to generate coverage data.
        
        Returns:
            Tuple of (success, log_content)
        """
        output_dir = os.path.join(self.temp_dir, "obj_dir")
        exe_path = f"{output_dir}/Vtb"
        
        if not os.path.exists(exe_path):
            return False, "Compiled testbench not found"
        
        try:
            result = subprocess.run(
                [exe_path],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.temp_dir,
            )
            
            log_content = result.stdout + result.stderr
            
            # Check for completion indicators
            completion_indicators = ["$finish", "Simulation Complete", "Coverage Report"]
            has_completion = any(ind in log_content for ind in completion_indicators)
            
            return has_completion or result.returncode == 0, log_content
        except subprocess.TimeoutExpired:
            return False, "Simulation timed out"
        except Exception as e:
            return False, str(e)
    
    def _parse_coverage_dat(self) -> CoverageData:
        """
        Parse Verilator coverage.dat file.
        
        Returns:
            CoverageData with parsed results
        """
        coverage = CoverageData()
        
        # Verilator creates coverage.dat in the working directory
        dat_files = [
            os.path.join(self.temp_dir, "coverage.dat"),
            os.path.join(self.temp_dir, "obj_dir", "coverage.dat"),
        ]
        
        dat_file = None
        for f in dat_files:
            if os.path.exists(f):
                dat_file = f
                break
        
        if not dat_file:
            return coverage
        
        coverage.coverage_files.append(dat_file)
        
        try:
            with open(dat_file, 'r') as f:
                content = f.read()
            
            # Parse line coverage
            line_matches = re.findall(r'C\s+\'(\d+)\'\s+(\d+)', content)
            if line_matches:
                total = len(line_matches)
                covered = sum(1 for _, count in line_matches if int(count) > 0)
                coverage.total_lines = total
                coverage.covered_lines = covered
                coverage.line_coverage = (covered / total * 100) if total > 0 else 0.0
            
            # Parse toggle coverage
            toggle_matches = re.findall(r'T\s+\'(\d+)\'\s+(\d+)', content)
            if toggle_matches:
                total = len(toggle_matches)
                covered = sum(1 for _, count in toggle_matches if int(count) > 0)
                coverage.total_toggles = total
                coverage.covered_toggles = covered
                coverage.toggle_coverage = (covered / total * 100) if total > 0 else 0.0
            
            # Parse branch coverage (if available)
            branch_matches = re.findall(r'B\s+\'(\d+)\'\s+(\d+)', content)
            if branch_matches:
                total = len(branch_matches)
                covered = sum(1 for _, count in branch_matches if int(count) > 0)
                coverage.total_branches = total
                coverage.covered_branches = covered
                coverage.branch_coverage = (covered / total * 100) if total > 0 else 0.0
                
        except Exception:
            pass
        
        return coverage
    
    def _run_verilator_coverage_tool(self) -> Dict[str, float]:
        """
        Run verilator_coverage tool to get detailed report.
        
        Returns:
            Dict with coverage percentages
        """
        results = {
            "line_coverage": 0.0,
            "toggle_coverage": 0.0,
            "branch_coverage": 0.0,
        }
        
        dat_file = os.path.join(self.temp_dir, "coverage.dat")
        if not os.path.exists(dat_file):
            return results
        
        try:
            # Run verilator_coverage --annotate
            annotate_dir = os.path.join(self.temp_dir, "coverage_annotate")
            os.makedirs(annotate_dir, exist_ok=True)
            
            result = subprocess.run(
                ["verilator_coverage", "--annotate", annotate_dir, dat_file],
                capture_output=True,
                text=True,
                timeout=60,
            )
            
            # Parse output for summary statistics
            output = result.stdout + result.stderr
            
            # Look for percentage patterns
            line_match = re.search(r'Lines:\s*(\d+\.?\d*)%', output)
            if line_match:
                results["line_coverage"] = float(line_match.group(1))
            
            toggle_match = re.search(r'Toggles?:\s*(\d+\.?\d*)%', output)
            if toggle_match:
                results["toggle_coverage"] = float(toggle_match.group(1))
            
            branch_match = re.search(r'Branch(?:es)?:\s*(\d+\.?\d*)%', output)
            if branch_match:
                results["branch_coverage"] = float(branch_match.group(1))
                
        except FileNotFoundError:
            # verilator_coverage tool not available
            pass
        except Exception:
            pass
        
        return results
    
    def analyze_coverage(self) -> CoverageData:
        """
        Full coverage analysis workflow.
        
        Returns:
            CoverageData with coverage results
        """
        try:
            # Setup
            self._setup_temp_directory()
            
            # Compile with coverage
            compile_ok, compile_err = self._compile_with_coverage()
            if not compile_ok:
                return CoverageData()
            
            # Run simulation
            sim_ok, sim_log = self._run_simulation()
            if not sim_ok:
                return CoverageData()
            
            # Parse coverage data
            self.coverage_data = self._parse_coverage_dat()
            
            # Try to get more detailed coverage from tool
            tool_results = self._run_verilator_coverage_tool()
            if tool_results["line_coverage"] > 0:
                self.coverage_data.line_coverage = tool_results["line_coverage"]
            if tool_results["toggle_coverage"] > 0:
                self.coverage_data.toggle_coverage = tool_results["toggle_coverage"]
            if tool_results["branch_coverage"] > 0:
                self.coverage_data.branch_coverage = tool_results["branch_coverage"]
            
            return self.coverage_data
            
        finally:
            self._cleanup_temp_directory()
    
    def get_coverage_grade(self) -> Tuple[float, Dict[str, any]]:
        """
        Get a grade based on coverage analysis.
        
        Returns:
            Tuple of (score out of 100, detailed results dict)
        """
        coverage = self.analyze_coverage()
        
        # Calculate weighted coverage score
        # Line coverage: 50% weight
        # Toggle coverage: 30% weight
        # Branch coverage: 20% weight
        score = (
            coverage.line_coverage * 0.5 +
            coverage.toggle_coverage * 0.3 +
            coverage.branch_coverage * 0.2
        )
        
        details = {
            "line_coverage": coverage.line_coverage,
            "toggle_coverage": coverage.toggle_coverage,
            "branch_coverage": coverage.branch_coverage,
            "total_lines": coverage.total_lines,
            "covered_lines": coverage.covered_lines,
            "total_toggles": coverage.total_toggles,
            "covered_toggles": coverage.covered_toggles,
            "total_branches": coverage.total_branches,
            "covered_branches": coverage.covered_branches,
            "coverage_files": coverage.coverage_files,
            "weighted_score": score,
        }
        
        return score, details


def analyze_verilator_coverage(
    testbench_path: str,
    dut_files: List[str],
    design_root: str = ".",
) -> Tuple[float, Dict[str, any]]:
    """
    Convenience function to analyze coverage.
    
    Args:
        testbench_path: Path to testbench
        dut_files: List of DUT files
        design_root: Design root directory
        
    Returns:
        Tuple of (score, details)
    """
    checker = VerilatorCoverageChecker(testbench_path, dut_files, design_root)
    return checker.get_coverage_grade()


def format_coverage_report(details: Dict[str, any]) -> str:
    """
    Format a human-readable coverage report.
    
    Args:
        details: Coverage details from get_coverage_grade()
        
    Returns:
        Formatted report string
    """
    report = """
============================================================
Verilator Coverage Report
============================================================

Coverage Summary:
  Line Coverage:   {line_coverage:.1f}% ({covered_lines}/{total_lines})
  Toggle Coverage: {toggle_coverage:.1f}% ({covered_toggles}/{total_toggles})
  Branch Coverage: {branch_coverage:.1f}% ({covered_branches}/{total_branches})

Weighted Score: {weighted_score:.1f}/100

Coverage Grade:
""".format(**details)
    
    score = details.get("weighted_score", 0)
    if score >= 80:
        report += "  Grade: EXCELLENT (80%+)\n"
    elif score >= 60:
        report += "  Grade: GOOD (60-79%)\n"
    elif score >= 40:
        report += "  Grade: FAIR (40-59%)\n"
    else:
        report += "  Grade: POOR (<40%)\n"
    
    report += "\n============================================================\n"
    
    return report
