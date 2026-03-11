// MUTANT M04: RRESP Corrupt Bug
// Bug: RRESP always returns OKAY, ignoring decode errors
// =============================================================================\n
module axi4_read_channel
  import axi4_pkg::*;
#(
  parameter ADDR_WIDTH = AXI_ADDR_WIDTH,
  parameter DATA_WIDTH = AXI_DATA_WIDTH,
  parameter ID_WIDTH   = AXI_ID_WIDTH
)(
  input  logic                      clk,
  input  logic                      aresetn,
  
  // AXI4 Read Address Channel (AR)
  input  logic [ID_WIDTH-1:0]       arid,
  input  logic [ADDR_WIDTH-1:0]     araddr,
  input  logic [7:0]                arlen,
  input  logic [2:0]                arsize,
  input  logic [1:0]                arburst,
  input  logic                      arvalid,
  output logic                      arready,
  
  // AXI4 Read Data Channel (R)
  output logic [ID_WIDTH-1:0]       rid,
  output logic [DATA_WIDTH-1:0]     rdata,
  output logic [1:0]                rresp,
  output logic                      rlast,
  output logic                      rvalid,
  input  logic                      rready,
  
  // Memory Read Interface
  output logic                      mem_rd_en,
  output logic [ADDR_WIDTH-1:0]     mem_rd_addr,
  input  logic [DATA_WIDTH-1:0]     mem_rd_data,
  input  logic                      mem_rd_valid,
  
  // Decode Error Input
  input  logic                      decode_error
);

  // ==========================================================================
  // State Machine
  // ==========================================================================
  typedef enum logic [2:0] {
    IDLE,
    ADDR_RECV,
    MEM_READ,
    MEM_WAIT,
    SEND_DATA,
    WAIT_RREADY
  } state_t;
  
  state_t state, next_state;
  
  // ==========================================================================
  // Burst Tracking Registers
  // ==========================================================================
  logic [ID_WIDTH-1:0]    txn_id;
  logic [ADDR_WIDTH-1:0]  current_addr;
  logic [7:0]             burst_len;
  logic [7:0]             beat_count;
  logic [2:0]             burst_size;
  logic [1:0]             burst_type;
  logic                   has_decode_error;
  
  // Data register for holding memory read result
  logic [DATA_WIDTH-1:0]  data_reg;
  
  // Address increment calculation
  logic [ADDR_WIDTH-1:0] addr_incr;
  assign addr_incr = (1 << burst_size);
  
  // Wrap boundary calculation
  logic [ADDR_WIDTH-1:0] wrap_size;
  logic [ADDR_WIDTH-1:0] wrap_boundary;
  assign wrap_size = (burst_len + 1) << burst_size;
  
  // ==========================================================================
  // State Machine - Sequential
  // ==========================================================================
  always_ff @(posedge clk or negedge aresetn) begin
    if (!aresetn) begin
      state <= IDLE;
    end else begin
      state <= next_state;
    end
  end
  
  // ==========================================================================
  // State Machine - Combinational
  // ==========================================================================
  always_comb begin
    next_state = state;
    case (state)
      IDLE: begin
        if (arvalid && arready)
          next_state = ADDR_RECV;
      end
      
      ADDR_RECV: begin
        next_state = MEM_READ;
      end
      
      MEM_READ: begin
        next_state = MEM_WAIT;
      end
      
      MEM_WAIT: begin
        if (mem_rd_valid || has_decode_error)
          next_state = SEND_DATA;
      end
      
      SEND_DATA: begin
        if (rready) begin
          if (beat_count == burst_len)
            next_state = IDLE;
          else
            next_state = MEM_READ;
        end else begin
          next_state = WAIT_RREADY;
        end
      end
      
      WAIT_RREADY: begin
        if (rready) begin
          if (beat_count == burst_len)
            next_state = IDLE;
          else
            next_state = MEM_READ;
        end
      end
      
      default: next_state = IDLE;
    endcase
  end
  
  // ==========================================================================
  // Burst Parameter Capture and Address Generation
  // ==========================================================================
  always_ff @(posedge clk or negedge aresetn) begin
    if (!aresetn) begin
      txn_id           <= '0;
      current_addr     <= '0;
      burst_len        <= '0;
      beat_count       <= '0;
      burst_size       <= '0;
      burst_type       <= '0;
      wrap_boundary    <= '0;
      has_decode_error <= 1'b0;
      data_reg         <= '0;
    end else begin
      case (state)
        IDLE: begin
          if (arvalid && arready) begin
            txn_id           <= arid;
            current_addr     <= araddr;
            burst_len        <= arlen;
            burst_size       <= arsize;
            burst_type       <= arburst;
            wrap_boundary    <= (araddr & ~(wrap_size - 1));
            beat_count       <= '0;
            has_decode_error <= decode_error;
          end
        end
        
        MEM_WAIT: begin
          if (mem_rd_valid) begin
            data_reg <= mem_rd_data;
          end
        end
        
        SEND_DATA, WAIT_RREADY: begin
          if (rready && rvalid && (beat_count < burst_len)) begin
            beat_count <= beat_count + 1'b1;
            
            // Update ID for next beat (important for back-to-back tracking)
            // ID should remain stable throughout burst
            
            // Address generation based on burst type
            case (burst_type)
              BURST_FIXED: begin
                // Address stays the same
              end
              BURST_INCR: begin
                current_addr <= current_addr + addr_incr;
              end
              BURST_WRAP: begin
                if ((current_addr + addr_incr) >= (wrap_boundary + wrap_size))
                  current_addr <= wrap_boundary;
                else
                  current_addr <= current_addr + addr_incr;
              end
              default: begin
                current_addr <= current_addr + addr_incr;
              end
            endcase
          end
        end
        
        default: ;
      endcase
    end
  end
  
  // ==========================================================================
  // Output Assignments
  // ==========================================================================
  
  // AR Channel
  assign arready = (state == IDLE);
  
  // R Channel
  assign rid    = txn_id;
  assign rdata  = has_decode_error ? '0 : data_reg;
  assign rresp  = RESP_OKAY  // BUG: Always OKAY, ignores decode error;
  assign rlast  = (beat_count == burst_len);
  assign rvalid = (state == SEND_DATA) || (state == WAIT_RREADY);
  
  // Memory Interface
  assign mem_rd_en   = (state == MEM_READ) && !has_decode_error;
  assign mem_rd_addr = current_addr;

endmodule : axi4_read_channel

