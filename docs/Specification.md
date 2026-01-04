# AXI4 Burst Boundary Assertion Generation

## Overview

This task focuses on writing SystemVerilog Assertions (SVA) to verify AXI4 burst address calculations and boundary handling. You must implement assertions that check INCR, WRAP, and FIXED burst address generation.

## Design Architecture

The AXI4 slave implementation uses a 5-module architecture:

```
axi4_slave_top
├── axi4_write_channel  - Write Address (AW) + Write Data (W) + Write Response (B)
├── axi4_read_channel   - Read Address (AR) + Read Data (R)
├── axi4_memory         - Backend storage (4KB addressable)
├── axi4_decoder (wr)   - Write address decoder
└── axi4_decoder (rd)   - Read address decoder
```

## AXI4 Burst Types and Address Calculations

### FIXED Burst (AWBURST/ARBURST = 2'b00)

- Address remains constant for all beats
- Used for FIFO access
- **Assertion Focus**: Verify address does NOT change between beats

### INCR Burst (AWBURST/ARBURST = 2'b01)

- Address increments by transfer size for each beat
- Most common burst type
- **Address Formula**: `next_addr = current_addr + (1 << AWSIZE)`
- **Assertion Focus**: Verify correct address increment

### WRAP Burst (AWBURST/ARBURST = 2'b10)

- Address wraps at aligned boundary
- Only supports 2, 4, 8, or 16 beats
- **Wrap Boundary**: `wrap_boundary = (start_addr / (len * size)) * (len * size)`
- **Assertion Focus**: Verify wrap calculation and boundary behavior

## Burst Length and Size

| Signal | Description |
|--------|-------------|
| AWLEN/ARLEN | Burst length - 1 (0 = 1 beat, 15 = 16 beats) |
| AWSIZE/ARSIZE | Bytes per beat: 000=1B, 001=2B, 010=4B, 011=8B |

### Key Relationships

- **Total Beats**: AWLEN + 1
- **Bytes per Beat**: 1 << AWSIZE
- **Total Bytes**: (AWLEN + 1) * (1 << AWSIZE)

## 4KB Boundary Rule

AXI4 bursts must NOT cross a 4KB boundary (address bits [31:12] must not change).

**Example**: A burst starting at 0x0FFC with 4-byte transfers:
- 0x0FFC → OK
- 0x1000 → CROSSES 4KB BOUNDARY (violation if in same burst)

## Your Task: Write Burst Boundary Assertions

Add SVA assertions to verify:

### Required Assertions

1. **INCR Address Increment**
   - Each beat address = previous + (1 << SIZE)
   - Verify write and read channels

2. **FIXED Address Stability**
   - Address must NOT change during burst
   - Verify for both AW and AR channels

3. **WRAP Boundary Calculation**
   - Address wraps correctly at calculated boundary
   - Verify wrap occurs at: start_aligned + (len * size)

4. **4KB Boundary Check**
   - Burst must not cross 4KB address boundary
   - Check address bits [31:12] remain constant

5. **Burst Length Correctness**
   - WLAST/RLAST asserted on beat number (LEN + 1)
   - Beat counter matches expected length

## Files to Modify

- `verif/axi4_slave_tb.sv` - Add your SVA assertions in the marked section

## Testbench Signals

The testbench provides access to:

| Signal | Description |
|--------|-------------|
| aclk | Clock signal |
| aresetn | Active-low reset |
| aw* | Write address channel signals |
| w* | Write data channel signals |
| ar* | Read address channel signals |
| r* | Read data channel signals |
| b* | Write response channel signals |

## Success Criteria

Your assertions should:
1. Compile successfully with Verilator
2. Not fire on the correct (bug-free) design (no false positives)
3. Detect burst boundary violations when they occur
4. Use proper SVA syntax with `property`, `assert property`, and `disable iff`

## Example Assertion Structure

```systemverilog
// Track burst state
logic [31:0] expected_next_addr;
logic [7:0]  beat_count;
logic        in_burst;

// Example: INCR address check
property p_incr_addr_increment;
    @(posedge aclk) disable iff (!aresetn)
    (wvalid && wready && in_burst && burst_type == INCR)
    |-> (current_addr == expected_next_addr);
endproperty

assert property (p_incr_addr_increment)
    else $error("INCR burst address mismatch");
```

