// =============================================================================
// MUTANT M01: INCR Address Increment Bug
// Bug: INCR burst increments by wrong amount (1 instead of 1 << burst_size)
// =============================================================================

module axi4_write_channel
  import axi4_pkg::*;
#(
  parameter ADDR_WIDTH = AXI_ADDR_WIDTH,
  parameter DATA_WIDTH = AXI_DATA_WIDTH,
  parameter ID_WIDTH   = AXI_ID_WIDTH
)(
  input  logic                      clk,
  input  logic                      aresetn,
  input  logic [ID_WIDTH-1:0]       awid,
  input  logic [ADDR_WIDTH-1:0]     awaddr,
  input  logic [7:0]                awlen,
  input  logic [2:0]                awsize,
  input  logic [1:0]                awburst,
  input  logic                      awvalid,
  output logic                      awready,
  input  logic [DATA_WIDTH-1:0]     wdata,
  input  logic [DATA_WIDTH/8-1:0]   wstrb,
  input  logic                      wlast,
  input  logic                      wvalid,
  output logic                      wready,
  output logic [ID_WIDTH-1:0]       bid,
  output logic [1:0]                bresp,
  output logic                      bvalid,
  input  logic                      bready,
  output logic                      mem_wr_en,
  output logic [ADDR_WIDTH-1:0]     mem_wr_addr,
  output logic [DATA_WIDTH-1:0]     mem_wr_data,
  output logic [DATA_WIDTH/8-1:0]   mem_wr_strb,
  input  logic                      decode_error
);

  typedef enum logic [2:0] {
    IDLE, ADDR_RECV, DATA_BURST, SEND_RESP, WAIT_BREADY
  } state_t;
  
  state_t state, next_state;
  
  logic [ID_WIDTH-1:0]    txn_id;
  logic [ADDR_WIDTH-1:0]  current_addr;
  logic [7:0]             burst_len;
  logic [7:0]             beat_count;
  logic [2:0]             burst_size;
  logic [1:0]             burst_type;
  logic                   has_decode_error;
  logic                   has_wlast_error;
  
  // BUG: Wrong increment - should be (1 << burst_size) but using 1
  logic [ADDR_WIDTH-1:0] addr_incr;
  assign addr_incr = 1;  // BUG: Should be (1 << burst_size)
  
  logic [ADDR_WIDTH-1:0] wrap_size;
  logic [ADDR_WIDTH-1:0] wrap_boundary;
  assign wrap_size = (burst_len + 1) << burst_size;
  
  always_ff @(posedge clk or negedge aresetn) begin
    if (!aresetn) state <= IDLE;
    else state <= next_state;
  end
  
  always_comb begin
    next_state = state;
    case (state)
      IDLE: if (awvalid && awready) next_state = ADDR_RECV;
      ADDR_RECV: next_state = DATA_BURST;
      DATA_BURST: if (wvalid && wready && wlast) next_state = SEND_RESP;
      SEND_RESP: next_state = bready ? IDLE : WAIT_BREADY;
      WAIT_BREADY: if (bready) next_state = IDLE;
      default: next_state = IDLE;
    endcase
  end
  
  always_ff @(posedge clk or negedge aresetn) begin
    if (!aresetn) begin
      txn_id <= '0; current_addr <= '0; burst_len <= '0;
      beat_count <= '0; burst_size <= '0; burst_type <= '0;
      wrap_boundary <= '0; has_decode_error <= 1'b0; has_wlast_error <= 1'b0;
    end else begin
      case (state)
        IDLE: begin
          if (awvalid && awready) begin
            txn_id <= awid; current_addr <= awaddr; burst_len <= awlen;
            burst_size <= awsize; burst_type <= awburst;
            wrap_boundary <= (awaddr & ~(wrap_size - 1));
            beat_count <= '0; has_decode_error <= decode_error; has_wlast_error <= 1'b0;
          end
        end
        DATA_BURST: begin
          if (wvalid && wready) begin
            beat_count <= beat_count + 1'b1;
            if ((beat_count == burst_len) && !wlast) has_wlast_error <= 1'b1;
            case (burst_type)
              BURST_FIXED: ;
              BURST_INCR: current_addr <= current_addr + addr_incr;  // Uses buggy increment
              BURST_WRAP: begin
                if ((current_addr + addr_incr) >= (wrap_boundary + wrap_size))
                  current_addr <= wrap_boundary;
                else current_addr <= current_addr + addr_incr;
              end
              default: current_addr <= current_addr + addr_incr;
            endcase
          end
        end
        default: ;
      endcase
    end
  end
  
  logic [1:0] resp_value;
  always_comb begin
    if (has_decode_error) resp_value = RESP_DECERR;
    else if (has_wlast_error) resp_value = RESP_SLVERR;
    else resp_value = RESP_OKAY;
  end
  
  assign awready = (state == IDLE);
  assign wready = (state == DATA_BURST);
  assign bid = txn_id;
  assign bresp = resp_value;
  assign bvalid = (state == SEND_RESP) || (state == WAIT_BREADY);
  assign mem_wr_en = (state == DATA_BURST) && wvalid && wready && !has_decode_error;
  assign mem_wr_addr = current_addr;
  assign mem_wr_data = wdata;
  assign mem_wr_strb = wstrb;

endmodule : axi4_write_channel

