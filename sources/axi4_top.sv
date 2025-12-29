// AXI4 Top Module - Complete Implementation
// This is the top-level module that instantiates master, slave, and interrupt controller

module axi4_top (
    input logic clk,
    input logic resetn
);

    // AXI4 Write Address Channel Signals
    logic [31:0]  axi_awaddr;
    logic [7:0]   axi_awlen;
    logic [2:0]   axi_awsize;
    logic [1:0]   axi_awburst;
    logic         axi_awvalid;
    logic         axi_awready;
    
    // AXI4 Write Data Channel Signals
    logic [31:0]  axi_wdata;
    logic [3:0]   axi_wstrb;
    logic         axi_wlast;
    logic         axi_wvalid;
    logic         axi_wready;
    
    // AXI4 Write Response Channel Signals
    logic [1:0]   axi_bresp;
    logic         axi_bvalid;
    logic         axi_bready;
    
    // AXI4 Read Address Channel Signals
    logic [31:0]  axi_araddr;
    logic [7:0]   axi_arlen;
    logic [2:0]   axi_arsize;
    logic [1:0]   axi_arburst;
    logic         axi_arvalid;
    logic         axi_arready;
    
    // AXI4 Read Data Channel Signals
    logic [31:0]  axi_rdata;
    logic [1:0]   axi_rresp;
    logic         axi_rlast;
    logic         axi_rvalid;
    logic         axi_rready;
    
    // Interrupt signals
    logic         interrupt_req;
    logic         interrupt_ack;

    // AXI4 Master Instance
    axi4_master master (
        .clk(clk),
        .resetn(resetn),
        .axi_awaddr(axi_awaddr),
        .axi_awlen(axi_awlen),
        .axi_awsize(axi_awsize),
        .axi_awburst(axi_awburst),
        .axi_awvalid(axi_awvalid),
        .axi_awready(axi_awready),
        .axi_wdata(axi_wdata),
        .axi_wstrb(axi_wstrb),
        .axi_wlast(axi_wlast),
        .axi_wvalid(axi_wvalid),
        .axi_wready(axi_wready),
        .axi_bresp(axi_bresp),
        .axi_bvalid(axi_bvalid),
        .axi_bready(axi_bready),
        .axi_araddr(axi_araddr),
        .axi_arlen(axi_arlen),
        .axi_arsize(axi_arsize),
        .axi_arburst(axi_arburst),
        .axi_arvalid(axi_arvalid),
        .axi_arready(axi_arready),
        .axi_rdata(axi_rdata),
        .axi_rresp(axi_rresp),
        .axi_rlast(axi_rlast),
        .axi_rvalid(axi_rvalid),
        .axi_rready(axi_rready)
    );
    
    // AXI4 Slave Instance
    axi4_slave slave (
        .clk(clk),
        .resetn(resetn),
        .axi_awaddr(axi_awaddr),
        .axi_awlen(axi_awlen),
        .axi_awsize(axi_awsize),
        .axi_awburst(axi_awburst),
        .axi_awvalid(axi_awvalid),
        .axi_awready(axi_awready),
        .axi_wdata(axi_wdata),
        .axi_wstrb(axi_wstrb),
        .axi_wlast(axi_wlast),
        .axi_wvalid(axi_wvalid),
        .axi_wready(axi_wready),
        .axi_bresp(axi_bresp),
        .axi_bvalid(axi_bvalid),
        .axi_bready(axi_bready),
        .axi_araddr(axi_araddr),
        .axi_arlen(axi_arlen),
        .axi_arsize(axi_arsize),
        .axi_arburst(axi_arburst),
        .axi_arvalid(axi_arvalid),
        .axi_arready(axi_arready),
        .axi_rdata(axi_rdata),
        .axi_rresp(axi_rresp),
        .axi_rlast(axi_rlast),
        .axi_rvalid(axi_rvalid),
        .axi_rready(axi_rready)
    );
    
    // Interrupt Controller Instance
    axi4_interrupt interrupt_ctrl (
        .clk(clk),
        .resetn(resetn),
        .interrupt_req(interrupt_req),
        .interrupt_ack(interrupt_ack)
    );
    
    // ==========================================================================
    // FIXED COVERAGE MODULE (for grading agent stimulus quality)
    // This module is NOT modified by agents - it measures how well their
    // stimulus exercises the DUT.
    // ==========================================================================
    axi4_coverage #(
        .ADDR_WIDTH(32),
        .DATA_WIDTH(32)
    ) coverage_monitor (
        .clk(clk),
        .resetn(resetn),
        // Write Address Channel
        .awaddr(axi_awaddr),
        .awlen(axi_awlen),
        .awsize(axi_awsize),
        .awburst(axi_awburst),
        .awvalid(axi_awvalid),
        .awready(axi_awready),
        // Write Data Channel
        .wdata(axi_wdata),
        .wstrb(axi_wstrb),
        .wlast(axi_wlast),
        .wvalid(axi_wvalid),
        .wready(axi_wready),
        // Write Response Channel
        .bresp(axi_bresp),
        .bvalid(axi_bvalid),
        .bready(axi_bready),
        // Read Address Channel
        .araddr(axi_araddr),
        .arlen(axi_arlen),
        .arsize(axi_arsize),
        .arburst(axi_arburst),
        .arvalid(axi_arvalid),
        .arready(axi_arready),
        // Read Data Channel
        .rdata(axi_rdata),
        .rresp(axi_rresp),
        .rlast(axi_rlast),
        .rvalid(axi_rvalid),
        .rready(axi_rready)
    );

endmodule

