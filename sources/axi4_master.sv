// AXI4 Master Module - Fixed Implementation
// This module implements an AXI4 master that generates diverse transactions

module axi4_master (
    input logic clk,
    input logic resetn,
    
    // Write Address Channel
    output logic [31:0]  axi_awaddr,
    output logic [7:0]   axi_awlen,
    output logic [2:0]   axi_awsize,
    output logic [1:0]   axi_awburst,
    output logic         axi_awvalid,
    input logic          axi_awready,
    
    // Write Data Channel
    output logic [31:0]  axi_wdata,
    output logic [3:0]   axi_wstrb,
    output logic         axi_wlast,
    output logic         axi_wvalid,
    input logic          axi_wready,
    
    // Write Response Channel
    input logic [1:0]    axi_bresp,
    input logic          axi_bvalid,
    output logic         axi_bready,
    
    // Read Address Channel
    output logic [31:0]  axi_araddr,
    output logic [7:0]   axi_arlen,
    output logic [2:0]   axi_arsize,
    output logic [1:0]   axi_arburst,
    output logic         axi_arvalid,
    input logic          axi_arready,
    
    // Read Data Channel
    input logic [31:0]   axi_rdata,
    input logic [1:0]    axi_rresp,
    input logic          axi_rlast,
    input logic          axi_rvalid,
    output logic         axi_rready
);

    // Master State Machine
    typedef enum logic [2:0] {
        IDLE,
        WRITE_ADDR,
        WRITE_DATA,
        WRITE_RESP,
        READ_ADDR,
        READ_DATA
    } master_state_t;
    
    master_state_t state, next_state;
    
    // Transaction counter for generating diverse patterns
    logic [7:0] txn_count;
    logic       do_write;
    
    // Write transaction control
    logic [7:0]   write_count;
    logic [7:0]   write_length;
    
    // Read transaction control
    logic [7:0]   read_count;
    logic [7:0]   read_length;
    
    // Burst types
    localparam [1:0] FIXED = 2'b00;
    localparam [1:0] INCR  = 2'b01;
    localparam [1:0] WRAP  = 2'b10;
    
    // Transaction patterns for coverage
    // Addresses within valid range 0x000 - 0x3FF
    logic [31:0] test_addrs [0:7];
    logic [7:0]  test_lens  [0:7];
    logic [1:0]  test_bursts[0:7];
    logic [3:0]  test_strobes[0:7];
    
    // Initialize test patterns
    initial begin
        // Pattern 0: Single beat at address 0 (cp_addr_zero, cp_burst_single)
        test_addrs[0] = 32'h0000_0000;
        test_lens[0]  = 8'h0;
        test_bursts[0] = INCR;
        test_strobes[0] = 4'hF;
        
        // Pattern 1: INCR burst (cp_burst_incr)
        test_addrs[1] = 32'h0000_0010;
        test_lens[1]  = 8'h3;
        test_bursts[1] = INCR;
        test_strobes[1] = 4'hF;
        
        // Pattern 2: WRAP burst (cp_burst_wrap)
        test_addrs[2] = 32'h0000_0100;
        test_lens[2]  = 8'h3;
        test_bursts[2] = WRAP;
        test_strobes[2] = 4'hF;
        
        // Pattern 3: FIXED burst (cp_burst_fixed)
        test_addrs[3] = 32'h0000_0200;
        test_lens[3]  = 8'h3;
        test_bursts[3] = FIXED;
        test_strobes[3] = 4'hF;
        
        // Pattern 4: Max burst length (cp_burst_max)
        test_addrs[4] = 32'h0000_0040;
        test_lens[4]  = 8'hF;
        test_bursts[4] = INCR;
        test_strobes[4] = 4'hF;
        
        // Pattern 5: Partial strobe (cp_strobe_partial)
        test_addrs[5] = 32'h0000_0080;
        test_lens[5]  = 8'h0;
        test_bursts[5] = INCR;
        test_strobes[5] = 4'h3;
        
        // Pattern 6: Address at boundary (cp_addr_boundary)
        test_addrs[6] = 32'h0000_03FC;
        test_lens[6]  = 8'h0;
        test_bursts[6] = INCR;
        test_strobes[6] = 4'hF;
        
        // Pattern 7: Out of range for DECERR (cp_decode_error)
        test_addrs[7] = 32'h0000_1000;
        test_lens[7]  = 8'h0;
        test_bursts[7] = INCR;
        test_strobes[7] = 4'hF;
    end
    
    // State machine
    always_ff @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            state <= IDLE;
        end else begin
            state <= next_state;
        end
    end
    
    // Next state logic
    always_comb begin
        next_state = state;
        case (state)
            IDLE: begin
                if (txn_count < 16) begin
                    if (do_write)
                        next_state = WRITE_ADDR;
                    else
                        next_state = READ_ADDR;
                end
            end
            WRITE_ADDR: begin
                if (axi_awvalid && axi_awready) begin
                    next_state = WRITE_DATA;
                end
            end
            WRITE_DATA: begin
                if (axi_wvalid && axi_wready && axi_wlast) begin
                    next_state = WRITE_RESP;
                end
            end
            WRITE_RESP: begin
                if (axi_bvalid && axi_bready) begin
                    next_state = IDLE;
                end
            end
            READ_ADDR: begin
                if (axi_arvalid && axi_arready) begin
                    next_state = READ_DATA;
                end
            end
            READ_DATA: begin
                if (axi_rvalid && axi_rready && axi_rlast) begin
                    next_state = IDLE;
                end
            end
        endcase
    end
    
    // Transaction counter and write/read alternation
    always_ff @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            txn_count <= 8'h0;
            do_write <= 1'b1;
        end else begin
            if ((state == WRITE_RESP && axi_bvalid && axi_bready) ||
                (state == READ_DATA && axi_rvalid && axi_rready && axi_rlast)) begin
                txn_count <= txn_count + 1;
                do_write <= ~do_write;
            end
        end
    end
    
    // Pattern index
    wire [2:0] pattern_idx = txn_count[2:0];
    
    // Write Address Channel
    always_ff @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            axi_awvalid <= 1'b0;
            axi_awaddr <= 32'h0;
            axi_awlen <= 8'h0;
            axi_awsize <= 3'h2;
            axi_awburst <= INCR;
            write_length <= 8'h0;
        end else begin
            if (state == IDLE && next_state == WRITE_ADDR) begin
                axi_awaddr <= test_addrs[pattern_idx];
                axi_awlen <= test_lens[pattern_idx];
                axi_awsize <= 3'h2;
                axi_awburst <= test_bursts[pattern_idx];
                axi_awvalid <= 1'b1;
                write_length <= test_lens[pattern_idx];
            end else if (axi_awvalid && axi_awready) begin
                axi_awvalid <= 1'b0;
            end
        end
    end
    
    // Write Data Channel
    always_ff @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            axi_wvalid <= 1'b0;
            axi_wdata <= 32'h0;
            axi_wstrb <= 4'hF;
            axi_wlast <= 1'b0;
            write_count <= 8'h0;
        end else begin
            if (state == WRITE_DATA && !axi_wvalid) begin
                axi_wdata <= 32'hCAFE_0000 + {24'h0, write_count};
                axi_wstrb <= test_strobes[pattern_idx];
                axi_wlast <= (write_count == write_length);
                axi_wvalid <= 1'b1;
            end else if (axi_wvalid && axi_wready) begin
                if (axi_wlast) begin
                    axi_wvalid <= 1'b0;
                    axi_wlast <= 1'b0;
                    write_count <= 8'h0;
                end else begin
                    write_count <= write_count + 1;
                    axi_wdata <= 32'hCAFE_0000 + {24'h0, write_count + 8'h1};
                    axi_wlast <= (write_count + 1 == write_length);
                end
            end
        end
    end
    
    // Write Response Channel
    always_ff @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            axi_bready <= 1'b0;
        end else begin
            if (state == WRITE_RESP) begin
                axi_bready <= 1'b1;
            end else begin
                axi_bready <= 1'b0;
            end
        end
    end
    
    // Read Address Channel
    always_ff @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            axi_arvalid <= 1'b0;
            axi_araddr <= 32'h0;
            axi_arlen <= 8'h0;
            axi_arsize <= 3'h2;
            axi_arburst <= INCR;
            read_length <= 8'h0;
        end else begin
            if (state == IDLE && next_state == READ_ADDR) begin
                axi_araddr <= test_addrs[pattern_idx];
                axi_arlen <= test_lens[pattern_idx];
                axi_arsize <= 3'h2;
                axi_arburst <= test_bursts[pattern_idx];
                axi_arvalid <= 1'b1;
                read_length <= test_lens[pattern_idx];
            end else if (axi_arvalid && axi_arready) begin
                axi_arvalid <= 1'b0;
            end
        end
    end
    
    // Read Data Channel
    always_ff @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            axi_rready <= 1'b0;
            read_count <= 8'h0;
        end else begin
            if (state == READ_DATA) begin
                axi_rready <= 1'b1;
                if (axi_rvalid && axi_rready) begin
                    if (axi_rlast) begin
                        read_count <= 8'h0;
                    end else begin
                        read_count <= read_count + 1;
                    end
                end
            end else begin
                axi_rready <= 1'b0;
            end
        end
    end

endmodule
