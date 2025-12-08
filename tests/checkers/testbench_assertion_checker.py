"""
Testbench Assertion Checker for DV Task Grading.

This module:
1. Detects assertions in SystemVerilog testbenches
2. Compiles and simulates testbenches
3. Analyzes simulation logs for assertion execution
4. Grades testbenches based on assertion coverage
"""

import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class AssertionChecker:
    """Checks for assertions in testbenches and analyzes their execution."""
    
    def __init__(self, testbench_path: str, dut_path: Optional[str] = None, simulator: str = "icarus"):
        """
        Initialize the assertion checker.
        
        Args:
            testbench_path: Path to the testbench file
            dut_path: Optional path to DUT file (if testbench doesn't include it)
            simulator: Simulator to use ("icarus" or "verilator")
        """
        self.testbench_path = self._resolve_path(testbench_path)
        # Don't resolve dut_path here - it may contain multiple files separated by spaces
        # Resolution will happen in compile_testbench() when files are split
        self.dut_path = dut_path
        self.simulator = simulator.lower()
        # Use log directory for all logs - always use harness/patch/tests for grading
        # This ensures all logs are in one place for grading, regardless of testbench location
        # Testbench can be in verif/ but logs go to harness/patch/tests/log/
        if "harness/patch/tests" in self.testbench_path:
            self.log_dir = "harness/patch/tests/log"
            self.output_dir = "harness/patch/tests/sim_build"
        elif "harness/test" in self.testbench_path:
            self.log_dir = "harness/test/log"
            self.output_dir = "harness/test/sim_build"
        else:
            # Default: use harness/patch/tests for grading (even if testbench is in verif/)
            self.log_dir = "harness/patch/tests/log"
            self.output_dir = "harness/patch/tests/sim_build"
        self.sim_log_path = os.path.join(self.log_dir, "sim.log")
        self.compile_log_path = os.path.join(self.log_dir, "compile.log")
        
    def _resolve_path(self, file_path: str) -> str:
        """Resolve file path by searching common directories."""
        if not file_path:
            return file_path
            
        # If absolute path exists, use it
        if os.path.isabs(file_path) and os.path.exists(file_path):
            return file_path
            
        # Check current directory first
        if os.path.exists(file_path):
            return file_path
        
        # If path contains directory separators, don't try to resolve by filename only
        # This prevents finding wrong files (e.g., rtl/file.sv when looking for harness/patch/rtl/file.sv)
        has_path_components = os.path.dirname(file_path) and os.path.dirname(file_path) != "."
        
        # Check common directories with full path
        # Priority: verif first (for agent-generated testbenches)
        search_dirs = [
            "verif",
            ".",
            "..",
            "rtl",
            "harness/test",
            "harness/patch/test",
            "harness/patch/rtl",
        ]
        
        for search_dir in search_dirs:
            candidate = os.path.join(search_dir, file_path)
            if os.path.exists(candidate):
                return candidate
        
        # Only try resolving by filename if the original path had no directory components
        # This prevents accidentally finding wrong files
        if not has_path_components:
            for search_dir in search_dirs:
                candidate = os.path.join(search_dir, os.path.basename(file_path))
                if os.path.exists(candidate):
                    return candidate
        
        # Return original if not found (will fail later)
        return file_path
    
    def find_assertions(self) -> Dict[str, List[str]]:
        """
        Find all assertions in the testbench.
        
        Returns:
            Dictionary with 'immediate' and 'concurrent' assertion lists
        """
        if not os.path.exists(self.testbench_path):
            return {"immediate": [], "concurrent": []}
        
        with open(self.testbench_path, 'r') as f:
            content = f.read()
        
        # Pattern for immediate assertions: assert (condition) [else action];
        # More flexible pattern to match both single-line and multi-line assertions
        immediate_pattern = r'assert\s*\([^)]+\)'
        immediate_assertions = re.findall(immediate_pattern, content, re.MULTILINE | re.DOTALL)
        
        # Pattern for concurrent assertions: assert property(...) or assert sequence(...)
        concurrent_pattern = r'assert\s+(?:property|sequence)\s*\([^)]+\)'
        concurrent_assertions = re.findall(concurrent_pattern, content, re.MULTILINE)
        
        return {
            "immediate": immediate_assertions,
            "concurrent": concurrent_assertions,
        }
    
    def check_assertions_in_code(self) -> Dict[str, any]:
        """
        Check for assertions in the testbench code and return detailed analysis.
        
        Returns:
            Dictionary with assertion analysis results
        """
        if not os.path.exists(self.testbench_path):
            return {
                "valid": False,
                "has_assertions": False,
                "assertion_count": 0,
                "assertion_types": [],
                "assertion_locations": []
            }
        
        try:
            with open(self.testbench_path, 'r') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            return {
                "valid": False,
                "has_assertions": False,
                "assertion_count": 0,
                "assertion_types": [],
                "assertion_locations": []
            }
        
        # Find assertions
        assertions = self.find_assertions()
        total_assertions = len(assertions["immediate"]) + len(assertions["concurrent"])
        
        # Determine assertion types
        assertion_types = []
        if assertions["immediate"]:
            assertion_types.append("immediate_assertion")
        if assertions["concurrent"]:
            assertion_types.append("concurrent_assertion")
        
        # Check for error assertions
        if re.search(r'assert.*\$error', content, re.IGNORECASE):
            assertion_types.append("error_assertion")
        
        # Find assertion locations (line numbers)
        assertion_locations = []
        for i, line in enumerate(lines, 1):
            if re.search(r'\bassert\s+(?:property|sequence|\([^)]+\))', line):
                assertion_locations.append(i)
        
        return {
            "valid": True,
            "has_assertions": total_assertions > 0,
            "assertion_count": total_assertions,
            "assertion_types": list(set(assertion_types)),  # Remove duplicates
            "assertion_locations": assertion_locations
        }
    
    def compile_testbench(self) -> Tuple[bool, str]:
        """
        Compile the testbench with the configured simulator.
        
        Returns:
            (success, error_message)
        """
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Collect all source files
        source_files = []
        if self.dut_path:
            dut_files = self.dut_path.split()
            for dut_file in dut_files:
                dut_file = dut_file.strip()
                if not dut_file:
                    continue
                if os.path.exists(dut_file):
                    source_files.append(dut_file)
                else:
                    resolved = self._resolve_path(dut_file)
                    source_files.append(resolved)
        source_files.append(self.testbench_path)
        
        if self.simulator == "verilator":
            return self._compile_verilator(source_files)
        else:
            return self._compile_icarus(source_files)
    
    def _compile_icarus(self, source_files: List[str]) -> Tuple[bool, str]:
        """Compile with Icarus Verilog."""
        cmd = ["iverilog", "-g2012", "-o", f"{self.output_dir}/tb.out"] + source_files
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            with open(self.compile_log_path, 'w') as log_file:
                log_file.write(result.stdout)
                log_file.write(result.stderr)
            
            if result.returncode != 0:
                return False, result.stderr
            return True, ""
        except subprocess.TimeoutExpired:
            return False, "Compilation timed out"
        except Exception as e:
            return False, str(e)
    
    def _compile_verilator(self, source_files: List[str]) -> Tuple[bool, str]:
        """Compile with Verilator."""
        # Get the testbench module name (assume it's the filename without extension)
        tb_name = os.path.splitext(os.path.basename(self.testbench_path))[0]
        
        cmd = [
            "verilator",
            "--binary",
            "--timing",
            "-Wno-fatal",
            "-Wno-WIDTHEXPAND",
            "-Wno-WIDTHTRUNC", 
            "--top-module", tb_name,
            "-o", f"{self.output_dir}/Vtb",
            "--Mdir", f"{self.output_dir}/verilator_obj"
        ] + source_files
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120  # Verilator takes longer
            )
            
            with open(self.compile_log_path, 'w') as log_file:
                log_file.write(f"Command: {' '.join(cmd)}\n\n")
                log_file.write(result.stdout)
                log_file.write(result.stderr)
            
            if result.returncode != 0:
                return False, result.stderr
            return True, ""
        except subprocess.TimeoutExpired:
            return False, "Verilator compilation timed out"
        except Exception as e:
            return False, str(e)
    
    def run_simulation(self, timeout: int = 60) -> Tuple[bool, str]:
        """
        Run the simulation with the configured simulator.
        
        Args:
            timeout: Maximum simulation time in seconds
            
        Returns:
            (success, error_message)
        """
        if self.simulator == "verilator":
            exe_path = f"{self.output_dir}/Vtb"
        else:
            exe_path = f"{self.output_dir}/tb.out"
            
        if not os.path.exists(exe_path):
            return False, f"Compiled testbench not found at {exe_path}. Compile first."
        
        try:
            # Ensure log directory exists
            os.makedirs(self.log_dir, exist_ok=True)
            
            # Build simulation command
            if self.simulator == "verilator":
                sim_cmd = [exe_path]
            else:
                sim_cmd = ["vvp", exe_path]
            
            # Run simulation and capture output (overwrite any existing log)
            with open(self.sim_log_path, 'w') as log_file:
                result = subprocess.run(
                    sim_cmd,
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                    text=True,
                    timeout=timeout
                )
            
            # Check if simulation completed (look for $finish, VCD info, or completion messages)
            with open(self.sim_log_path, 'r') as f:
                log_content = f.read()
                # Check for successful completion indicators
                completion_indicators = [
                    "$finish",
                    "VCD info",
                    "Simulation Completed",
                    "Simulation finished",
                    "Test Summary",
                    "Coverage Report"
                ]
                has_completion = any(indicator in log_content for indicator in completion_indicators)
                
                if has_completion:
                    # Simulation completed successfully, even if return code is non-zero (might be warnings)
                    return True, ""
                elif result.returncode != 0:
                    # Check if it's just a warning (exit code 1-2) vs fatal error
                    if result.returncode <= 2 and len(log_content) > 100:
                        # Likely just warnings, simulation may have completed
                        return True, ""
                    return False, f"Simulation failed with code {result.returncode}"
                else:
                    # Simulation may have completed without explicit indicators
                    return True, ""
        except subprocess.TimeoutExpired:
            return False, f"Simulation timed out after {timeout} seconds"
        except Exception as e:
            return False, str(e)
    
    def check_assertions_in_log(self, log_path: Optional[str] = None) -> Dict[str, int]:
        """
        Analyze simulation log for assertion execution.
        
        Args:
            log_path: Path to simulation log (default: self.sim_log_path)
            
        Returns:
            Dictionary with assertion statistics
        """
        # Default to log directory if no path specified
        if log_path is None:
            log_file = self.sim_log_path
        elif os.path.isabs(log_path) or os.path.dirname(log_path):
            log_file = log_path
        else:
            # If relative path, try log directory first
            log_file = os.path.join(self.log_dir, log_path) if not os.path.exists(log_path) else log_path
        
        if not os.path.exists(log_file):
            return {
                "assertions_executed": 0,
                "assertion_passes": 0,
                "assertion_failures": 0,
            }
        
        with open(log_file, 'r') as f:
            content = f.read()
        
        # Count assertion failures
        # Patterns match: "ASSERTION FAILED", "ASSERTION 1 FAILED", "[ASSERTION 2 FAILED]", etc.
        failure_patterns = [
            r'ASSERTION\s*\d*\s*FAILED',      # Matches "ASSERTION FAILED", "ASSERTION 1 FAILED", etc.
            r'\[ASSERTION\s+\d+\s+FAILED\]',  # Matches "[ASSERTION 2 FAILED]"
            r'Assertion.*failed',
            r'assert.*failed',
        ]
        failures = 0
        for pattern in failure_patterns:
            failures += len(re.findall(pattern, content, re.IGNORECASE))
        
        # Count assertion passes (if logged)
        # Patterns match: "ASSERTION PASSED", "ASSERTION 1 PASSED", "[ASSERTION 2 PASSED]", etc.
        pass_patterns = [
            r'ASSERTION\s*\d*\s*PASSED',      # Matches "ASSERTION PASSED", "ASSERTION 1 PASSED", etc.
            r'\[ASSERTION\s+\d+\s+PASSED\]',  # Matches "[ASSERTION 2 PASSED]"
            r'Assertion.*passed',
        ]
        passes = 0
        for pattern in pass_patterns:
            passes += len(re.findall(pattern, content, re.IGNORECASE))
        
        # If no explicit passes, assume assertions executed if we see any assertion activity
        executed = failures + passes
        if executed == 0:
            # Check for assertion-related output
            if re.search(r'assert', content, re.IGNORECASE):
                executed = 1  # At least one assertion was present
        
        return {
            "assertions_executed": executed,
            "assertion_passes": passes,
            "assertion_failures": failures,
        }
    
    def grade(self) -> Dict[str, any]:
        """
        Complete grading workflow: find assertions, compile, simulate, analyze.
        
        Returns:
            Dictionary with grading results
        """
        results = {
            "assertions_found": 0,
            "compilation_success": False,
            "simulation_success": False,
            "assertions_executed": 0,
            "assertion_passes": 0,
            "assertion_failures": 0,
            "score": 0.0,
            "errors": [],
        }
        
        # Step 1: Find assertions
        assertions = self.find_assertions()
        total_assertions = len(assertions["immediate"]) + len(assertions["concurrent"])
        results["assertions_found"] = total_assertions
        
        if total_assertions == 0:
            results["errors"].append("No assertions found in testbench")
            return results
        
        # Step 2: Compile
        compile_success, compile_error = self.compile_testbench()
        results["compilation_success"] = compile_success
        if not compile_success:
            results["errors"].append(f"Compilation failed: {compile_error}")
            return results
        
        # Step 3: Simulate
        sim_success, sim_error = self.run_simulation()
        results["simulation_success"] = sim_success
        if not sim_success:
            results["errors"].append(f"Simulation failed: {sim_error}")
            return results
        
        # Step 4: Analyze log
        log_stats = self.check_assertions_in_log()
        results["assertions_executed"] = log_stats["assertions_executed"]
        results["assertion_passes"] = log_stats["assertion_passes"]
        results["assertion_failures"] = log_stats["assertion_failures"]
        
        # Step 5: Calculate score
        # Score based on: assertions found (30%), compilation (20%), simulation (20%), execution (30%)
        score = 0.0
        if total_assertions > 0:
            score += 30.0  # Has assertions
        if compile_success:
            score += 20.0
        if sim_success:
            score += 20.0
        if log_stats["assertions_executed"] > 0:
            score += 30.0
        
        results["score"] = score
        
        return results


