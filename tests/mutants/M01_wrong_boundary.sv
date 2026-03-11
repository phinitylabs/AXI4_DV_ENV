// Mutant M01: Wrong upper boundary check (uses < instead of <=)
module axi4_decoder
  import axi4_pkg::*;
#(
  parameter ADDR_WIDTH = AXI_ADDR_WIDTH,
  parameter BASE_ADDR  = 32'h0000_0000,
  parameter ADDR_RANGE = 32'h0000_FFFF
)(
  input  logic [ADDR_WIDTH-1:0] addr,
  input  logic                  valid,
  
  output logic                  select,
  output logic                  decode_error
);

  logic addr_in_range;
  
  // BUG: Uses < instead of <= for upper bound
  assign addr_in_range = (addr >= BASE_ADDR) && (addr < (BASE_ADDR + ADDR_RANGE));
  
  assign select       = valid && addr_in_range;
  assign decode_error = valid && !addr_in_range;

endmodule : axi4_decoder

