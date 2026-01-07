// =============================================================================
// AXI4 Memory Data Integrity Testbench - Starter Template
// Task: Add SVA assertions to verify memory read/write data integrity
// =============================================================================
//
// The memory module stores data at addresses and returns it on read.
// Your task: Write assertions to verify data integrity
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
    // DATA TRACKING - Use these for your assertions (already implemented)
    // =========================================================================
    
    // Track expected memory contents
    logic [DATA_WIDTH-1:0] expected_mem [0:MEM_DEPTH-1];
    logic                  mem_written [0:MEM_DEPTH-1];
    
    // Last read address for checking
    logic [ADDR_WIDTH-1:0] last_rd_addr;
    logic                  last_rd_en;
    
    // Memory address mapping
    localparam MEM_ADDR_WIDTH = $clog2(MEM_DEPTH);
    logic [MEM_ADDR_WIDTH-1:0] wr_mem_idx, rd_mem_idx;
    assign wr_mem_idx = wr_addr[MEM_ADDR_WIDTH+1:2];
    assign rd_mem_idx = rd_addr[MEM_ADDR_WIDTH+1:2];
    
    // Track writes
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (int i = 0; i < MEM_DEPTH; i++) begin
                expected_mem[i] <= '0;
                mem_written[i] <= 1'b0;
            end
        end else if (wr_en && wr_strb == 4'b1111) begin
            expected_mem[wr_mem_idx] <= wr_data;
            mem_written[wr_mem_idx] <= 1'b1;
        end
    end
    
    // Track last read
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            last_rd_addr <= '0;
            last_rd_en <= 1'b0;
        end else begin
            last_rd_addr <= rd_addr;
            last_rd_en <= rd_en;
        end
    end
    
    logic [MEM_ADDR_WIDTH-1:0] last_rd_mem_idx;
    assign last_rd_mem_idx = last_rd_addr[MEM_ADDR_WIDTH+1:2];

    // =========================================================================
    // ADD YOUR DATA INTEGRITY ASSERTIONS HERE
    // =========================================================================
    //
    // Required assertions:
    // 1. Read after write - data matches what was written
    // 2. Read from unwritten address returns 0
    // 3. Read valid timing - rd_valid follows rd_en by 1 cycle
    //
    // Use the tracking signals above in your assertions.
    //
    // Example assertion structure:
    //
    // property p_read_data_matches;
    //     @(posedge clk) disable iff (!rst_n)
    //     (rd_valid && mem_written[last_rd_mem_idx])
    //     |-> (rd_data == expected_mem[last_rd_mem_idx]);
    // endproperty
    // assert property (p_read_data_matches) else $error("Data mismatch!");
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

    // Read Task
    task automatic mem_read(input logic [ADDR_WIDTH-1:0] addr, output logic [DATA_WIDTH-1:0] data);
        rd_addr = addr;
        rd_en = 1;
        @(posedge clk);
        rd_en = 0;
        @(posedge clk);
        data = rd_data;
    endtask

    // Test: Write and read back
    task automatic test_write_read();
        logic [DATA_WIDTH-1:0] read_data;
        test_count++;
        $display("\n[TEST %0d] Write and Read Back", test_count);
        
        mem_write(32'h0000_0100, 32'hDEAD_BEEF);
        mem_read(32'h0000_0100, read_data);
        
        if (read_data !== 32'hDEAD_BEEF) begin
            $error("FAIL: Expected 0xDEAD_BEEF, got 0x%08h", read_data);
            fail_count++;
        end else begin
            $display("  PASS: Read data matches written data");
            pass_count++;
        end
    endtask

    // Test: Multiple addresses
    task automatic test_multiple_addresses();
        logic [DATA_WIDTH-1:0] read_data;
        int errors = 0;
        test_count++;
        $display("\n[TEST %0d] Multiple Addresses", test_count);
        
        // Write to several addresses
        for (int i = 0; i < 4; i++) begin
            mem_write(32'h0000_0200 + (i * 4), 32'hABCD_0000 + i);
        end
        
        // Read back and verify
        for (int i = 0; i < 4; i++) begin
            mem_read(32'h0000_0200 + (i * 4), read_data);
            if (read_data !== (32'hABCD_0000 + i)) begin
                $error("FAIL at addr 0x%04h: expected 0x%08h, got 0x%08h", 
                       32'h0000_0200 + (i * 4), 32'hABCD_0000 + i, read_data);
                errors++;
            end
        end
        
        if (errors == 0) begin
            $display("  PASS: All addresses verified");
            pass_count++;
        end else begin
            fail_count++;
        end
    endtask

    // Main test sequence
    initial begin
        $dumpfile("axi4_memory_tb.vcd");
        $dumpvars(0, axi4_memory_tb);
        
        $display("================================================================");
        $display(" AXI4 Memory Data Integrity Testbench");
        $display("================================================================");

        reset_dut();
        
        test_write_read();
        test_multiple_addresses();

        #(CLK_PERIOD * 20);

        $display("\n================================================================");
        $display(" Test Summary: Total=%0d, PASSED=%0d, FAILED=%0d", 
                 test_count, pass_count, fail_count);
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

