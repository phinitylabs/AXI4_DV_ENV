// =============================================================================
// AXI4 Memory - Backend storage with byte-enable write support
// =============================================================================

module axi4_memory
  import axi4_pkg::*;
#(
  parameter ADDR_WIDTH = AXI_ADDR_WIDTH,
  parameter DATA_WIDTH = AXI_DATA_WIDTH,
  parameter MEM_DEPTH  = 4096  // 16KB for 32-bit data
)(
  input  logic                      clk,
  input  logic                      rst_n,
  
  // Write Port
  input  logic                      wr_en,
  input  logic [ADDR_WIDTH-1:0]     wr_addr,
  input  logic [DATA_WIDTH-1:0]     wr_data,
  input  logic [DATA_WIDTH/8-1:0]   wr_strb,
  
  // Read Port
  input  logic                      rd_en,
  input  logic [ADDR_WIDTH-1:0]     rd_addr,
  output logic [DATA_WIDTH-1:0]     rd_data,
  output logic                      rd_valid
);

  localparam MEM_ADDR_WIDTH = $clog2(MEM_DEPTH);
  
  // Memory array
  logic [DATA_WIDTH-1:0] mem [0:MEM_DEPTH-1];
  
  // Address mapping (word-aligned)
  logic [MEM_ADDR_WIDTH-1:0] wr_mem_addr, rd_mem_addr;
  assign wr_mem_addr = wr_addr[MEM_ADDR_WIDTH+1:2];
  assign rd_mem_addr = rd_addr[MEM_ADDR_WIDTH+1:2];
  
  // Write with byte strobes
  always_ff @(posedge clk) begin
    if (wr_en) begin
      for (int i = 0; i < DATA_WIDTH/8; i++) begin
        if (wr_strb[i]) begin
          mem[wr_mem_addr][i*8 +: 8] <= wr_data[i*8 +: 8];
        end
      end
    end
  end
  
  // Read with registered output
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      rd_data  <= '0;
      rd_valid <= 1'b0;
    end else begin
      rd_valid <= rd_en;
      if (rd_en) begin
        rd_data <= mem[rd_mem_addr];
      end
    end
  end
  
  // Initialize memory to zero (simulation only)
  initial begin
    for (int i = 0; i < MEM_DEPTH; i++) begin
      mem[i] = '0;
    end
  end

endmodule : axi4_memory

