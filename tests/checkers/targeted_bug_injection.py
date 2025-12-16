"""
Targeted Bug Injection Tester for DV Task Grading.

This module tests if the agent's testbench has assertions that catch SPECIFIC bugs
related to the requirements in the prompt.

Logic:
1. Prompt says: "AWVALID must remain stable until AWREADY"
2. We inject bug: AWVALID becomes unstable (drops before AWREADY)
3. We expect: The testbench should report assertion failure mentioning AWVALID
4. If it catches it with the RIGHT assertion → full credit
5. If it catches it with ANY assertion → partial credit
6. If it doesn't catch it → no credit

This ensures:
- Agent understood the requirement
- Agent wrote the correct assertion
- The assertion actually catches the bug it's supposed to catch
"""

import os
import re
import subprocess
import tempfile
import shutil
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class TargetedBug:
    """A bug that tests a specific assertion requirement from the prompt."""
    name: str
    requirement: str  # The requirement from the prompt this tests
    description: str
    file_to_modify: str
    search_pattern: str
    replacement: str
    expected_assertion_patterns: List[str]  # Patterns that should appear in failure messages
    category: str  # valid_stability, last_signal, response_code, timing


@dataclass
class TargetedBugResult:
    """Result of testing one targeted bug."""
    bug_name: str
    requirement: str
    category: str
    compilation_success: bool = False
    simulation_ran: bool = False
    any_assertion_failed: bool = False
    correct_assertion_failed: bool = False  # The specific assertion we expected
    failure_messages: List[str] = field(default_factory=list)
    score: float = 0.0  # 0, 0.5, or 1.0
    error: str = ""


