// =============================================================================
// AXI4 Decoder Testbench - Implementation Required
// Task: Write comprehensive tests to verify the address decoder module
// =============================================================================
//
// Module Under Test: axi4_decoder
//
// The decoder checks if an address is within a valid range:
// - BASE_ADDR = 0x0000_0000
// - ADDR_RANGE = 0x0000_FFFF (valid range: 0x0000 to 0xFFFF)
//
// Decoder Behavior:
// - When 'valid' is asserted and address is in range: select=1, decode_error=0
// - When 'valid' is asserted and address is out of range: select=0, decode_error=1
// - When 'valid' is deasserted: both outputs are 0
//
// Your task: Write comprehensive test cases that verify ALL decoder behaviors
// including boundary conditions and edge cases.
//
// IMPORTANT: Tests must detect bugs in mutant designs. A basic test that only
// checks one address will NOT be sufficient to pass the benchmark.
// =============================================================================

`timescale 1ns/1ps

module axi4_decoder_tb;

    // Parameters
    parameter ADDR_WIDTH = 32;
    parameter BASE_ADDR  = 32'h0000_0000;
    parameter ADDR_RANGE = 32'h0000_FFFF;
    parameter CLK_PERIOD = 10;

    // Signals
    logic clk;
    logic [ADDR_WIDTH-1:0] addr;
    logic valid;
    logic select;
    logic decode_error;

    // Test tracking
    int test_count = 0;
    int pass_count = 0;
    int fail_count = 0;

    // Clock generation
    initial begin
        clk = 0;
        forever #(CLK_PERIOD/2) clk = ~clk;
    end

    // DUT instantiation
    axi4_decoder #(
        .ADDR_WIDTH(ADDR_WIDTH),
        .BASE_ADDR(BASE_ADDR),
        .ADDR_RANGE(ADDR_RANGE)
    ) dut (
        .addr(addr),
        .valid(valid),
        .select(select),
        .decode_error(decode_error)
    );

    // =========================================================================
    // IMPLEMENT YOUR TEST CASES BELOW
    // =========================================================================
    //
    // You need to write test tasks that:
    // 1. Test valid addresses (in range) - verify select=1, decode_error=0
    // 2. Test invalid addresses (out of range) - verify select=0, decode_error=1
    // 3. Test boundary conditions (exactly at boundaries)
    // 4. Test valid signal deassertion behavior
    //
    // Your tests MUST use $error() for failures to be detected by the grader.
    //
    // =========================================================================



    // =========================================================================
    // END OF TEST SECTION
    // =========================================================================

    // Main test sequence
    initial begin
        $dumpfile("axi4_decoder_tb.vcd");
        $dumpvars(0, axi4_decoder_tb);
        
        $display("================================================================");
        $display(" AXI4 Decoder Testbench");
        $display("================================================================");
        $display(" BASE_ADDR: 0x%08h", BASE_ADDR);
        $display(" ADDR_RANGE: 0x%08h", ADDR_RANGE);
        $display(" Valid range: 0x%08h to 0x%08h", BASE_ADDR, BASE_ADDR + ADDR_RANGE);
        $display("================================================================");

        // Initialize
        addr = 0;
        valid = 0;
        #(CLK_PERIOD * 5);

        // TODO: Call your test tasks here


        #(CLK_PERIOD * 10);

        $display("\n================================================================");
        $display(" Test Summary: Total=%0d, PASSED=%0d, FAILED=%0d", 
                 test_count, pass_count, fail_count);
        $display("================================================================");
        
        if (fail_count > 0) begin
            $error("TESTBENCH FAILED");
        end
        
        $finish;
    end

    // Timeout
    initial begin
        #1000000;
        $display("ERROR: Timeout!");
        $finish;
    end

endmodule