def grade_generated_testbench(
    testbench_path: str,
    dut_path: Optional[str] = None,
    require_assertions: bool = True,
    simulator: str = "icarus"
) -> Tuple[bool, Dict[str, any], str]:
    """
    Grade a generated testbench.
    
    Args:
        testbench_path: Path to testbench
        dut_path: Optional path to DUT
        require_assertions: Whether assertions are required
        simulator: Simulator to use (icarus, verilator, etc.)
        
    Returns:
        Tuple of (passed, grade_dict, report_string)
    """
    checker = AssertionChecker(testbench_path, dut_path)
    checker.simulator = simulator
    results = checker.grade()
    
    # Add requirement check
    if require_assertions and results["assertions_found"] == 0:
        results["errors"].append("Assertions are required but none were found")
        results["score"] = 0.0
    
    # Create formatted report
    report = f"""
============================================================
Testbench Assertion Grading Report
============================================================
Testbench: {testbench_path}
Simulator: {simulator}
Code Analysis:
  Has Assertions: {results["assertions_found"] > 0}
  Assertion Count: {results["assertions_found"]}
Compilation:
  Status: {'PASS' if results['compilation_success'] else 'FAIL'}
Simulation:
  Status: {'PASS' if results['simulation_success'] else 'FAIL'}
Assertion Execution:
  Executed: {results['assertions_executed'] > 0}
  Passes: {results['assertion_passes']}
  Failures: {results['assertion_failures']}
Score: {results['score']:.1f}/100.0
Result: {'PASS' if results['score'] >= 70.0 else 'FAIL'}
"""
    if results["errors"]:
        report += "\nErrors:\n"
        for error in results["errors"]:
            report += f"  - {error}\n"
    report += "============================================================\n"
    
    # Determine pass/fail
    passed = results["score"] >= 70.0
    if require_assertions:
        passed = passed and results["assertions_found"] > 0 and results["assertions_executed"] > 0
    
    # Add convenience fields for test assertions
    results["has_assertions"] = results["assertions_found"] > 0
    results["assertions_work"] = results["assertions_executed"] > 0
    results["compiles"] = results["compilation_success"]
    results["simulates"] = results["simulation_success"]
    
    return passed, results, report

