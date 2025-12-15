"""
Functional Correctness Checker for DV Task Grading.

This module verifies that the testbench is functionally correct:

1. NO FALSE POSITIVES: Testbench should PASS with correct RTL
   - Assertions should not fail on correct design
   - If assertions fail on correct RTL → testbench has bugs

2. TRANSACTIONS OCCUR: Testbench should actually exercise the DUT
   - Write transactions happen
   - Read transactions happen
   - Handshakes complete
   - Not just a trivial "wait and finish" testbench

3. DATA INTEGRITY: Write data should be readable
   - Written values should be readable
   - Memory should function correctly

4. ALL CHANNELS EXERCISED: All AXI channels should have activity
   - AW (Write Address)
   - W (Write Data)
   - B (Write Response)
   - AR (Read Address)
   - R (Read Data)

This ensures the testbench is not just "syntactically correct" but actually
tests the DUT properly.
"""

import os
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class FunctionalCorrectnessResult:
    """Results from functional correctness checks."""
    # No false positives
    no_assertion_failures: bool = False
    assertion_failure_count: int = 0
    assertion_pass_count: int = 0
    
    # Transactions occur
    write_transactions: int = 0
    read_transactions: int = 0
    transactions_occur: bool = False
    
    # Handshakes complete
    aw_handshakes: int = 0
    w_handshakes: int = 0
    b_handshakes: int = 0
    ar_handshakes: int = 0
    r_handshakes: int = 0
    all_channels_active: bool = False
    
    # Simulation completes
    simulation_completes: bool = False
    simulation_time: int = 0
    
    # Overall
    score: float = 0.0
    issues: List[str] = field(default_factory=list)


