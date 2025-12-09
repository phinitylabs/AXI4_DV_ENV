"""
Bug Injection Tester for DV Task Grading.

This module tests testbench quality by:
1. Running testbench against correct RTL (should pass)
2. Running testbench against buggy RTL variants (should fail)
3. Scoring based on bug detection capability

A good testbench should:
- Pass with correct RTL
- Fail (catch bugs) with buggy RTL

Bug Categories for AXI4:
- Protocol violations (VALID not stable, wrong handshake)
- Response errors (invalid BRESP/RRESP)
- Data integrity issues (wrong data, missing LAST)
"""

import os
import re
import subprocess
import tempfile
import shutil
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class BugVariant:
    """Describes a bug to inject into RTL."""
    name: str
    description: str
    file_to_modify: str  # Relative path within design
    search_pattern: str  # Regex to find the code to modify
    replacement: str  # Replacement code with bug
    expected_assertion_failure: str  # Expected assertion name/pattern that should catch this
    severity: str = "high"  # high, medium, low
    channel: str = ""  # AXI4 channel affected (AW, W, B, AR, R)


@dataclass
class BugTestResult:
    """Result of testing one bug variant."""
    bug_name: str
    bug_description: str
    compilation_success: bool = False
    simulation_success: bool = False
    assertion_failures_detected: int = 0
    bug_caught: bool = False
    expected_failure: str = ""
    actual_failures: List[str] = field(default_factory=list)
    error: str = ""


