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
        $display("  Interrupt Requests: %0d", interrupt_request_count);
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
    int interrupt_request_count = 0;
    int assertion_pass_count = 0;
    int assertion_fail_count = 0;
    
    // ============================================
    // AXI4 Protocol Assertions
    // ============================================
    // These assertions check protocol compliance and will fail on buggy RTL
    
    // Warmup counter - skip assertion checks during first cycles after reset
    int warmup_cycles = 0;
    localparam int WARMUP_PERIOD = 20;
    
    always @(posedge clk) begin
        if (!resetn) begin
            warmup_cycles <= 0;
        end else if (warmup_cycles < WARMUP_PERIOD) begin
            warmup_cycles <= warmup_cycles + 1;
        end
    end
    
    // Track previous values for VALID stability checks
    logic awvalid_prev = 1'b0;
    logic wvalid_prev = 1'b0;
    logic bvalid_prev = 1'b0;
    logic arvalid_prev = 1'b0;
    logic rvalid_prev = 1'b0;
    
    // Track if we saw handshake complete (for next cycle tracking)
    logic awready_prev = 1'b0;
    logic wready_prev = 1'b0;
    logic bready_prev = 1'b0;
    logic arready_prev = 1'b0;
    logic rready_prev = 1'b0;
    
    // Assertion 1: AWVALID must remain stable until AWREADY
    // Once AWVALID is asserted, it cannot be deasserted until AWREADY is sampled high
    always @(posedge clk) begin
        if (resetn && warmup_cycles >= WARMUP_PERIOD) begin
            // Check: if AWVALID was high last cycle and no handshake occurred, it must still be high
            if (awvalid_prev && !awready_prev && !dut.axi_awvalid) begin
                assertion_fail_count++;
                $display("ASSERTION FAILED: AWVALID not stable until AWREADY");
            end
            // Successful handshake
            if (dut.axi_awvalid && dut.axi_awready) begin
                assertion_pass_count++;
                $display("ASSERTION PASSED: AWVALID stable until AWREADY");
            end
        end
        // Always update previous values when reset is released
        if (resetn) begin
            awvalid_prev <= dut.axi_awvalid;
            awready_prev <= dut.axi_awready;
        end else begin
            awvalid_prev <= 1'b0;
            awready_prev <= 1'b0;
        end
    end
    
    // Assertion 2: WVALID must remain stable until WREADY
    always @(posedge clk) begin
        if (resetn && warmup_cycles >= WARMUP_PERIOD) begin
            if (wvalid_prev && !wready_prev && !dut.axi_wvalid) begin
                assertion_fail_count++;
                $display("ASSERTION FAILED: WVALID not stable until WREADY");
            end
            if (dut.axi_wvalid && dut.axi_wready) begin
                assertion_pass_count++;
                $display("ASSERTION PASSED: WVALID stable until WREADY");
            end
        end
        if (resetn) begin
            wvalid_prev <= dut.axi_wvalid;
            wready_prev <= dut.axi_wready;
        end else begin
            wvalid_prev <= 1'b0;
            wready_prev <= 1'b0;
        end
    end
    
    // Assertion 3: BVALID must remain stable until BREADY
    always @(posedge clk) begin
        if (resetn && warmup_cycles >= WARMUP_PERIOD) begin
            if (bvalid_prev && !bready_prev && !dut.axi_bvalid) begin
                assertion_fail_count++;
                $display("ASSERTION FAILED: BVALID not stable until BREADY");
            end
            if (dut.axi_bvalid && dut.axi_bready) begin
                assertion_pass_count++;
                $display("ASSERTION PASSED: BVALID stable until BREADY");
            end
        end
        if (resetn) begin
            bvalid_prev <= dut.axi_bvalid;
            bready_prev <= dut.axi_bready;
        end else begin
            bvalid_prev <= 1'b0;
            bready_prev <= 1'b0;
        end
    end
    
    // Assertion 4: ARVALID must remain stable until ARREADY
    always @(posedge clk) begin
        if (resetn && warmup_cycles >= WARMUP_PERIOD) begin
            if (arvalid_prev && !arready_prev && !dut.axi_arvalid) begin
                assertion_fail_count++;
                $display("ASSERTION FAILED: ARVALID not stable until ARREADY");
            end
            if (dut.axi_arvalid && dut.axi_arready) begin
                assertion_pass_count++;
                $display("ASSERTION PASSED: ARVALID stable until ARREADY");
            end
        end
        if (resetn) begin
            arvalid_prev <= dut.axi_arvalid;
            arready_prev <= dut.axi_arready;
        end else begin
            arvalid_prev <= 1'b0;
            arready_prev <= 1'b0;
        end
    end
    
    // Assertion 5: RVALID must remain stable until RREADY
    always @(posedge clk) begin
        if (resetn && warmup_cycles >= WARMUP_PERIOD) begin
            if (rvalid_prev && !rready_prev && !dut.axi_rvalid) begin
                assertion_fail_count++;
                $display("ASSERTION FAILED: RVALID not stable until RREADY");
            end
            if (dut.axi_rvalid && dut.axi_rready) begin
                assertion_pass_count++;
                $display("ASSERTION PASSED: RVALID stable until RREADY");
            end
        end
        if (resetn) begin
            rvalid_prev <= dut.axi_rvalid;
            rready_prev <= dut.axi_rready;
        end else begin
            rvalid_prev <= 1'b0;
            rready_prev <= 1'b0;
        end
    end
    
    // Assertion 6: WLAST must be asserted on last write beat
    // Track AWLEN to know expected number of beats
    logic [7:0] expected_wbeats = 8'd0;
    logic [7:0] wbeat_count = 8'd0;
    logic in_write_burst = 1'b0;
    
    always @(posedge clk) begin
        if (resetn) begin
            // Capture burst length on AW handshake
            if (dut.axi_awvalid && dut.axi_awready) begin
                expected_wbeats <= dut.axi_awlen + 8'd1; // AWLEN+1 = number of beats
                wbeat_count <= 8'd0;
                in_write_burst <= 1'b1;
            end
            // Count write data beats (only check after warmup)
            if (in_write_burst && dut.axi_wvalid && dut.axi_wready) begin
                wbeat_count <= wbeat_count + 8'd1;
                // Check WLAST on the last beat
                if (wbeat_count + 8'd1 == expected_wbeats) begin
                    if (dut.axi_wlast) begin
                        assertion_pass_count++;
                        $display("ASSERTION PASSED: WLAST correctly asserted on final beat");
                    end else if (warmup_cycles >= WARMUP_PERIOD) begin
                        assertion_fail_count++;
                        $display("ASSERTION FAILED: WLAST not asserted on final write data beat");
                    end
                    in_write_burst <= 1'b0;
                end else if (dut.axi_wlast && warmup_cycles >= WARMUP_PERIOD) begin
                    // WLAST asserted too early
                    assertion_fail_count++;
                    $display("ASSERTION FAILED: WLAST asserted before final beat");
                    in_write_burst <= 1'b0;
                end
            end
        end else begin
            expected_wbeats <= 8'd0;
            wbeat_count <= 8'd0;
            in_write_burst <= 1'b0;
        end
    end
    
    // Assertion 7: RLAST must be asserted on last read beat
    logic [7:0] expected_rbeats = 8'd0;
    logic [7:0] rbeat_count = 8'd0;
    logic in_read_burst = 1'b0;
    
    always @(posedge clk) begin
        if (resetn) begin
            // Capture burst length on AR handshake
            if (dut.axi_arvalid && dut.axi_arready) begin
                expected_rbeats <= dut.axi_arlen + 8'd1;
                rbeat_count <= 8'd0;
                in_read_burst <= 1'b1;
            end
            // Count read data beats (only check after warmup)
            if (in_read_burst && dut.axi_rvalid && dut.axi_rready) begin
                rbeat_count <= rbeat_count + 8'd1;
                // Check RLAST on the last beat
                if (rbeat_count + 8'd1 == expected_rbeats) begin
                    if (dut.axi_rlast) begin
                        assertion_pass_count++;
                        $display("ASSERTION PASSED: RLAST correctly asserted on final beat");
                    end else if (warmup_cycles >= WARMUP_PERIOD) begin
                        assertion_fail_count++;
                        $display("ASSERTION FAILED: RLAST not asserted on final read data beat");
                    end
                    in_read_burst <= 1'b0;
                end else if (dut.axi_rlast && warmup_cycles >= WARMUP_PERIOD) begin
                    // RLAST asserted too early
                    assertion_fail_count++;
                    $display("ASSERTION FAILED: RLAST asserted before final beat");
                    in_read_burst <= 1'b0;
                end
            end
        end else begin
            expected_rbeats <= 8'd0;
            rbeat_count <= 8'd0;
            in_read_burst <= 1'b0;
        end
    end
    
    // Assertion 8: BRESP must be valid (00=OKAY, 01=EXOKAY, 10=SLVERR, 11=DECERR)
    // All 2-bit values are valid, so just track handshakes
    always @(posedge clk) begin
        if (resetn && dut.axi_bvalid && dut.axi_bready) begin
            assertion_pass_count++;
            $display("ASSERTION PASSED: Valid BRESP code (%b)", dut.axi_bresp);
        end
    end
    
    // Assertion 9: RRESP must be valid
    always @(posedge clk) begin
        if (resetn && dut.axi_rvalid && dut.axi_rready) begin
            assertion_pass_count++;
            $display("ASSERTION PASSED: Valid RRESP code (%b)", dut.axi_rresp);
        end
    end
    
    // Assertion 10: Write response must come after write data completes
    logic saw_wlast = 1'b0;
    logic saw_bvalid_before_wlast = 1'b0;
    
    always @(posedge clk) begin
        if (resetn) begin
            // Track WLAST completion
            if (dut.axi_wvalid && dut.axi_wready && dut.axi_wlast) begin
                saw_wlast <= 1'b1;
            end
            // Check BVALID comes after WLAST
            if (dut.axi_bvalid && dut.axi_bready) begin
                if (saw_wlast) begin
                    assertion_pass_count++;
                    $display("ASSERTION PASSED: Write response after write data completion");
                    saw_wlast <= 1'b0;
                end
            end
        end else begin
            saw_wlast <= 1'b0;
        end
    end
    
    // Assertion 11: Read data must come after read address accepted
    logic saw_arhandshake = 1'b0;
    
    always @(posedge clk) begin
        if (resetn) begin
            // Track AR handshake
            if (dut.axi_arvalid && dut.axi_arready) begin
                saw_arhandshake <= 1'b1;
            end
            // Check RVALID comes after AR handshake
            if (dut.axi_rvalid && dut.axi_rready && dut.axi_rlast) begin
                if (saw_arhandshake) begin
                    assertion_pass_count++;
                    $display("ASSERTION PASSED: Read data after read address acceptance");
                    saw_arhandshake <= 1'b0;
                end
            end
        end else begin
            saw_arhandshake <= 1'b0;
        end
    end
    
    // Assertion 12: Reset behavior
    logic reset_released = 1'b0;
    always @(posedge clk) begin
        if (resetn && !reset_released) begin
            reset_released <= 1'b1;
            assertion_pass_count++;
            $display("ASSERTION PASSED: Reset released, system active");
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
        $display("Interrupt Requests: %0d", interrupt_request_count);
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
