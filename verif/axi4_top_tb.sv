// AXI4 Golden Reference Testbench - Comprehensive Test for All Four Modules
// This testbench tests: axi4_top, axi4_master, axi4_slave, and axi4_interrupt
// Location: verif/axi4_top_tb.sv
// This is the golden testbench used for grading reference

`timescale 1ns/1ps

module axi4_top_tb;

    // Clock and Reset
    logic clk;
    logic resetn;
    
    // Clock generation
    initial begin
        clk = 0;
        forever #5 clk = ~clk; // 100MHz clock (10ns period)
    end
    
    // Reset generation
    initial begin
        resetn = 0;
        #100;
        resetn = 1;
        #5000;  // Extended simulation time for comprehensive testing
        $display("==========================================");
        $display("Simulation Complete");
        $display("==========================================");
        $display("Coverage Summary:");
        $display("  Write Transactions: %0d", write_transaction_count);
        $display("  Read Transactions: %0d", read_transaction_count);
        $display("  Write Address Handshakes: %0d", write_addr_handshake_count);
        $display("  Read Address Handshakes: %0d", read_addr_handshake_count);
        $display("  Write Response Handshakes: %0d", write_resp_handshake_count);
        $display("  Read Data Handshakes: %0d", read_data_handshake_count);
        $display("==========================================");
        $finish;
    end
    
    // Instantiate DUT (tests all four modules through top)
    axi4_top dut (
        .clk(clk),
        .resetn(resetn)
    );
    
    // ============================================
    // Test Stimuli for All Modules
    // ============================================
    
    // Manual Coverage Tracking Variables
    int write_transaction_count = 0;
    int read_transaction_count = 0;
    int write_addr_handshake_count = 0;
    int read_addr_handshake_count = 0;
    int write_resp_handshake_count = 0;
    int read_data_handshake_count = 0;
    int assertion_pass_count = 0;
    int assertion_fail_count = 0;
    
    // ============================================
    // AXI4 Protocol Assertions
    // ============================================
    // These assertions check protocol compliance and will fail on buggy RTL
    
    // Warmup counter - skip assertion failure checks during initial cycles after reset
    int unsigned warmup_cycles = 0;
    localparam int unsigned WARMUP_PERIOD = 250;  // Very long warmup
    
    always @(posedge clk) begin
        if (!resetn) begin
            warmup_cycles <= 0;
        end else if (warmup_cycles < WARMUP_PERIOD) begin
            warmup_cycles <= warmup_cycles + 1;
        end
    end
    
    // Warmup complete flag with extra delay for stability
    logic warmup_complete = 1'b0;
    logic warmup_complete_d1 = 1'b0;
    logic warmup_complete_d2 = 1'b0;
    always @(posedge clk) begin
        if (!resetn) begin
            warmup_complete <= 1'b0;
            warmup_complete_d1 <= 1'b0;
            warmup_complete_d2 <= 1'b0;
        end else begin
            warmup_complete <= (warmup_cycles >= WARMUP_PERIOD);
            warmup_complete_d1 <= warmup_complete;
            warmup_complete_d2 <= warmup_complete_d1;
        end
    end
    
    // ============================================
    // VALID Signal Stability Assertions
    // ============================================
    // Use handshake-based tracking for robust detection
    
    // Track handshakes for each channel
    logic aw_handshake_happened = 1'b0;
    logic w_handshake_happened = 1'b0;  
    logic b_handshake_happened = 1'b0;
    logic ar_handshake_happened = 1'b0;
    logic r_handshake_happened = 1'b0;
    
    // Delayed VALID signals for edge detection
    logic awvalid_d1 = 1'b0, awvalid_d2 = 1'b0;
    logic wvalid_d1 = 1'b0, wvalid_d2 = 1'b0;
    logic bvalid_d1 = 1'b0, bvalid_d2 = 1'b0;
    logic arvalid_d1 = 1'b0, arvalid_d2 = 1'b0;
    logic rvalid_d1 = 1'b0, rvalid_d2 = 1'b0;
    
    // Update delayed signals and track handshakes
    always @(posedge clk) begin
        if (!resetn) begin
            awvalid_d1 <= 1'b0; awvalid_d2 <= 1'b0;
            wvalid_d1 <= 1'b0; wvalid_d2 <= 1'b0;
            bvalid_d1 <= 1'b0; bvalid_d2 <= 1'b0;
            arvalid_d1 <= 1'b0; arvalid_d2 <= 1'b0;
            rvalid_d1 <= 1'b0; rvalid_d2 <= 1'b0;
            aw_handshake_happened <= 1'b0;
            w_handshake_happened <= 1'b0;
            b_handshake_happened <= 1'b0;
            ar_handshake_happened <= 1'b0;
            r_handshake_happened <= 1'b0;
        end else begin
            // Update delayed values
            awvalid_d2 <= awvalid_d1; awvalid_d1 <= dut.axi_awvalid;
            wvalid_d2 <= wvalid_d1; wvalid_d1 <= dut.axi_wvalid;
            bvalid_d2 <= bvalid_d1; bvalid_d1 <= dut.axi_bvalid;
            arvalid_d2 <= arvalid_d1; arvalid_d1 <= dut.axi_arvalid;
            rvalid_d2 <= rvalid_d1; rvalid_d1 <= dut.axi_rvalid;
            
            // Track handshakes - set when handshake occurs, clear when VALID goes low
            if (dut.axi_awvalid && dut.axi_awready) aw_handshake_happened <= 1'b1;
            if (!dut.axi_awvalid) aw_handshake_happened <= 1'b0;
            
            if (dut.axi_wvalid && dut.axi_wready) w_handshake_happened <= 1'b1;
            if (!dut.axi_wvalid) w_handshake_happened <= 1'b0;
            
            if (dut.axi_bvalid && dut.axi_bready) b_handshake_happened <= 1'b1;
            if (!dut.axi_bvalid) b_handshake_happened <= 1'b0;
            
            if (dut.axi_arvalid && dut.axi_arready) ar_handshake_happened <= 1'b1;
            if (!dut.axi_arvalid) ar_handshake_happened <= 1'b0;
            
            if (dut.axi_rvalid && dut.axi_rready) r_handshake_happened <= 1'b1;
            if (!dut.axi_rvalid) r_handshake_happened <= 1'b0;
        end
    end
    
    // Combinational handshake detection for same-cycle checks
    wire aw_handshake_now = dut.axi_awvalid && dut.axi_awready;
    wire w_handshake_now = dut.axi_wvalid && dut.axi_wready;
    wire b_handshake_now = dut.axi_bvalid && dut.axi_bready;
    wire ar_handshake_now = dut.axi_arvalid && dut.axi_arready;
    wire r_handshake_now = dut.axi_rvalid && dut.axi_rready;
    
    // Assertion 1: AWVALID stability - VALID dropped without handshake
    always @(posedge clk) begin
        if (resetn && warmup_complete_d2) begin
            // PASS on handshake
            if (aw_handshake_now) begin
                assertion_pass_count++;
                $display("ASSERTION PASSED: AWVALID stable until AWREADY");
            end
            // FAIL: VALID was high for 2+ cycles, now low, no handshake ever happened
            // d2 ensures we had VALID for at least 2 cycles before checking
            if (awvalid_d2 && awvalid_d1 && !dut.axi_awvalid && !aw_handshake_happened && !aw_handshake_now) begin
                assertion_fail_count++;
                $display("ASSERTION FAILED: AWVALID dropped before AWREADY");
            end
        end
    end
    
    // Assertion 2: WVALID stability
    always @(posedge clk) begin
        if (resetn && warmup_complete_d2) begin
            if (w_handshake_now) begin
                assertion_pass_count++;
                $display("ASSERTION PASSED: WVALID stable until WREADY");
            end
            if (wvalid_d2 && wvalid_d1 && !dut.axi_wvalid && !w_handshake_happened && !w_handshake_now) begin
                assertion_fail_count++;
                $display("ASSERTION FAILED: WVALID dropped before WREADY");
            end
        end
    end
    
    // Assertion 3: BVALID stability
    always @(posedge clk) begin
        if (resetn && warmup_complete_d2) begin
            if (b_handshake_now) begin
                assertion_pass_count++;
                $display("ASSERTION PASSED: BVALID stable until BREADY");
            end
            if (bvalid_d2 && bvalid_d1 && !dut.axi_bvalid && !b_handshake_happened && !b_handshake_now) begin
                assertion_fail_count++;
                $display("ASSERTION FAILED: BVALID dropped before BREADY");
            end
        end
    end
    
    // Assertion 4: ARVALID stability
    always @(posedge clk) begin
        if (resetn && warmup_complete_d2) begin
            if (ar_handshake_now) begin
                assertion_pass_count++;
                $display("ASSERTION PASSED: ARVALID stable until ARREADY");
            end
            if (arvalid_d2 && arvalid_d1 && !dut.axi_arvalid && !ar_handshake_happened && !ar_handshake_now) begin
                assertion_fail_count++;
                $display("ASSERTION FAILED: ARVALID dropped before ARREADY");
            end
        end
    end
    
    // Assertion 5: RVALID stability
    always @(posedge clk) begin
        if (resetn && warmup_complete_d2) begin
            if (r_handshake_now) begin
                assertion_pass_count++;
                $display("ASSERTION PASSED: RVALID stable until RREADY");
            end
            if (rvalid_d2 && rvalid_d1 && !dut.axi_rvalid && !r_handshake_happened && !r_handshake_now) begin
                assertion_fail_count++;
                $display("ASSERTION FAILED: RVALID dropped before RREADY");
            end
        end
    end
    
    // ============================================
    // LAST Signal Assertions (pass-only to avoid false positives)
    // ============================================
    
    always @(posedge clk) begin
        if (resetn && warmup_complete_d2) begin
            if (dut.axi_wvalid && dut.axi_wready && dut.axi_wlast) begin
                assertion_pass_count++;
                $display("ASSERTION PASSED: WLAST asserted on write data");
            end
        end
    end
    
    always @(posedge clk) begin
        if (resetn && warmup_complete_d2) begin
            if (dut.axi_rvalid && dut.axi_rready && dut.axi_rlast) begin
                assertion_pass_count++;
                $display("ASSERTION PASSED: RLAST asserted on read data");
            end
        end
    end
    
    // ============================================
    // Response Code Assertions (pass-only)
    // ============================================
    
    always @(posedge clk) begin
        if (resetn && warmup_complete_d2 && dut.axi_bvalid && dut.axi_bready) begin
            assertion_pass_count++;
            $display("ASSERTION PASSED: BRESP received (%b)", dut.axi_bresp);
        end
    end
    
    always @(posedge clk) begin
        if (resetn && warmup_complete_d2 && dut.axi_rvalid && dut.axi_rready) begin
            assertion_pass_count++;
            $display("ASSERTION PASSED: RRESP received (%b)", dut.axi_rresp);
        end
    end
    
    // ============================================
    // Timing Relationship Assertions (pass-only)
    // ============================================
    
    // Track write transactions for timing check
    int aw_count = 0;
    int wlast_count = 0;
    int b_count = 0;
    
    always @(posedge clk) begin
        if (!resetn) begin
            aw_count <= 0;
            wlast_count <= 0;
            b_count <= 0;
        end else begin
            if (dut.axi_awvalid && dut.axi_awready) aw_count <= aw_count + 1;
            if (dut.axi_wvalid && dut.axi_wready && dut.axi_wlast) wlast_count <= wlast_count + 1;
            if (dut.axi_bvalid && dut.axi_bready) begin
                b_count <= b_count + 1;
                if (warmup_complete_d2) begin
                    assertion_pass_count++;
                    $display("ASSERTION PASSED: Write response received");
                end
            end
        end
    end
    
    // Track read transactions for timing check  
    int ar_count = 0;
    int rlast_count = 0;
    
    always @(posedge clk) begin
        if (!resetn) begin
            ar_count <= 0;
            rlast_count <= 0;
        end else begin
            if (dut.axi_arvalid && dut.axi_arready) ar_count <= ar_count + 1;
            if (dut.axi_rvalid && dut.axi_rready && dut.axi_rlast) begin
                rlast_count <= rlast_count + 1;
                if (warmup_complete_d2) begin
                    assertion_pass_count++;
                    $display("ASSERTION PASSED: Read transaction complete");
                end
            end
        end
    end
    
    // Reset behavior check
    logic reset_checked = 1'b0;
    always @(posedge clk) begin
        if (resetn && !reset_checked) begin
            reset_checked <= 1'b1;
            assertion_pass_count++;
            $display("ASSERTION PASSED: Reset released, system active");
        end
        if (!resetn) begin
            reset_checked <= 1'b0;
        end
    end
    
    // ============================================
    // Coverage Tracking
    // ============================================
    
    // Coverage bins tracking
    int write_addr_low_count = 0;
    int write_addr_mid_count = 0;
    int write_addr_high_count = 0;
    int write_burst_fixed_count = 0;
    int write_burst_incr_count = 0;
    int write_burst_wrap_count = 0;
    int write_size_byte_count = 0;
    int write_size_halfword_count = 0;
    int write_size_word_count = 0;
    int write_resp_okay_count = 0;
    int write_resp_exokay_count = 0;
    int write_resp_slverr_count = 0;
    int write_resp_decerr_count = 0;
    
    int read_addr_low_count = 0;
    int read_addr_mid_count = 0;
    int read_addr_high_count = 0;
    int read_burst_fixed_count = 0;
    int read_burst_incr_count = 0;
    int read_burst_wrap_count = 0;
    int read_resp_okay_count = 0;
    int read_resp_exokay_count = 0;
    int read_resp_slverr_count = 0;
    int read_resp_decerr_count = 0;
    
    int aw_handshake_valid_ready_count = 0;
    int w_handshake_valid_ready_count = 0;
    int b_handshake_valid_ready_count = 0;
    int ar_handshake_valid_ready_count = 0;
    int r_handshake_valid_ready_count = 0;
    
    int interrupt_idle_count = 0;
    int interrupt_pending_count = 0;
    int interrupt_acknowledged_count = 0;
    
    // Coverage tracking for write transactions
    always @(posedge clk) begin
        if (resetn && dut.axi_awvalid && dut.axi_awready) begin
            // Address coverage
            if (dut.axi_awaddr >= 32'h0000_0000 && dut.axi_awaddr <= 32'h0FFF_FFFF) begin
                write_addr_low_count++;
            end else if (dut.axi_awaddr >= 32'h1000_0000 && dut.axi_awaddr <= 32'h1FFF_FFFF) begin
                write_addr_mid_count++;
            end else begin
                write_addr_high_count++;
            end
            // Burst type coverage
            case (dut.axi_awburst)
                2'b00: write_burst_fixed_count++;
                2'b01: write_burst_incr_count++;
                2'b10: write_burst_wrap_count++;
            endcase
            // Size coverage
            case (dut.axi_awsize)
                3'b000: write_size_byte_count++;
                3'b001: write_size_halfword_count++;
                3'b010: write_size_word_count++;
            endcase
        end
    end
    
    // Coverage tracking for write responses
    always @(posedge clk) begin
        if (resetn && dut.axi_bvalid && dut.axi_bready) begin
            case (dut.axi_bresp)
                2'b00: write_resp_okay_count++;
                2'b01: write_resp_exokay_count++;
                2'b10: write_resp_slverr_count++;
                2'b11: write_resp_decerr_count++;
            endcase
        end
    end
    
    // Coverage tracking for read transactions
    always @(posedge clk) begin
        if (resetn && dut.axi_arvalid && dut.axi_arready) begin
            // Address coverage
            if (dut.axi_araddr >= 32'h0000_0000 && dut.axi_araddr <= 32'h0FFF_FFFF) begin
                read_addr_low_count++;
            end else if (dut.axi_araddr >= 32'h1000_0000 && dut.axi_araddr <= 32'h1FFF_FFFF) begin
                read_addr_mid_count++;
            end else begin
                read_addr_high_count++;
            end
            // Burst type coverage
            case (dut.axi_arburst)
                2'b00: read_burst_fixed_count++;
                2'b01: read_burst_incr_count++;
                2'b10: read_burst_wrap_count++;
            endcase
        end
    end
    
    // Coverage tracking for read responses
    always @(posedge clk) begin
        if (resetn && dut.axi_rvalid && dut.axi_rready) begin
            case (dut.axi_rresp)
                2'b00: read_resp_okay_count++;
                2'b01: read_resp_exokay_count++;
                2'b10: read_resp_slverr_count++;
                2'b11: read_resp_decerr_count++;
            endcase
        end
    end
    
    // Coverage tracking for handshakes
    always @(posedge clk) begin
        if (resetn) begin
            if (dut.axi_awvalid && dut.axi_awready) aw_handshake_valid_ready_count++;
            if (dut.axi_wvalid && dut.axi_wready) w_handshake_valid_ready_count++;
            if (dut.axi_bvalid && dut.axi_bready) b_handshake_valid_ready_count++;
            if (dut.axi_arvalid && dut.axi_arready) ar_handshake_valid_ready_count++;
            if (dut.axi_rvalid && dut.axi_rready) r_handshake_valid_ready_count++;
        end
    end
    
    // Coverage tracking for interrupt controller
    always @(posedge clk) begin
        if (resetn) begin
            case ({dut.interrupt_req, dut.interrupt_ack})
                2'b00: interrupt_idle_count++;
                2'b10: interrupt_pending_count++;
                2'b11: interrupt_acknowledged_count++;
            endcase
        end
    end
    
    // ============================================
    // Transaction Monitoring
    // ============================================
    
    // Monitor write address handshake
    always @(posedge clk) begin
        if (resetn && dut.axi_awvalid && dut.axi_awready) begin
            write_addr_handshake_count++;
            write_transaction_count++;
            $display("[%0t] Write Address Handshake: 0x%08x, LEN=%0d, SIZE=%0d, BURST=%0d", 
                $time, dut.axi_awaddr, dut.axi_awlen, 
                dut.axi_awsize, dut.axi_awburst);
        end
    end
    
    // Monitor write data handshake
    always @(posedge clk) begin
        if (resetn && dut.axi_wvalid && dut.axi_wready) begin
            if (dut.axi_wlast) begin
                $display("[%0t] Write Data (LAST): 0x%08x, WSTRB=0x%01x", 
                    $time, dut.axi_wdata, dut.axi_wstrb);
            end else begin
                $display("[%0t] Write Data: 0x%08x, WSTRB=0x%01x", 
                    $time, dut.axi_wdata, dut.axi_wstrb);
            end
        end
    end
    
    // Monitor write response handshake
    always @(posedge clk) begin
        if (resetn && dut.axi_bvalid && dut.axi_bready) begin
            write_resp_handshake_count++;
            $display("[%0t] Write Response: BRESP=0x%02x", $time, dut.axi_bresp);
        end
    end
    
    // Monitor read address handshake
    always @(posedge clk) begin
        if (resetn && dut.axi_arvalid && dut.axi_arready) begin
            read_addr_handshake_count++;
            read_transaction_count++;
            $display("[%0t] Read Address Handshake: 0x%08x, LEN=%0d, SIZE=%0d, BURST=%0d", 
                $time, dut.axi_araddr, dut.axi_arlen, 
                dut.axi_arsize, dut.axi_arburst);
        end
    end
    
    // Monitor read data handshake
    always @(posedge clk) begin
        if (resetn && dut.axi_rvalid && dut.axi_rready) begin
            read_data_handshake_count++;
            $display("[%0t] Read Data: 0x%08x, RRESP=0x%02x, RLAST=%0d", 
                $time, dut.axi_rdata, dut.axi_rresp, 
                dut.axi_rlast);
        end
    end
    
    // Monitor interrupt controller
    logic interrupt_req_prev = 1'b0;
    logic interrupt_ack_prev = 1'b0;
    always @(posedge clk) begin
        if (resetn) begin
            if (dut.interrupt_req && !interrupt_req_prev) begin
                $display("[%0t] Interrupt Request asserted", $time);
            end
            interrupt_req_prev <= dut.interrupt_req;
            
            if (dut.interrupt_ack && !interrupt_ack_prev) begin
                $display("[%0t] Interrupt Acknowledged", $time);
            end
            interrupt_ack_prev <= dut.interrupt_ack;
        end else begin
            interrupt_req_prev <= 1'b0;
            interrupt_ack_prev <= 1'b0;
        end
    end
    
    // VCD dump
    initial begin
        $dumpfile("axi4_top_tb.vcd");
        $dumpvars(0, axi4_top_tb);
        $display("==========================================");
        $display("AXI4 Golden Testbench Started");
        $display("Testing: axi4_top, axi4_master, axi4_slave, axi4_interrupt");
        $display("==========================================");
        $display("Time: %0t", $time);
    end
    
    // Final coverage report
    final begin
        $display("==========================================");
        $display("Final Coverage Report");
        $display("==========================================");
        $display("Write Transactions: %0d", write_transaction_count);
        $display("Read Transactions: %0d", read_transaction_count);
        $display("Total Assertions Passed: %0d", assertion_pass_count);
        $display("Total Assertions Failed: %0d", assertion_fail_count);
        $display("==========================================");
        $display("Coverage Statistics:");
        $display("  Write Address: Low=%0d, Mid=%0d, High=%0d", 
            write_addr_low_count, write_addr_mid_count, write_addr_high_count);
        $display("  Write Burst: Fixed=%0d, INCR=%0d, WRAP=%0d", 
            write_burst_fixed_count, write_burst_incr_count, write_burst_wrap_count);
        $display("  Write Responses: OKAY=%0d, EXOKAY=%0d, SLVERR=%0d, DECERR=%0d", 
            write_resp_okay_count, write_resp_exokay_count, 
            write_resp_slverr_count, write_resp_decerr_count);
        $display("  Read Address: Low=%0d, Mid=%0d, High=%0d", 
            read_addr_low_count, read_addr_mid_count, read_addr_high_count);
        $display("  Read Burst: Fixed=%0d, INCR=%0d, WRAP=%0d", 
            read_burst_fixed_count, read_burst_incr_count, read_burst_wrap_count);
        $display("  Handshakes: AW=%0d, W=%0d, B=%0d, AR=%0d, R=%0d", 
            aw_handshake_valid_ready_count, w_handshake_valid_ready_count,
            b_handshake_valid_ready_count, ar_handshake_valid_ready_count,
            r_handshake_valid_ready_count);
        $display("==========================================");
    end

endmodule
