"""
Assertion Requirement Checker for DV Task Grading.

This module verifies that the agent's testbench checks the SPECIFIC assertions
required by the prompt. It does this by:
1. Running the testbench against the golden RTL
2. Parsing simulation logs for assertion messages
3. Verifying required protocol checks are present

Required Assertions (from prompt):
1. VALID Signal Stability:
   - AWVALID stable until AWREADY
   - WVALID stable until WREADY
   - ARVALID stable until ARREADY
   - BVALID stable until BREADY
   - RVALID stable until RREADY

2. LAST Signal Correctness:
   - WLAST asserted on final write beat
   - RLAST asserted on final read beat

3. Response Code Validation:
   - BRESP is valid
   - RRESP is valid

4. Timing Relationships:
   - Write response follows write data
   - Read data follows read address
"""

import os
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class RequiredAssertion:
    """Describes a required assertion from the prompt."""
    name: str
    description: str
    category: str  # valid_stability, last_signal, response_code, timing
    log_patterns: List[str]  # Patterns to search for in simulation log
    code_patterns: List[str]  # Patterns to search for in testbench code
    weight: float = 1.0  # Weight for scoring


# Define the required assertions based on the prompt
# Patterns are designed to match common testbench output formats
REQUIRED_ASSERTIONS = [
    # VALID Signal Stability
    RequiredAssertion(
        name="AWVALID_STABILITY",
        description="AWVALID must remain stable until AWREADY",
        category="valid_stability",
        log_patterns=[
            r"AWVALID.*stable",
            r"AWVALID.*until.*AWREADY",
            r"AW.*PASSED",
            r"Write Address Handshake",
        ],
        code_patterns=[
            r"awvalid.*awready",
            r"axi_awvalid.*axi_awready",
            r"awvalid_asserted",
        ],
        weight=1.0,
    ),
    RequiredAssertion(
        name="WVALID_STABILITY",
        description="WVALID must remain stable until WREADY",
        category="valid_stability",
        log_patterns=[
            r"WVALID.*stable",
            r"WVALID.*until.*WREADY",
            r"W.*PASSED.*WVALID",
            r"Write Data",
        ],
        code_patterns=[
            r"wvalid.*wready",
            r"axi_wvalid.*axi_wready",
            r"wvalid_asserted",
        ],
        weight=1.0,
    ),
    RequiredAssertion(
        name="ARVALID_STABILITY",
        description="ARVALID must remain stable until ARREADY",
        category="valid_stability",
        log_patterns=[
            r"ARVALID.*stable",
            r"ARVALID.*until.*ARREADY",
            r"AR.*PASSED",
            r"Read Address Handshake",
        ],
        code_patterns=[
            r"arvalid.*arready",
            r"axi_arvalid.*axi_arready",
            r"arvalid_asserted",
        ],
        weight=1.0,
    ),
    RequiredAssertion(
        name="BVALID_STABILITY",
        description="BVALID must remain stable until BREADY",
        category="valid_stability",
        log_patterns=[
            r"BVALID.*stable",
            r"BVALID.*until.*BREADY",
            r"B.*PASSED.*BVALID",
            r"Write Response",
        ],
        code_patterns=[
            r"bvalid.*bready",
            r"axi_bvalid.*axi_bready",
            r"bvalid_asserted",
        ],
        weight=1.0,
    ),
    RequiredAssertion(
        name="RVALID_STABILITY",
        description="RVALID must remain stable until RREADY",
        category="valid_stability",
        log_patterns=[
            r"RVALID.*stable",
            r"RVALID.*until.*RREADY",
            r"R.*PASSED.*RVALID",
            r"Read Data:",
        ],
        code_patterns=[
            r"rvalid.*rready",
            r"axi_rvalid.*axi_rready",
            r"rvalid_asserted",
        ],
        weight=1.0,
    ),
    
    # LAST Signal Correctness
    RequiredAssertion(
        name="WLAST_CHECK",
        description="WLAST must be asserted on final write data beat",
        category="last_signal",
        log_patterns=[
            r"WLAST.*correct",
            r"WLAST.*assert",
            r"WLAST.*PASSED",
            r"Write Data \(LAST\)",
        ],
        code_patterns=[
            r"wlast",
            r"axi_wlast",
            r"wlast_seen",
        ],
        weight=1.0,
    ),
    RequiredAssertion(
        name="RLAST_CHECK",
        description="RLAST must be asserted on final read data beat",
        category="last_signal",
        log_patterns=[
            r"RLAST.*correct",
            r"RLAST.*assert",
            r"RLAST.*PASSED",
            r"RLAST=1",
        ],
        code_patterns=[
            r"rlast",
            r"axi_rlast",
            r"rlast_seen",
        ],
        weight=1.0,
    ),
    
    # Response Code Validation
    RequiredAssertion(
        name="BRESP_VALID",
        description="BRESP must be valid (OKAY, EXOKAY, SLVERR, DECERR)",
        category="response_code",
        log_patterns=[
            r"BRESP.*valid",
            r"Valid BRESP",
            r"BRESP=",
            r"Write Response.*BRESP",
        ],
        code_patterns=[
            r"bresp",
            r"axi_bresp",
        ],
        weight=1.0,
    ),
    RequiredAssertion(
        name="RRESP_VALID",
        description="RRESP must be valid (OKAY, EXOKAY, SLVERR, DECERR)",
        category="response_code",
        log_patterns=[
            r"RRESP.*valid",
            r"Valid RRESP",
            r"RRESP=",
            r"Read Data.*RRESP",
        ],
        code_patterns=[
            r"rresp",
            r"axi_rresp",
        ],
        weight=1.0,
    ),
    
    # Timing Relationships
    RequiredAssertion(
        name="WRITE_RESPONSE_TIMING",
        description="Write response (BVALID) must follow write data completion (WLAST)",
        category="timing",
        log_patterns=[
            r"Write response.*after",
            r"response.*received.*after",
            r"BVALID.*after.*WLAST",
            r"write_data_complete",
        ],
        code_patterns=[
            r"wlast.*bvalid",
            r"write.*complete.*bvalid",
            r"write_data_complete_cycles",
        ],
        weight=1.0,
    ),
    RequiredAssertion(
        name="READ_DATA_TIMING",
        description="Read data (RVALID) must follow read address acceptance (ARREADY)",
        category="timing",
        log_patterns=[
            r"Read data.*after",
            r"data.*received.*after.*address",
            r"RVALID.*after.*ARREADY",
            r"read_addr_cycles",
        ],
        code_patterns=[
            r"arready.*rvalid",
            r"read.*addr.*rvalid",
            r"read_addr_cycles",
        ],
        weight=1.0,
    ),
]