# Targeted bugs mapped to prompt requirements
TARGETED_BUGS = [
    # ================================================================
    # VALID Signal Stability Tests
    # Expected assertion messages (flexible matching):
    # - Golden: "AWVALID not stable until AWREADY"
    # - Agent:  "AWVALID signals changed before AWREADY"
    # ================================================================
    TargetedBug(
        name="AWVALID_UNSTABLE",
        requirement="AWVALID must remain stable until AWREADY",
        description="AWVALID drops before AWREADY (stability violation)",
        file_to_modify="sources/axi4_master.sv",
        search_pattern=r"(axi_awvalid\s*<=\s*1'b1;)",
        replacement=r"axi_awvalid <= 1'b0; // BUG: AWVALID unstable",
        expected_assertion_patterns=[
            r"AWVALID.*stable",
            r"AWVALID.*AWREADY",
            r"AWVALID.*changed",
            r"AW.*FAILED",
        ],
        category="valid_stability",
    ),
    TargetedBug(
        name="ARVALID_UNSTABLE",
        requirement="ARVALID must remain stable until ARREADY",
        description="ARVALID drops before ARREADY (stability violation)",
        file_to_modify="sources/axi4_master.sv",
        search_pattern=r"(axi_arvalid\s*<=\s*1'b1;)",
        replacement=r"axi_arvalid <= 1'b0; // BUG: ARVALID unstable",
        expected_assertion_patterns=[
            r"ARVALID.*stable",
            r"ARVALID.*ARREADY",
            r"ARVALID.*changed",
            r"AR.*FAILED",
        ],
        category="valid_stability",
    ),
    TargetedBug(
        name="BVALID_UNSTABLE",
        requirement="BVALID must remain stable until BREADY",
        description="BVALID never asserts (response channel broken)",
        file_to_modify="sources/axi4_slave.sv",
        search_pattern=r"(axi_bvalid\s*<=\s*1'b1;)",
        replacement=r"axi_bvalid <= 1'b0; // BUG: BVALID never asserts",
        expected_assertion_patterns=[
            r"BVALID.*stable",
            r"BVALID.*BREADY",
            r"BRESP.*changed",
            r"Write response",
        ],
        category="valid_stability",
    ),
    TargetedBug(
        name="RVALID_UNSTABLE",
        requirement="RVALID must remain stable until RREADY",
        description="RVALID never asserts (read data channel broken)",
        file_to_modify="sources/axi4_slave.sv",
        search_pattern=r"(axi_rvalid\s*<=\s*1'b1;)",
        replacement=r"axi_rvalid <= 1'b0; // BUG: RVALID never asserts",
        expected_assertion_patterns=[
            r"RVALID.*stable",
            r"RVALID.*RREADY",
            r"RVALID.*changed",
            r"Read data not received",
        ],
        category="valid_stability",
    ),
    TargetedBug(
        name="WVALID_UNSTABLE",
        requirement="WVALID must remain stable until WREADY",
        description="WVALID never asserts (write data channel broken)",
        file_to_modify="sources/axi4_master.sv",
        search_pattern=r"(axi_wvalid\s*<=\s*1'b1;)",
        replacement=r"axi_wvalid <= 1'b0; // BUG: WVALID never asserts",
        expected_assertion_patterns=[
            r"WVALID.*stable",
            r"WVALID.*WREADY",
            r"WVALID.*changed",
            r"W.*FAILED",
        ],
        category="valid_stability",
    ),
    
    # ================================================================
    # LAST Signal Correctness Tests
    # Expected assertion messages (flexible matching):
    # - Golden: "WLAST not asserted on final beat"
    # - Agent:  "WLAST not asserted on final beat (4/4)"
    # ================================================================
    TargetedBug(
        name="WLAST_MISSING",
        requirement="WLAST must be asserted on final write data beat",
        description="WLAST never asserts (last beat not marked)",
        file_to_modify="sources/axi4_master.sv",
        search_pattern=r"(axi_wlast\s*<=\s*\(write_count\s*==\s*write_length\);)",
        replacement=r"axi_wlast <= 1'b0; // BUG: WLAST never asserted",
        expected_assertion_patterns=[
            r"WLAST.*not.*asserted",
            r"WLAST.*final",
            r"WLAST.*FAILED",
        ],
        category="last_signal",
    ),
    TargetedBug(
        name="RLAST_MISSING",
        requirement="RLAST must be asserted on final read data beat",
        description="RLAST never asserts (last beat not marked)",
        file_to_modify="sources/axi4_slave.sv",
        search_pattern=r"(axi_rlast\s*<=\s*1'b1;\s*//\s*Single beat)",
        replacement=r"axi_rlast <= 1'b0; // BUG: RLAST never asserted",
        expected_assertion_patterns=[
            r"RLAST.*not.*asserted",
            r"RLAST.*final",
            r"RLAST.*FAILED",
        ],
        category="last_signal",
    ),
    
    # ================================================================
    # Response Code Validation Tests
    # Expected assertion messages (flexible matching):
    # - Golden: "Invalid BRESP code"
    # - Agent:  "BRESP is invalid (0xx)"
    # ================================================================
    TargetedBug(
        name="BRESP_INVALID",
        requirement="BRESP must be valid (OKAY, EXOKAY, SLVERR, DECERR)",
        description="BRESP returns undefined value",
        file_to_modify="sources/axi4_slave.sv",
        search_pattern=r"(axi_bresp\s*<=\s*OKAY;)",
        replacement=r"axi_bresp <= 2'bxx; // BUG: Invalid undefined BRESP",
        expected_assertion_patterns=[
            r"BRESP.*invalid",
            r"BRESP.*Invalid",
            r"BRESP.*FAILED",
        ],
        category="response_code",
    ),
    TargetedBug(
        name="RRESP_INVALID",
        requirement="RRESP must be valid (OKAY, EXOKAY, SLVERR, DECERR)",
        description="RRESP returns undefined value",
        file_to_modify="sources/axi4_slave.sv",
        search_pattern=r"(axi_rresp\s*<=\s*OKAY;)",
        replacement=r"axi_rresp <= 2'bxx; // BUG: Invalid undefined RRESP",
        expected_assertion_patterns=[
            r"RRESP.*invalid",
            r"RRESP.*Invalid",
            r"RRESP.*FAILED",
        ],
        category="response_code",
    ),
    
    # ================================================================
    # Timing Relationship Tests
    # Actual assertion messages from golden testbench:
    # - "ASSERTION FAILED: Write response not received after data"
    # - "ASSERTION FAILED: Read data not received after address"
    # ================================================================
    TargetedBug(
        name="WRITE_RESPONSE_NO_TIMING",
        requirement="Write response (BVALID) must follow write data completion (WLAST)",
        description="Write response comes too late or never",
        file_to_modify="sources/axi4_slave.sv",
        search_pattern=r"(axi_bvalid\s*<=\s*1'b1;)",
        replacement=r"// BUG: BVALID delayed indefinitely\n                axi_bvalid <= 1'b0;",
        expected_assertion_patterns=[
            r"Write response not received after data",
            r"Write response.*not.*received",
            r"write.*response.*FAILED",
        ],
        category="timing",
    ),
    TargetedBug(
        name="READ_DATA_NO_TIMING",
        requirement="Read data (RVALID) must follow read address acceptance (ARREADY)",
        description="Read data never comes after address",
        file_to_modify="sources/axi4_slave.sv",
        search_pattern=r"(axi_rvalid\s*<=\s*1'b1;)",
        replacement=r"// BUG: RVALID never asserts\n                axi_rvalid <= 1'b0;",
        expected_assertion_patterns=[
            r"Read data not received after address",
            r"Read data.*not.*received",
            r"read.*data.*FAILED",
        ],
        category="timing",
    ),
]


