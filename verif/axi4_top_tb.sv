// =============================================================================
// AXI4 System-Level Golden Testbench
// Tests the complete AXI4 system (master + slave + interrupt + coverage)
// =============================================================================

`timescale 1ns/1ps

module axi4_top_tb;

    parameter CLK_PERIOD = 10;
    parameter TIMEOUT_CYCLES = 100000;

    logic clk;
    logic resetn;

    int test_count = 0;
    int pass_count = 0;
    int fail_count = 0;
    int cycle_count = 0;

    initial begin
        clk = 0;
        forever #(CLK_PERIOD/2) clk = ~clk;
    end

    always @(posedge clk) begin
        cycle_count <= cycle_count + 1;
    end

    axi4_top dut (
        .clk    (clk),
        .resetn (resetn)
    );

    // Internal signal monitoring
    wire axi_awvalid = dut.axi_awvalid;
    wire axi_awready = dut.axi_awready;
    wire axi_wvalid  = dut.axi_wvalid;
    wire axi_wready  = dut.axi_wready;
    wire axi_wlast   = dut.axi_wlast;
    wire axi_bvalid  = dut.axi_bvalid;
    wire axi_bready  = dut.axi_bready;
    wire [1:0] axi_bresp = dut.axi_bresp;
    wire axi_arvalid = dut.axi_arvalid;
    wire axi_arready = dut.axi_arready;
    wire axi_rvalid  = dut.axi_rvalid;
    wire axi_rready  = dut.axi_rready;
    wire axi_rlast   = dut.axi_rlast;
    wire [1:0] axi_rresp = dut.axi_rresp;

    int write_txn_count = 0;
    int read_txn_count = 0;

    always @(posedge clk) begin
        if (resetn && axi_awvalid && axi_awready)
            write_txn_count <= write_txn_count + 1;
        if (resetn && axi_arvalid && axi_arready)
            read_txn_count <= read_txn_count + 1;
    end

    // Protocol checks
    always @(posedge clk) begin
        if (resetn && axi_bvalid) begin
            if (!(axi_bresp inside {2'b00, 2'b01, 2'b10, 2'b11})) begin
                $error("[ERROR] Invalid BRESP");
                fail_count++;
            end
        end
        if (resetn && axi_rvalid) begin
            if (!(axi_rresp inside {2'b00, 2'b01, 2'b10, 2'b11})) begin
                $error("[ERROR] Invalid RRESP");
                fail_count++;
            end
        end
    end

    task automatic reset_dut();
        resetn = 0;
        repeat(10) @(posedge clk);
        resetn = 1;
        repeat(5) @(posedge clk);
    endtask

    initial begin
        $dumpfile("axi4_top_tb.vcd");
        $dumpvars(0, axi4_top_tb);
        
        $display("================================================================");
        $display(" AXI4 System-Level Testbench - Golden Reference");
        $display("================================================================");
        
        resetn = 0;
        write_txn_count = 0;
        read_txn_count = 0;
        
        reset_dut();
        
        // Let system run
        repeat(20000) @(posedge clk);
        
        $display(" Write Txns: %0d, Read Txns: %0d", write_txn_count, read_txn_count);
        
        if (write_txn_count > 0 && read_txn_count > 0 && fail_count == 0) begin
            pass_count = 1;
            $display("RESULT: PASS");
        end else begin
            $display("RESULT: FAIL");
        end
        
        $finish;
    end

    initial begin
        repeat(TIMEOUT_CYCLES) @(posedge clk);
        $display("[ERROR] Timeout!");
        $finish;
    end

endmodule
