"""
AXI4 Protocol Coverage Checker for DV Task Grading.

This module analyzes testbenches to determine:
1. Which AXI4 channels are covered (AW, W, B, AR, R)
2. Which protocol rules are checked (handshakes, responses, etc.)
3. Coverage completeness score

AXI4 Protocol Reference:
- Write Address Channel (AW): AWVALID, AWREADY, AWADDR, AWLEN, AWSIZE, AWBURST
- Write Data Channel (W): WVALID, WREADY, WDATA, WSTRB, WLAST
- Write Response Channel (B): BVALID, BREADY, BRESP
- Read Address Channel (AR): ARVALID, ARREADY, ARADDR, ARLEN, ARSIZE, ARBURST
- Read Data Channel (R): RVALID, RREADY, RDATA, RRESP, RLAST
"""

import os
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class ProtocolCheck:
    """Represents a specific protocol check."""
    name: str
    description: str
    pattern: str  # Regex pattern to detect this check
    channel: str  # AW, W, B, AR, R
    weight: float = 1.0  # Importance weight for scoring
    required: bool = False  # If True, must be present to pass


@dataclass
class ChannelCoverage:
    """Coverage information for a single AXI4 channel."""
    name: str
    signals_monitored: List[str] = field(default_factory=list)
    checks_found: List[str] = field(default_factory=list)
    coverage_score: float = 0.0