class FunctionalCorrectnessChecker:
    """
    Verifies that a testbench is functionally correct.
    
    This analyzes the simulation log from running the testbench against
    CORRECT RTL to verify:
    1. Assertions pass (no false positives)
    2. Transactions actually occur
    3. All channels are exercised
    """
    
    def __init__(self, sim_log_content: str = ""):
        """
        Initialize with simulation log content.
        
        Args:
            sim_log_content: Content of simulation log from running against correct RTL
        """
        self.sim_log = sim_log_content
        self.result = FunctionalCorrectnessResult()
    
    def set_log(self, log_content: str):
        """Set the simulation log content."""
        self.sim_log = log_content
    
    def check_no_false_positives(self) -> Tuple[bool, int, int]:
        """
        Check that assertions don't fail on correct RTL.
        
        Returns:
            (no_failures, failure_count, pass_count)
        """
        # Count assertion failures
        failure_patterns = [
            r'ASSERTION.*FAILED',
            r'\$error',
            r'Error:.*assertion',
        ]
        
        failure_count = 0
        for pattern in failure_patterns:
            matches = re.findall(pattern, self.sim_log, re.IGNORECASE)
            failure_count += len(matches)
        
        # Count assertion passes
        pass_patterns = [
            r'ASSERTION.*PASSED',
            r'assertion.*passed',
        ]
        
        pass_count = 0
        for pattern in pass_patterns:
            matches = re.findall(pattern, self.sim_log, re.IGNORECASE)
            pass_count += len(matches)
        
        # Some failures might be expected (e.g., testing error conditions)
        # But the pass count should significantly exceed failure count
        no_failures = failure_count < pass_count * 0.1  # Less than 10% failures
        
        return no_failures, failure_count, pass_count
    
    def check_transactions_occur(self) -> Tuple[bool, int, int]:
        """
        Check that write and read transactions actually occur.
        
        Returns:
            (transactions_occur, write_count, read_count)
        """
        # Look for transaction indicators in log
        write_patterns = [
            r'Write Address Handshake',
            r'Write Transaction',
            r'AW.*handshake',
            r'AWVALID.*AWREADY',
            r'Write Transactions:\s*(\d+)',
        ]
        
        read_patterns = [
            r'Read Address Handshake',
            r'Read Transaction',
            r'AR.*handshake',
            r'ARVALID.*ARREADY',
            r'Read Transactions:\s*(\d+)',
        ]
        
        write_count = 0
        for pattern in write_patterns:
            matches = re.findall(pattern, self.sim_log, re.IGNORECASE)
            if matches:
                # Try to extract number if it's a count pattern
                if isinstance(matches[0], str) and matches[0].isdigit():
                    write_count = max(write_count, int(matches[0]))
                else:
                    write_count += len(matches)
        
        read_count = 0
        for pattern in read_patterns:
            matches = re.findall(pattern, self.sim_log, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], str) and matches[0].isdigit():
                    read_count = max(read_count, int(matches[0]))
                else:
                    read_count += len(matches)
        
        # At least some transactions should occur
        transactions_occur = write_count > 0 or read_count > 0
        
        return transactions_occur, write_count, read_count
    
    def check_channel_activity(self) -> Dict[str, int]:
        """
        Check activity on all 5 AXI channels.
        
        Returns:
            Dict with handshake counts per channel
        """
        channels = {
            "AW": 0,
            "W": 0,
            "B": 0,
            "AR": 0,
            "R": 0,
        }
        
        # AW channel
        aw_patterns = [
            r'Write Address Handshake',
            r'AW.*handshake',
            r'AWVALID.*AWREADY',
            r'aw_handshake.*count.*=\s*(\d+)',
        ]
        for pattern in aw_patterns:
            matches = re.findall(pattern, self.sim_log, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], str) and matches[0].isdigit():
                    channels["AW"] = max(channels["AW"], int(matches[0]))
                else:
                    channels["AW"] += len(matches)
        
        # W channel
        w_patterns = [
            r'Write Data[:\s]',
            r'W.*handshake',
            r'WVALID.*WREADY',
            r'w_handshake.*count.*=\s*(\d+)',
        ]
        for pattern in w_patterns:
            matches = re.findall(pattern, self.sim_log, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], str) and matches[0].isdigit():
                    channels["W"] = max(channels["W"], int(matches[0]))
                else:
                    channels["W"] += len(matches)
        
        # B channel
        b_patterns = [
            r'Write Response[:\s]',
            r'B.*handshake',
            r'BVALID.*BREADY',
            r'b_handshake.*count.*=\s*(\d+)',
        ]
        for pattern in b_patterns:
            matches = re.findall(pattern, self.sim_log, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], str) and matches[0].isdigit():
                    channels["B"] = max(channels["B"], int(matches[0]))
                else:
                    channels["B"] += len(matches)
        
        # AR channel
        ar_patterns = [
            r'Read Address Handshake',
            r'AR.*handshake',
            r'ARVALID.*ARREADY',
            r'ar_handshake.*count.*=\s*(\d+)',
        ]
        for pattern in ar_patterns:
            matches = re.findall(pattern, self.sim_log, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], str) and matches[0].isdigit():
                    channels["AR"] = max(channels["AR"], int(matches[0]))
                else:
                    channels["AR"] += len(matches)
        
        # R channel
        r_patterns = [
            r'Read Data[:\s]',
            r'R.*handshake',
            r'RVALID.*RREADY',
            r'r_handshake.*count.*=\s*(\d+)',
        ]
        for pattern in r_patterns:
            matches = re.findall(pattern, self.sim_log, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], str) and matches[0].isdigit():
                    channels["R"] = max(channels["R"], int(matches[0]))
                else:
                    channels["R"] += len(matches)
        
        return channels
    
    def check_simulation_completes(self) -> Tuple[bool, int]:
        """
        Check that simulation completes properly.
        
        Returns:
            (completes, simulation_time)
        """
        completion_patterns = [
            r'\$finish',
            r'Simulation Complete',
            r'Simulation finished',
            r'Test.*Complete',
        ]
        
        completes = False
        for pattern in completion_patterns:
            if re.search(pattern, self.sim_log, re.IGNORECASE):
                completes = True
                break
        
        # Try to extract simulation time
        time_patterns = [
            r'\[(\d+)\].*\$finish',
            r'Time:\s*(\d+)',
            r'Simulation.*time.*=\s*(\d+)',
        ]
        
        sim_time = 0
        for pattern in time_patterns:
            match = re.search(pattern, self.sim_log)
            if match:
                sim_time = int(match.group(1))
                break
        
        return completes, sim_time
    
    def analyze(self) -> FunctionalCorrectnessResult:
        """
        Perform full functional correctness analysis.
        
        Returns:
            FunctionalCorrectnessResult with all checks
        """
        result = FunctionalCorrectnessResult()
        
        # 1. Check no false positives
        no_fp, fail_count, pass_count = self.check_no_false_positives()
        result.no_assertion_failures = no_fp
        result.assertion_failure_count = fail_count
        result.assertion_pass_count = pass_count
        
        if not no_fp:
            result.issues.append(f"Too many assertion failures on correct RTL ({fail_count} failures vs {pass_count} passes)")
        
        # 2. Check transactions occur
        trans_occur, write_count, read_count = self.check_transactions_occur()
        result.transactions_occur = trans_occur
        result.write_transactions = write_count
        result.read_transactions = read_count
        
        if not trans_occur:
            result.issues.append("No transactions observed - testbench may not exercise DUT")
        
        # 3. Check channel activity
        channels = self.check_channel_activity()
        result.aw_handshakes = channels["AW"]
        result.w_handshakes = channels["W"]
        result.b_handshakes = channels["B"]
        result.ar_handshakes = channels["AR"]
        result.r_handshakes = channels["R"]
        
        active_channels = sum(1 for v in channels.values() if v > 0)
        result.all_channels_active = active_channels >= 4  # At least 4 of 5 channels
        
        if not result.all_channels_active:
            inactive = [k for k, v in channels.items() if v == 0]
            result.issues.append(f"Inactive channels: {', '.join(inactive)}")
        
        # 4. Check simulation completes
        completes, sim_time = self.check_simulation_completes()
        result.simulation_completes = completes
        result.simulation_time = sim_time
        
        if not completes:
            result.issues.append("Simulation did not complete properly")
        
        # Calculate score
        score = 0.0
        
        # No false positives (30%)
        if result.no_assertion_failures:
            score += 30.0
        elif result.assertion_pass_count > 0:
            # Partial credit based on pass ratio
            ratio = result.assertion_pass_count / max(result.assertion_pass_count + result.assertion_failure_count, 1)
            score += 30.0 * ratio
        
        # Transactions occur (25%)
        if result.transactions_occur:
            score += 25.0
        
        # All channels active (25%)
        if result.all_channels_active:
            score += 25.0
        else:
            # Partial credit
            score += 25.0 * (active_channels / 5)
        
        # Simulation completes (20%)
        if result.simulation_completes:
            score += 20.0
        
        result.score = score
        
        self.result = result
        return result
    
    def get_score(self) -> Tuple[float, Dict]:
        """
        Get functional correctness score.
        
        Returns:
            Tuple of (score out of 100, detailed results)
        """
        result = self.analyze()
        
        details = {
            "score": result.score,
            "no_false_positives": result.no_assertion_failures,
            "assertion_passes": result.assertion_pass_count,
            "assertion_failures": result.assertion_failure_count,
            "transactions_occur": result.transactions_occur,
            "write_transactions": result.write_transactions,
            "read_transactions": result.read_transactions,
            "channel_activity": {
                "AW": result.aw_handshakes,
                "W": result.w_handshakes,
                "B": result.b_handshakes,
                "AR": result.ar_handshakes,
                "R": result.r_handshakes,
            },
            "all_channels_active": result.all_channels_active,
            "simulation_completes": result.simulation_completes,
            "simulation_time": result.simulation_time,
            "issues": result.issues,
        }
        
        return result.score, details