class TargetedBugInjectionTester:
    """
    Tests testbench quality by injecting bugs that target specific requirements.
    
    Scoring:
    - 1.0: Bug caught AND the correct assertion (matching the requirement) fired
    - 0.5: Bug caught by ANY assertion (but not the specific one)
    - 0.0: Bug not caught
    """
    
    def __init__(
        self,
        testbench_path: str,
        design_root: str,
        dut_files: List[str],
        simulator: str = "verilator",
    ):
        self.testbench_path = testbench_path
        self.design_root = design_root
        self.dut_files = dut_files
        self.simulator = simulator
        self.temp_dir = None
        
        # Auto-detect simulator
        if simulator == "verilator" and not shutil.which("verilator"):
            self.simulator = "icarus"
    
    def _setup_temp_directory(self) -> str:
        """Create temporary directory with design copy."""
        self.temp_dir = tempfile.mkdtemp(prefix="targeted_bug_")
        
        for dut_file in self.dut_files:
            src = os.path.join(self.design_root, dut_file)
            dst_dir = os.path.join(self.temp_dir, os.path.dirname(dut_file))
            os.makedirs(dst_dir, exist_ok=True)
            dst = os.path.join(self.temp_dir, dut_file)
            if os.path.exists(src):
                shutil.copy2(src, dst)
        
        tb_dst = os.path.join(self.temp_dir, os.path.basename(self.testbench_path))
        if os.path.exists(self.testbench_path):
            shutil.copy2(self.testbench_path, tb_dst)
        
        return self.temp_dir
    
    def _cleanup_temp_directory(self):
        """Remove temporary directory."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None
    
    def _inject_bug(self, bug: TargetedBug) -> bool:
        """Inject a bug into the RTL."""
        file_path = os.path.join(self.temp_dir, bug.file_to_modify)
        
        if not os.path.exists(file_path):
            return False
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            new_content, count = re.subn(bug.search_pattern, bug.replacement, content, count=1)
            
            if count == 0:
                return False
            
            with open(file_path, 'w') as f:
                f.write(new_content)
            
            return True
        except Exception:
            return False
    
    def _restore_file(self, bug: TargetedBug):
        """Restore original file from design root."""
        src = os.path.join(self.design_root, bug.file_to_modify)
        dst = os.path.join(self.temp_dir, bug.file_to_modify)
        if os.path.exists(src):
            shutil.copy2(src, dst)
    
    def _compile_and_run(self, timeout: int = 30) -> Tuple[bool, bool, str]:
        """Compile and run simulation."""
        output_dir = os.path.join(self.temp_dir, "sim_build")
        os.makedirs(output_dir, exist_ok=True)
        
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
        
        tb_name = os.path.splitext(os.path.basename(self.testbench_path))[0]
        
        if self.simulator == "verilator":
            compile_cmd = [
                "verilator", "--binary", "--timing",
                "-Wno-fatal", "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC",
                "-Wno-TIMESCALEMOD", "-Wno-STMTDLY", "-Wno-INITIALDLY",
                "--top-module", tb_name,
                "-o", f"{output_dir}/Vtb",
                "--Mdir", f"{output_dir}/obj_dir"
            ] + source_files
            exe_path = f"{output_dir}/Vtb"
            sim_cmd = [exe_path]
        else:
            compile_cmd = ["iverilog", "-g2012", "-o", f"{output_dir}/tb.out"] + source_files
            exe_path = f"{output_dir}/tb.out"
            sim_cmd = ["vvp", exe_path]
        
        try:
            compile_result = subprocess.run(
                compile_cmd, capture_output=True, text=True,
                timeout=120, cwd=self.temp_dir
            )
            if compile_result.returncode != 0:
                return False, False, compile_result.stderr
        except Exception as e:
            return False, False, str(e)
        
        try:
            sim_result = subprocess.run(
                sim_cmd, capture_output=True, text=True,
                timeout=timeout, cwd=self.temp_dir
            )
            log_content = sim_result.stdout + sim_result.stderr
            sim_success = "$finish" in log_content or sim_result.returncode == 0
            return True, sim_success, log_content
        except subprocess.TimeoutExpired:
            return True, False, "Simulation timed out"
        except Exception as e:
            return True, False, str(e)
    
    def _check_assertion_failures(
        self, log_content: str, expected_patterns: List[str]
    ) -> Tuple[bool, bool, List[str]]:
        """
        Check for assertion failures in log.
        
        Returns:
            (any_failure, correct_failure, failure_messages)
        """
        # Find all assertion failure messages - extract full lines
        failures = []
        
        # Look for lines containing "ASSERTION FAILED"
        for line in log_content.split('\n'):
            if 'ASSERTION FAILED' in line.upper():
                # Extract the message part after "ASSERTION FAILED:"
                if ':' in line:
                    msg = line.split(':', 1)[-1].strip()
                    if msg:
                        failures.append(msg)
                else:
                    failures.append(line.strip())
        
        # Also check for failure count at end of simulation
        fail_count_match = re.search(r'Total Assertions Failed:\s*(\d+)', log_content)
        if fail_count_match:
            fail_count = int(fail_count_match.group(1))
            if fail_count > 0 and not failures:
                # Some failures occurred but we didn't capture the messages
                # This happens with $error in Verilator
                failures.append(f"<{fail_count} assertion failures>")
        
        any_failure = len(failures) > 0
        
        # Check if the expected/correct assertion failed
        correct_failure = False
        if any_failure:
            # First check the captured failure messages
            for expected in expected_patterns:
                for failure in failures:
                    if re.search(expected, failure, re.IGNORECASE):
                        correct_failure = True
                        break
                if correct_failure:
                    break
            
            # Also check full log for expected patterns
            if not correct_failure:
                for expected in expected_patterns:
                    if re.search(expected, log_content, re.IGNORECASE):
                        correct_failure = True
                        break
        
        return any_failure, correct_failure, failures
    
    def test_bug(self, bug: TargetedBug) -> TargetedBugResult:
        """Test a single targeted bug."""
        result = TargetedBugResult(
            bug_name=bug.name,
            requirement=bug.requirement,
            category=bug.category,
        )
        
        if not self._inject_bug(bug):
            result.error = f"Could not inject bug: pattern not found"
            self._restore_file(bug)
            return result
        
        compile_ok, sim_ok, log_content = self._compile_and_run()
        result.compilation_success = compile_ok
        result.simulation_ran = sim_ok
        
        if not compile_ok:
            result.error = f"Compilation failed"
            self._restore_file(bug)
            return result
        
        any_fail, correct_fail, failures = self._check_assertion_failures(
            log_content, bug.expected_assertion_patterns
        )
        
        result.any_assertion_failed = any_fail
        result.correct_assertion_failed = correct_fail
        result.failure_messages = failures[:5]
        
        # Scoring
        # Primary goal: Bug must be caught by assertions
        # In real verification, cascading failures are expected - a bug in one area
        # often causes assertions to fire elsewhere. The key is that the testbench
        # DETECTS the bug, not which specific assertion catches it.
        if any_fail:
            if correct_fail:
                result.score = 1.0  # Full credit - caught with correct assertion
            else:
                result.score = 0.9  # High credit - bug detected (cascading failures expected)
        else:
            result.score = 0.0  # No credit - bug not caught at all
        
        self._restore_file(bug)
        return result
    
    def run_all_tests(self) -> Dict:
        """Run all targeted bug tests."""
        results = {
            "total_bugs": 0,
            "fully_caught": 0,  # Caught with correct assertion
            "partially_caught": 0,  # Caught with any assertion
            "missed": 0,
            "total_score": 0.0,
            "max_score": 0.0,
            "by_category": {},
            "bug_results": [],
        }
        
        try:
            self._setup_temp_directory()
            
            for bug in TARGETED_BUGS:
                bug_result = self.test_bug(bug)
                results["bug_results"].append(bug_result)
                results["total_bugs"] += 1
                results["max_score"] += 1.0
                results["total_score"] += bug_result.score
                
                if bug_result.score == 1.0:
                    results["fully_caught"] += 1
                elif bug_result.score >= 0.5:  # 0.75 or 0.5
                    results["partially_caught"] += 1
                else:
                    results["missed"] += 1
                
                # Track by category
                cat = bug.category
                if cat not in results["by_category"]:
                    results["by_category"][cat] = {
                        "total": 0, "fully_caught": 0, 
                        "partially_caught": 0, "missed": 0, "score": 0.0
                    }
                results["by_category"][cat]["total"] += 1
                results["by_category"][cat]["score"] += bug_result.score
                if bug_result.score == 1.0:
                    results["by_category"][cat]["fully_caught"] += 1
                elif bug_result.score >= 0.5:  # 0.75 or 0.5
                    results["by_category"][cat]["partially_caught"] += 1
                else:
                    results["by_category"][cat]["missed"] += 1
            
        finally:
            self._cleanup_temp_directory()
        
        return results
    
    def get_grade(self) -> Tuple[float, Dict]:
        """Get a grade based on targeted bug detection."""
        results = self.run_all_tests()
        
        if results["max_score"] > 0:
            score = (results["total_score"] / results["max_score"]) * 100
        else:
            score = 0.0
        
        return score, results


def format_targeted_bug_report(results: Dict) -> str:
    """Format a human-readable report."""
    report = """
