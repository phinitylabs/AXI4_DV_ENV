// =============================================================================
// AXI4 Slave Top - Complete AXI4 Slave with 5-module architecture
// =============================================================================
// 
// Module Hierarchy:
//   axi4_slave_top (this module)
//     ├── axi4_write_channel  - Combined AW+W+B channels
//     ├── axi4_read_channel   - Combined AR+R channels
//     ├── axi4_memory         - Backend storage
//     ├── axi4_decoder (wr)   - Write address decoder
//     └── axi4_decoder (rd)   - Read address decoder
//
// =============================================================================

module axi4_slave_top
  import axi4_pkg::*;
#(
  parameter ADDR_WIDTH = AXI_ADDR_WIDTH,
  parameter DATA_WIDTH = AXI_DATA_WIDTH,
  parameter ID_WIDTH   = AXI_ID_WIDTH,
  parameter MEM_DEPTH  = 4096
)(
  input  logic                      aclk,
  input  logic                      aresetn,
  
  // Write Address Channel
  input  logic [ID_WIDTH-1:0]       awid,
  input  logic [ADDR_WIDTH-1:0]     awaddr,
  input  logic [7:0]                awlen,
  input  logic [2:0]                awsize,
  input  logic [1:0]                awburst,
  input  logic                      awvalid,
  output logic                      awready,
  
  // Write Data Channel
  input  logic [DATA_WIDTH-1:0]     wdata,
  input  logic [DATA_WIDTH/8-1:0]   wstrb,
  input  logic                      wlast,
  input  logic                      wvalid,
  output logic                      wready,
  
  // Write Response Channel
  output logic [ID_WIDTH-1:0]       bid,
  output logic [1:0]                bresp,
  output logic                      bvalid,
  input  logic                      bready,
  
  // Read Address Channel
  input  logic [ID_WIDTH-1:0]       arid,
  input  logic [ADDR_WIDTH-1:0]     araddr,
  input  logic [7:0]                arlen,
  input  logic [2:0]                arsize,
  input  logic [1:0]                arburst,
  input  logic                      arvalid,
  output logic                      arready,
  
  // Read Data Channel
  output logic [ID_WIDTH-1:0]       rid,
  output logic [DATA_WIDTH-1:0]     rdata,
  output logic [1:0]                rresp,
  output logic                      rlast,
  output logic                      rvalid,
  input  logic                      rready
);

  // ==========================================================================
  // Internal Signals
  // ==========================================================================
  
  // Write path signals
  logic                      wr_decode_error;
  logic                      mem_wr_en;
  logic [ADDR_WIDTH-1:0]     mem_wr_addr;
  logic [DATA_WIDTH-1:0]     mem_wr_data;
  logic [DATA_WIDTH/8-1:0]   mem_wr_strb;
  
  // Read path signals
  logic                      rd_decode_error;
  logic                      mem_rd_en;
  logic [ADDR_WIDTH-1:0]     mem_rd_addr;
  logic [DATA_WIDTH-1:0]     mem_rd_data;
  logic                      mem_rd_valid;
  
  // ==========================================================================
  // Write Address Decoder
  // ==========================================================================
  axi4_decoder #(
    .ADDR_WIDTH(ADDR_WIDTH),
    .BASE_ADDR(32'h0000_0000),
    .ADDR_RANGE(32'h0000_FFFF)
  ) u_wr_decoder (
    .addr         (awaddr),
    .valid        (awvalid),
    .select       (),  // Not used
    .decode_error (wr_decode_error)
  );
  
  // ==========================================================================
  // Write Channel (AW + W + B combined)
  // ==========================================================================
  axi4_write_channel #(
    .ADDR_WIDTH(ADDR_WIDTH),
    .DATA_WIDTH(DATA_WIDTH),
    .ID_WIDTH(ID_WIDTH)
  ) u_write_channel (
    .clk          (aclk),
    .aresetn      (aresetn),
    // AW Channel
    .awid         (awid),
    .awaddr       (awaddr),
    .awlen        (awlen),
    .awsize       (awsize),
    .awburst      (awburst),
    .awvalid      (awvalid),
    .awready      (awready),
    // W Channel
    .wdata        (wdata),
    .wstrb        (wstrb),
    .wlast        (wlast),
    .wvalid       (wvalid),
    .wready       (wready),
    // B Channel
    .bid          (bid),
    .bresp        (bresp),
    .bvalid       (bvalid),
    .bready       (bready),
    // Memory Interface
    .mem_wr_en    (mem_wr_en),
    .mem_wr_addr  (mem_wr_addr),
    .mem_wr_data  (mem_wr_data),
    .mem_wr_strb  (mem_wr_strb),
    // Decode Error
    .decode_error (wr_decode_error)
  );
  
  // ==========================================================================
  // Read Address Decoder
  // ==========================================================================
  axi4_decoder #(
    .ADDR_WIDTH(ADDR_WIDTH),
    .BASE_ADDR(32'h0000_0000),
    .ADDR_RANGE(32'h0000_FFFF)
  ) u_rd_decoder (
    .addr         (araddr),
    .valid        (arvalid),
    .select       (),  // Not used
    .decode_error (rd_decode_error)
  );
  
  // ==========================================================================
  // Read Channel (AR + R combined)
  // ==========================================================================
  axi4_read_channel #(
    .ADDR_WIDTH(ADDR_WIDTH),
    .DATA_WIDTH(DATA_WIDTH),
    .ID_WIDTH(ID_WIDTH)
  ) u_read_channel (
    .clk          (aclk),
    .aresetn      (aresetn),
    // AR Channel
    .arid         (arid),
    .araddr       (araddr),
    .arlen        (arlen),
    .arsize       (arsize),
    .arburst      (arburst),
    .arvalid      (arvalid),
    .arready      (arready),
    // R Channel
    .rid          (rid),
    .rdata        (rdata),
    .rresp        (rresp),
    .rlast        (rlast),
    .rvalid       (rvalid),
    .rready       (rready),
    // Memory Interface
    .mem_rd_en    (mem_rd_en),
    .mem_rd_addr  (mem_rd_addr),
    .mem_rd_data  (mem_rd_data),
    .mem_rd_valid (mem_rd_valid),
    // Decode Error
    .decode_error (rd_decode_error)
  );
  
  // ==========================================================================
  // Memory Backend
  // ==========================================================================
  axi4_memory #(
    .ADDR_WIDTH(ADDR_WIDTH),
    .DATA_WIDTH(DATA_WIDTH),
    .MEM_DEPTH(MEM_DEPTH)
  ) u_memory (
    .clk      (aclk),
    .rst_n    (aresetn),
    // Write Port
    .wr_en    (mem_wr_en),
    .wr_addr  (mem_wr_addr),
    .wr_data  (mem_wr_data),
    .wr_strb  (mem_wr_strb),
    // Read Port
    .rd_en    (mem_rd_en),
    .rd_addr  (mem_rd_addr),
    .rd_data  (mem_rd_data),
    .rd_valid (mem_rd_valid)
  );

endmodule : axi4_slave_top
