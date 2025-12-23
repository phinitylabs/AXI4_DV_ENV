// =============================================================================
// AXI4 Slave Testbench - Starter (Add Assertions Here)
// =============================================================================

`timescale 1ns/1ps

module axi4_slave_tb;

    // Parameters
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
    // YOUR TASK: ADD SVA ASSERTIONS BELOW  
    // Required: 5-10 assertions for AXI4 protocol compliance
    // ==========================================================================

    // TODO: Add your assertions here

    // ==========================================================================
    // Tasks and Tests
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
        input  logic [1:0]            burst = 2'b01,
        input  logic [STRB_WIDTH-1:0] strobe = 4'b1111,
        output logic [1:0]            resp
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
            wdata = data + i; wstrb = strobe;
            wlast = (i == len); wvalid = 1'b1;
            timeout_cnt = 0;
            while (!wready && timeout_cnt < 100) begin
                @(posedge aclk);
                timeout_cnt++;
            end
            @(posedge aclk);
        end
        wvalid = 1'b0; wlast = 1'b0;

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
        input  logic [1:0]            burst = 2'b01,
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

    task automatic axi_write_simple(input logic [ADDR_WIDTH-1:0] addr, input logic [DATA_WIDTH-1:0] data);
        logic [1:0] resp;
        axi_write(addr, data, 0, 0, 2'b01, 4'b1111, resp);
    endtask

    task automatic axi_read_simple(input logic [ADDR_WIDTH-1:0] addr, output logic [DATA_WIDTH-1:0] data);
        logic [1:0] resp;
        axi_read(addr, 0, 0, 2'b01, data, resp);
    endtask

    // Test Cases
    task automatic test_single_write_read();
        logic [DATA_WIDTH-1:0] wr_data, rd_data;
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] Single Write/Read", test_count);
        wr_data = 32'hDEAD_BEEF;
        axi_write(32'h0000_1000, wr_data, 0, 0, 2'b01, 4'b1111, resp);
        axi_read(32'h0000_1000, 0, 0, 2'b01, rd_data, resp);
        if (rd_data !== wr_data) begin fail_count++; $display("  FAIL"); end
        else begin pass_count++; $display("  PASS"); end
    endtask

    task automatic test_burst();
        logic [DATA_WIDTH-1:0] rd_data;
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] Burst", test_count);
        axi_write(32'h0000_3000, 32'hBEEF_0000, 0, 3, 2'b01, 4'b1111, resp);
        axi_read(32'h0000_3000, 0, 3, 2'b01, rd_data, resp);
        pass_count++; $display("  PASS");
    endtask

    task automatic test_decode_error();
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] Decode Error", test_count);
        axi_write(32'h0001_0000, 32'hDEAD, 0, 0, 2'b01, 4'b1111, resp);
        if (resp !== 2'b11) begin fail_count++; $display("  FAIL"); end
        else begin pass_count++; $display("  PASS"); end
    endtask

    // Main
    initial begin
        $dumpfile("axi4_slave_tb.vcd");
        $dumpvars(0, axi4_slave_tb);
        $display("================================================================");
        $display(" AXI4 Slave Testbench");
        $display("================================================================");
        reset_dut();
        test_single_write_read();
        test_burst();
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