class AssertionRequirementChecker:
    """
    Verifies that a testbench implements the required assertions.
    
    This checker:
    1. Analyzes testbench code for assertion patterns
    2. Runs simulation and parses logs for assertion execution
    3. Scores based on which required assertions are verified
    """
    
    def __init__(self, testbench_path: str, sim_log_path: Optional[str] = None):
        """
        Initialize the checker.
        
        Args:
            testbench_path: Path to the testbench file
            sim_log_path: Optional path to simulation log (if already run)
        """
        self.testbench_path = testbench_path
        self.sim_log_path = sim_log_path
        self.testbench_content = ""
        self.sim_log_content = ""
        self.results: Dict[str, Dict] = {}
        
        # Load testbench content
        if os.path.exists(testbench_path):
            with open(testbench_path, 'r') as f:
                self.testbench_content = f.read().lower()
        
        # Load simulation log if provided
        if sim_log_path and os.path.exists(sim_log_path):
            with open(sim_log_path, 'r') as f:
                self.sim_log_content = f.read()
    
    def set_simulation_log(self, log_content: str):
        """Set simulation log content directly."""
        self.sim_log_content = log_content
    
    def load_simulation_log(self, log_path: str):
        """Load simulation log from file."""
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                self.sim_log_content = f.read()
    
    def check_code_patterns(self, assertion: RequiredAssertion) -> bool:
        """Check if assertion patterns exist in testbench code."""
        if not self.testbench_content:
            return False
        
        for pattern in assertion.code_patterns:
            if re.search(pattern, self.testbench_content, re.IGNORECASE):
                return True
        return False
    
    def check_log_patterns(self, assertion: RequiredAssertion) -> Tuple[bool, int]:
        """
        Check if assertion messages appear in simulation log.
        
        Returns:
            Tuple of (found, count) - whether pattern found and how many times
        """
        if not self.sim_log_content:
            return False, 0
        
        total_count = 0
        found = False
        
        for pattern in assertion.log_patterns:
            matches = re.findall(pattern, self.sim_log_content, re.IGNORECASE)
            if matches:
                found = True
                total_count += len(matches)
        
        return found, total_count
    
    def check_assertion(self, assertion: RequiredAssertion) -> Dict:
        """
        Check if a specific required assertion is implemented.
        
        Returns:
            Dict with check results
        """
        code_present = self.check_code_patterns(assertion)
        log_found, log_count = self.check_log_patterns(assertion)
        
        # An assertion is considered verified if:
        # 1. Patterns appear in the simulation log, OR
        # 2. Code patterns exist AND any assertion activity in log (backup check)
        verified = log_found and log_count > 0
        
        # Backup: if code is present and we see general assertion activity
        if not verified and code_present:
            # Check for general assertion activity
            if self.sim_log_content:
                has_assertion_activity = bool(re.search(
                    r'ASSERTION.*PASSED|ASSERTION.*FAILED', 
                    self.sim_log_content, 
                    re.IGNORECASE
                ))
                # Give partial credit if code exists and assertions are running
                if has_assertion_activity:
                    verified = True
                    log_count = 1  # Minimum credit
        
        return {
            "name": assertion.name,
            "description": assertion.description,
            "category": assertion.category,
            "code_present": code_present,
            "log_found": log_found,
            "log_count": log_count,
            "verified": verified,
            "weight": assertion.weight,
        }
    
    def check_all_assertions(self) -> Dict[str, Dict]:
        """
        Check all required assertions.
        
        Returns:
            Dict mapping assertion names to their check results
        """
        self.results = {}
        
        for assertion in REQUIRED_ASSERTIONS:
            self.results[assertion.name] = self.check_assertion(assertion)
        
        return self.results
    
    def get_score(self) -> Tuple[float, Dict]:
        """
        Calculate score based on verified assertions.
        
        Returns:
            Tuple of (score out of 100, detailed results)
        """
        if not self.results:
            self.check_all_assertions()
        
        total_weight = sum(a.weight for a in REQUIRED_ASSERTIONS)
        verified_weight = sum(
            self.results[a.name]["weight"]
            for a in REQUIRED_ASSERTIONS
            if self.results[a.name]["verified"]
        )
        
        score = (verified_weight / total_weight) * 100 if total_weight > 0 else 0
        
        # Group by category
        by_category = {}
        for assertion in REQUIRED_ASSERTIONS:
            cat = assertion.category
            if cat not in by_category:
                by_category[cat] = {"total": 0, "verified": 0, "assertions": []}
            by_category[cat]["total"] += 1
            if self.results[assertion.name]["verified"]:
                by_category[cat]["verified"] += 1
            by_category[cat]["assertions"].append(self.results[assertion.name])
        
        details = {
            "score": score,
            "total_assertions": len(REQUIRED_ASSERTIONS),
            "verified_assertions": sum(1 for r in self.results.values() if r["verified"]),
            "by_category": by_category,
            "all_results": self.results,
        }
        
        return score, details


