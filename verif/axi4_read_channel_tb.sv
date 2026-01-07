// =============================================================================
// AXI4 Read Channel Testbench - Starter Template
// Task: Write BOTH tests AND SVA assertions for complete verification
// =============================================================================
//
// This is a combined testbench + assertion problem:
// 1. Write test tasks to exercise read transactions
// 2. Write SVA assertions to verify protocol correctness
// =============================================================================

`timescale 1ns/1ps

module axi4_read_channel_tb
  import axi4_pkg::*;
;

    // Parameters
    parameter ADDR_WIDTH = 32;
    parameter DATA_WIDTH = 32;
    parameter ID_WIDTH   = 4;
    parameter MEM_DEPTH  = 4096;
    parameter CLK_PERIOD = 10;

    // Signals
    logic clk;
    logic aresetn;

    // AR Channel
    logic [ID_WIDTH-1:0]   arid;
    logic [ADDR_WIDTH-1:0] araddr;
    logic [7:0]            arlen;
    logic [2:0]            arsize;
    logic [1:0]            arburst;
    logic                  arvalid;
    logic                  arready;

    // R Channel
    logic [ID_WIDTH-1:0]   rid;
    logic [DATA_WIDTH-1:0] rdata;
    logic [1:0]            rresp;
    logic                  rlast;
    logic                  rvalid;
    logic                  rready;

    // Memory Interface
    logic                  mem_rd_en;
    logic [ADDR_WIDTH-1:0] mem_rd_addr;
    logic [DATA_WIDTH-1:0] mem_rd_data;
    logic                  mem_rd_valid;
    logic                  decode_error;

    // Test counters
    int test_count = 0;
    int pass_count = 0;
    int fail_count = 0;

    // Clock generation
    initial begin
        clk = 0;
        forever #(CLK_PERIOD/2) clk = ~clk;
    end

    // DUT instantiation
    axi4_read_channel #(
        .ADDR_WIDTH(ADDR_WIDTH),
        .DATA_WIDTH(DATA_WIDTH),
        .ID_WIDTH(ID_WIDTH)
    ) dut (
        .clk(clk),
        .aresetn(aresetn),
        .arid(arid),
        .araddr(araddr),
        .arlen(arlen),
        .arsize(arsize),
        .arburst(arburst),
        .arvalid(arvalid),
        .arready(arready),
        .rid(rid),
        .rdata(rdata),
        .rresp(rresp),
        .rlast(rlast),
        .rvalid(rvalid),
        .rready(rready),
        .mem_rd_en(mem_rd_en),
        .mem_rd_addr(mem_rd_addr),
        .mem_rd_data(mem_rd_data),
        .mem_rd_valid(mem_rd_valid),
        .decode_error(decode_error)
    );

    // =========================================================================
    // MEMORY MODEL (already implemented)
    // =========================================================================
    logic [DATA_WIDTH-1:0] mem [0:MEM_DEPTH-1];
    
    // Initialize memory with pattern
    initial begin
        for (int i = 0; i < MEM_DEPTH; i++) begin
            mem[i] = 32'hDADA_0000 + i;
        end
    end
    
    // Memory read response
    always_ff @(posedge clk or negedge aresetn) begin
        if (!aresetn) begin
            mem_rd_data <= '0;
            mem_rd_valid <= 1'b0;
        end else begin
            mem_rd_valid <= mem_rd_en;
            if (mem_rd_en) begin
                mem_rd_data <= mem[mem_rd_addr[13:2]];
            end
        end
    end

    // =========================================================================
    // TRACKING SIGNALS FOR ASSERTIONS (use these, don't access DUT internals)
    // =========================================================================
    
    // Track read address phase
    logic                  rd_in_burst;
    logic [ADDR_WIDTH-1:0] rd_start_addr;
    logic [7:0]            rd_total_beats;
    logic [7:0]            rd_beat_count;
    logic [1:0]            rd_burst_type;
    logic [2:0]            rd_burst_size;
    
    always_ff @(posedge clk or negedge aresetn) begin
        if (!aresetn) begin
            rd_in_burst <= 1'b0;
            rd_start_addr <= '0;
            rd_total_beats <= '0;
            rd_beat_count <= '0;
            rd_burst_type <= '0;
            rd_burst_size <= '0;
        end else begin
            if (arvalid && arready) begin
                rd_in_burst <= 1'b1;
                rd_start_addr <= araddr;
                rd_total_beats <= arlen + 1;
                rd_beat_count <= '0;
                rd_burst_type <= arburst;
                rd_burst_size <= arsize;
            end else if (rvalid && rready) begin
                rd_beat_count <= rd_beat_count + 1;
                if (rlast) begin
                    rd_in_burst <= 1'b0;
                end
            end
        end
    end

    // =========================================================================
    // ADD YOUR SVA ASSERTIONS HERE
    // =========================================================================
    //
    // Required assertions:
    // 1. RLAST timing - asserts on final beat of burst
    // 2. RVALID/RREADY handshake - data held until accepted
    // 3. Response correctness - proper RRESP values
    //
    // Example assertion structure:
    //
    // property p_rlast_timing;
    //     @(posedge clk) disable iff (!aresetn)
    //     (rvalid && rready && rd_in_burst && rd_beat_count == rd_total_beats - 1)
    //     |-> rlast;
    // endproperty
    // assert property (p_rlast_timing) else $error("RLAST timing error!");
    //
    // =========================================================================



    // =========================================================================
    // END OF ASSERTION SECTION
    // =========================================================================

    // Reset Task
    task automatic reset_dut();
        aresetn = 0;
        arid = 0;
        araddr = 0;
        arlen = 0;
        arsize = 2;  // 4 bytes
        arburst = BURST_INCR;
        arvalid = 0;
        rready = 0;
        decode_error = 0;
        repeat(10) @(posedge clk);
        aresetn = 1;
        repeat(5) @(posedge clk);
    endtask

    // =========================================================================
    // ADD YOUR READ TEST TASKS HERE
    // =========================================================================
    //
    // Required tests:
    // 1. Single beat read
    // 2. Burst read (INCR type)
    // 3. RLAST verification
    //
    // Example task structure:
    //
    // task automatic test_single_read();
    //     test_count++;
    //     $display("[TEST %0d] Single Beat Read", test_count);
    //     
    //     // Issue read address
    //     araddr = 32'h0000_0100;
    //     arlen = 0;  // 1 beat
    //     arburst = BURST_INCR;
    //     arvalid = 1;
    //     
    //     wait(arready);
    //     @(posedge clk);
    //     arvalid = 0;
    //     
    //     // Collect response
    //     rready = 1;
    //     wait(rvalid && rlast);
    //     @(posedge clk);
    //     rready = 0;
    //     
    //     pass_count++;
    // endtask
    //
    // =========================================================================



    // =========================================================================
    // END OF TEST SECTION
    // =========================================================================

    // Main test sequence
    initial begin
        $dumpfile("axi4_read_channel_tb.vcd");
        $dumpvars(0, axi4_read_channel_tb);
        
        $display("================================================================");
        $display(" AXI4 Read Channel Testbench");
        $display("================================================================");

        reset_dut();

        // ADD YOUR TEST TASK CALLS HERE
        // test_single_read();
        // test_burst_read();
        // test_rlast_check();

        #(CLK_PERIOD * 100);

        $display("\n================================================================");
        $display(" Test Summary: Total=%0d, PASSED=%0d, FAILED=%0d", 
                 test_count, pass_count, fail_count);
        $display("================================================================");

        if (fail_count > 0) begin
            $error("TESTBENCH FAILED");
        end

        $finish;
    end

    // Timeout
    initial begin
        #5000000;
        $display("ERROR: Timeout!");
        $finish;
    end

endmodule

