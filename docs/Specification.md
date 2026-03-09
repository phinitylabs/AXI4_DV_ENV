# AXI4 Slave Implementation Specification

## Overview

This is a 5-module AXI4 (Advanced eXtensible Interface 4) slave implementation supporting all five channels of the AXI4 protocol. The design is fully parameterizable and includes memory-mapped storage with burst transaction support.

## AXI4 Protocol Summary

AXI4 is an ARM AMBA protocol for high-performance, high-frequency system designs. It uses separate address/data channels for reads and writes, enabling simultaneous bidirectional data transfer.

### Key Features
- **Separate Read/Write Channels**: Allows concurrent read and write operations
- **Burst Transfers**: FIXED, INCR, and WRAP burst types supported
- **Outstanding Transactions**: Multiple pending transactions via ID tags
- **Byte Strobes**: Fine-grained write enables per byte
- **Out-of-Order Completion**: Responses can return in any order (by ID)

## Module Architecture (5 Modules)

### 1. `axi4_pkg.sv` - Package
Common definitions including parameters, burst types, response codes, and data structures used across all modules.

**Key Definitions:**
- `BURST_FIXED`, `BURST_INCR`, `BURST_WRAP` - Burst type enumerations
- `RESP_OKAY`, `RESP_SLVERR`, `RESP_DECERR` - Response codes
- Address/data width parameters

### 2. `axi4_slave_top.sv` - Top Module
Integrates all sub-modules into a complete AXI4 slave. Handles signal routing and module interconnection.

**Sub-module Instances:**
- `u_write_channel` - Write channel (AW+W+B)
- `u_read_channel` - Read channel (AR+R)
- `u_wr_decoder` - Write address decoder
- `u_rd_decoder` - Read address decoder
- `u_memory` - Memory backend

### 3. `axi4_write_channel.sv` - Write Channel
Combined write address (AW), write data (W), and write response (B) channel logic.

**Features:**
- Address capture and burst parameter latching
- Beat counting for burst transactions
- Address generation for FIXED, INCR, WRAP bursts
- WLAST checking and error detection
- Response generation (OKAY, SLVERR, DECERR)

**State Machine:**
```
IDLE → ADDR_RECV → DATA_BURST → SEND_RESP → WAIT_BREADY → IDLE
```

### 4. `axi4_read_channel.sv` - Read Channel  
Combined read address (AR) and read data (R) channel logic.

**Features:**
- Address capture and burst parameter latching
- Memory read request generation
- Beat counting and address generation
- RLAST generation on final beat
- Response generation with decode error support

**State Machine:**
```
IDLE → ADDR_RECV → MEM_READ → MEM_WAIT → SEND_DATA → WAIT_RREADY → ...
```

### 5. `axi4_decoder.sv` - Address Decoder
Validates addresses against configured address range. Generates decode errors for out-of-range accesses.

**Parameters:**
- `BASE_ADDR` - Start of valid address range (default: 0x0000_0000)
- `ADDR_RANGE` - Size of valid range (default: 0x0000_FFFF)

**Outputs:**
- `select` - Address is in valid range
- `decode_error` - Address is out of range

### 6. `axi4_memory.sv` - Memory Backend
Byte-addressable memory with strobe support for partial writes.

**Features:**
- Parameterized depth (default: 4096 words = 16KB)
- Byte-enable writes via WSTRB
- Single-cycle read latency (registered output)
- Dual-port (separate read/write ports)

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| ADDR_WIDTH | 32 | Address bus width |
| DATA_WIDTH | 32 | Data bus width |
| ID_WIDTH | 4 | Transaction ID width |
| MEM_DEPTH | 4096 | Memory depth in words |

## Supported Features

- ✅ All burst types (FIXED, INCR, WRAP)
- ✅ Burst lengths 1-256 beats (AWLEN/ARLEN 0-255)
- ✅ Byte strobes for partial writes
- ✅ Transaction IDs (BID/RID reflection)
- ✅ Proper response generation (OKAY, SLVERR, DECERR)
- ✅ Address decode error detection

## Address Map

| Start | End | Description |
|-------|-----|-------------|
| 0x0000_0000 | 0x0000_FFFF | Valid memory range (64KB) |
| 0x0001_0000+ | - | Decode error region |

## Timing Diagrams

### Single Write Transaction
```
         ___     ___     ___     ___     ___     ___
clk   __|   |___|   |___|   |___|   |___|   |___|   |___

awvalid ___|‾‾‾‾‾|_________________________________
awready ‾‾‾‾‾‾‾‾‾|___|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
awaddr  ====X=ADDR=X================================

wvalid  ________|‾‾‾‾‾|____________________________
wready  ______________|‾‾‾‾‾|______________________
wdata   ========X=DATA=X============================
wlast   ________|‾‾‾‾‾|____________________________

bvalid  ____________________|‾‾‾‾‾|________________
bready  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|________________
bresp   ====================X=OKAY=X================
```

### Burst Read Transaction (4 beats)
```
         ___     ___     ___     ___     ___     ...
clk   __|   |___|   |___|   |___|   |___|   |___

arvalid ___|‾‾‾‾‾|_________________________________
arready ‾‾‾‾‾‾‾‾‾|___|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
araddr  ====X=ADDR=X================================
arlen   ====X=0x03=X================================

rvalid  ______________|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|________
rready  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
rdata   ==============X=D0=X=D1=X=D2=X=D3=X========
rlast   __________________________________|‾‾‾|____
```

## Response Codes

| Code | Name | Binary | Description |
|------|------|--------|-------------|
| OKAY | Normal | 2'b00 | Transaction completed successfully |
| EXOKAY | Exclusive OK | 2'b01 | Exclusive access success (not used) |
| SLVERR | Slave Error | 2'b10 | Protocol error (e.g., WLAST mismatch) |
| DECERR | Decode Error | 2'b11 | Address out of valid range |

## Important: Error Reporting Requirements

When your testbench detects an error, use `$error()` not `$display()`:

```systemverilog
if (rdata !== expected_data)
    $error("ASSERTION FAILED: read data mismatch at addr 0x%h: got 0x%h expected 0x%h",
           addr, rdata, expected_data);
```

At simulation end, call `$fatal()` if any failures occurred:

```systemverilog
if (fail_count > 0)
    $fatal(1, "TESTBENCH FAILED: %0d errors detected", fail_count);
```

`$error()` writes to stderr with a `%Error` prefix that the grader detects. `$display()` is not visible to the grader.
