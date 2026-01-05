// =============================================================================
// AXI4 Interrupt Controller Testbench - GOLDEN Solution
// Contains comprehensive interrupt verification with SVA assertions
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
    
    // Test tracking
    int test_count = 0;
    int pass_count = 0;
    int fail_count = 0;

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
    // STATE TRACKING FOR ASSERTIONS
    // =========================================================================
    
    // Track previous values for edge detection
    logic interrupt_req_prev;
    logic interrupt_ack_prev;
    logic [7:0] cycles_since_req;
    logic req_was_high;
    
    always_ff @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            interrupt_req_prev <= 1'b0;
            interrupt_ack_prev <= 1'b0;
            cycles_since_req <= '0;
            req_was_high <= 1'b0;
        end else begin
            interrupt_req_prev <= interrupt_req;
            interrupt_ack_prev <= interrupt_ack;
            
            if (interrupt_req && !interrupt_req_prev) begin
                cycles_since_req <= '0;
                req_was_high <= 1'b1;
            end else if (req_was_high && cycles_since_req < 255) begin
                cycles_since_req <= cycles_since_req + 1;
            end
            
            if (!interrupt_req && interrupt_req_prev)
                req_was_high <= 1'b0;
        end
    end

    // =========================================================================
    // SVA ASSERTIONS FOR INTERRUPT CONTROLLER
    // =========================================================================

    // 1. Ack only after request: interrupt_ack should not assert without interrupt_req
    property p_ack_requires_request;
        @(posedge clk) disable iff (!resetn)
        $rose(interrupt_ack) |-> req_was_high;
    endproperty
    
    assert property (p_ack_requires_request)
        else $error("ASSERTION FAILED: interrupt_ack asserted without prior interrupt_req");

    // 2. Ack timing: interrupt_ack should assert within 3 cycles of interrupt_req
    property p_ack_timing;
        @(posedge clk) disable iff (!resetn)
        $rose(interrupt_req) |-> ##2 interrupt_ack;
    endproperty
    
    assert property (p_ack_timing)
        else $error("ASSERTION FAILED: interrupt_ack not asserted within 3 cycles of request");

    // 3. Ack stability: interrupt_ack stays high while interrupt_req is high (after ack)
    property p_ack_stable_while_req;
        @(posedge clk) disable iff (!resetn)
        (interrupt_ack && interrupt_req) |=> (interrupt_ack || !interrupt_req);
    endproperty
    
    assert property (p_ack_stable_while_req)
        else $error("ASSERTION FAILED: interrupt_ack unstable while interrupt_req high");

    // 4. Ack deassert: interrupt_ack should deassert after interrupt_req deasserts
    property p_ack_deassert;
        @(posedge clk) disable iff (!resetn)
        $fell(interrupt_req) && interrupt_ack |-> ##2 !interrupt_ack;
    endproperty
    
    assert property (p_ack_deassert)
        else $error("ASSERTION FAILED: interrupt_ack stuck high after request deasserted");

    // 5. No ack without request: interrupt_ack should be low when interrupt_req has been low
    property p_no_spurious_ack;
        @(posedge clk) disable iff (!resetn)
        (!interrupt_req && !interrupt_req_prev && !req_was_high) |-> !interrupt_ack;
    endproperty
    
    assert property (p_no_spurious_ack)
        else $error("ASSERTION FAILED: Spurious interrupt_ack without request");

    // 6. Reset behavior: After reset, interrupt_ack should be low
    property p_reset_ack_low;
        @(posedge clk)
        $rose(resetn) |-> !interrupt_ack;
    endproperty
    
    assert property (p_reset_ack_low)
        else $error("ASSERTION FAILED: interrupt_ack not low after reset");

    // =========================================================================
    // TEST TASKS
    // =========================================================================

    task automatic reset_dut();
        $display("\n[INFO] Resetting DUT...");
        resetn = 0;
        interrupt_req = 0;
        repeat(10) @(posedge clk);
        resetn = 1;
        repeat(5) @(posedge clk);
        $display("[INFO] Reset complete");
    endtask

    task automatic test_basic_handshake();
        test_count++;
        $display("\n[TEST %0d] Basic Interrupt Handshake", test_count);
        
        // Assert interrupt request
        @(posedge clk);
        interrupt_req = 1;
        $display("  -> interrupt_req asserted");
        
        // Wait for acknowledge (max 5 cycles)
        repeat(5) begin
            @(posedge clk);
            if (interrupt_ack) break;
        end
        
        if (interrupt_ack) begin
            $display("  -> interrupt_ack received");
            pass_count++;
            $display("  PASS");
        end else begin
            fail_count++;
            $display("  FAIL: No acknowledge received");
        end
        
        // Deassert request
        repeat(2) @(posedge clk);
        interrupt_req = 0;
        
        // Wait for ack to deassert
        repeat(5) @(posedge clk);
    endtask

    task automatic test_ack_timing();
        test_count++;
        $display("\n[TEST %0d] Interrupt Acknowledge Timing", test_count);
        
        // Start fresh
        interrupt_req = 0;
        repeat(5) @(posedge clk);
        
        // Assert request and count cycles to ack
        @(posedge clk);
        interrupt_req = 1;
        
        for (int i = 0; i < 10; i++) begin
            @(posedge clk);
            if (interrupt_ack) begin
                $display("  -> Ack received after %0d cycles", i+1);
                if (i+1 <= 3) begin
                    pass_count++;
                    $display("  PASS");
                end else begin
                    fail_count++;
                    $display("  FAIL: Ack too slow (>3 cycles)");
                end
                break;
            end
        end
        
        // Cleanup
        repeat(2) @(posedge clk);
        interrupt_req = 0;
        repeat(5) @(posedge clk);
    endtask

    task automatic test_multiple_interrupts();
        test_count++;
        $display("\n[TEST %0d] Multiple Successive Interrupts", test_count);
        
        for (int cycle = 0; cycle < 3; cycle++) begin
            $display("  -> Interrupt cycle %0d", cycle);
            interrupt_req = 0;
            repeat(5) @(posedge clk);
            
            interrupt_req = 1;
            repeat(5) @(posedge clk);
            
            if (!interrupt_ack) begin
                fail_count++;
                $display("  FAIL: No ack on cycle %0d", cycle);
                return;
            end
            
            interrupt_req = 0;
            repeat(5) @(posedge clk);
            
            if (interrupt_ack) begin
                fail_count++;
                $display("  FAIL: Ack stuck on cycle %0d", cycle);
                return;
            end
        end
        
        pass_count++;
        $display("  PASS");
    endtask

    task automatic test_reset_behavior();
        test_count++;
        $display("\n[TEST %0d] Reset Behavior", test_count);
        
        // Get into acknowledged state
        interrupt_req = 1;
        repeat(5) @(posedge clk);
        
        // Apply reset
        resetn = 0;
        repeat(5) @(posedge clk);
        
        // Check ack is low after reset
        if (!interrupt_ack) begin
            pass_count++;
            $display("  PASS: Ack low after reset");
        end else begin
            fail_count++;
            $display("  FAIL: Ack not cleared by reset");
        end
        
        // Release reset
        resetn = 1;
        interrupt_req = 0;
        repeat(5) @(posedge clk);
    endtask

    task automatic test_hold_requirement();
        test_count++;
        $display("\n[TEST %0d] Hold Requirement", test_count);
        
        // Assert request
        interrupt_req = 1;
        repeat(5) @(posedge clk);
        
        // Verify ack stays high while req is high
        for (int i = 0; i < 5; i++) begin
            @(posedge clk);
            if (!interrupt_ack && interrupt_req) begin
                fail_count++;
                $display("  FAIL: Ack dropped while req high");
                interrupt_req = 0;
                return;
            end
        end
        
        pass_count++;
        $display("  PASS");
        
        interrupt_req = 0;
        repeat(5) @(posedge clk);
    endtask

    // =========================================================================
    // MAIN TEST SEQUENCE
    // =========================================================================

    initial begin
        $dumpfile("axi4_top_tb.vcd");
        $dumpvars(0, axi4_top_tb);
        $display("================================================================");
        $display(" AXI4 Interrupt Controller Testbench");
        $display("================================================================");
        
        reset_dut();
        
        test_basic_handshake();
        test_ack_timing();
        test_hold_requirement();
        test_multiple_interrupts();
        test_reset_behavior();
        
        repeat(100) @(posedge clk);
        
        $display("\n================================================================");
        $display(" Test Summary: %0d tests, %0d passed, %0d failed", 
                 test_count, pass_count, fail_count);
        $display("================================================================");
        
        if (fail_count == 0)
            $display(" ALL TESTS PASSED!");
        else
            $display(" SOME TESTS FAILED!");
        
        $finish;
    end

    // Timeout
    initial begin
        repeat(TIMEOUT_CYCLES) @(posedge clk);
        $display("ERROR: Timeout!");
        $finish;
    end

endmodule

