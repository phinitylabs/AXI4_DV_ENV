// =============================================================================
// MUTANT E09: Partial Strobe Bug
// Bug: Only byte 0 strobe works, other strobes are ignored
// =============================================================================

module axi4_memory
  import axi4_pkg::*;
#(
  parameter ADDR_WIDTH = AXI_ADDR_WIDTH,
  parameter DATA_WIDTH = AXI_DATA_WIDTH,
  parameter MEM_DEPTH  = 4096
)(
  input  logic                      clk,
  input  logic                      rst_n,
  
  input  logic                      wr_en,
  input  logic [ADDR_WIDTH-1:0]     wr_addr,
  input  logic [DATA_WIDTH-1:0]     wr_data,
  input  logic [DATA_WIDTH/8-1:0]   wr_strb,
  
  input  logic                      rd_en,
  input  logic [ADDR_WIDTH-1:0]     rd_addr,
  output logic [DATA_WIDTH-1:0]     rd_data,
  output logic                      rd_valid
);

  localparam MEM_ADDR_WIDTH = $clog2(MEM_DEPTH);
  
  logic [DATA_WIDTH-1:0] mem [0:MEM_DEPTH-1];
  
  logic [MEM_ADDR_WIDTH-1:0] wr_mem_addr, rd_mem_addr;
  assign wr_mem_addr = wr_addr[MEM_ADDR_WIDTH+1:2];
  assign rd_mem_addr = rd_addr[MEM_ADDR_WIDTH+1:2];
  
  // BUG: Only checks wr_strb[0], ignores other strobes!
  always_ff @(posedge clk) begin
    if (wr_en) begin
      // BUG: All bytes use strobe[0] instead of their own strobe bit
      if (wr_strb[0]) begin
        mem[wr_mem_addr][7:0]   <= wr_data[7:0];
      end
      if (wr_strb[0]) begin  // BUG: Should be wr_strb[1]
        mem[wr_mem_addr][15:8]  <= wr_data[15:8];
      end
      if (wr_strb[0]) begin  // BUG: Should be wr_strb[2]
        mem[wr_mem_addr][23:16] <= wr_data[23:16];
      end
      if (wr_strb[0]) begin  // BUG: Should be wr_strb[3]
        mem[wr_mem_addr][31:24] <= wr_data[31:24];
      end
    end
  end
  
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
  
  initial begin
    for (int i = 0; i < MEM_DEPTH; i++) begin
      mem[i] = '0;
    end
  end

endmodule : axi4_memory