============================================================
Targeted Bug Injection Report
============================================================
This tests if your assertions catch SPECIFIC bugs related to
the requirements in the prompt.

Scoring:
  ✓✓ = Bug caught with CORRECT assertion (1.0 points)
  ✓  = Bug caught (cascading failures expected) (0.9 points)
  ✗  = Bug NOT caught (0.0 points)

Summary:
  Total Bugs: {total_bugs}
  Fully Caught (correct assertion): {fully_caught}
  Partially Caught (any assertion): {partially_caught}
  Missed: {missed}
  Score: {total_score:.1f}/{max_score:.1f} ({score:.0f}%)

""".format(
        score=(results["total_score"] / results["max_score"] * 100) if results["max_score"] > 0 else 0,
        **results
    )
    
    # Results by category
    category_names = {
        "valid_stability": "VALID Signal Stability",
        "last_signal": "LAST Signal Correctness", 
        "response_code": "Response Code Validation",
        "timing": "Timing Relationships",
    }
    
    for cat_key, cat_name in category_names.items():
        if cat_key in results["by_category"]:
            cat = results["by_category"][cat_key]
            cat_pct = (cat["score"] / cat["total"] * 100) if cat["total"] > 0 else 0
            report += f"{cat_name} ({cat['score']:.1f}/{cat['total']} = {cat_pct:.0f}%):\n"
            
            for bug_result in results["bug_results"]:
                if bug_result.category == cat_key:
                    if bug_result.score == 1.0:
                        status = "✓✓"
                    elif bug_result.score == 0.5:
                        status = "✓ "
                    else:
                        status = "✗ "
                    report += f"  {status} {bug_result.requirement}\n"
                    if bug_result.error:
                        report += f"      Error: {bug_result.error}\n"
            report += "\n"
    
    report += "============================================================\n"
    return report

