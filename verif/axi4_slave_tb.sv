// =============================================================================
// AXI4 Burst Boundary Assertion Testbench - Starter Template
// Task: Add SVA assertions for burst address calculation verification
// =============================================================================

`timescale 1ns/1ps

module axi4_slave_tb;

    // Parameters
    parameter ADDR_WIDTH = 32;
    parameter DATA_WIDTH = 32;
    parameter ID_WIDTH   = 4;
    parameter STRB_WIDTH = DATA_WIDTH / 8;
    parameter CLK_PERIOD = 10;

    // Burst type constants
    localparam BURST_FIXED = 2'b00;
    localparam BURST_INCR  = 2'b01;
    localparam BURST_WRAP  = 2'b10;

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

    // =========================================================================
    // BURST STATE TRACKING (Use these for your assertions)
    // =========================================================================
    
    // Write burst tracking
    logic        wr_in_burst;
    logic [31:0] wr_start_addr;
    logic [31:0] wr_current_addr;
    logic [7:0]  wr_beat_count;
    logic [7:0]  wr_total_beats;
    logic [2:0]  wr_burst_size;
    logic [1:0]  wr_burst_type;
    
    // Read burst tracking
    logic        rd_in_burst;
    logic [31:0] rd_start_addr;
    logic [31:0] rd_current_addr;
    logic [7:0]  rd_beat_count;
    logic [7:0]  rd_total_beats;
    logic [2:0]  rd_burst_size;
    logic [1:0]  rd_burst_type;

    // =========================================================================
    // ADD YOUR BURST BOUNDARY ASSERTIONS HERE
    // =========================================================================
    //
    // Required assertions:
    // 1. INCR address increment verification
    // 2. FIXED address stability verification
    // 3. WRAP boundary calculation verification
    // 4. 4KB boundary check
    // 5. Burst length (WLAST/RLAST) correctness
    //
    // Use the burst tracking signals above in your assertions.
    // Example structure:
    //
    // property p_incr_addr_increment;
    //     @(posedge aclk) disable iff (!aresetn)
    //     // your assertion logic here
    // endproperty
    //
    // assert property (p_incr_addr_increment)
    //     else $error("INCR burst address mismatch");
    //
    // =========================================================================



    // =========================================================================
    // END OF ASSERTION SECTION
    // =========================================================================

    // Reset Task
    task automatic reset_dut();
        aresetn = 0;
        awid = 0; awaddr = 0; awlen = 0; awsize = 3'b010; awburst = 2'b01; awvalid = 0;
        wdata = 0; wstrb = 0; wlast = 0; wvalid = 0;
        bready = 1;
        arid = 0; araddr = 0; arlen = 0; arsize = 3'b010; arburst = 2'b01; arvalid = 0;
        rready = 1;
        repeat(10) @(posedge aclk);
        aresetn = 1;
        repeat(5) @(posedge aclk);
    endtask

    // AXI Write Task
    task automatic axi_write(
        input logic [ADDR_WIDTH-1:0] addr,
        input logic [DATA_WIDTH-1:0] data,
        input logic [ID_WIDTH-1:0]   id,
        input logic [7:0]            len,
        input logic [1:0]            burst,
        input logic [3:0]            strb,
        output logic [1:0]           resp
    );
        int timeout_cnt;
        awid = id; awaddr = addr; awlen = len;
        awburst = burst; awsize = 3'b010; awvalid = 1'b1;
        
        timeout_cnt = 0;
        while (!awready && timeout_cnt < 100) begin
            @(posedge aclk);
            timeout_cnt++;
        end
        @(posedge aclk);
        awvalid = 1'b0;
        
        for (int i = 0; i <= len; i++) begin
            wdata = data + i;
            wstrb = strb;
            wlast = (i == len);
            wvalid = 1'b1;
            timeout_cnt = 0;
            while (!wready && timeout_cnt < 100) begin
                @(posedge aclk);
                timeout_cnt++;
            end
            @(posedge aclk);
        end
        wvalid = 1'b0;
        wlast = 1'b0;
        
        timeout_cnt = 0;
        while (!bvalid && timeout_cnt < 100) begin
            @(posedge aclk);
            timeout_cnt++;
        end
        resp = bresp;
        @(posedge aclk);
    endtask

    // AXI Read Task
    task automatic axi_read(
        input logic [ADDR_WIDTH-1:0]  addr,
        input logic [ID_WIDTH-1:0]    id,
        input logic [7:0]             len,
        input logic [1:0]             burst,
        output logic [DATA_WIDTH-1:0] data_out,
        output logic [1:0]            resp
    );
        logic [DATA_WIDTH-1:0] read_data[$];
        int timeout_cnt;
        logic got_rlast;

        read_data.delete();
        arid = id; araddr = addr; arlen = len;
        arburst = burst; arsize = 3'b010; arvalid = 1'b1;

        timeout_cnt = 0;
        while (!arready && timeout_cnt < 100) begin
            @(posedge aclk);
            timeout_cnt++;
        end
        @(posedge aclk);
        arvalid = 1'b0;

        got_rlast = 0;
        while (!got_rlast) begin
            timeout_cnt = 0;
            while (!rvalid && timeout_cnt < 100) begin
                @(posedge aclk);
                timeout_cnt++;
            end
            if (rvalid) begin
                read_data.push_back(rdata);
                resp = rresp;
                got_rlast = rlast;
                @(posedge aclk);
            end else break;
        end
        data_out = (read_data.size() > 0) ? read_data[0] : '0;
        @(posedge aclk);
    endtask

    // Simple Write/Read Tasks
    task automatic axi_write_simple(input logic [ADDR_WIDTH-1:0] addr, input logic [DATA_WIDTH-1:0] data);
        logic [1:0] resp;
        axi_write(addr, data, 0, 0, BURST_INCR, 4'b1111, resp);
    endtask

    task automatic axi_read_simple(input logic [ADDR_WIDTH-1:0] addr, output logic [DATA_WIDTH-1:0] data);
        logic [1:0] resp;
        axi_read(addr, 0, 0, BURST_INCR, data, resp);
    endtask

    // Test Cases
    task automatic test_single_write_read();
        logic [DATA_WIDTH-1:0] wr_data, rd_data;
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] Single Write/Read", test_count);
        wr_data = 32'hDEAD_BEEF;
        axi_write(32'h0000_1000, wr_data, 0, 0, BURST_INCR, 4'b1111, resp);
        axi_read(32'h0000_1000, 0, 0, BURST_INCR, rd_data, resp);
        if (rd_data !== wr_data) begin fail_count++; $display("  FAIL"); end
        else begin pass_count++; $display("  PASS"); end
    endtask

    task automatic test_incr_burst();
        logic [DATA_WIDTH-1:0] rd_data;
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] INCR Burst (4 beats)", test_count);
        axi_write(32'h0000_2000, 32'hBEEF_0000, 0, 3, BURST_INCR, 4'b1111, resp);
        axi_read(32'h0000_2000, 0, 3, BURST_INCR, rd_data, resp);
        pass_count++; $display("  PASS");
    endtask

    task automatic test_fixed_burst();
        logic [DATA_WIDTH-1:0] rd_data;
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] FIXED Burst", test_count);
        axi_write(32'h0000_3000, 32'hFIXD_0000, 0, 3, BURST_FIXED, 4'b1111, resp);
        axi_read(32'h0000_3000, 0, 3, BURST_FIXED, rd_data, resp);
        pass_count++; $display("  PASS");
    endtask

    task automatic test_wrap_burst();
        logic [DATA_WIDTH-1:0] rd_data;
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] WRAP Burst (4 beats)", test_count);
        axi_write(32'h0000_4008, 32'hWRAP_0000, 0, 3, BURST_WRAP, 4'b1111, resp);
        axi_read(32'h0000_4008, 0, 3, BURST_WRAP, rd_data, resp);
        pass_count++; $display("  PASS");
    endtask

    task automatic test_decode_error();
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] Decode Error (out of range)", test_count);
        axi_write(32'h0001_0000, 32'hDEAD, 0, 0, BURST_INCR, 4'b1111, resp);
        if (resp !== 2'b11) begin fail_count++; $display("  FAIL"); end
        else begin pass_count++; $display("  PASS"); end
    endtask

    // Main Test Sequence
    initial begin
        $dumpfile("axi4_slave_tb.vcd");
        $dumpvars(0, axi4_slave_tb);
        $display("================================================================");
        $display(" AXI4 Burst Boundary Assertion Testbench");
        $display("================================================================");
        reset_dut();
        test_single_write_read();
        test_incr_burst();
        test_fixed_burst();
        test_wrap_burst();
        test_decode_error();
        repeat(100) @(posedge aclk);
        $display("\n================================================================");
        $display(" Total: %0d, PASSED: %0d, FAILED: %0d", test_count, pass_count, fail_count);
        $display("================================================================");
        $finish;
    end

    initial begin
        #5000000;
        $display("ERROR: Timeout!");
        $finish;
    end

endmodule