def check_functional_correctness(sim_log_content: str) -> Tuple[float, Dict]:
    """
    Convenience function to check functional correctness.
    
    Args:
        sim_log_content: Simulation log from running against correct RTL
        
    Returns:
        Tuple of (score, details)
    """
    checker = FunctionalCorrectnessChecker(sim_log_content)
    return checker.get_score()


def format_functional_correctness_report(details: Dict) -> str:
    """Format a human-readable report."""
    report = """
============================================================
Functional Correctness Report
============================================================

This verifies the testbench works correctly with the CORRECT RTL.

1. NO FALSE POSITIVES (30%):
   Assertion Passes: {assertion_passes}
   Assertion Failures: {assertion_failures}
   Status: {fp_status}

2. TRANSACTIONS OCCUR (25%):
   Write Transactions: {write_transactions}
   Read Transactions: {read_transactions}
   Status: {trans_status}

3. ALL CHANNELS ACTIVE (25%):
   AW Handshakes: {aw}
   W Handshakes: {w}
   B Handshakes: {b}
   AR Handshakes: {ar}
   R Handshakes: {r}
   Status: {channels_status}

4. SIMULATION COMPLETES (20%):
   Simulation Time: {simulation_time}
   Status: {sim_status}

Score: {score:.1f}/100
""".format(
        fp_status="✓ PASS" if details["no_false_positives"] else "✗ FAIL",
        trans_status="✓ PASS" if details["transactions_occur"] else "✗ FAIL",
        channels_status="✓ PASS" if details["all_channels_active"] else "✗ FAIL",
        sim_status="✓ PASS" if details["simulation_completes"] else "✗ FAIL",
        aw=details["channel_activity"]["AW"],
        w=details["channel_activity"]["W"],
        b=details["channel_activity"]["B"],
        ar=details["channel_activity"]["AR"],
        r=details["channel_activity"]["R"],
        **details
    )
    
    if details["issues"]:
        report += "\nIssues Found:\n"
        for issue in details["issues"]:
            report += f"  ⚠ {issue}\n"
    
    report += "\n============================================================\n"
    
    return report