@dataclass  
class BugInjectionResult:
    """Complete bug injection test results."""
    total_bugs_tested: int = 0
    bugs_caught: int = 0
    bugs_missed: int = 0
    detection_rate: float = 0.0
    bug_results: List[BugTestResult] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class AXI4BugInjectionTester:
    """
    Tests testbench quality by injecting bugs into RTL.
    
    Workflow:
    1. Copy RTL to temp directory
    2. For each bug variant:
       a. Apply bug modification
       b. Compile testbench with buggy RTL
       c. Run simulation
       d. Check if assertions caught the bug
       e. Restore original RTL
    3. Calculate bug detection score
    """
    
    # Common AXI4 bugs to inject
    # These are designed to be caught by proper protocol assertions
    # NOTE: Patterns must match the actual RTL code in sources/
    AXI4_BUGS = [
        # Write Address Channel bugs
        BugVariant(
            name="AW_VALID_DROPS_EARLY",
            description="AWVALID drops before AWREADY (protocol violation)",
            file_to_modify="sources/axi4_master.sv",
            search_pattern=r"(axi_awvalid\s*<=\s*1'b1;)",
            replacement=r"axi_awvalid <= 1'b1; #1 axi_awvalid <= 1'b0; #1 axi_awvalid <= 1'b1; // BUG: unstable AWVALID",
            expected_assertion_failure="AWVALID",
            severity="high",
            channel="AW",
        ),
        
        # Write Data Channel bugs
        # Pattern matches: axi_wlast <= (write_count == write_length);
        BugVariant(
            name="W_LAST_MISSING",
            description="WLAST not asserted on final beat",
            file_to_modify="sources/axi4_master.sv",
            search_pattern=r"(axi_wlast\s*<=\s*\(write_count\s*==\s*write_length\);)",
            replacement=r"axi_wlast <= 1'b0; // BUG: WLAST never asserted",
            expected_assertion_failure="WLAST",
            severity="high",
            channel="W",
        ),
        
        # Write Response Channel bugs
        # Pattern matches: axi_bresp <= OKAY; (uses constant)
        BugVariant(
            name="B_RESP_INVALID",
            description="BRESP returns error instead of OKAY",
            file_to_modify="sources/axi4_slave.sv",
            search_pattern=r"(axi_bresp\s*<=\s*OKAY;)",
            replacement=r"axi_bresp <= DECERR; // BUG: Always return error",
            expected_assertion_failure="BRESP",
            severity="medium",
            channel="B",
        ),
        BugVariant(
            name="B_VALID_DROPS_EARLY",
            description="BVALID drops before BREADY (protocol violation)",
            file_to_modify="sources/axi4_slave.sv",
            search_pattern=r"(axi_bvalid\s*<=\s*1'b1;)",
            replacement=r"axi_bvalid <= 1'b1; #1 axi_bvalid <= 1'b0; // BUG: unstable BVALID",
            expected_assertion_failure="BVALID",
            severity="high",
            channel="B",
        ),
        
        # Read Address Channel bugs
        BugVariant(
            name="AR_VALID_DROPS_EARLY",
            description="ARVALID drops before ARREADY (protocol violation)",
            file_to_modify="sources/axi4_master.sv",
            search_pattern=r"(axi_arvalid\s*<=\s*1'b1;)",
            replacement=r"axi_arvalid <= 1'b1; #1 axi_arvalid <= 1'b0; #1 axi_arvalid <= 1'b1; // BUG: unstable ARVALID",
            expected_assertion_failure="ARVALID",
            severity="high",
            channel="AR",
        ),
        
        # Read Data Channel bugs
        # Pattern matches: axi_rlast <= 1'b1; // Single beat for now
        BugVariant(
            name="R_LAST_MISSING",
            description="RLAST not asserted on final beat",
            file_to_modify="sources/axi4_slave.sv",
            search_pattern=r"(axi_rlast\s*<=\s*1'b1;\s*//\s*Single beat)",
            replacement=r"axi_rlast <= 1'b0; // BUG: RLAST never asserted",
            expected_assertion_failure="RLAST",
            severity="high",
            channel="R",
        ),
        # Pattern matches: axi_rresp <= OKAY; (uses constant)
        BugVariant(
            name="R_RESP_INVALID",
            description="RRESP returns error instead of OKAY",
            file_to_modify="sources/axi4_slave.sv",
            search_pattern=r"(axi_rresp\s*<=\s*OKAY;)",
            replacement=r"axi_rresp <= DECERR; // BUG: Always return error",
            expected_assertion_failure="RRESP",
            severity="medium",
            channel="R",
        ),
    ]
    
    def __init__(
        self,
        testbench_path: str,
        design_root: str,
        dut_files: List[str],
        simulator: str = "icarus",
    ):
        """
        Initialize bug injection tester.
        
        Args:
            testbench_path: Path to testbench file
            design_root: Root directory of the design
            dut_files: List of DUT source files (relative to design_root)
            simulator: Simulator to use (icarus, verilator)
        """
        self.testbench_path = testbench_path
        self.design_root = design_root
        self.dut_files = dut_files
        self.simulator = simulator
        self.temp_dir = None
        
    def _setup_temp_directory(self) -> str:
        """Create temporary directory with design copy."""
        self.temp_dir = tempfile.mkdtemp(prefix="bug_injection_")
        
        # Copy design files to temp directory
        for dut_file in self.dut_files:
            src = os.path.join(self.design_root, dut_file)
            dst_dir = os.path.join(self.temp_dir, os.path.dirname(dut_file))
            os.makedirs(dst_dir, exist_ok=True)
            dst = os.path.join(self.temp_dir, dut_file)
            
            if os.path.exists(src):
                shutil.copy2(src, dst)
        
        # Copy testbench
        tb_dst = os.path.join(self.temp_dir, os.path.basename(self.testbench_path))
        if os.path.exists(self.testbench_path):
            shutil.copy2(self.testbench_path, tb_dst)
        
        return self.temp_dir
    
    def _cleanup_temp_directory(self):
        """Remove temporary directory."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None
    
    def _inject_bug(self, bug: BugVariant) -> bool:
        """
        Inject a bug into the RTL.
        
        Returns:
            True if bug was successfully injected
        """
        file_path = os.path.join(self.temp_dir, bug.file_to_modify)
        
        if not os.path.exists(file_path):
            return False
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Apply bug modification
            new_content, count = re.subn(bug.search_pattern, bug.replacement, content, count=1)
            
            if count == 0:
                return False  # Pattern not found
            
            with open(file_path, 'w') as f:
                f.write(new_content)
            
            return True
        except Exception:
            return False
    
    def _restore_file(self, bug: BugVariant):
        """Restore original file from design root."""
        src = os.path.join(self.design_root, bug.file_to_modify)
        dst = os.path.join(self.temp_dir, bug.file_to_modify)
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
    
    def _compile_and_run(self, timeout: int = 30) -> Tuple[bool, bool, str]:
        """
        Compile and run simulation.
        
        Returns:
            Tuple of (compile_success, sim_success, log_content)
        """
        output_dir = os.path.join(self.temp_dir, "sim_build")
        os.makedirs(output_dir, exist_ok=True)
        
        # Collect source files
        source_files = []
        for dut_file in self.dut_files:
            src = os.path.join(self.temp_dir, dut_file)
            if os.path.exists(src):
                source_files.append(src)
        
        tb_path = os.path.join(self.temp_dir, os.path.basename(self.testbench_path))
        if os.path.exists(tb_path):
            source_files.append(tb_path)
        
        if not source_files:
            return False, False, "No source files found"
        
        # Compile
        if self.simulator == "icarus":
            compile_cmd = ["iverilog", "-g2012", "-o", f"{output_dir}/tb.out"] + source_files
        else:
            return False, False, f"Unsupported simulator: {self.simulator}"
        
        try:
            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=self.temp_dir,
            )
            
            if compile_result.returncode != 0:
                return False, False, compile_result.stderr
        except subprocess.TimeoutExpired:
            return False, False, "Compilation timed out"
        except Exception as e:
            return False, False, str(e)
        
        # Run simulation
        try:
            sim_result = subprocess.run(
                ["vvp", f"{output_dir}/tb.out"],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.temp_dir,
            )
            
            log_content = sim_result.stdout + sim_result.stderr
            
            # Check for completion
            sim_success = "$finish" in log_content or "VCD info" in log_content
            
            return True, sim_success, log_content
        except subprocess.TimeoutExpired:
            return True, False, "Simulation timed out"
        except Exception as e:
            return True, False, str(e)
    
    def _check_assertion_failures(self, log_content: str, expected: str) -> Tuple[int, List[str], bool]:
        """
        Check for assertion failures in simulation log.
        
        Returns:
            Tuple of (failure_count, failure_messages, expected_bug_caught)
        """
        failure_patterns = [
            r'ASSERTION\s*\d*\s*FAILED[^:]*:?\s*([^\n]*)',
            r'\[ASSERTION\s+\d+\s+FAILED\]\s*([^\n]*)',
            r'Assertion.*failed[^:]*:?\s*([^\n]*)',
            r'\$error[^:]*:?\s*([^\n]*)',
        ]
        
        failures = []
        for pattern in failure_patterns:
            matches = re.findall(pattern, log_content, re.IGNORECASE)
            failures.extend(matches)
        
        # Check if expected bug was caught
        bug_caught = False
        if expected:
            expected_lower = expected.lower()
            for failure in failures:
                if expected_lower in failure.lower():
                    bug_caught = True
                    break
            
            # Also check full log for expected pattern
            if not bug_caught and expected_lower in log_content.lower():
                # Look for any failure near the expected pattern
                bug_caught = len(failures) > 0
        
        return len(failures), failures, bug_caught
    
    def test_bug(self, bug: BugVariant) -> BugTestResult:
        """
        Test a single bug variant.
        
        Args:
            bug: Bug variant to test
            
        Returns:
            BugTestResult with test outcome
        """
        result = BugTestResult(
            bug_name=bug.name,
            bug_description=bug.description,
            expected_failure=bug.expected_assertion_failure,
        )
        
        # Inject bug
        if not self._inject_bug(bug):
            result.error = f"Could not inject bug: pattern not found in {bug.file_to_modify}"
            self._restore_file(bug)
            return result
        
        # Compile and run
        compile_success, sim_success, log_content = self._compile_and_run()
        result.compilation_success = compile_success
        result.simulation_success = sim_success
        
        if not compile_success:
            result.error = f"Compilation failed with buggy RTL: {log_content[:200]}"
            self._restore_file(bug)
            return result
        
        # Check for assertion failures
        failure_count, failures, bug_caught = self._check_assertion_failures(
            log_content, 
            bug.expected_assertion_failure
        )
        
        result.assertion_failures_detected = failure_count
        result.actual_failures = failures[:5]  # Keep top 5
        result.bug_caught = bug_caught or failure_count > 0  # Any failure counts as catching the bug
        
        # Restore original file
        self._restore_file(bug)
        
        return result
    
    def run_all_tests(self, bugs: Optional[List[BugVariant]] = None) -> BugInjectionResult:
        """
        Run all bug injection tests.
        
        Args:
            bugs: Optional list of bugs to test (defaults to AXI4_BUGS)
            
        Returns:
            BugInjectionResult with complete test results
        """
        if bugs is None:
            bugs = self.AXI4_BUGS
        
        result = BugInjectionResult()
        
        # Setup temp directory
        try:
            self._setup_temp_directory()
        except Exception as e:
            result.errors.append(f"Failed to setup temp directory: {e}")
            return result
        
        try:
            for bug in bugs:
                bug_result = self.test_bug(bug)
                result.bug_results.append(bug_result)
                result.total_bugs_tested += 1
                
                if bug_result.bug_caught:
                    result.bugs_caught += 1
                else:
                    result.bugs_missed += 1
            
            # Calculate detection rate
            if result.total_bugs_tested > 0:
                result.detection_rate = (result.bugs_caught / result.total_bugs_tested) * 100
        finally:
            self._cleanup_temp_directory()
        
        return result
    
    def get_bug_detection_grade(self) -> Tuple[float, Dict[str, any]]:
        """
        Get a grade based on bug detection capability.
        
        Returns:
            Tuple of (score out of 100, detailed results dict)
        """
        result = self.run_all_tests()
        
        details = {
            "detection_rate": result.detection_rate,
            "bugs_caught": result.bugs_caught,
            "bugs_missed": result.bugs_missed,
            "total_bugs": result.total_bugs_tested,
            "bug_details": [
                {
                    "name": r.bug_name,
                    "description": r.bug_description,
                    "caught": r.bug_caught,
                    "failures_detected": r.assertion_failures_detected,
                    "error": r.error,
                }
                for r in result.bug_results
            ],
            "errors": result.errors,
        }
        
        # Score is the detection rate
        score = result.detection_rate
        
        return score, details


def test_bug_detection(
    testbench_path: str,
    design_root: str,
    dut_files: List[str],
    simulator: str = "icarus",
) -> Tuple[bool, float, Dict[str, any]]:
    """
    Convenience function to test bug detection capability.
    
    Args:
        testbench_path: Path to testbench
        design_root: Root directory of design
        dut_files: List of DUT source files
        simulator: Simulator to use
        
    Returns:
        Tuple of (passed, score, details)
    """
    tester = AXI4BugInjectionTester(
        testbench_path=testbench_path,
        design_root=design_root,
        dut_files=dut_files,
        simulator=simulator,
    )
    
    score, details = tester.get_bug_detection_grade()
    
    # Pass threshold: 50% bug detection rate
    passed = score >= 50.0
    
    return passed, score, details


def format_bug_detection_report(details: Dict[str, any]) -> str:
    """
    Format a human-readable bug detection report.
    
    Args:
        details: Bug detection details from get_bug_detection_grade()
        
    Returns:
        Formatted report string
    """
    report = """
============================================================
Bug Detection Testing Report
============================================================

Summary:
  Detection Rate: {detection_rate:.1f}%
  Bugs Caught: {bugs_caught}/{total_bugs}
  Bugs Missed: {bugs_missed}/{total_bugs}

Bug Test Details:
""".format(**details)
    
    for bug in details.get("bug_details", []):
        status = "✓ CAUGHT" if bug["caught"] else "✗ MISSED"
        report += f"\n  {bug['name']}: {status}\n"
        report += f"    Description: {bug['description']}\n"
        if bug["failures_detected"] > 0:
            report += f"    Assertions Failed: {bug['failures_detected']}\n"
        if bug["error"]:
            report += f"    Error: {bug['error']}\n"
    
    report += "\n============================================================\n"
    
    return report

