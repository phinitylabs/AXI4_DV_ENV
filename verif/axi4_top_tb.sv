// =============================================================================
// AXI4 Interrupt Controller Testbench - Starter Template
// Task: Create testbench with assertions for interrupt verification
// =============================================================================

`timescale 1ns/1ps

module axi4_top_tb;

    // Parameters
    parameter CLK_PERIOD = 10;
    parameter TIMEOUT_CYCLES = 50000;

    // Signals
    logic clk;
    logic resetn;
    
    // Interrupt interface
    logic interrupt_req;
    logic interrupt_ack;

    // Clock Generation
    initial begin
        clk = 0;
        forever #(CLK_PERIOD/2) clk = ~clk;
    end

    // DUT Instantiation
    axi4_top dut (
        .clk(clk),
        .resetn(resetn),
        .interrupt_req(interrupt_req),
        .interrupt_ack(interrupt_ack)
    );

    // =========================================================================
    // ADD YOUR INTERRUPT TESTBENCH AND ASSERTIONS HERE
    // =========================================================================
    //
    // Required tests:
    // 1. Basic interrupt handshake
    // 2. Interrupt acknowledge timing
    // 3. Multiple successive interrupts
    // 4. Reset behavior
    //
    // Required assertions:
    // 1. interrupt_ack only asserts after interrupt_req
    // 2. interrupt_ack timing requirements
    // 3. State machine correctness
    //
    // =========================================================================



    // =========================================================================
    // END OF USER CODE SECTION
    // =========================================================================

    // Basic Test Sequence
    initial begin
        $dumpfile("axi4_top_tb.vcd");
        $dumpvars(0, axi4_top_tb);
        $display("================================================================");
        $display(" AXI4 Interrupt Controller Testbench");
        $display("================================================================");
        
        // Reset sequence
        resetn = 0;
        interrupt_req = 0;
        repeat(10) @(posedge clk);
        resetn = 1;
        repeat(5) @(posedge clk);
        
        $display("\n[INFO] Starting basic interrupt test...");
        
        // TODO: Add your test sequences here
        
        repeat(100) @(posedge clk);
        $display("\n================================================================");
        $display(" Test Complete");
        $display("================================================================");
        $finish;
    end

    // Timeout
    initial begin
        repeat(TIMEOUT_CYCLES) @(posedge clk);
        $display("ERROR: Timeout!");
        $finish;
    end

endmodule

