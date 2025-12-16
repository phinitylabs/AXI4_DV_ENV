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
        #10000;  // Extended simulation time to see activity after warmup
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
    
    // Instantiate DUT
    axi4_top dut (
        .clk(clk),
        .resetn(resetn)
    );
    
    // Manual Coverage Tracking Variables
    int write_transaction_count = 0;
    int read_transaction_count = 0;
    int write_addr_handshake_count = 0;
    int read_addr_handshake_count = 0;
    int write_resp_handshake_count = 0;
    int read_data_handshake_count = 0;
    int assertion_pass_count = 0;
    int assertion_fail_count = 0;
    
    // Warmup counter - minimal to catch early transactions  
    int unsigned warmup_cycles = 0;
    localparam int unsigned WARMUP_PERIOD = 1;  // 1 cycle warmup after reset
    
    always @(posedge clk) begin
        if (!resetn) begin
            warmup_cycles <= 0;
        end else if (warmup_cycles < WARMUP_PERIOD) begin
            warmup_cycles <= warmup_cycles + 1;
        end
    end
    
    // Use combinational logic for warmup_complete to avoid one-cycle delay
    wire warmup_complete = (warmup_cycles >= WARMUP_PERIOD);
    
    // ============================================
    // Previous cycle signal tracking for stability checks
    // ============================================
    logic awvalid_prev, arvalid_prev, wvalid_prev, bvalid_prev, rvalid_prev;
    logic awready_prev, arready_prev, wready_prev, bready_prev, rready_prev;
    
    always @(posedge clk) begin
        if (!resetn) begin
            awvalid_prev <= 1'b0;
            arvalid_prev <= 1'b0;
            wvalid_prev <= 1'b0;
            bvalid_prev <= 1'b0;
            rvalid_prev <= 1'b0;
            awready_prev <= 1'b0;
            arready_prev <= 1'b0;
            wready_prev <= 1'b0;
            bready_prev <= 1'b0;
            rready_prev <= 1'b0;
        end else begin
            awvalid_prev <= dut.axi_awvalid;
            arvalid_prev <= dut.axi_arvalid;
            wvalid_prev <= dut.axi_wvalid;
            bvalid_prev <= dut.axi_bvalid;
            rvalid_prev <= dut.axi_rvalid;
            awready_prev <= dut.axi_awready;
            arready_prev <= dut.axi_arready;
            wready_prev <= dut.axi_wready;
            bready_prev <= dut.axi_bready;
            rready_prev <= dut.axi_rready;
        end
    end
    
    // ============================================
    // Activity Counters for Bug Detection
    // ============================================
    int total_aw_handshakes = 0;
    int total_w_handshakes = 0;
    int total_b_handshakes = 0;
    int total_ar_handshakes = 0;
    int total_r_handshakes = 0;
    int total_wlast_seen = 0;
    int total_rlast_seen = 0;
    
    // Track when VALID signals have ever been seen high
    logic awvalid_ever_seen = 1'b0;
    logic arvalid_ever_seen = 1'b0;
    logic wvalid_ever_seen = 1'b0;
    logic bvalid_ever_seen = 1'b0;
    logic rvalid_ever_seen = 1'b0;
    
    always @(posedge clk) begin
        if (!resetn) begin
            awvalid_ever_seen <= 1'b0;
            arvalid_ever_seen <= 1'b0;
            wvalid_ever_seen <= 1'b0;
            bvalid_ever_seen <= 1'b0;
            rvalid_ever_seen <= 1'b0;
        end else if (warmup_complete) begin
            if (dut.axi_awvalid) awvalid_ever_seen <= 1'b1;
            if (dut.axi_arvalid) arvalid_ever_seen <= 1'b1;
            if (dut.axi_wvalid) wvalid_ever_seen <= 1'b1;
            if (dut.axi_bvalid) bvalid_ever_seen <= 1'b1;
            if (dut.axi_rvalid) rvalid_ever_seen <= 1'b1;
        end
    end
    
    always @(posedge clk) begin
        if (resetn && warmup_complete) begin
            if (dut.axi_awvalid && dut.axi_awready) total_aw_handshakes++;
            if (dut.axi_wvalid && dut.axi_wready) total_w_handshakes++;
            if (dut.axi_bvalid && dut.axi_bready) total_b_handshakes++;
            if (dut.axi_arvalid && dut.axi_arready) total_ar_handshakes++;
            if (dut.axi_rvalid && dut.axi_rready) total_r_handshakes++;
            if (dut.axi_wvalid && dut.axi_wready && dut.axi_wlast) total_wlast_seen++;
            if (dut.axi_rvalid && dut.axi_rready && dut.axi_rlast) total_rlast_seen++;
        end
    end
    
    // ============================================
    // VALID Stability Assertions (AXI Protocol)
    // ============================================
    // Rule: Once VALID is asserted, it must remain asserted until READY
    // Detection: VALID drops (1->0) while READY was not asserted
    
    // AWVALID stability check
    always @(posedge clk) begin
        if (resetn && warmup_complete) begin
            // Check if AWVALID dropped while AWREADY was not asserted
            if (awvalid_prev && !dut.axi_awvalid && !awready_prev) begin
                assertion_fail_count++;
                $display("ASSERTION FAILED: AWVALID not stable until AWREADY");
            end else if (dut.axi_awvalid && dut.axi_awready) begin
                assertion_pass_count++;
                $display("ASSERTION PASSED: AWVALID/AWREADY handshake");
            end
        end
    end
    
    // ARVALID stability check
    always @(posedge clk) begin
        if (resetn && warmup_complete) begin
            if (arvalid_prev && !dut.axi_arvalid && !arready_prev) begin
                assertion_fail_count++;
                $display("ASSERTION FAILED: ARVALID not stable until ARREADY");
            end else if (dut.axi_arvalid && dut.axi_arready) begin
                assertion_pass_count++;
                $display("ASSERTION PASSED: ARVALID/ARREADY handshake");
            end
        end
    end
    
    // WVALID stability check
    always @(posedge clk) begin
        if (resetn && warmup_complete) begin
            if (wvalid_prev && !dut.axi_wvalid && !wready_prev) begin
                assertion_fail_count++;
                $display("ASSERTION FAILED: WVALID not stable until WREADY");
            end else if (dut.axi_wvalid && dut.axi_wready) begin
                assertion_pass_count++;
                $display("ASSERTION PASSED: WVALID/WREADY handshake");
            end
        end
    end
    
    // BVALID stability check
    always @(posedge clk) begin
        if (resetn && warmup_complete) begin
            if (bvalid_prev && !dut.axi_bvalid && !bready_prev) begin
                assertion_fail_count++;
                $display("ASSERTION FAILED: BVALID not stable until BREADY");
            end else if (dut.axi_bvalid && dut.axi_bready) begin
                assertion_pass_count++;
                $display("ASSERTION PASSED: BVALID/BREADY handshake");
            end
        end
    end
    
    // RVALID stability check
    always @(posedge clk) begin
        if (resetn && warmup_complete) begin
            if (rvalid_prev && !dut.axi_rvalid && !rready_prev) begin
                assertion_fail_count++;
                $display("ASSERTION FAILED: RVALID not stable until RREADY");
            end else if (dut.axi_rvalid && dut.axi_rready) begin
                assertion_pass_count++;
                $display("ASSERTION PASSED: RVALID/RREADY handshake");
            end
        end
    end
    
    // ============================================
    // WLAST/RLAST Assertions
    // ============================================
    // Track write burst and check WLAST at final beat
    
    int write_beat_count = 0;
    int write_burst_len = 0;
    logic write_burst_active = 1'b0;
    
    always @(posedge clk) begin
        if (!resetn) begin
            write_beat_count <= 0;
            write_burst_len <= 0;
            write_burst_active <= 1'b0;
        end else if (warmup_complete) begin
            // Start of write burst (AW handshake)
            if (dut.axi_awvalid && dut.axi_awready) begin
                write_burst_active <= 1'b1;
                write_burst_len <= dut.axi_awlen + 1; // AWLEN+1 beats
                write_beat_count <= 0;
            end
            
            // Track write data beats
            if (write_burst_active && dut.axi_wvalid && dut.axi_wready) begin
                write_beat_count <= write_beat_count + 1;
                if (dut.axi_wlast) begin
                    // Check WLAST on final beat
                    if (write_beat_count + 1 == write_burst_len) begin
                        assertion_pass_count++;
                        $display("ASSERTION PASSED: WLAST asserted on final beat");
                    end
                    write_burst_active <= 1'b0;
                end else if (write_beat_count + 1 == write_burst_len) begin
                    // Final beat but WLAST not asserted
                    assertion_fail_count++;
                    $display("ASSERTION FAILED: WLAST not asserted on final beat");
                    write_burst_active <= 1'b0;
                end
            end
        end
    end
    
    // Track read burst and check RLAST at final beat
    int read_beat_count = 0;
    int read_burst_len = 0;
    logic read_burst_active = 1'b0;
    
    always @(posedge clk) begin
        if (!resetn) begin
            read_beat_count <= 0;
            read_burst_len <= 0;
            read_burst_active <= 1'b0;
        end else if (warmup_complete) begin
            // Start of read burst (AR handshake)
            if (dut.axi_arvalid && dut.axi_arready) begin
                read_burst_active <= 1'b1;
                read_burst_len <= dut.axi_arlen + 1; // ARLEN+1 beats
                read_beat_count <= 0;
            end
            
            // Track read data beats
            if (read_burst_active && dut.axi_rvalid && dut.axi_rready) begin
                read_beat_count <= read_beat_count + 1;
                if (dut.axi_rlast) begin
                    // Check RLAST on final beat
                    if (read_beat_count + 1 == read_burst_len) begin
                        assertion_pass_count++;
                        $display("ASSERTION PASSED: RLAST asserted on final beat");
                    end
                    read_burst_active <= 1'b0;
                end else if (read_beat_count + 1 == read_burst_len) begin
                    // Final beat but RLAST not asserted
                    assertion_fail_count++;
                    $display("ASSERTION FAILED: RLAST not asserted on final beat");
                    read_burst_active <= 1'b0;
                end
            end
        end
    end
    
    // ============================================
    // Response Code Validation
    // ============================================
    // All 2-bit values are valid AXI responses, so we just log them
    
    always @(posedge clk) begin
        if (resetn && warmup_complete && dut.axi_bvalid && dut.axi_bready) begin
            assertion_pass_count++;
            $display("ASSERTION PASSED: Valid BRESP (%b)", dut.axi_bresp);
        end
    end
    
    always @(posedge clk) begin
        if (resetn && warmup_complete && dut.axi_rvalid && dut.axi_rready) begin
            assertion_pass_count++;
            $display("ASSERTION PASSED: Valid RRESP (%b)", dut.axi_rresp);
        end
    end
    
    // ============================================
    // Timing Relationship Checks with Timeout
    // ============================================
    // Write response must follow write data completion
    // Read data must follow read address acceptance
    
    logic aw_seen = 1'b0;
    logic wlast_handshake_seen = 1'b0;
    int aw_timeout_counter = 0;
    int w_timeout_counter = 0;
    localparam int RESPONSE_TIMEOUT = 100;
    
    always @(posedge clk) begin
        if (!resetn) begin
            aw_seen <= 1'b0;
            wlast_handshake_seen <= 1'b0;
            aw_timeout_counter <= 0;
            w_timeout_counter <= 0;
        end else if (warmup_complete) begin
            // Track AW handshake
            if (dut.axi_awvalid && dut.axi_awready) begin
                aw_seen <= 1'b1;
                aw_timeout_counter <= 0;
            end else if (aw_seen && !wlast_handshake_seen) begin
                aw_timeout_counter <= aw_timeout_counter + 1;
            end
            
            // Track WLAST handshake
            if (dut.axi_wvalid && dut.axi_wready && dut.axi_wlast) begin
                wlast_handshake_seen <= 1'b1;
                w_timeout_counter <= 0;
            end else if (wlast_handshake_seen) begin
                w_timeout_counter <= w_timeout_counter + 1;
            end
            
            // Check write response follows write data
            if (dut.axi_bvalid && dut.axi_bready) begin
                if (wlast_handshake_seen || aw_seen) begin
                    assertion_pass_count++;
                    $display("ASSERTION PASSED: Write response follows write data");
                end
                aw_seen <= 1'b0;
                wlast_handshake_seen <= 1'b0;
            end
            
            // Timeout check for write response
            if (wlast_handshake_seen && w_timeout_counter > RESPONSE_TIMEOUT) begin
                assertion_fail_count++;
                $display("ASSERTION FAILED: Write response timeout after WLAST");
                wlast_handshake_seen <= 1'b0;
                w_timeout_counter <= 0;
            end
        end
    end
    
    // Read data timing - Track pending read transactions
    int pending_ar_count = 0;  // Number of AR handshakes awaiting RLAST
    int ar_no_data_counter = 0;  // Cycles since AR without any RVALID
    logic ever_saw_rvalid = 1'b0;
    
    always @(posedge clk) begin
        if (!resetn) begin
            pending_ar_count <= 0;
            ar_no_data_counter <= 0;
            ever_saw_rvalid <= 1'b0;
        end else if (warmup_complete) begin
            // Track AR handshake - increment pending count
            if (dut.axi_arvalid && dut.axi_arready) begin
                pending_ar_count <= pending_ar_count + 1;
            end
            
            // Track RVALID activity
            if (dut.axi_rvalid) begin
                ever_saw_rvalid <= 1'b1;
            end
            
            // Track completed reads (RLAST)
            if (dut.axi_rvalid && dut.axi_rready) begin
                if (pending_ar_count > 0) begin
                    assertion_pass_count++;
                    $display("ASSERTION PASSED: Read data follows read address");
                end
                if (dut.axi_rlast && pending_ar_count > 0) begin
                    pending_ar_count <= pending_ar_count - 1;
                end
            end
            
            // Count cycles without RVALID when we have pending reads
            if (pending_ar_count > 0 && !dut.axi_rvalid) begin
                ar_no_data_counter <= ar_no_data_counter + 1;
            end else begin
                ar_no_data_counter <= 0;
            end
            
            // Timeout check - if many cycles with pending AR but no RVALID
            if (pending_ar_count > 0 && ar_no_data_counter > RESPONSE_TIMEOUT) begin
                assertion_fail_count++;
                $display("ASSERTION FAILED: RVALID not asserted after ARVALID - read data timeout");
                ar_no_data_counter <= 0;
            end
        end
    end
    
    // ============================================
    // Activity Checks for Read/Write Paths
    // ============================================
    // The master issues reads and writes. If no handshakes occur,
    // the VALID signals are likely stuck at 0 (bug).
    
    localparam int VALID_ACTIVITY_TIMEOUT = 500;  // Cycles to expect activity
    int ar_activity_counter = 0;
    int aw_activity_counter = 0;
    logic ar_activity_checked = 1'b0;
    logic aw_activity_checked = 1'b0;
    
    always @(posedge clk) begin
        if (!resetn) begin
            ar_activity_counter <= 0;
            ar_activity_checked <= 1'b0;
        end else if (warmup_complete && !ar_activity_checked) begin
            ar_activity_counter <= ar_activity_counter + 1;
            
            // If we see an AR handshake, we're good
            if (total_ar_handshakes > 0) begin
                ar_activity_checked <= 1'b1;
                assertion_pass_count++;
                $display("ASSERTION PASSED: ARVALID activity detected");
            end
            
            // Timeout - no AR activity at all
            if (ar_activity_counter >= VALID_ACTIVITY_TIMEOUT && total_ar_handshakes == 0) begin
                ar_activity_checked <= 1'b1;
                assertion_fail_count++;
                $display("ASSERTION FAILED: ARVALID never asserted - read address channel stuck");
            end
        end
    end
    
    always @(posedge clk) begin
        if (!resetn) begin
            aw_activity_counter <= 0;
            aw_activity_checked <= 1'b0;
        end else if (warmup_complete && !aw_activity_checked) begin
            aw_activity_counter <= aw_activity_counter + 1;
            
            // If we see an AW handshake, we're good
            if (total_aw_handshakes > 0) begin
                aw_activity_checked <= 1'b1;
                assertion_pass_count++;
                $display("ASSERTION PASSED: AWVALID activity detected");
            end
            
            // Timeout - no AW activity at all
            if (aw_activity_counter >= VALID_ACTIVITY_TIMEOUT && total_aw_handshakes == 0) begin
                aw_activity_checked <= 1'b1;
                assertion_fail_count++;
                $display("ASSERTION FAILED: AWVALID never asserted - write address channel stuck");
            end
        end
    end
    
    // Reset behavior check
    logic reset_checked = 1'b0;
    always @(posedge clk) begin
        if (resetn && !reset_checked) begin
            reset_checked <= 1'b1;
            assertion_pass_count++;
            $display("ASSERTION PASSED: Reset released");
        end
        if (!resetn) reset_checked <= 1'b0;
    end
    
    // ============================================
    // Coverage Tracking
    // ============================================
    
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
    
    always @(posedge clk) begin
        if (resetn && dut.axi_awvalid && dut.axi_awready) begin
            if (dut.axi_awaddr >= 32'h0000_0000 && dut.axi_awaddr <= 32'h0FFF_FFFF)
                write_addr_low_count++;
            else if (dut.axi_awaddr >= 32'h1000_0000 && dut.axi_awaddr <= 32'h1FFF_FFFF)
                write_addr_mid_count++;
            else
                write_addr_high_count++;
            case (dut.axi_awburst)
                2'b00: write_burst_fixed_count++;
                2'b01: write_burst_incr_count++;
                2'b10: write_burst_wrap_count++;
            endcase
            case (dut.axi_awsize)
                3'b000: write_size_byte_count++;
                3'b001: write_size_halfword_count++;
                3'b010: write_size_word_count++;
            endcase
        end
    end
    
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
    
    always @(posedge clk) begin
        if (resetn && dut.axi_arvalid && dut.axi_arready) begin
            if (dut.axi_araddr >= 32'h0000_0000 && dut.axi_araddr <= 32'h0FFF_FFFF)
                read_addr_low_count++;
            else if (dut.axi_araddr >= 32'h1000_0000 && dut.axi_araddr <= 32'h1FFF_FFFF)
                read_addr_mid_count++;
            else
                read_addr_high_count++;
            case (dut.axi_arburst)
                2'b00: read_burst_fixed_count++;
                2'b01: read_burst_incr_count++;
                2'b10: read_burst_wrap_count++;
            endcase
        end
    end
    
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
    
    always @(posedge clk) begin
        if (resetn) begin
            if (dut.axi_awvalid && dut.axi_awready) aw_handshake_valid_ready_count++;
            if (dut.axi_wvalid && dut.axi_wready) w_handshake_valid_ready_count++;
            if (dut.axi_bvalid && dut.axi_bready) b_handshake_valid_ready_count++;
            if (dut.axi_arvalid && dut.axi_arready) ar_handshake_valid_ready_count++;
            if (dut.axi_rvalid && dut.axi_rready) r_handshake_valid_ready_count++;
        end
    end
    
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
    
    always @(posedge clk) begin
        if (resetn && dut.axi_awvalid && dut.axi_awready) begin
            write_addr_handshake_count++;
            write_transaction_count++;
            $display("[%0t] Write Address: 0x%08x, LEN=%0d", $time, dut.axi_awaddr, dut.axi_awlen);
        end
    end
    
    always @(posedge clk) begin
        if (resetn && dut.axi_wvalid && dut.axi_wready) begin
            if (dut.axi_wlast)
                $display("[%0t] Write Data (LAST): 0x%08x", $time, dut.axi_wdata);
            else
                $display("[%0t] Write Data: 0x%08x", $time, dut.axi_wdata);
        end
    end
    
    always @(posedge clk) begin
        if (resetn && dut.axi_bvalid && dut.axi_bready) begin
            write_resp_handshake_count++;
            $display("[%0t] Write Response: BRESP=0x%02x", $time, dut.axi_bresp);
        end
    end
    
    always @(posedge clk) begin
        if (resetn && dut.axi_arvalid && dut.axi_arready) begin
            read_addr_handshake_count++;
            read_transaction_count++;
            $display("[%0t] Read Address: 0x%08x, LEN=%0d", $time, dut.axi_araddr, dut.axi_arlen);
        end
    end
    
    always @(posedge clk) begin
        if (resetn && dut.axi_rvalid && dut.axi_rready) begin
            read_data_handshake_count++;
            $display("[%0t] Read Data: 0x%08x, RLAST=%0d", $time, dut.axi_rdata, dut.axi_rlast);
        end
    end
    
    logic interrupt_req_prev = 1'b0;
    logic interrupt_ack_prev = 1'b0;
    always @(posedge clk) begin
        if (resetn) begin
            if (dut.interrupt_req && !interrupt_req_prev) $display("[%0t] Interrupt Request", $time);
            interrupt_req_prev <= dut.interrupt_req;
            if (dut.interrupt_ack && !interrupt_ack_prev) $display("[%0t] Interrupt Ack", $time);
            interrupt_ack_prev <= dut.interrupt_ack;
        end else begin
            interrupt_req_prev <= 1'b0;
            interrupt_ack_prev <= 1'b0;
        end
    end
    
    initial begin
        $dumpfile("axi4_top_tb.vcd");
        $dumpvars(0, axi4_top_tb);
        $display("==========================================");
        $display("AXI4 Golden Testbench Started");
        $display("==========================================");
    end
    
    final begin
        $display("==========================================");
        $display("Final Report");
        $display("==========================================");
        $display("Transactions: Write=%0d, Read=%0d", write_transaction_count, read_transaction_count);
        $display("Handshakes: AW=%0d, W=%0d, B=%0d, AR=%0d, R=%0d", 
                 total_aw_handshakes, total_w_handshakes, total_b_handshakes,
                 total_ar_handshakes, total_r_handshakes);
        $display("LAST signals: WLAST=%0d, RLAST=%0d", total_wlast_seen, total_rlast_seen);
        $display("Checks: pass_count=%0d, error_count=%0d", assertion_pass_count, assertion_fail_count);
        $display("==========================================");
    end

endmodule
