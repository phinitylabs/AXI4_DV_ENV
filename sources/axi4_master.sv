// AXI4 Master Module - Complete Implementation
// This module implements an AXI4 master that can perform write and read transactions

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
    
    // Write transaction control
    logic [7:0]   write_count;
    logic [31:0]  write_base_addr;
    logic [7:0]   write_length;
    logic [2:0]   write_size;
    logic [1:0]   write_burst;
    logic         write_in_progress;
    
    // Read transaction control
    logic [7:0]   read_count;
    logic [31:0]  read_base_addr;
    logic [7:0]   read_length;
    logic [2:0]   read_size;
    logic [1:0]   read_burst;
    logic         read_in_progress;
    
    // Burst types
    localparam [1:0] FIXED = 2'b00;
    localparam [1:0] INCR  = 2'b01;
    localparam [1:0] WRAP  = 2'b10;
    
    // Response codes
    localparam [1:0] OKAY   = 2'b00;
    localparam [1:0] EXOKAY = 2'b01;
    localparam [1:0] SLVERR = 2'b10;
    localparam [1:0] DECERR = 2'b11;
    
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
                // Can start write or read transaction
                next_state = IDLE;
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
    
    // Write Address Channel
    always_ff @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            axi_awvalid <= 1'b0;
            axi_awaddr <= 32'h0;
            axi_awlen <= 8'h0;
            axi_awsize <= 3'h0;
            axi_awburst <= 2'h0;
            write_base_addr <= 32'h0;
            write_length <= 8'h0;
            write_size <= 3'h0;
            write_burst <= 2'h0;
            write_in_progress <= 1'b0;
        end else begin
            if (state == IDLE && !write_in_progress && !read_in_progress) begin
                // Start a write transaction (example: write to address 0x1000_0000)
                axi_awaddr <= 32'h1000_0000;
                axi_awlen <= 8'h3;  // 4 beats (length is 0-based)
                axi_awsize <= 3'h2; // 4 bytes
                axi_awburst <= INCR;
                axi_awvalid <= 1'b1;
                write_base_addr <= 32'h1000_0000;
                write_length <= 8'h3;
                write_size <= 3'h2;
                write_burst <= INCR;
            end else if (axi_awvalid && axi_awready) begin
                axi_awvalid <= 1'b0;
                write_in_progress <= 1'b1;
            end
        end
    end
    
    // Write Data Channel
    always_ff @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            axi_wvalid <= 1'b0;
            axi_wdata <= 32'h0;
            axi_wstrb <= 4'h0;
            axi_wlast <= 1'b0;
            write_count <= 8'h0;
        end else begin
            if (state == WRITE_DATA && !axi_wvalid) begin
                // Start sending write data
                axi_wdata <= 32'hDEAD_BEEF + write_count;
                axi_wstrb <= 4'hF; // All bytes valid
                axi_wlast <= (write_count == write_length);
                axi_wvalid <= 1'b1;
            end else if (axi_wvalid && axi_wready) begin
                if (axi_wlast) begin
                    axi_wvalid <= 1'b0;
                    axi_wlast <= 1'b0;
                    write_count <= 8'h0;
                end else begin
                    write_count <= write_count + 1;
                    axi_wdata <= 32'hDEAD_BEEF + write_count + 1;
                    axi_wlast <= (write_count + 1 == write_length);
                end
            end
        end
    end
    
    // Write Response Channel
    always_ff @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            axi_bready <= 1'b0;
            write_in_progress <= 1'b0;
        end else begin
            if (state == WRITE_RESP) begin
                axi_bready <= 1'b1;
            end else if (axi_bvalid && axi_bready) begin
                axi_bready <= 1'b0;
                write_in_progress <= 1'b0;
            end
        end
    end
    
    // Read Address Channel
    always_ff @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            axi_arvalid <= 1'b0;
            axi_araddr <= 32'h0;
            axi_arlen <= 8'h0;
            axi_arsize <= 3'h0;
            axi_arburst <= 2'h0;
            read_base_addr <= 32'h0;
            read_length <= 8'h0;
            read_size <= 3'h0;
            read_burst <= 2'h0;
            read_in_progress <= 1'b0;
        end else begin
            if (state == IDLE && !write_in_progress && !read_in_progress) begin
                // Start a read transaction (example: read from address 0x1000_0000)
                axi_araddr <= 32'h1000_0000;
                axi_arlen <= 8'h0;  // Single beat
                axi_arsize <= 3'h2; // 4 bytes
                axi_arburst <= INCR;
                axi_arvalid <= 1'b1;
                read_base_addr <= 32'h1000_0000;
                read_length <= 8'h0;
                read_size <= 3'h2;
                read_burst <= INCR;
            end else if (axi_arvalid && axi_arready) begin
                axi_arvalid <= 1'b0;
                read_in_progress <= 1'b1;
            end
        end
    end
    
    // Read Data Channel
    always_ff @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            axi_rready <= 1'b0;
            read_in_progress <= 1'b0;
            read_count <= 8'h0;
        end else begin
            if (state == READ_DATA) begin
                axi_rready <= 1'b1;
            end else if (axi_rvalid && axi_rready) begin
                if (axi_rlast) begin
                    axi_rready <= 1'b0;
                    read_in_progress <= 1'b0;
                    read_count <= 8'h0;
                end else begin
                    read_count <= read_count + 1;
                end
            end
        end
    end

endmodule

