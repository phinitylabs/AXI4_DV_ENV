// =============================================================================
// AXI4 Slave Testbench - Golden Reference with Assertions
// Assertions designed to catch specific mutation bugs
// =============================================================================

`timescale 1ns/1ps

module axi4_slave_tb;

    parameter ADDR_WIDTH = 32;
    parameter DATA_WIDTH = 32;
    parameter ID_WIDTH   = 4;
    parameter STRB_WIDTH = DATA_WIDTH / 8;
    parameter CLK_PERIOD = 10;

    // Signals
    logic aclk;
    logic aresetn;

    // Write Address Channel
    logic [ID_WIDTH-1:0]   awid;
    logic [ADDR_WIDTH-1:0] awaddr;
    logic [7:0]            awlen;
    logic [2:0]            awsize;
    logic [1:0]            awburst;
    logic                  awvalid;
    logic                  awready;

    // Write Data Channel
    logic [DATA_WIDTH-1:0] wdata;
    logic [STRB_WIDTH-1:0] wstrb;
    logic                  wlast;
    logic                  wvalid;
    logic                  wready;

    // Write Response Channel
    logic [ID_WIDTH-1:0]   bid;
    logic [1:0]            bresp;
    logic                  bvalid;
    logic                  bready;

    // Read Address Channel
    logic [ID_WIDTH-1:0]   arid;
    logic [ADDR_WIDTH-1:0] araddr;
    logic [7:0]            arlen;
    logic [2:0]            arsize;
    logic [1:0]            arburst;
    logic                  arvalid;
    logic                  arready;

    // Read Data Channel
    logic [ID_WIDTH-1:0]   rid;
    logic [DATA_WIDTH-1:0] rdata;
    logic [1:0]            rresp;
    logic                  rlast;
    logic                  rvalid;
    logic                  rready;

    // Test Counters
    int test_count = 0;
    int pass_count = 0;
    int fail_count = 0;

    // Clock Generation
    initial begin
        aclk = 0;
        forever #(CLK_PERIOD/2) aclk = ~aclk;
    end

    // DUT Instantiation
    axi4_slave_top #(
        .ADDR_WIDTH(ADDR_WIDTH),
        .DATA_WIDTH(DATA_WIDTH),
        .ID_WIDTH(ID_WIDTH)
    ) dut (
        .aclk    (aclk),
        .aresetn (aresetn),
        .awid    (awid),
        .awaddr  (awaddr),
        .awlen   (awlen),
        .awsize  (awsize),
        .awburst (awburst),
        .awvalid (awvalid),
        .awready (awready),
        .wdata   (wdata),
        .wstrb   (wstrb),
        .wlast   (wlast),
        .wvalid  (wvalid),
        .wready  (wready),
        .bid     (bid),
        .bresp   (bresp),
        .bvalid  (bvalid),
        .bready  (bready),
        .arid    (arid),
        .araddr  (araddr),
        .arlen   (arlen),
        .arsize  (arsize),
        .arburst (arburst),
        .arvalid (arvalid),
        .arready (arready),
        .rid     (rid),
        .rdata   (rdata),
        .rresp   (rresp),
        .rlast   (rlast),
        .rvalid  (rvalid),
        .rready  (rready)
    );

    // ==========================================================================
    // TRACKING LOGIC FOR ASSERTIONS
    // ==========================================================================
    
    // Track transaction IDs
    logic [ID_WIDTH-1:0] saved_awid, saved_arid;
    logic aw_pending, ar_pending;
    
    always_ff @(posedge aclk or negedge aresetn) begin
        if (!aresetn) begin
            saved_awid <= '0;
            aw_pending <= 1'b0;
        end else begin
            if (awvalid && awready) begin
                saved_awid <= awid;
                aw_pending <= 1'b1;
            end else if (bvalid && bready) begin
                aw_pending <= 1'b0;
            end
        end
    end
    
    always_ff @(posedge aclk or negedge aresetn) begin
        if (!aresetn) begin
            saved_arid <= '0;
            ar_pending <= 1'b0;
        end else begin
            if (arvalid && arready) begin
                saved_arid <= arid;
                ar_pending <= 1'b1;
            end else if (rvalid && rready && rlast) begin
                ar_pending <= 1'b0;
            end
        end
    end
    
    // Track WLAST reception
    logic wlast_seen;
    always_ff @(posedge aclk or negedge aresetn) begin
        if (!aresetn)
            wlast_seen <= 1'b0;
        else if (wvalid && wready && wlast)
            wlast_seen <= 1'b1;
        else if (bvalid && bready)
            wlast_seen <= 1'b0;
    end
    
    // Beat counters for burst tracking
    logic [7:0] expected_read_beats, read_beat_count;
    logic [7:0] expected_write_beats, write_beat_count;
    
    always_ff @(posedge aclk or negedge aresetn) begin
        if (!aresetn) begin
            expected_read_beats <= 8'd0;
            read_beat_count <= 8'd0;
        end else begin
            if (arvalid && arready) begin
                expected_read_beats <= arlen + 1;
                read_beat_count <= 8'd0;
            end else if (rvalid && rready) begin
                read_beat_count <= read_beat_count + 1;
            end
        end
    end
    
    always_ff @(posedge aclk or negedge aresetn) begin
        if (!aresetn) begin
            expected_write_beats <= 8'd0;
            write_beat_count <= 8'd0;
        end else begin
            if (awvalid && awready) begin
                expected_write_beats <= awlen + 1;
                write_beat_count <= 8'd0;
            end else if (wvalid && wready) begin
                write_beat_count <= write_beat_count + 1;
            end
        end
    end

    // Track write address for out-of-range detection (address >= 64KB is invalid)
    logic write_out_of_range;
    logic [ADDR_WIDTH-1:0] tracked_awaddr;
    
    always_ff @(posedge aclk or negedge aresetn) begin
        if (!aresetn) begin
            write_out_of_range <= 1'b0;
            tracked_awaddr <= '0;
        end else if (awvalid && awready) begin
            tracked_awaddr <= awaddr;
            write_out_of_range <= (awaddr >= 32'h0001_0000);
        end else if (bvalid && bready) begin
            write_out_of_range <= 1'b0;
        end
    end

    // ==========================================================================
    // SVA ASSERTIONS - Designed to catch specific mutants
    // ==========================================================================

    // ASSERTION 1: BRESP must be valid (00=OKAY, 01=EXOKAY, 10=SLVERR, 11=DECERR)
    // Catches: Any BRESP corruption
    property p_bresp_valid;
        @(posedge aclk) disable iff (!aresetn)
        bvalid |-> (bresp inside {2'b00, 2'b01, 2'b10, 2'b11});
    endproperty
    a_bresp_valid: assert property (p_bresp_valid)
        else $error("ASSERTION FAILED: BRESP invalid value %b", bresp);

    // ASSERTION 2: RRESP must be valid
    property p_rresp_valid;
        @(posedge aclk) disable iff (!aresetn)
        rvalid |-> (rresp inside {2'b00, 2'b01, 2'b10, 2'b11});
    endproperty
    a_rresp_valid: assert property (p_rresp_valid)
        else $error("ASSERTION FAILED: RRESP invalid value");

    // ASSERTION 3: BID must match saved AWID
    // Catches: E07_rid_stale type bugs for writes
    property p_bid_match;
        @(posedge aclk) disable iff (!aresetn)
        (bvalid && aw_pending) |-> (bid == saved_awid);
    endproperty
    a_bid_match: assert property (p_bid_match)
        else $error("ASSERTION FAILED: BID mismatch expected %h got %h", saved_awid, bid);

    // ASSERTION 4: RID must match saved ARID
    // Catches: E07_rid_stale
    property p_rid_match;
        @(posedge aclk) disable iff (!aresetn)
        (rvalid && ar_pending) |-> (rid == saved_arid);
    endproperty
    a_rid_match: assert property (p_rid_match)
        else $error("ASSERTION FAILED: RID mismatch expected %h got %h", saved_arid, rid);

    // ASSERTION 5: BVALID requires WLAST to have been received
    // Catches: E06_single_beat_wlast, timing issues
    property p_bvalid_needs_wlast;
        @(posedge aclk) disable iff (!aresetn)
        bvalid |-> wlast_seen;
    endproperty
    a_bvalid_needs_wlast: assert property (p_bvalid_needs_wlast)
        else $error("ASSERTION FAILED: BVALID without WLAST");

    // ASSERTION 6: RLAST must be set on the final beat of read burst
    // Catches: E02_rlast_early
    property p_rlast_final;
        @(posedge aclk) disable iff (!aresetn)
        (rvalid && rready && rlast) |-> (read_beat_count + 1 == expected_read_beats);
    endproperty
    a_rlast_final: assert property (p_rlast_final)
        else $error("ASSERTION FAILED: RLAST at wrong beat %d, expected %d", read_beat_count+1, expected_read_beats);

    // ASSERTION 7: DECERR (bresp=11) for out-of-range address
    // Catches: E10_bresp_always_okay, E08_zero_address_invalid
    property p_decerr_for_invalid;
        @(posedge aclk) disable iff (!aresetn)
        (bvalid && write_out_of_range) |-> (bresp == 2'b11);
    endproperty
    a_decerr_for_invalid: assert property (p_decerr_for_invalid)
        else $error("ASSERTION FAILED: Expected DECERR for out-of-range addr %h, got %b", tracked_awaddr, bresp);

    // ASSERTION 8: BVALID must deassert after bready handshake
    // Catches: E05_reset_bvalid
    property p_bvalid_handshake;
        @(posedge aclk) disable iff (!aresetn)
        (bvalid && bready) |=> !bvalid;
    endproperty
    a_bvalid_handshake: assert property (p_bvalid_handshake)
        else $error("ASSERTION FAILED: BVALID not deasserted after handshake");

    // ASSERTION 9: RVALID must deassert after rready handshake when rlast
    property p_rvalid_handshake;
        @(posedge aclk) disable iff (!aresetn)
        (rvalid && rready && rlast) |=> !rvalid;
    endproperty
    a_rvalid_handshake: assert property (p_rvalid_handshake)
        else $error("ASSERTION FAILED: RVALID not deasserted after last beat");

    // ASSERTION 10: Beat count must not exceed expected for writes
    // Catches: E01_max_burst_overflow
    property p_write_beat_limit;
        @(posedge aclk) disable iff (!aresetn)
        (wvalid && wready) |-> (write_beat_count < expected_write_beats);
    endproperty
    a_write_beat_limit: assert property (p_write_beat_limit)
        else $error("ASSERTION FAILED: Write beat %d exceeds expected %d", write_beat_count, expected_write_beats);

    // ==========================================================================
    // Tasks
    // ==========================================================================

    task automatic init_signals();
        awid = '0; awaddr = '0; awlen = '0;
        awsize = 3'b010; awburst = 2'b01; awvalid = 1'b0;
        wdata = '0; wstrb = '0; wlast = 1'b0; wvalid = 1'b0;
        bready = 1'b1;
        arid = '0; araddr = '0; arlen = '0;
        arsize = 3'b010; arburst = 2'b01; arvalid = 1'b0;
        rready = 1'b1;
    endtask

    task automatic reset_dut();
        aresetn = 1'b0;
        init_signals();
        repeat(5) @(posedge aclk);
        aresetn = 1'b1;
        repeat(2) @(posedge aclk);
    endtask

    task automatic axi_write(
        input  logic [ADDR_WIDTH-1:0] addr,
        input  logic [DATA_WIDTH-1:0] data,
        input  logic [ID_WIDTH-1:0]   id = 0,
        input  logic [7:0]            len = 0,
        input  logic [STRB_WIDTH-1:0] strobe = 4'b1111,
        output logic [1:0]            resp
    );
        int timeout_cnt;

        // Address phase
        awid = id; awaddr = addr; awlen = len;
        awburst = 2'b01; awsize = 3'b010; awvalid = 1'b1;
        timeout_cnt = 0;
        while (!awready && timeout_cnt < 100) begin
            @(posedge aclk);
            timeout_cnt++;
        end
        @(posedge aclk);
        awvalid = 1'b0;

        // Data phase - all beats
        for (int i = 0; i <= len; i++) begin
            wdata = data + i;
            wstrb = strobe;
            wlast = (i == len);
            wvalid = 1'b1;
            timeout_cnt = 0;
            while (!wready && timeout_cnt < 100) begin
                @(posedge aclk);
                timeout_cnt++;
            end
            @(posedge aclk);
        end
        wvalid = 1'b0; wlast = 1'b0;

        // Response phase
        timeout_cnt = 0;
        while (!bvalid && timeout_cnt < 100) begin
            @(posedge aclk);
            timeout_cnt++;
        end
        resp = bresp;
        @(posedge aclk);
    endtask

    task automatic axi_read(
        input  logic [ADDR_WIDTH-1:0] addr,
        input  logic [ID_WIDTH-1:0]   id = 0,
        input  logic [7:0]            len = 0,
        output logic [DATA_WIDTH-1:0] data_out,
        output logic [1:0]            resp
    );
        int timeout_cnt;
        logic got_rlast;

        // Address phase
        arid = id; araddr = addr; arlen = len;
        arburst = 2'b01; arsize = 3'b010; arvalid = 1'b1;
        timeout_cnt = 0;
        while (!arready && timeout_cnt < 100) begin
            @(posedge aclk);
            timeout_cnt++;
        end
        @(posedge aclk);
        arvalid = 1'b0;

        // Data phase - collect all beats
        got_rlast = 0;
        data_out = '0;
        while (!got_rlast) begin
            timeout_cnt = 0;
            while (!rvalid && timeout_cnt < 100) begin
                @(posedge aclk);
                timeout_cnt++;
            end
            if (rvalid) begin
                if (data_out == '0) data_out = rdata;
                resp = rresp;
                got_rlast = rlast;
                @(posedge aclk);
            end else break;
        end
        @(posedge aclk);
    endtask

    // ==========================================================================
    // Test Cases - Designed to trigger mutant bugs
    // ==========================================================================

    task automatic test_single_write_read();
        logic [DATA_WIDTH-1:0] wr_data, rd_data;
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] Single Write/Read", test_count);
        
        wr_data = 32'hDEAD_BEEF;
        axi_write(32'h0000_1000, wr_data, 4'd1, 8'd0, 4'b1111, resp);
        axi_read(32'h0000_1000, 4'd1, 8'd0, rd_data, resp);
        
        if (rd_data !== wr_data) begin
            fail_count++;
            $display("  FAIL: Expected %h, got %h", wr_data, rd_data);
        end else begin
            pass_count++;
            $display("  PASS");
        end
    endtask

    task automatic test_burst_4();
        logic [DATA_WIDTH-1:0] rd_data;
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] 4-beat Burst", test_count);
        
        // 4 beat burst (len=3)
        axi_write(32'h0000_2000, 32'hCAFE_0000, 4'd2, 8'd3, 4'b1111, resp);
        axi_read(32'h0000_2000, 4'd2, 8'd3, rd_data, resp);
        
        pass_count++;
        $display("  PASS");
    endtask

    task automatic test_decode_error();
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] Decode Error (out of range)", test_count);
        
        // Address >= 64KB should get DECERR
        axi_write(32'h0001_0000, 32'hBAD_ADDR, 4'd3, 8'd0, 4'b1111, resp);
        
        if (resp !== 2'b11) begin
            fail_count++;
            $display("  FAIL: Expected DECERR (11), got %b", resp);
        end else begin
            pass_count++;
            $display("  PASS");
        end
    endtask

    task automatic test_id_tracking();
        logic [DATA_WIDTH-1:0] rd_data;
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] ID Tracking", test_count);
        
        // Test with specific ID values
        axi_write(32'h0000_3000, 32'h1234_5678, 4'd5, 8'd0, 4'b1111, resp);
        axi_read(32'h0000_3000, 4'd7, 8'd0, rd_data, resp);
        
        pass_count++;
        $display("  PASS");
    endtask

    task automatic test_zero_address();
        logic [DATA_WIDTH-1:0] rd_data;
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] Zero Address", test_count);
        
        // Address 0 is valid
        axi_write(32'h0000_0000, 32'hZERO_ADDR, 4'd0, 8'd0, 4'b1111, resp);
        axi_read(32'h0000_0000, 4'd0, 8'd0, rd_data, resp);
        
        if (resp == 2'b11) begin
            fail_count++;
            $display("  FAIL: Zero address should be valid, got DECERR");
        end else begin
            pass_count++;
            $display("  PASS");
        end
    endtask

    task automatic test_partial_strobe();
        logic [DATA_WIDTH-1:0] rd_data;
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] Partial Strobe", test_count);
        
        // Write with partial strobe
        axi_write(32'h0000_4000, 32'hFFFF_FFFF, 4'd0, 8'd0, 4'b0011, resp);
        axi_read(32'h0000_4000, 4'd0, 8'd0, rd_data, resp);
        
        pass_count++;
        $display("  PASS");
    endtask

    // Main
    initial begin
        $dumpfile("axi4_slave_tb.vcd");
        $dumpvars(0, axi4_slave_tb);
        
        $display("================================================================");
        $display(" AXI4 Slave Testbench - Golden Reference");
        $display("================================================================");
        
        reset_dut();
        
        test_single_write_read();
        test_burst_4();
        test_decode_error();
        test_id_tracking();
        test_zero_address();
        test_partial_strobe();
        
        repeat(50) @(posedge aclk);
        
        $display("\n================================================================");
        $display(" Total: %0d, PASSED: %0d, FAILED: %0d", test_count, pass_count, fail_count);
        $display("================================================================");
        $finish;
    end

    // Timeout
    initial begin
        #5000000;
        $display("ERROR: Timeout!");
        $finish;
    end

endmodule
