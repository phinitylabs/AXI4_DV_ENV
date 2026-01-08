// =============================================================================
// AXI4 Package - Common definitions, parameters, and types
// =============================================================================

package axi4_pkg;

  // AXI4 Parameters
  parameter AXI_ADDR_WIDTH = 32;
  parameter AXI_DATA_WIDTH = 32;
  parameter AXI_ID_WIDTH   = 4;
  parameter AXI_STRB_WIDTH = AXI_DATA_WIDTH / 8;
  
  // Burst Types
  typedef enum logic [1:0] {
    BURST_FIXED = 2'b00,
    BURST_INCR  = 2'b01,
    BURST_WRAP  = 2'b10,
    BURST_RSVD  = 2'b11
  } axi_burst_t;
  
  // Response Types
  typedef enum logic [1:0] {
    RESP_OKAY   = 2'b00,
    RESP_EXOKAY = 2'b01,
    RESP_SLVERR = 2'b10,
    RESP_DECERR = 2'b11
  } axi_resp_t;
  
  // Lock Types
  typedef enum logic {
    LOCK_NORMAL    = 1'b0,
    LOCK_EXCLUSIVE = 1'b1
  } axi_lock_t;
  
  // Memory Types (Cache)
  typedef struct packed {
    logic bufferable;
    logic cacheable;
    logic read_allocate;
    logic write_allocate;
  } axi_cache_t;
  
  // Protection Types
  typedef struct packed {
    logic privileged;
    logic non_secure;
    logic instruction;
  } axi_prot_t;

endpackage : axi4_pkg

