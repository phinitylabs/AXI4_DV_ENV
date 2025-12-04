# AXI4 Slave SVA Task

## Task Description

Create a SystemVerilog testbench for the AXI4 slave module with assertions.

The agent should create `verif/axi4_slave_tb.sv` that:
1. Instantiates the DUT (`sources/axi4_slave.sv`)
2. Contains assertions to verify AXI4 behavior
3. Provides test stimulus
4. Compiles and simulates successfully

## Directory Structure

- `sources/` - RTL files (golden implementation)
- `verif/` - Testbench directory (agent creates testbench here)
- `tests/` - Hidden grading scripts
- `docs/` - Documentation

## Running Tests

```bash
pytest tests/test_axi4_slave_sva_hidden.py -v
```
