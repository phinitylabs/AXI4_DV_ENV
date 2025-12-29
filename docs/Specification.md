# AXI4 Full System Implementation Specification

## Overview

This is a complete AXI4 (Advanced eXtensible Interface 4) system implementation containing a master, slave, interrupt controller, and coverage collector. The design demonstrates full system-level verification of AXI4 protocol compliance.

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

## Module Descriptions

### 1. `axi4_top.sv` - Top Module
Integrates all sub-modules into a complete AXI4 system.

**Instantiated Modules:**
- `u_master` - AXI4 master (transaction generator)
- `u_slave` - AXI4 slave (memory responder)
- `u_interrupt` - Interrupt controller
- `u_coverage` - Coverage collector

### 2. `axi4_master.sv` - Master Module
Generates AXI4 transactions including:
- Write address (AW) channel control
- Write data (W) channel with WLAST
- Write response (B) channel handling
- Read address (AR) channel control
- Read data (R) channel with RLAST handling

**Features:**
- Programmable burst types (FIXED, INCR, WRAP)
- Configurable burst lengths (1-256 beats)
- Transaction ID tagging
- Timeout detection

### 3. `axi4_slave.sv` - Slave Module
Responds to AXI4 transactions with:
- Address decoding
- Memory read/write operations
- Response generation (OKAY, SLVERR, DECERR)
- Proper RLAST/WLAST handling

### 4. `axi4_interrupt.sv` - Interrupt Controller
Manages interrupt signals:
- Transaction complete interrupts
- Error interrupts
- Interrupt enable/disable control

### 5. `axi4_coverage.sv` - Coverage Collector
Collects functional coverage:
- Transaction type coverage
- Burst type coverage
- Address range coverage
- Response type coverage

## AXI4 Protocol Summary

### Five Channels
1. **Write Address (AW)**: AWID, AWADDR, AWLEN, AWSIZE, AWBURST, AWVALID, AWREADY
2. **Write Data (W)**: WDATA, WSTRB, WLAST, WVALID, WREADY
3. **Write Response (B)**: BID, BRESP, BVALID, BREADY
4. **Read Address (AR)**: ARID, ARADDR, ARLEN, ARSIZE, ARBURST, ARVALID, ARREADY
5. **Read Data (R)**: RID, RDATA, RRESP, RLAST, RVALID, RREADY

### Key Protocol Rules
- VALID must remain stable until READY
- WLAST must be asserted on final write beat
- RLAST must be asserted on final read beat
- Response codes: OKAY (00), EXOKAY (01), SLVERR (10), DECERR (11)
- BID must match AWID, RID must match ARID

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| ADDR_WIDTH | 32 | Address bus width |
| DATA_WIDTH | 32 | Data bus width |
| ID_WIDTH | 4 | Transaction ID width |
| MEM_DEPTH | 4096 | Memory depth in words |

## Address Map

| Start | End | Description |
|-------|-----|-------------|
| 0x0000_0000 | 0x0000_FFFF | Valid memory range (64KB) |
| 0x0001_0000+ | - | Decode error region |

## Timing Diagrams

### Write Transaction Flow
```
Master                              Slave
  |                                   |
  |------ AWVALID, AWADDR ----------->|
  |<----- AWREADY --------------------|
  |                                   |
  |------ WVALID, WDATA, WLAST ------>|
  |<----- WREADY ---------------------|
  |                                   |
  |<----- BVALID, BRESP --------------|
  |------ BREADY -------------------->|
```

### Read Transaction Flow
```
Master                              Slave
  |                                   |
  |------ ARVALID, ARADDR ----------->|
  |<----- ARREADY --------------------|
  |                                   |
  |<----- RVALID, RDATA, RLAST -------|
  |------ RREADY -------------------->|
```

## Testbench Requirements

Your testbench should:
1. Instantiate `axi4_top` as DUT
2. Provide clock and reset signals
3. Generate various transaction patterns
4. Verify data integrity (write-read consistency)
5. Test error conditions (out-of-range addresses)
6. Cover burst transactions (FIXED, INCR, WRAP)
7. Include timeout protection
