// =============================================================================
// AXI4 Decoder Testbench - GOLDEN Solution
// Verifies the address decoder module correctly routes transactions
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
    // TEST TASKS - GOLDEN SOLUTION
    // =========================================================================

    // Test 1: Valid address in middle of range
    task automatic test_valid_middle();
        test_count++;
        $display("\n[TEST %0d] Valid address in middle of range (0x1000)", test_count);
        addr = 32'h0000_1000;
        valid = 1;
        #1;
        if (select !== 1 || decode_error !== 0) begin
            $error("FAIL: Expected select=1, decode_error=0, got select=%b, decode_error=%b", 
                   select, decode_error);
            fail_count++;
        end else begin
            $display("  PASS: select=%b, decode_error=%b", select, decode_error);
            pass_count++;
        end
        valid = 0;
        #(CLK_PERIOD);
    endtask

    // Test 2: Valid address at lower boundary (0x0000)
    task automatic test_boundary_low();
        test_count++;
        $display("\n[TEST %0d] Boundary: lowest valid address (0x0000)", test_count);
        addr = 32'h0000_0000;
        valid = 1;
        #1;
        if (select !== 1 || decode_error !== 0) begin
            $error("FAIL: Address 0x0000 should be valid. Got select=%b, decode_error=%b", 
                   select, decode_error);
            fail_count++;
        end else begin
            $display("  PASS: select=%b, decode_error=%b", select, decode_error);
            pass_count++;
        end
        valid = 0;
        #(CLK_PERIOD);
    endtask

    // Test 3: Valid address at upper boundary (0xFFFF)
    task automatic test_boundary_high();
        test_count++;
        $display("\n[TEST %0d] Boundary: highest valid address (0xFFFF)", test_count);
        addr = 32'h0000_FFFF;
        valid = 1;
        #1;
        if (select !== 1 || decode_error !== 0) begin
            $error("FAIL: Address 0xFFFF should be valid. Got select=%b, decode_error=%b", 
                   select, decode_error);
            fail_count++;
        end else begin
            $display("  PASS: select=%b, decode_error=%b", select, decode_error);
            pass_count++;
        end
        valid = 0;
        #(CLK_PERIOD);
    endtask

    // Test 4: Invalid address just above range (0x10000)
    task automatic test_invalid_above();
        test_count++;
        $display("\n[TEST %0d] Invalid: address just above range (0x10000)", test_count);
        addr = 32'h0001_0000;
        valid = 1;
        #1;
        if (select !== 0 || decode_error !== 1) begin
            $error("FAIL: Address 0x10000 should be invalid. Got select=%b, decode_error=%b", 
                   select, decode_error);
            fail_count++;
        end else begin
            $display("  PASS: select=%b, decode_error=%b", select, decode_error);
            pass_count++;
        end
        valid = 0;
        #(CLK_PERIOD);
    endtask

    // Test 5: Invalid address far out of range
    task automatic test_invalid_far();
        test_count++;
        $display("\n[TEST %0d] Invalid: address far out of range (0x80000000)", test_count);
        addr = 32'h8000_0000;
        valid = 1;
        #1;
        if (select !== 0 || decode_error !== 1) begin
            $error("FAIL: Address 0x80000000 should be invalid. Got select=%b, decode_error=%b", 
                   select, decode_error);
            fail_count++;
        end else begin
            $display("  PASS: select=%b, decode_error=%b", select, decode_error);
            pass_count++;
        end
        valid = 0;
        #(CLK_PERIOD);
    endtask

    // Test 6: Valid deasserted - outputs should be 0
    task automatic test_valid_deasserted();
        test_count++;
        $display("\n[TEST %0d] Valid deasserted - both outputs should be 0", test_count);
        addr = 32'h0000_5000;  // Valid address
        valid = 0;  // But valid is deasserted
        #1;
        if (select !== 0 || decode_error !== 0) begin
            $error("FAIL: With valid=0, both outputs should be 0. Got select=%b, decode_error=%b", 
                   select, decode_error);
            fail_count++;
        end else begin
            $display("  PASS: select=%b, decode_error=%b", select, decode_error);
            pass_count++;
        end
        #(CLK_PERIOD);
    endtask

    // Test 7: Multiple valid addresses in sequence
    task automatic test_multiple_valid();
        test_count++;
        $display("\n[TEST %0d] Multiple valid addresses in sequence", test_count);
        int errors = 0;
        
        for (int i = 0; i < 4; i++) begin
            addr = 32'h0000_1000 + (i * 32'h1000);
            valid = 1;
            #1;
            if (select !== 1 || decode_error !== 0) begin
                $error("FAIL: Address 0x%08h should be valid", addr);
                errors++;
            end
            #(CLK_PERIOD);
        end
        valid = 0;
        
        if (errors == 0) begin
            $display("  PASS: All addresses validated correctly");
            pass_count++;
        end else begin
            fail_count++;
        end
        #(CLK_PERIOD);
    endtask

    // =========================================================================
    // END OF TEST SECTION
    // =========================================================================

    // Main test sequence
    initial begin
        $dumpfile("axi4_decoder_tb.vcd");
        $dumpvars(0, axi4_decoder_tb);
        
        $display("================================================================");
        $display(" AXI4 Decoder Testbench - GOLDEN Solution");
        $display("================================================================");
        $display(" Valid address range: 0x%08h to 0x%08h", BASE_ADDR, BASE_ADDR + ADDR_RANGE);
        $display("================================================================");

        // Initialize
        addr = 0;
        valid = 0;
        #(CLK_PERIOD * 5);

        // Run all tests
        test_valid_middle();
        test_boundary_low();
        test_boundary_high();
        test_invalid_above();
        test_invalid_far();
        test_valid_deasserted();
        test_multiple_valid();

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
