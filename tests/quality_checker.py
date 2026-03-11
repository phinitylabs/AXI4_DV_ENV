#!/usr/bin/env python3
"""
AXI4 Testbench Quality Checker - Anti-cheating and structural validation.

This module provides utilities for checking testbench quality:
1. Structural requirements (clock gen, reset, DUT instantiation)
2. Anti-cheating (no DUT introspection, no force/release)
3. Lazy strategy detection
4. Error format validation
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class QualityReport:
    """Detailed quality analysis report."""
    
    # Structural checks
    has_module_declaration: bool = False
    has_clock_generation: bool = False
    has_reset_sequence: bool = False
    has_dut_instantiation: bool = False
    has_write_task: bool = False
    has_read_task: bool = False
    has_finish_call: bool = False
    has_vcd_dump: bool = False
    
    # Anti-cheat checks
    illegal_hierarchical_refs: list = field(default_factory=list)
    has_force_statement: bool = False
    has_release_statement: bool = False
    
    # Lazy strategy indicators
    error_before_stimulus: bool = False
    fixed_cycle_errors: bool = False
    excessive_error_ratio: bool = False
    
    # Error format check
    error_tags_found: list = field(default_factory=list)
    error_format_valid: bool = True
    
    # Metrics
    total_lines: int = 0
    task_count: int = 0
    assertion_count: int = 0
    
    @property
    def structural_score(self) -> int:
        """Calculate structural score (out of 8)."""
        checks = [
            self.has_module_declaration,
            self.has_clock_generation,
            self.has_reset_sequence,
            self.has_dut_instantiation,
            self.has_write_task,
            self.has_read_task,
            self.has_finish_call,
            self.has_vcd_dump
        ]
        return sum(checks)
    
    @property
    def is_valid(self) -> bool:
        """Check if testbench passes all quality requirements."""
        return (
            not self.illegal_hierarchical_refs and
            not self.has_force_statement and
            not self.has_release_statement and
            not self.error_before_stimulus and
            not self.excessive_error_ratio and
            self.has_dut_instantiation
        )


# Allowed port-level signals for DUT access
ALLOWED_DUT_SIGNALS = {
    "aclk", "aresetn",
    "awid", "awaddr", "awlen", "awsize", "awburst", "awvalid", "awready",
    "wdata", "wstrb", "wlast", "wvalid", "wready",
    "bid", "bresp", "bvalid", "bready",
    "arid", "araddr", "arlen", "arsize", "arburst", "arvalid", "arready",
    "rid", "rdata", "rresp", "rlast", "rvalid", "rready"
}


def analyze_testbench(tb_path: str | Path) -> QualityReport:
    """
    Perform comprehensive quality analysis on a testbench file.
    
    Args:
        tb_path: Path to the testbench SystemVerilog file
        
    Returns:
        QualityReport with detailed analysis results
    """
    report = QualityReport()
    
    path = Path(tb_path)
    if not path.exists():
        return report
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    lines = content.split('\n')
    report.total_lines = len(lines)
    
    # =========================================================================
    # Structural Checks
    # =========================================================================
    
    # Module declaration
    report.has_module_declaration = bool(re.search(
        r'\bmodule\s+\w+',
        content
    ))
    
    # Clock generation patterns
    clock_patterns = [
        r'forever\s+#\s*\d+\s+\w+\s*=\s*~?\s*\w+',  # forever #5 clk = ~clk
        r'always\s+#\s*\d+\s+\w+\s*=\s*~?\s*\w+',   # always #5 clk = ~clk
        r'initial\s+begin[^]*?forever',              # initial begin ... forever
    ]
    report.has_clock_generation = any(
        re.search(p, content, re.MULTILINE | re.DOTALL)
        for p in clock_patterns
    )
    
    # Reset sequence
    reset_patterns = [
        r'aresetn\s*<=?\s*[01\'bh]',
        r'aresetn\s*=\s*[01\'bh]',
        r'rst_n\s*<=?\s*[01\'bh]',
        r'reset\s*<=?\s*[01\'bh]',
    ]
    report.has_reset_sequence = any(
        re.search(p, content, re.IGNORECASE)
        for p in reset_patterns
    )
    
    # DUT instantiation
    report.has_dut_instantiation = bool(re.search(
        r'axi4_top\s+\w+\s*\(',
        content
    ))
    
    # Write task
    report.has_write_task = bool(re.search(
        r'task\s+(automatic\s+)?(\w*write\w*|axi_write|axi_wr|wr_txn)',
        content, re.IGNORECASE
    ))
    
    # Read task
    report.has_read_task = bool(re.search(
        r'task\s+(automatic\s+)?(\w*read\w*|axi_read|axi_rd|rd_txn)',
        content, re.IGNORECASE
    ))
    
    # $finish call
    report.has_finish_call = '$finish' in content
    
    # VCD dump
    report.has_vcd_dump = bool(re.search(
        r'\$dumpfile\s*\(|dumpvars',
        content
    ))
    
    # Count tasks
    report.task_count = len(re.findall(r'\btask\s+', content))
    
    # Count assertions (procedural checks)
    report.assertion_count = len(re.findall(r'\$error\s*\(', content))
    
    # =========================================================================
    # Anti-Cheat Checks
    # =========================================================================
    
    # Check for illegal hierarchical references
    # Pattern: dut.u_something.signal or dut.internal_signal
    hier_refs = re.findall(r'\bdut\.(\w+)(?:\.(\w+))?', content)
    for ref in hier_refs:
        top_signal = ref[0]
        sub_signal = ref[1] if len(ref) > 1 and ref[1] else None
        
        if sub_signal:
            # Hierarchical reference like dut.u_write_channel.state
            report.illegal_hierarchical_refs.append(f"dut.{top_signal}.{sub_signal}")
        elif top_signal not in ALLOWED_DUT_SIGNALS:
            # Direct reference to non-port signal
            if not top_signal.startswith('u_'):  # Skip submodule names
                report.illegal_hierarchical_refs.append(f"dut.{top_signal}")
    
    # Check for force/release statements
    report.has_force_statement = bool(re.search(
        r'\bforce\s+\w+',
        content
    ))
    report.has_release_statement = bool(re.search(
        r'\brelease\s+\w+',
        content
    ))
    
    # =========================================================================
    # Lazy Strategy Detection
    # =========================================================================
    
    # Find position of first $error and first stimulus
    first_error_match = re.search(r'\$error', content)
    first_stimulus_match = re.search(r'awvalid\s*<=?\s*1|arvalid\s*<=?\s*1', content)
    
    if first_error_match and first_stimulus_match:
        if first_error_match.start() < first_stimulus_match.start():
            report.error_before_stimulus = True
    
    # Check for fixed-cycle error patterns (e.g., $error after specific cycle)
    fixed_cycle_pattern = r'repeat\s*\(\s*\d+\s*\)[^;]*@[^;]*;\s*\$error'
    if re.search(fixed_cycle_pattern, content):
        report.fixed_cycle_errors = True
    
    # Check error ratio (if more than 50% of lines contain $error, suspicious)
    error_lines = sum(1 for line in lines if '$error' in line)
    if report.total_lines > 0 and error_lines / report.total_lines > 0.1:
        report.excessive_error_ratio = True
    
    # =========================================================================
    # Error Format Validation
    # =========================================================================
    
    # Extract error tags like [DATA_MISMATCH], [RLAST_ERROR], etc.
    error_tags = re.findall(r'\$error\s*\(\s*"?\[([A-Z_]+)\]', content)
    report.error_tags_found = list(set(error_tags))
    
    # Check if errors use required format
    malformed_errors = re.findall(r'\$error\s*\(\s*"(?!\[)', content)
    if malformed_errors and not error_tags:
        report.error_format_valid = False
    
    return report


def validate_no_dut_introspection(content: str) -> list[str]:
    """
    Check for any access to internal DUT signals.
    Returns list of violations found.
    """
    violations = []
    
    # Pattern for accessing internal hierarchy
    patterns = [
        (r'dut\.u_\w+\.\w+', "Accessing internal submodule signal"),
        (r'dut\.\w+_reg', "Accessing internal register"),
        (r'dut\.state', "Accessing internal state"),
        (r'dut\.next_state', "Accessing internal state"),
        (r'\$root\.\w+', "Using $root for hierarchical access"),
    ]
    
    for pattern, description in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            violations.append(f"{description}: {match}")
    
    return violations


def check_stimulus_completeness(content: str) -> dict:
    """
    Check if testbench exercises required scenarios.
    Returns dict of scenario -> bool indicating if covered.
    """
    scenarios = {
        "single_write": bool(re.search(r'awlen\s*<=?\s*[08\'hbdx]*0\b', content)),
        "single_read": bool(re.search(r'arlen\s*<=?\s*[08\'hbdx]*0\b', content)),
        "burst_incr": bool(re.search(r'awburst\s*<=?\s*2\'b01|arburst\s*<=?\s*2\'b01', content)),
        "burst_fixed": bool(re.search(r'awburst\s*<=?\s*2\'b00|arburst\s*<=?\s*2\'b00', content)),
        "burst_wrap": bool(re.search(r'awburst\s*<=?\s*2\'b10|arburst\s*<=?\s*2\'b10', content)),
        "byte_strobe_full": bool(re.search(r'wstrb\s*<=?\s*4\'b1111', content)),
        "byte_strobe_partial": bool(re.search(r'wstrb\s*<=?\s*4\'b0+1|wstrb\s*<=?\s*4\'b0011', content)),
        "address_zero": bool(re.search(r'awaddr\s*<=?\s*32\'h0+\b|araddr\s*<=?\s*32\'h0+\b', content)),
        "address_boundary": bool(re.search(r'awaddr\s*<=?\s*32\'h0*[fF]{4}|araddr\s*<=?\s*32\'h0*[fF]{4}', content)),
        "decode_error": bool(re.search(r'awaddr\s*<=?\s*32\'h0*1|araddr\s*<=?\s*32\'h0*1', content)),
    }
    return scenarios


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python quality_checker.py <testbench.sv>")
        sys.exit(1)
    
    tb_path = sys.argv[1]
    report = analyze_testbench(tb_path)
    
    print("=" * 60)
    print("TESTBENCH QUALITY REPORT")
    print("=" * 60)
    print(f"\nFile: {tb_path}")
    print(f"Total Lines: {report.total_lines}")
    
    print("\n--- Structural Checks ---")
    print(f"Module Declaration:   {'✓' if report.has_module_declaration else '✗'}")
    print(f"Clock Generation:     {'✓' if report.has_clock_generation else '✗'}")
    print(f"Reset Sequence:       {'✓' if report.has_reset_sequence else '✗'}")
    print(f"DUT Instantiation:    {'✓' if report.has_dut_instantiation else '✗'}")
    print(f"Write Task:           {'✓' if report.has_write_task else '✗'}")
    print(f"Read Task:            {'✓' if report.has_read_task else '✗'}")
    print(f"$finish Call:         {'✓' if report.has_finish_call else '✗'}")
    print(f"VCD Dump:             {'✓' if report.has_vcd_dump else '✗'}")
    print(f"Structural Score:     {report.structural_score}/8")
    
    print("\n--- Anti-Cheat Checks ---")
    print(f"Illegal Hier Refs:    {report.illegal_hierarchical_refs or 'None'}")
    print(f"Force Statement:      {'✗ FOUND' if report.has_force_statement else '✓ None'}")
    print(f"Release Statement:    {'✗ FOUND' if report.has_release_statement else '✓ None'}")
    
    print("\n--- Lazy Strategy Detection ---")
    print(f"Error Before Stimulus: {'✗ YES' if report.error_before_stimulus else '✓ No'}")
    print(f"Fixed Cycle Errors:    {'✗ YES' if report.fixed_cycle_errors else '✓ No'}")
    print(f"Excessive Error Ratio: {'✗ YES' if report.excessive_error_ratio else '✓ No'}")
    
    print("\n--- Error Format ---")
    print(f"Error Tags Found:     {report.error_tags_found or 'None'}")
    print(f"Format Valid:         {'✓' if report.error_format_valid else '✗'}")
    
    print("\n" + "=" * 60)
    print(f"OVERALL VALID: {'✓ YES' if report.is_valid else '✗ NO'}")
    print("=" * 60)

