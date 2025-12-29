// =============================================================================
// AXI4 Slave Testbench - Baseline (Agent adds assertions)
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
    // YOUR TASK: Add SVA Assertions Here
    // ==========================================================================
    // 
    // Add 8-12 SystemVerilog Assertions (SVA) to verify AXI4 protocol compliance.
    // Your assertions will be tested against MUTANT designs containing bugs.
    // To pass, your assertions must DETECT these bugs.
    //
    // REQUIREMENTS:
    // 1. Use proper SVA syntax with `property` and `assert property`
    // 2. Include `disable iff (!aresetn)` for reset handling
    // 3. Assertions must NOT fire on the correct design (no false positives)
    // 4. Minimum 8 assertions
    //
    // SUGGESTED ASSERTIONS:
    // - BRESP/RRESP validity (values must be 00, 01, 10, or 11)
    // - BID must match AWID, RID must match ARID
    // - BVALID should require WLAST to have been seen
    // - RLAST must be set on the final beat of read burst
    // - DECERR (bresp=11) for out-of-range addresses (>= 0x10000)
    // - Valid addresses (0x0000-0xFFFF) should NOT get DECERR
    // - BVALID/RVALID handshake behavior
    // - Beat count limits for burst transactions
    //
    // EXAMPLE ASSERTION:
    // property p_bresp_valid;
    //     @(posedge aclk) disable iff (!aresetn)
    //     bvalid |-> (bresp inside {2'b00, 2'b01, 2'b10, 2'b11});
    // endproperty
    // a_bresp_valid: assert property (p_bresp_valid)
    //     else $error("ASSERTION FAILED: BRESP invalid value");
    //
    // ==========================================================================

    // TODO: Add your SVA assertions here


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
    // Test Cases
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
        axi_write(32'h0001_0000, 32'hBADA_DD00, 4'd3, 8'd0, 4'b1111, resp);
        
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
        axi_write(32'h0000_0000, 32'h0000_0000, 4'd0, 8'd0, 4'b1111, resp);
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
        
        // First clear the memory location with full strobe
        axi_write(32'h0000_4000, 32'h0000_0000, 4'd0, 8'd0, 4'b1111, resp);
        
        // Write with partial strobe (only bytes 0 and 1)
        axi_write(32'h0000_4000, 32'hAABB_CCDD, 4'd0, 8'd0, 4'b0011, resp);
        axi_read(32'h0000_4000, 4'd0, 8'd0, rd_data, resp);
        
        // Bytes 0 and 1 should have new data (0xCCDD), bytes 2 and 3 should be 0
        if ((rd_data[15:0] !== 16'hCCDD)) begin
            fail_count++;
            $display("  FAIL: Expected bytes 0-1 = 0xCCDD, got %h", rd_data[15:0]);
        end else begin
            pass_count++;
            $display("  PASS: Strobed bytes correct");
        end
    endtask

    task automatic test_boundary_address();
        logic [DATA_WIDTH-1:0] rd_data;
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] Boundary Address 0xFFFF", test_count);
        
        awsize = 3'b000;  // 1 byte transfer
        axi_write(32'h0000_FFFF, 32'h000000AB, 4'd0, 8'd0, 4'b0001, resp);
        awsize = 3'b010;  // Reset to 4 bytes
        
        if (resp == 2'b11) begin
            fail_count++;
            $display("  FAIL: Address 0xFFFF should be valid, got DECERR");
        end else begin
            pass_count++;
            $display("  PASS: 0xFFFF correctly accepted");
        end
        
        test_count++;
        $display("\n[TEST %0d] Boundary Address 0xFFFC", test_count);
        axi_write(32'h0000_FFFC, 32'h12345678, 4'd0, 8'd0, 4'b1111, resp);
        
        if (resp == 2'b11) begin
            fail_count++;
            $display("  FAIL: Address 0xFFFC should be valid, got DECERR");
        end else begin
            pass_count++;
            $display("  PASS");
        end
    endtask

    task automatic test_strobe_byte2();
        logic [DATA_WIDTH-1:0] rd_data;
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] Strobe Byte 2 Only", test_count);
        
        // Clear memory location
        axi_write(32'h0000_5000, 32'h0000_0000, 4'd0, 8'd0, 4'b1111, resp);
        
        // Write with strobe only on byte 2
        axi_write(32'h0000_5000, 32'h00FF_0000, 4'd0, 8'd0, 4'b0100, resp);
        axi_read(32'h0000_5000, 4'd0, 8'd0, rd_data, resp);
        
        if (rd_data[23:16] !== 8'hFF) begin
            fail_count++;
            $display("  FAIL: Byte 2 should be 0xFF, got %h, full data %h", rd_data[23:16], rd_data);
        end else if (rd_data[15:0] !== 16'h0000 || rd_data[31:24] !== 8'h00) begin
            fail_count++;
            $display("  FAIL: Non-strobed bytes should be 0, got %h", rd_data);
        end else begin
            pass_count++;
            $display("  PASS");
        end
    endtask

    // Main
    initial begin
        $dumpfile("axi4_slave_tb.vcd");
        $dumpvars(0, axi4_slave_tb);
        
        $display("================================================================");
        $display(" AXI4 Slave Testbench - Baseline");
        $display("================================================================");
        
        reset_dut();
        
        test_single_write_read();
        test_burst_4();
        test_decode_error();
        test_id_tracking();
        test_zero_address();
        test_partial_strobe();
        test_boundary_address();
        test_strobe_byte2();
        
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

