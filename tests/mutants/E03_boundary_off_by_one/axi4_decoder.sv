// =============================================================================
// MUTANT E03: Boundary Off-by-One Bug
// Bug: Uses > instead of >= for boundary check, making 0xFFFF invalid
// =============================================================================

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
  
  // BUG: Uses < instead of <=, so address 0xFFFF is treated as out of range!
  // Should be: (addr >= BASE_ADDR) && (addr <= (BASE_ADDR + ADDR_RANGE))
  assign addr_in_range = (addr >= BASE_ADDR) && (addr < (BASE_ADDR + ADDR_RANGE));  // BUG
  
  assign select       = valid && addr_in_range;
  assign decode_error = valid && !addr_in_range;

endmodule : axi4_decoder