@dataclass
class ProtocolCoverageResult:
    """Complete protocol coverage analysis result."""
    channels: Dict[str, ChannelCoverage] = field(default_factory=dict)
    total_checks_possible: int = 0
    total_checks_found: int = 0
    required_checks_found: int = 0
    required_checks_total: int = 0
    coverage_score: float = 0.0
    missing_checks: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class AXI4ProtocolCoverageChecker:
    """
    Checks AXI4 protocol coverage in SystemVerilog testbenches.
    
    Analyzes testbench code to determine:
    1. Which AXI4 signals are monitored
    2. Which protocol rules are checked via assertions
    3. Coverage completeness score
    """
    
    # AXI4 signal patterns for each channel
    AXI4_SIGNALS = {
        "AW": ["awvalid", "awready", "awaddr", "awlen", "awsize", "awburst", "awid", "awlock", "awcache", "awprot"],
        "W": ["wvalid", "wready", "wdata", "wstrb", "wlast"],
        "B": ["bvalid", "bready", "bresp", "bid"],
        "AR": ["arvalid", "arready", "araddr", "arlen", "arsize", "arburst", "arid", "arlock", "arcache", "arprot"],
        "R": ["rvalid", "rready", "rdata", "rresp", "rlast", "rid"],
    }
    
    # Protocol checks to look for (with patterns and weights)
    PROTOCOL_CHECKS = [
        # Write Address Channel
        ProtocolCheck(
            name="AW_VALID_STABLE",
            description="AWVALID must remain stable until AWREADY",
            pattern=r"(awvalid.*awready|awvalid.*stable|awvalid.*!.*awready)",
            channel="AW",
            weight=2.0,
            required=True,
        ),
        ProtocolCheck(
            name="AW_HANDSHAKE",
            description="Write address handshake (AWVALID && AWREADY)",
            pattern=r"awvalid\s*&&\s*awready|awvalid\s*&\s*awready|awready\s*&&\s*awvalid",
            channel="AW",
            weight=1.5,
            required=True,
        ),
        
        # Write Data Channel
        ProtocolCheck(
            name="W_VALID_STABLE",
            description="WVALID must remain stable until WREADY",
            pattern=r"(wvalid.*wready|wvalid.*stable)",
            channel="W",
            weight=2.0,
            required=True,
        ),
        ProtocolCheck(
            name="W_LAST_CHECK",
            description="WLAST must be asserted on last beat",
            pattern=r"wlast",
            channel="W",
            weight=2.0,
            required=True,
        ),
        ProtocolCheck(
            name="W_HANDSHAKE",
            description="Write data handshake (WVALID && WREADY)",
            pattern=r"wvalid\s*&&\s*wready|wvalid\s*&\s*wready|wready\s*&&\s*wvalid",
            channel="W",
            weight=1.5,
            required=False,
        ),
        
        # Write Response Channel
        ProtocolCheck(
            name="B_VALID_STABLE",
            description="BVALID must remain stable until BREADY",
            pattern=r"(bvalid.*bready|bvalid.*stable)",
            channel="B",
            weight=2.0,
            required=True,
        ),
        ProtocolCheck(
            name="B_RESP_CHECK",
            description="BRESP must be valid (OKAY, EXOKAY, SLVERR, DECERR)",
            pattern=r"bresp\s*(==|!=|<=|>=|<|>)\s*(2'b|2'd|\d)",
            channel="B",
            weight=2.0,
            required=True,
        ),
        ProtocolCheck(
            name="B_HANDSHAKE",
            description="Write response handshake (BVALID && BREADY)",
            pattern=r"bvalid\s*&&\s*bready|bvalid\s*&\s*bready|bready\s*&&\s*bvalid",
            channel="B",
            weight=1.5,
            required=False,
        ),
        
        # Read Address Channel
        ProtocolCheck(
            name="AR_VALID_STABLE",
            description="ARVALID must remain stable until ARREADY",
            pattern=r"(arvalid.*arready|arvalid.*stable|arvalid.*!.*arready)",
            channel="AR",
            weight=2.0,
            required=True,
        ),
        ProtocolCheck(
            name="AR_HANDSHAKE",
            description="Read address handshake (ARVALID && ARREADY)",
            pattern=r"arvalid\s*&&\s*arready|arvalid\s*&\s*arready|arready\s*&&\s*arvalid",
            channel="AR",
            weight=1.5,
            required=False,
        ),
        
        # Read Data Channel
        ProtocolCheck(
            name="R_VALID_STABLE",
            description="RVALID must remain stable until RREADY",
            pattern=r"(rvalid.*rready|rvalid.*stable)",
            channel="R",
            weight=2.0,
            required=True,
        ),
        ProtocolCheck(
            name="R_LAST_CHECK",
            description="RLAST must be asserted on last beat",
            pattern=r"rlast",
            channel="R",
            weight=2.0,
            required=True,
        ),
        ProtocolCheck(
            name="R_RESP_CHECK",
            description="RRESP must be valid",
            pattern=r"rresp\s*(==|!=|<=|>=|<|>)\s*(2'b|2'd|\d)",
            channel="R",
            weight=1.5,
            required=False,
        ),
        ProtocolCheck(
            name="R_HANDSHAKE",
            description="Read data handshake (RVALID && RREADY)",
            pattern=r"rvalid\s*&&\s*rready|rvalid\s*&\s*rready|rready\s*&&\s*rvalid",
            channel="R",
            weight=1.5,
            required=False,
        ),
    ]
    
    def __init__(self, testbench_path: str):
        """
        Initialize the protocol coverage checker.
        
        Args:
            testbench_path: Path to the testbench file
        """
        self.testbench_path = testbench_path
        self.content = ""
        self.content_lower = ""
        
    def load_testbench(self) -> bool:
        """Load the testbench content."""
        if not os.path.exists(self.testbench_path):
            return False
        
        try:
            with open(self.testbench_path, 'r') as f:
                self.content = f.read()
                self.content_lower = self.content.lower()
            return True
        except Exception:
            return False
    
    def check_signal_monitoring(self) -> Dict[str, List[str]]:
        """
        Check which AXI4 signals are being monitored in the testbench.
        
        Returns:
            Dictionary mapping channel names to lists of monitored signals
        """
        monitored = {}
        
        for channel, signals in self.AXI4_SIGNALS.items():
            monitored[channel] = []
            for signal in signals:
                # Check if signal appears in the testbench (case-insensitive)
                # Look for patterns like: dut.axi_awvalid, awvalid, axi_awvalid
                patterns = [
                    rf'\b{signal}\b',
                    rf'\baxi_{signal}\b',
                    rf'\.{signal}\b',
                ]
                for pattern in patterns:
                    if re.search(pattern, self.content_lower):
                        if signal not in monitored[channel]:
                            monitored[channel].append(signal)
                        break
        
        return monitored
    
    def check_protocol_rules(self) -> Dict[str, List[ProtocolCheck]]:
        """
        Check which protocol rules are being verified.
        
        Returns:
            Dictionary mapping channel names to lists of found protocol checks
        """
        found_checks = {channel: [] for channel in self.AXI4_SIGNALS.keys()}
        
        for check in self.PROTOCOL_CHECKS:
            if re.search(check.pattern, self.content_lower):
                found_checks[check.channel].append(check)
        
        return found_checks
    
    def analyze_coverage(self) -> ProtocolCoverageResult:
        """
        Perform complete protocol coverage analysis.
        
        Returns:
            ProtocolCoverageResult with detailed coverage information
        """
        result = ProtocolCoverageResult()
        
        # Load testbench
        if not self.load_testbench():
            result.errors.append(f"Could not load testbench: {self.testbench_path}")
            return result
        
        # Check signal monitoring
        monitored_signals = self.check_signal_monitoring()
        
        # Check protocol rules
        found_checks = self.check_protocol_rules()
        
        # Calculate coverage for each channel
        total_weight = sum(check.weight for check in self.PROTOCOL_CHECKS)
        found_weight = 0.0
        
        for channel in self.AXI4_SIGNALS.keys():
            channel_coverage = ChannelCoverage(name=channel)
            channel_coverage.signals_monitored = monitored_signals.get(channel, [])
            channel_coverage.checks_found = [c.name for c in found_checks.get(channel, [])]
            
            # Calculate channel-specific coverage
            channel_checks = [c for c in self.PROTOCOL_CHECKS if c.channel == channel]
            channel_weight = sum(c.weight for c in channel_checks)
            channel_found_weight = sum(c.weight for c in found_checks.get(channel, []))
            
            if channel_weight > 0:
                channel_coverage.coverage_score = (channel_found_weight / channel_weight) * 100
            
            result.channels[channel] = channel_coverage
            found_weight += channel_found_weight
        
        # Calculate totals
        result.total_checks_possible = len(self.PROTOCOL_CHECKS)
        result.total_checks_found = sum(len(checks) for checks in found_checks.values())
        
        # Check required checks
        required_checks = [c for c in self.PROTOCOL_CHECKS if c.required]
        result.required_checks_total = len(required_checks)
        result.required_checks_found = sum(
            1 for c in required_checks
            if c in found_checks.get(c.channel, [])
        )
        
        # Find missing checks
        for check in self.PROTOCOL_CHECKS:
            if check not in found_checks.get(check.channel, []):
                result.missing_checks.append(f"{check.name}: {check.description}")
        
        # Calculate overall coverage score (weighted)
        if total_weight > 0:
            result.coverage_score = (found_weight / total_weight) * 100
        
        return result
    
    def get_coverage_grade(self) -> Tuple[float, Dict[str, any]]:
        """
        Get a grade based on protocol coverage.
        
        Returns:
            Tuple of (score out of 100, detailed results dict)
        """
        result = self.analyze_coverage()
        
        details = {
            "coverage_score": result.coverage_score,
            "channels_covered": sum(1 for c in result.channels.values() if c.coverage_score > 0),
            "total_channels": len(result.channels),
            "checks_found": result.total_checks_found,
            "checks_possible": result.total_checks_possible,
            "required_checks_found": result.required_checks_found,
            "required_checks_total": result.required_checks_total,
            "all_required_present": result.required_checks_found == result.required_checks_total,
            "missing_checks": result.missing_checks[:5],  # Top 5 missing
            "channel_details": {
                name: {
                    "signals": cov.signals_monitored,
                    "checks": cov.checks_found,
                    "score": cov.coverage_score,
                }
                for name, cov in result.channels.items()
            },
            "errors": result.errors,
        }
        
        # Score calculation:
        # - 60% based on weighted coverage score
        # - 40% based on required checks (all-or-nothing for full points)
        score = result.coverage_score * 0.6
        
        if result.required_checks_found == result.required_checks_total:
            score += 40.0
        else:
            # Partial credit for required checks
            if result.required_checks_total > 0:
                score += 40.0 * (result.required_checks_found / result.required_checks_total)
        
        return min(score, 100.0), details


