// Mutant M03: Missing valid check on outputs
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
  
  assign addr_in_range = (addr >= BASE_ADDR) && (addr <= (BASE_ADDR + ADDR_RANGE));
  
  // BUG: Missing valid check - outputs always active based on address
  assign select       = addr_in_range;
  assign decode_error = !addr_in_range;

endmodule : axi4_decoder

