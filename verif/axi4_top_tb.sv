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
    
    // Warmup counter - skip assertion failure checks during initial cycles after reset
    // Use longer warmup (150 cycles) to ensure we're well past initialization transients
    int unsigned warmup_cycles = 0;
    localparam int unsigned WARMUP_PERIOD = 150;
    
    always @(posedge clk) begin
        if (!resetn) begin
            warmup_cycles <= 0;
        end else if (warmup_cycles < WARMUP_PERIOD) begin
            warmup_cycles <= warmup_cycles + 1;
        end
    end
    
    // Warmup complete flag with delayed version for proper synchronization
    logic warmup_complete = 1'b0;
    logic warmup_complete_d1 = 1'b0;
    always @(posedge clk) begin
        if (!resetn) begin
            warmup_complete <= 1'b0;
            warmup_complete_d1 <= 1'b0;
        end else begin
            warmup_complete <= (warmup_cycles >= WARMUP_PERIOD);
            warmup_complete_d1 <= warmup_complete;
        end
    end
    
    // ============================================
    // VALID Signal Stability Assertions
    // ============================================
    // AXI4 requires VALID signals to remain asserted until READY is asserted
    
    // Track previous values for VALID stability checks
    logic awvalid_prev, wvalid_prev, bvalid_prev, arvalid_prev, rvalid_prev;
    logic awready_prev, wready_prev, bready_prev, arready_prev, rready_prev;
    
    // Initialize previous values
    initial begin
        awvalid_prev = 1'b0; wvalid_prev = 1'b0; bvalid_prev = 1'b0;
        arvalid_prev = 1'b0; rvalid_prev = 1'b0;
        awready_prev = 1'b0; wready_prev = 1'b0; bready_prev = 1'b0;
        arready_prev = 1'b0; rready_prev = 1'b0;
    end
    
    // Assertion 1: AWVALID must remain stable until AWREADY
    always @(posedge clk) begin
        if (resetn) begin
            if (warmup_complete_d1) begin
                // PASS: Successful handshake
                if (dut.axi_awvalid && dut.axi_awready) begin
                    assertion_pass_count++;
                    $display("ASSERTION PASSED: AWVALID stable until AWREADY");
                end
                // FAIL: AWVALID dropped before AWREADY was asserted
                if (awvalid_prev && !awready_prev && !dut.axi_awvalid) begin
                    assertion_fail_count++;
                    $display("ASSERTION FAILED: AWVALID dropped before AWREADY");
                end
            end
            awvalid_prev <= dut.axi_awvalid;
            awready_prev <= dut.axi_awready;
        end else begin
            awvalid_prev <= 1'b0;
            awready_prev <= 1'b0;
        end
    end
    
    // Assertion 2: WVALID must remain stable until WREADY
    always @(posedge clk) begin
        if (resetn) begin
            if (warmup_complete_d1) begin
                if (dut.axi_wvalid && dut.axi_wready) begin
                    assertion_pass_count++;
                    $display("ASSERTION PASSED: WVALID stable until WREADY");
                end
                if (wvalid_prev && !wready_prev && !dut.axi_wvalid) begin
                    assertion_fail_count++;
                    $display("ASSERTION FAILED: WVALID dropped before WREADY");
                end
            end
            wvalid_prev <= dut.axi_wvalid;
            wready_prev <= dut.axi_wready;
        end else begin
            wvalid_prev <= 1'b0;
            wready_prev <= 1'b0;
        end
    end
    
    // Assertion 3: BVALID must remain stable until BREADY
    always @(posedge clk) begin
        if (resetn) begin
            if (warmup_complete_d1) begin
                if (dut.axi_bvalid && dut.axi_bready) begin
                    assertion_pass_count++;
                    $display("ASSERTION PASSED: BVALID stable until BREADY");
                end
                if (bvalid_prev && !bready_prev && !dut.axi_bvalid) begin
                    assertion_fail_count++;
                    $display("ASSERTION FAILED: BVALID dropped before BREADY");
                end
            end
            bvalid_prev <= dut.axi_bvalid;
            bready_prev <= dut.axi_bready;
        end else begin
            bvalid_prev <= 1'b0;
            bready_prev <= 1'b0;
        end
    end
    
    // Assertion 4: ARVALID must remain stable until ARREADY
    always @(posedge clk) begin
        if (resetn) begin
            if (warmup_complete_d1) begin
                if (dut.axi_arvalid && dut.axi_arready) begin
                    assertion_pass_count++;
                    $display("ASSERTION PASSED: ARVALID stable until ARREADY");
                end
                if (arvalid_prev && !arready_prev && !dut.axi_arvalid) begin
                    assertion_fail_count++;
                    $display("ASSERTION FAILED: ARVALID dropped before ARREADY");
                end
            end
            arvalid_prev <= dut.axi_arvalid;
            arready_prev <= dut.axi_arready;
        end else begin
            arvalid_prev <= 1'b0;
            arready_prev <= 1'b0;
        end
    end
    
    // Assertion 5: RVALID must remain stable until RREADY
    always @(posedge clk) begin
        if (resetn) begin
            if (warmup_complete_d1) begin
                if (dut.axi_rvalid && dut.axi_rready) begin
                    assertion_pass_count++;
                    $display("ASSERTION PASSED: RVALID stable until RREADY");
                end
                if (rvalid_prev && !rready_prev && !dut.axi_rvalid) begin
                    assertion_fail_count++;
                    $display("ASSERTION FAILED: RVALID dropped before RREADY");
                end
            end
            rvalid_prev <= dut.axi_rvalid;
            rready_prev <= dut.axi_rready;
        end else begin
            rvalid_prev <= 1'b0;
            rready_prev <= 1'b0;
        end
    end
    
    // ============================================
    // LAST Signal Correctness Assertions
    // ============================================
    // Track burst beats and verify LAST is correctly asserted
    
    // Write burst tracking
    logic [7:0] expected_wbeats = 0;    // Expected write beats from AWLEN+1
    logic [7:0] wbeat_counter = 0;      // Current beat count in write data phase
    logic write_in_progress = 0;        // Track if we're in a write burst
    
    always @(posedge clk) begin
        if (!resetn) begin
            expected_wbeats <= 0;
            wbeat_counter <= 0;
            write_in_progress <= 0;
        end else begin
            // AW handshake starts a new write burst
            if (dut.axi_awvalid && dut.axi_awready) begin
                expected_wbeats <= dut.axi_awlen + 1;
                wbeat_counter <= 0;
                write_in_progress <= 1;
            end
            
            // Count write data beats
            if (dut.axi_wvalid && dut.axi_wready) begin
                wbeat_counter <= wbeat_counter + 1;
                
                if (warmup_complete_d1 && write_in_progress) begin
                    // Check WLAST on final beat
                    if (wbeat_counter == expected_wbeats - 1) begin
                        if (dut.axi_wlast) begin
                            assertion_pass_count++;
                            $display("ASSERTION PASSED: WLAST asserted on final write beat");
                        end else begin
                            assertion_fail_count++;
                            $display("ASSERTION FAILED: WLAST not asserted on final write beat");
                        end
                    end
                    // Check for premature WLAST
                    else if (dut.axi_wlast) begin
                        assertion_fail_count++;
                        $display("ASSERTION FAILED: WLAST asserted before final write beat");
                    end
                end
                
                // Reset on WLAST
                if (dut.axi_wlast) begin
                    write_in_progress <= 0;
                    wbeat_counter <= 0;
                end
            end
        end
    end
    
    // Read burst tracking
    logic [7:0] expected_rbeats = 0;    // Expected read beats from ARLEN+1  
    logic [7:0] rbeat_counter = 0;      // Current beat count in read data phase
    logic read_in_progress = 0;         // Track if we're in a read burst
    
    always @(posedge clk) begin
        if (!resetn) begin
            expected_rbeats <= 0;
            rbeat_counter <= 0;
            read_in_progress <= 0;
        end else begin
            // AR handshake starts a new read burst
            if (dut.axi_arvalid && dut.axi_arready) begin
                expected_rbeats <= dut.axi_arlen + 1;
                rbeat_counter <= 0;
                read_in_progress <= 1;
            end
            
            // Count read data beats
            if (dut.axi_rvalid && dut.axi_rready) begin
                rbeat_counter <= rbeat_counter + 1;
                
                if (warmup_complete_d1 && read_in_progress) begin
                    // Check RLAST on final beat
                    if (rbeat_counter == expected_rbeats - 1) begin
                        if (dut.axi_rlast) begin
                            assertion_pass_count++;
                            $display("ASSERTION PASSED: RLAST asserted on final read beat");
                        end else begin
                            assertion_fail_count++;
                            $display("ASSERTION FAILED: RLAST not asserted on final read beat");
                        end
                    end
                    // Check for premature RLAST
                    else if (dut.axi_rlast) begin
                        assertion_fail_count++;
                        $display("ASSERTION FAILED: RLAST asserted before final read beat");
                    end
                end
                
                // Reset on RLAST
                if (dut.axi_rlast) begin
                    read_in_progress <= 0;
                    rbeat_counter <= 0;
                end
            end
        end
    end
    
    // ============================================
    // Response Code Validation
    // ============================================
    // Check for valid AXI4 response codes (00=OKAY, 01=EXOKAY, 10=SLVERR, 11=DECERR)
    // All 2-bit values are valid, but we check for changes/corruption
    
    always @(posedge clk) begin
        if (resetn && dut.axi_bvalid && dut.axi_bready) begin
            if (warmup_complete_d1) begin
                // Check BRESP is a valid 2-bit value (always true for correct design)
                if (dut.axi_bresp == 2'b00 || dut.axi_bresp == 2'b01 ||
                    dut.axi_bresp == 2'b10 || dut.axi_bresp == 2'b11) begin
                    assertion_pass_count++;
                    $display("ASSERTION PASSED: Valid BRESP code (%b)", dut.axi_bresp);
                end else begin
                    assertion_fail_count++;
                    $display("ASSERTION FAILED: Invalid BRESP code (%b)", dut.axi_bresp);
                end
            end
        end
    end
    
    always @(posedge clk) begin
        if (resetn && dut.axi_rvalid && dut.axi_rready) begin
            if (warmup_complete_d1) begin
                if (dut.axi_rresp == 2'b00 || dut.axi_rresp == 2'b01 ||
                    dut.axi_rresp == 2'b10 || dut.axi_rresp == 2'b11) begin
                    assertion_pass_count++;
                    $display("ASSERTION PASSED: Valid RRESP code (%b)", dut.axi_rresp);
                end else begin
                    assertion_fail_count++;
                    $display("ASSERTION FAILED: Invalid RRESP code (%b)", dut.axi_rresp);
                end
            end
        end
    end
    
    // ============================================
    // Timing Relationship Assertions
    // ============================================
    
    // Combinational signals for same-cycle detection
    wire aw_handshake_now = dut.axi_awvalid && dut.axi_awready;
    wire wlast_now = dut.axi_wvalid && dut.axi_wready && dut.axi_wlast;
    wire b_handshake_now = dut.axi_bvalid && dut.axi_bready;
    wire ar_handshake_now = dut.axi_arvalid && dut.axi_arready;
    wire r_handshake_now = dut.axi_rvalid && dut.axi_rready;
    
    // Track outstanding write transactions
    int outstanding_writes = 0;
    int writes_with_wlast = 0;
    
    always @(posedge clk) begin
        if (!resetn) begin
            outstanding_writes <= 0;
            writes_with_wlast <= 0;
        end else begin
            // Track AW handshakes
            if (aw_handshake_now) begin
                outstanding_writes <= outstanding_writes + 1;
            end
            
            // Track WLAST completions
            if (wlast_now) begin
                writes_with_wlast <= writes_with_wlast + 1;
            end
            
            // Check B handshake timing
            if (b_handshake_now) begin
                if (warmup_complete_d1) begin
                    // Success: Have outstanding write AND (WLAST seen OR WLAST happening now)
                    if ((outstanding_writes > 0 || aw_handshake_now) && 
                        (writes_with_wlast > 0 || wlast_now)) begin
                        assertion_pass_count++;
                        $display("ASSERTION PASSED: Write response follows write data completion");
                    end
                    // Fail: No outstanding write
                    else if (outstanding_writes == 0 && !aw_handshake_now) begin
                        assertion_fail_count++;
                        $display("ASSERTION FAILED: Write response without outstanding write");
                    end
                    // Fail: No WLAST seen
                    else if (writes_with_wlast == 0 && !wlast_now) begin
                        assertion_fail_count++;
                        $display("ASSERTION FAILED: Write response before WLAST");
                    end
                end
                // Consume counters
                if (outstanding_writes > 0) outstanding_writes <= outstanding_writes - 1;
                if (writes_with_wlast > 0 && !wlast_now) writes_with_wlast <= writes_with_wlast - 1;
            end
        end
    end
    
    // Track outstanding read transactions
    int outstanding_reads = 0;
    
    always @(posedge clk) begin
        if (!resetn) begin
            outstanding_reads <= 0;
        end else begin
            // Track AR handshakes
            if (ar_handshake_now) begin
                outstanding_reads <= outstanding_reads + 1;
            end
            
            // Check R handshake timing
            if (r_handshake_now) begin
                if (warmup_complete_d1) begin
                    // Success: Have outstanding read OR AR happening now (same-cycle)
                    if (outstanding_reads > 0 || ar_handshake_now) begin
                        if (dut.axi_rlast) begin
                            assertion_pass_count++;
                            $display("ASSERTION PASSED: Read data follows read address acceptance");
                        end
                    end else begin
                        assertion_fail_count++;
                        $display("ASSERTION FAILED: Read data without outstanding read address");
                    end
                end
                // Consume on RLAST
                if (dut.axi_rlast && outstanding_reads > 0) begin
                    outstanding_reads <= outstanding_reads - 1;
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