def check_protocol_coverage(testbench_path: str) -> Tuple[bool, float, Dict[str, any]]:
    """
    Convenience function to check protocol coverage.
    
    Args:
        testbench_path: Path to testbench file
        
    Returns:
        Tuple of (passed, score, details)
    """
    checker = AXI4ProtocolCoverageChecker(testbench_path)
    score, details = checker.get_coverage_grade()
    
    # Pass threshold: 70% coverage with all required checks
    passed = score >= 70.0 and details.get("all_required_present", False)
    
    return passed, score, details


def format_coverage_report(details: Dict[str, any]) -> str:
    """
    Format a human-readable coverage report.
    
    Args:
        details: Coverage details from get_coverage_grade()
        
    Returns:
        Formatted report string
    """
    # Pre-compute the checkmark
    required_status = '✓' if details.get('all_required_present') else '✗'
    
    report = f"""
============================================================
AXI4 Protocol Coverage Report
============================================================

Summary:
  Coverage Score: {details.get('coverage_score', 0):.1f}%
  Channels Covered: {details.get('channels_covered', 0)}/{details.get('total_channels', 5)}
  Protocol Checks: {details.get('checks_found', 0)}/{details.get('checks_possible', 0)}
  Required Checks: {details.get('required_checks_found', 0)}/{details.get('required_checks_total', 0)} {required_status}

Channel Details:
"""
    
    for channel, info in details.get("channel_details", {}).items():
        report += f"\n  {channel} Channel ({info['score']:.1f}%):\n"
        report += f"    Signals: {', '.join(info['signals']) if info['signals'] else 'None'}\n"
        report += f"    Checks: {', '.join(info['checks']) if info['checks'] else 'None'}\n"
    
    if details.get("missing_checks"):
        report += "\nMissing Checks:\n"
        for check in details["missing_checks"]:
            report += f"  - {check}\n"
    
    report += "\n============================================================\n"
    
    return report

