# AXI4 Protocol Specification

## Overview

AXI4 (Advanced eXtensible Interface 4) is an industry-standard bus protocol developed by ARM as part of the AMBA specification. AXI4 defines high-performance communication between master and slave components in system-on-chip (SoC) designs. It provides point-to-point interconnect and supports multiple outstanding transactions, separate read and write channels, and robust data transfer.

AXI4 transactions are burst-based, allowing the transfer of multiple data items in a single transaction. Each AXI4 interface consists of five independent unidirectional channels: Write Address (AW), Write Data (W), Write Response (B), Read Address (AR), and Read Data (R).

## AXI4 Protocol Channels

1. **Write Address Channel (AW)**: Carries address and control information for write transactions
2. **Write Data Channel (W)**: Transports the actual write data
3. **Write Response Channel (B)**: Carries response signal from slave to master
4. **Read Address Channel (AR)**: Carries address and control information for read transactions
5. **Read Data Channel (R)**: Carries read data and response information

Each channel uses a valid-ready handshake (VALID and READY signals) to synchronize data transfer.

## AXI4 Write Transaction

1. Master asserts AWVALID with write address and control information
2. Slave asserts AWREADY when ready (both signals high = address accepted)
3. Master asserts WVALID with write data
4. Slave asserts WREADY when ready (both signals high = data accepted)
5. Master asserts WLAST on the last data transfer
6. Slave provides write response on B channel with BVALID and response code
7. Master asserts BREADY to acknowledge response

## AXI4 Read Transaction

1. Master asserts ARVALID with read address and control information
2. Slave asserts ARREADY when ready (both signals high = address accepted)
3. Slave transmits read data on R channel with RVALID
4. Master asserts RREADY when able to receive data
5. Slave asserts RLAST on the last data transfer

## Burst Types

- **FIXED**: Address remains constant for every data transfer
- **INCR**: Address increments after each data transfer
- **WRAP**: Address wraps around at the boundary of a defined length

Burst length (AWLEN/ARLEN) specifies number of transfers in the burst (0 = 1 transfer, 1 = 2 transfers, etc.).

## Available Modules

The design includes four SystemVerilog modules:

1. **axi4_slave**: AXI4 slave module that responds to master requests, handles write and read transactions, and manages a 4KB memory array
2. **axi4_master**: AXI4 master module that initiates transactions
3. **axi4_interrupt**: Interrupt controller module
4. **axi4_top**: Top-level module that instantiates and connects the master, slave, and interrupt controller

## Task Requirements

Create a SystemVerilog testbench (`verif/axi4_top_tb.sv`) that:

1. **Instantiate the DUT**:
   - Instantiate `axi4_top` from `sources/axi4_top.sv` (NOT axi4_slave directly!)
   - The axi4_top module internally connects axi4_master, axi4_slave, and axi4_interrupt
   - Your testbench monitors the internal AXI signals between master and slave
   - Provide clock and reset signals

2. **Add Protocol Assertions** to verify:
   - VALID signal stability (AWVALID, WVALID, ARVALID, BVALID, RVALID must remain stable until corresponding READY)
   - LAST signal correctness (WLAST, RLAST on final beats)
   - Response code validation (BRESP, RRESP must be valid: 00=OKAY, 01=EXOKAY, 10=SLVERR, 11=DECERR)
   - Timing relationships (BVALID after WLAST, RVALID after ARREADY)

3. **Provide Test Stimulus** including:
   - Single-beat write transactions
   - Multi-beat burst writes (INCR, FIXED, WRAP)
   - Read transactions with various burst lengths
   - Different address ranges

4. **Testbench Quality**:
   - Must compile AND simulate successfully with Verilator
   - Assertion failures MUST use `$error()` — NOT `$display()`:
     ```systemverilog
     assert property (p_my_check)
       else $error("ASSERTION FAILED: description");
     ```
   - Simulation MUST exit nonzero if any check fails:
     ```systemverilog
     if (fail_count > 0)
       $fatal(1, "TESTBENCH FAILED: %0d failure(s)", fail_count);
     ```
   - **Why**: The grader uses differential comparison. `$error()` writes to stderr
     with `%Error` prefix that the grader detects. `$display()` is invisible and
     will not count as bug detection.

## Verification Command

**IMPORTANT**: Your testbench MUST pass this verification before submission:

```bash
# Compile for simulation (NOT just lint-only!)
verilator --binary --timing -Wno-fatal \
    sources/axi4_top.sv sources/axi4_master.sv sources/axi4_slave.sv sources/axi4_interrupt.sv \
    verif/axi4_top_tb.sv --top-module axi4_top_tb -o sim_tb

# Run simulation
./sim_tb
```

**NOTE**: `verilator --lint-only` is NOT sufficient! You MUST test with `--binary` and run the actual simulation.

## Key Signals

- **AWADDR/ARADDR**: Address of the first data transfer
- **AWLEN/ARLEN**: Number of transfers in burst (0-based, so 0 = 1 transfer)
- **AWSIZE/ARSIZE**: Size of each transfer in bytes (2 = 4 bytes)
- **AWBURST/ARBURST**: Burst type (00=FIXED, 01=INCR, 10=WRAP)
- **WDATA/RDATA**: Write and read data
- **WSTRB**: Write strobes indicating valid data bytes
- **WLAST/RLAST**: Last transfer in burst indicator
- **BRESP/RRESP**: Response codes (00=OKAY, 10=SLVERR)

## Response Codes

- **OKAY (2'b00)**: Normal successful access
- **SLVERR (2'b10)**: Slave error (e.g., out-of-range address)

The slave module returns SLVERR for addresses >= 0x1000 (outside the 4KB memory range).

