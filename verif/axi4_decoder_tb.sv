// =============================================================================
// AXI4 Decoder Testbench - Starter Template
// Task: Write tests to verify the address decoder module
// =============================================================================
//
// The decoder checks if an address is within a valid range:
// - BASE_ADDR = 0x0000_0000
// - ADDR_RANGE = 0x0000_FFFF (valid range: 0x0000 to 0xFFFF)
//
// When 'valid' is asserted:
// - 'select' = 1 if address is in range
// - 'decode_error' = 1 if address is out of range
//
// Your task: Write test cases to verify this behavior
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

    // Test counters
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
    // ADD YOUR TEST CASES HERE
    // =========================================================================
    //
    // Required test scenarios:
    // 1. Valid address in range - should set select=1, decode_error=0
    // 2. Invalid address out of range - should set select=0, decode_error=1
    // 3. Boundary conditions (address at 0x0000, 0xFFFF, 0x10000)
    // 4. Valid signal deasserted - both outputs should be 0
    //
    // Example test pattern:
    //
    // task automatic test_valid_address();
    //     test_count++;
    //     $display("[TEST %0d] Valid address in range", test_count);
    //     addr = 32'h0000_1000;
    //     valid = 1;
    //     #1;
    //     if (select !== 1 || decode_error !== 0) begin
    //         $error("FAIL: Expected select=1, decode_error=0");
    //         fail_count++;
    //     end else begin
    //         $display("  PASS");
    //         pass_count++;
    //     end
    //     valid = 0;
    //     #(CLK_PERIOD);
    // endtask
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
        $display(" Valid address range: 0x%08h to 0x%08h", BASE_ADDR, BASE_ADDR + ADDR_RANGE);
        $display("================================================================");

        // Initialize
        addr = 0;
        valid = 0;
        #(CLK_PERIOD * 5);

        // ADD YOUR TEST TASK CALLS HERE
        // Example:
        // test_valid_address();
        // test_invalid_address();
        // test_boundary_low();
        // test_boundary_high();
        // test_valid_deasserted();

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

