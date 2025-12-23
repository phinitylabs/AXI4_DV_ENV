# AXI4 Slave Design Specification

## Overview

This document describes the AXI4 slave design and the requirements for writing SystemVerilog Assertions (SVA) to verify protocol compliance.

## Design Architecture

The AXI4 slave implementation uses a 5-module architecture:

\\\
axi4_slave_top
├── axi4_write_channel  - Write Address (AW) + Write Data (W) + Write Response (B)
├── axi4_read_channel   - Read Address (AR) + Read Data (R)
├── axi4_memory         - Backend storage (4KB addressable)
├── axi4_decoder (wr)   - Write address decoder
└── axi4_decoder (rd)   - Read address decoder
\\\

## Source Files

| File | Description |
|------|-------------|
| \sources/axi4_pkg.sv\ | Package with AXI4 type definitions and parameters |
| \sources/axi4_slave_top.sv\ | Top-level module that instantiates all submodules |
| \sources/axi4_write_channel.sv\ | Handles AW, W, and B channels |
| \sources/axi4_read_channel.sv\ | Handles AR and R channels |
| \sources/axi4_memory.sv\ | Simple dual-port memory backend |
| \sources/axi4_decoder.sv\ | Address decoder for valid address range |

## AXI4 Interface Signals

### Write Address Channel (AW)

| Signal | Width | Direction | Description |
|--------|-------|-----------|-------------|
| AWID | 4 | Input | Write transaction ID |
| AWADDR | 32 | Input | Write address |
| AWLEN | 8 | Input | Burst length (0 = 1 beat, 255 = 256 beats) |
| AWSIZE | 3 | Input | Burst size (010 = 4 bytes) |
| AWBURST | 2 | Input | Burst type (00=FIXED, 01=INCR, 10=WRAP) |
| AWVALID | 1 | Input | Address valid |
| AWREADY | 1 | Output | Slave ready to accept address |

### Write Data Channel (W)

| Signal | Width | Direction | Description |
|--------|-------|-----------|-------------|
| WDATA | 32 | Input | Write data |
| WSTRB | 4 | Input | Byte strobes (1 bit per byte) |
| WLAST | 1 | Input | Last beat of write burst |
| WVALID | 1 | Input | Write data valid |
| WREADY | 1 | Output | Slave ready to accept data |

### Write Response Channel (B)

| Signal | Width | Direction | Description |
|--------|-------|-----------|-------------|
| BID | 4 | Output | Response ID (matches AWID) |
| BRESP | 2 | Output | Write response (00=OKAY, 11=DECERR) |
| BVALID | 1 | Output | Response valid |
| BREADY | 1 | Input | Master ready to accept response |

### Read Address Channel (AR)

| Signal | Width | Direction | Description |
|--------|-------|-----------|-------------|
| ARID | 4 | Input | Read transaction ID |
| ARADDR | 32 | Input | Read address |
| ARLEN | 8 | Input | Burst length |
| ARSIZE | 3 | Input | Burst size |
| ARBURST | 2 | Input | Burst type |
| ARVALID | 1 | Input | Address valid |
| ARREADY | 1 | Output | Slave ready to accept address |

### Read Data Channel (R)

| Signal | Width | Direction | Description |
|--------|-------|-----------|-------------|
| RID | 4 | Output | Response ID (matches ARID) |
| RDATA | 32 | Output | Read data |
| RRESP | 2 | Output | Read response |
| RLAST | 1 | Output | Last beat of read burst |
| RVALID | 1 | Output | Read data valid |
| RREADY | 1 | Input | Master ready to accept data |

## AXI4 Protocol Rules

### VALID/READY Handshake

The AXI4 protocol uses a VALID/READY handshake mechanism:

1. **VALID Stability Rule**: Once VALID is asserted, it must remain HIGH until READY is also HIGH (handshake complete).

2. **No Dependency**: VALID must not depend on READY. The source can assert VALID before READY.

3. **Handshake Completion**: A transfer occurs when both VALID and READY are HIGH on the rising clock edge.

### Response Codes

| Value | Name | Description |
|-------|------|-------------|
| 2'b00 | OKAY | Normal access success |
| 2'b01 | EXOKAY | Exclusive access success |
| 2'b10 | SLVERR | Slave error |
| 2'b11 | DECERR | Decode error (address out of range) |

### Burst Types

| Value | Name | Description |
|-------|------|-------------|
| 2'b00 | FIXED | Fixed address for all beats |
| 2'b01 | INCR | Incrementing address |
| 2'b10 | WRAP | Wrapping burst |

### LAST Signal Timing

- **WLAST**: Must be asserted (HIGH) on the final beat of a write burst
- **RLAST**: Must be asserted (HIGH) on the final beat of a read burst

The beat count is determined by AWLEN/ARLEN + 1.

## Address Range

- **Valid Range**: 0x0000_0000 to 0x0000_FFFF (64KB)
- **Out of Range**: Addresses >= 0x0001_0000 return DECERR response

## Your Task: Write SVA Assertions

Add SystemVerilog Assertions (SVA) to the testbench to verify AXI4 protocol compliance.

Requirements:
- Write assertions that verify the AXI4 protocol rules described above
- Assertions should compile with Verilator and not produce false positives
- Use proper SVA syntax with \property\, \ssert property\, and \disable iff\



## Files to Modify

- \erif/axi4_slave_tb.sv\ - Add your SVA assertions in the marked section

## Success Criteria

Your assertions should:
1. Compile successfully with Verilator
2. Not fire on the correct (bug-free) design
3. Detect protocol violations if they were to occur