def check_required_assertions(
    testbench_path: str,
    sim_log_path: Optional[str] = None,
    sim_log_content: Optional[str] = None,
) -> Tuple[float, Dict]:
    """
    Convenience function to check required assertions.
    
    Args:
        testbench_path: Path to testbench
        sim_log_path: Optional path to simulation log file
        sim_log_content: Optional simulation log content directly
        
    Returns:
        Tuple of (score, details)
    """
    checker = AssertionRequirementChecker(testbench_path, sim_log_path)
    
    if sim_log_content:
        checker.set_simulation_log(sim_log_content)
    
    return checker.get_score()


def format_assertion_requirement_report(details: Dict) -> str:
    """
    Format a human-readable report.
    
    Args:
        details: Details from get_score()
        
    Returns:
        Formatted report string
    """
    report = """
============================================================
Required Assertion Verification Report
============================================================

Summary:
  Verified: {verified_assertions}/{total_assertions} assertions
  Score: {score:.1f}%

""".format(**details)
    
    # Report by category
    category_names = {
        "valid_stability": "VALID Signal Stability",
        "last_signal": "LAST Signal Correctness",
        "response_code": "Response Code Validation",
        "timing": "Timing Relationships",
    }
    
    for cat_key, cat_name in category_names.items():
        if cat_key in details["by_category"]:
            cat = details["by_category"][cat_key]
            report += f"{cat_name} ({cat['verified']}/{cat['total']}):\n"
            for assertion in cat["assertions"]:
                status = "✓" if assertion["verified"] else "✗"
                log_info = f"(log: {assertion['log_count']})" if assertion["log_found"] else ""
                report += f"  {status} {assertion['description']} {log_info}\n"
            report += "\n"
    
    report += "============================================================\n"
    
    return report

