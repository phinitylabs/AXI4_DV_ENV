# AXI4 Interrupt Controller Verification

## Overview

This task requires creating a SystemVerilog testbench with assertions to verify the interrupt controller functionality in a complete AXI4 system. The focus is on verifying interrupt request/acknowledge handshaking and proper state machine behavior.

## System Architecture

```
                    +----------------+
                    |   axi4_top     |
                    +----------------+
                           |
         +-----------------+-----------------+
         |                 |                 |
    +----------+     +----------+     +-----------+
    |axi4_master|<-->|axi4_slave |     |axi4_inter |
    +----------+     +----------+     | rupt      |
                           |         +-----------+
                    +----------+
                    |axi4_cover|
                    | age      |
                    +----------+
```

## Module: axi4_interrupt

The interrupt controller has a simple 3-state state machine:

| State | Description |
|-------|-------------|
| IDLE | Waiting for interrupt request |
| PENDING | Interrupt request received, processing |
| ACKNOWLEDGED | Interrupt acknowledged |

### Signals

| Signal | Direction | Description |
|--------|-----------|-------------|
| clk | Input | Clock signal |
| resetn | Input | Active-low reset |
| interrupt_req | Input | Interrupt request from master |
| interrupt_ack | Output | Interrupt acknowledge to master |

### State Transitions

1. **IDLE → PENDING**: When `interrupt_req` goes HIGH
2. **PENDING → ACKNOWLEDGED**: Automatic (1 cycle delay)
3. **ACKNOWLEDGED → IDLE**: When `interrupt_req` goes LOW

### Interrupt Timing

```
           ____________________
interrupt_req  |                  |_______
                    __________
interrupt_ack  ____|          |___________

State:     IDLE  PENDING  ACKNOWLEDGED  IDLE
```

## Your Task

Create a comprehensive testbench (`verif/axi4_top_tb.sv`) and C++ wrapper (`verif/sim_main.cpp`) that:

### 1. Testbench Requirements

- Clock generation (10ns period)
- Reset sequence
- DUT instantiation (`axi4_top`)
- Test stimulus generation

### 2. Interrupt Test Scenarios

Write tests that verify:
- **Basic handshake**: Assert `interrupt_req`, verify `interrupt_ack` timing
- **Hold requirement**: `interrupt_ack` stays HIGH while `interrupt_req` is HIGH
- **De-assertion**: `interrupt_ack` goes LOW after `interrupt_req` goes LOW
- **Multiple interrupts**: Successive interrupt cycles work correctly
- **Reset behavior**: State machine resets properly

### 3. SVA Assertions

Add assertions to verify:
- `interrupt_ack` only asserts after `interrupt_req`
- `interrupt_ack` remains stable during acknowledge state
- State machine does not enter invalid states
- Timing between request and acknowledge is correct

## Files to Create/Modify

- `verif/axi4_top_tb.sv` - Main testbench with interrupt tests and assertions
- `verif/sim_main.cpp` - Verilator C++ wrapper

## Quality Requirements

**Important**: Do NOT use hierarchical references to access internal DUT signals (e.g., `dut.u_interrupt.state`). Only use the top-level ports.

## Example Testbench Structure

```systemverilog
module axi4_top_tb;
    // Clock and reset
    logic clk;
    logic resetn;
    
    // Interrupt interface
    logic interrupt_req;
    logic interrupt_ack;
    
    // DUT instantiation
    axi4_top dut (
        .clk(clk),
        .resetn(resetn),
        // ... other ports ...
        .interrupt_req(interrupt_req),
        .interrupt_ack(interrupt_ack)
    );
    
    // Clock generation
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end
    
    // Test sequence
    initial begin
        // Reset
        resetn = 0;
        interrupt_req = 0;
        repeat(10) @(posedge clk);
        resetn = 1;
        
        // Test interrupt handshake
        // ... your test code ...
        
        $finish;
    end
    
    // SVA Assertions
    // assert property (...);
endmodule
```

## Success Criteria

Your testbench should:
1. Compile successfully with Verilator
2. Pass all tests on the correct design
3. Detect bugs in faulty interrupt implementations
4. Include meaningful SVA assertions
5. Avoid hierarchical references (quality check)

