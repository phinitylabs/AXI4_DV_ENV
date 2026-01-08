// =============================================================================
// AXI4 Memory Data Integrity Testbench - SVA Assertions Required
// Task: Add SVA assertions to verify memory read/write data integrity
// =============================================================================
//
// Module Under Test: axi4_memory
//
// The memory module behavior:
// - Write: When wr_en=1, data is written to mem[wr_addr] using wr_strb byte enables
// - Read: When rd_en=1, data is read from mem[rd_addr], rd_valid asserts next cycle
//
// Your task: Write SVA assertions that verify:
// 1. Data integrity - reads return what was written
// 2. Correct timing - rd_valid follows rd_en by 1 cycle
// 3. Unwritten addresses return 0
//
// IMPORTANT: 
// - You must implement your own tracking/reference model
// - Your assertions must detect bugs in mutant designs
// - Simple assertions that don't track state will NOT pass
// =============================================================================

`timescale 1ns/1ps

module axi4_memory_tb;

    // Parameters
    parameter ADDR_WIDTH = 32;
    parameter DATA_WIDTH = 32;
    parameter MEM_DEPTH  = 4096;
    parameter CLK_PERIOD = 10;

    // Signals
    logic clk;
    logic rst_n;

    // Write Port
    logic                     wr_en;
    logic [ADDR_WIDTH-1:0]    wr_addr;
    logic [DATA_WIDTH-1:0]    wr_data;
    logic [DATA_WIDTH/8-1:0]  wr_strb;

    // Read Port
    logic                     rd_en;
    logic [ADDR_WIDTH-1:0]    rd_addr;
    logic [DATA_WIDTH-1:0]    rd_data;
    logic                     rd_valid;

    // Clock generation
    initial begin
        clk = 0;
        forever #(CLK_PERIOD/2) clk = ~clk;
    end

    // DUT instantiation
    axi4_memory #(
        .ADDR_WIDTH(ADDR_WIDTH),
        .DATA_WIDTH(DATA_WIDTH),
        .MEM_DEPTH(MEM_DEPTH)
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .wr_en(wr_en),
        .wr_addr(wr_addr),
        .wr_data(wr_data),
        .wr_strb(wr_strb),
        .rd_en(rd_en),
        .rd_addr(rd_addr),
        .rd_data(rd_data),
        .rd_valid(rd_valid)
    );

    // =========================================================================
    // IMPLEMENT YOUR TRACKING LOGIC AND ASSERTIONS BELOW
    // =========================================================================
    //
    // You need to:
    // 1. Create a reference model that tracks expected memory contents
    // 2. Write SVA assertions that compare DUT output against reference
    // 3. Verify timing relationships (rd_valid timing)
    //
    // Hint: You'll need to track:
    // - What data was written to each address
    // - Whether each address has been written
    // - The previous read address (for checking rd_data on rd_valid)
    //
    // Your assertions MUST use $error() to report failures.
    //
    // =========================================================================



    // =========================================================================
    // END OF ASSERTION SECTION
    // =========================================================================

    // Reset Task
    task automatic reset_dut();
        rst_n = 0;
        wr_en = 0;
        wr_addr = 0;
        wr_data = 0;
        wr_strb = 0;
        rd_en = 0;
        rd_addr = 0;
        repeat(10) @(posedge clk);
        rst_n = 1;
        repeat(5) @(posedge clk);
    endtask

    // Write Task
    task automatic mem_write(input logic [ADDR_WIDTH-1:0] addr, input logic [DATA_WIDTH-1:0] data);
        wr_addr = addr;
        wr_data = data;
        wr_strb = 4'b1111;
        wr_en = 1;
        @(posedge clk);
        wr_en = 0;
        @(posedge clk);
    endtask

    // Read Task (no verification - assertions should catch errors)
    task automatic mem_read(input logic [ADDR_WIDTH-1:0] addr);
        rd_addr = addr;
        rd_en = 1;
        @(posedge clk);
        rd_en = 0;
        @(posedge clk);
    endtask

    // Stimulus: Exercise the memory interface
    initial begin
        $dumpfile("axi4_memory_tb.vcd");
        $dumpvars(0, axi4_memory_tb);
        
        $display("================================================================");
        $display(" AXI4 Memory Data Integrity Testbench");
        $display("================================================================");
        $display(" Your assertions should detect any data integrity issues.");
        $display("================================================================");

        reset_dut();
        
        // Basic write and read
        mem_write(32'h0000_0100, 32'hDEAD_BEEF);
        mem_read(32'h0000_0100);
        
        // Multiple addresses
        for (int i = 0; i < 4; i++) begin
            mem_write(32'h0000_0200 + (i * 4), 32'hABCD_0000 + i);
        end
        for (int i = 0; i < 4; i++) begin
            mem_read(32'h0000_0200 + (i * 4));
        end
        
        // Read from unwritten address
        mem_read(32'h0000_1000);

        #(CLK_PERIOD * 20);

        $display("\n================================================================");
        $display(" Stimulus Complete - Assertions should have detected any bugs");
        $display("================================================================");

        $finish;
    end

    // Timeout
    initial begin
        #5000000;
        $display("ERROR: Timeout!");
        $finish;
    end

endmodule
