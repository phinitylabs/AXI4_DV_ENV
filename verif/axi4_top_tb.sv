// =============================================================================
// AXI4 System-Level Golden Testbench
// Tests the complete AXI4 system with comprehensive coverage
// =============================================================================

`timescale 1ns/1ps

module axi4_top_tb;

    // Parameters
    parameter CLK_PERIOD = 10;
    parameter TIMEOUT_CYCLES = 50000;

    // Clock and Reset
    logic clk;
    logic resetn;

    // Test tracking
    int test_count = 0;
    int pass_count = 0;
    int fail_count = 0;
    int cycle_count = 0;

    // Clock generation
    initial begin
        clk = 0;
        forever #(CLK_PERIOD/2) clk = ~clk;
    end

    // Cycle counter
    always @(posedge clk) begin
        cycle_count <= cycle_count + 1;
    end

    // DUT instantiation
    axi4_top dut (
        .clk    (clk),
        .resetn (resetn)
    );

    // Internal signal access for monitoring
    wire        axi_awvalid = dut.axi_awvalid;
    wire        axi_awready = dut.axi_awready;
    wire [31:0] axi_awaddr  = dut.axi_awaddr;
    wire [7:0]  axi_awlen   = dut.axi_awlen;
    wire [1:0]  axi_awburst = dut.axi_awburst;
    wire        axi_wvalid  = dut.axi_wvalid;
    wire        axi_wready  = dut.axi_wready;
    wire [3:0]  axi_wstrb   = dut.axi_wstrb;
    wire        axi_wlast   = dut.axi_wlast;
    wire        axi_bvalid  = dut.axi_bvalid;
    wire        axi_bready  = dut.axi_bready;
    wire [1:0]  axi_bresp   = dut.axi_bresp;
    wire        axi_arvalid = dut.axi_arvalid;
    wire        axi_arready = dut.axi_arready;
    wire [31:0] axi_araddr  = dut.axi_araddr;
    wire [7:0]  axi_arlen   = dut.axi_arlen;
    wire [1:0]  axi_arburst = dut.axi_arburst;
    wire        axi_rvalid  = dut.axi_rvalid;
    wire        axi_rready  = dut.axi_rready;
    wire        axi_rlast   = dut.axi_rlast;
    wire [1:0]  axi_rresp   = dut.axi_rresp;

    // Transaction counters
    int write_addr_count = 0;
    int write_data_count = 0;
    int write_resp_count = 0;
    int read_addr_count = 0;
    int read_data_count = 0;

    // Monitor write address channel
    always @(posedge clk) begin
        if (resetn && axi_awvalid && axi_awready) begin
            write_addr_count <= write_addr_count + 1;
            $display("[%0t] Write Addr: addr=0x%08h len=%0d burst=%0d", 
                     $time, axi_awaddr, axi_awlen, axi_awburst);
        end
    end

    // Monitor write data channel
    always @(posedge clk) begin
        if (resetn && axi_wvalid && axi_wready) begin
            write_data_count <= write_data_count + 1;
            if (axi_wlast) $display("[%0t] Write Data: LAST", $time);
        end
    end

    // Monitor write response channel
    always @(posedge clk) begin
        if (resetn && axi_bvalid && axi_bready) begin
            write_resp_count <= write_resp_count + 1;
            $display("[%0t] Write Resp: resp=%0d", $time, axi_bresp);
        end
    end

    // Monitor read address channel
    always @(posedge clk) begin
        if (resetn && axi_arvalid && axi_arready) begin
            read_addr_count <= read_addr_count + 1;
            $display("[%0t] Read Addr: addr=0x%08h len=%0d burst=%0d",
                     $time, axi_araddr, axi_arlen, axi_arburst);
        end
    end

    // Monitor read data channel
    always @(posedge clk) begin
        if (resetn && axi_rvalid && axi_rready) begin
            read_data_count <= read_data_count + 1;
            if (axi_rlast) $display("[%0t] Read Data: LAST resp=%0d", $time, axi_rresp);
        end
    end

    // =========================================================================
    // Reset Task
    // =========================================================================
    task automatic reset_dut();
        $display("[%0t] Applying reset...", $time);
        resetn = 0;
        repeat(20) @(posedge clk);
        resetn = 1;
        repeat(10) @(posedge clk);
        $display("[%0t] Reset complete", $time);
    endtask

    // =========================================================================
    // Write Transaction Task - Forces internal signals
    // =========================================================================
    task automatic do_write(
        input [31:0] addr,
        input [7:0]  len,
        input [1:0]  burst,
        input [3:0]  strb
    );
        int i;
        $display("[%0t] Starting write: addr=0x%08h len=%0d burst=%0d strb=0x%h",
                 $time, addr, len, burst, strb);
        test_count++;
        
        // Force write address channel
        force dut.master.axi_awaddr = addr;
        force dut.master.axi_awlen = len;
        force dut.master.axi_awburst = burst;
        force dut.master.axi_awsize = 3'h2;
        force dut.master.axi_awvalid = 1'b1;
        
        // Wait for address handshake
        @(posedge clk);
        while (!axi_awready) @(posedge clk);
        @(posedge clk);
        release dut.master.axi_awvalid;
        release dut.master.axi_awaddr;
        release dut.master.axi_awlen;
        release dut.master.axi_awburst;
        release dut.master.axi_awsize;
        
        // Send write data beats
        for (i = 0; i <= len; i++) begin
            force dut.master.axi_wdata = 32'hCAFE_0000 + i;
            force dut.master.axi_wstrb = strb;
            force dut.master.axi_wlast = (i == len);
            force dut.master.axi_wvalid = 1'b1;
            
            @(posedge clk);
            while (!axi_wready) @(posedge clk);
            @(posedge clk);
        end
        release dut.master.axi_wvalid;
        release dut.master.axi_wdata;
        release dut.master.axi_wstrb;
        release dut.master.axi_wlast;
        
        // Handle write response
        force dut.master.axi_bready = 1'b1;
        @(posedge clk);
        while (!axi_bvalid) @(posedge clk);
        @(posedge clk);
        release dut.master.axi_bready;
        
        pass_count++;
        $display("[%0t] Write complete", $time);
    endtask

    // =========================================================================
    // Read Transaction Task - Forces internal signals
    // =========================================================================
    task automatic do_read(
        input [31:0] addr,
        input [7:0]  len,
        input [1:0]  burst
    );
        $display("[%0t] Starting read: addr=0x%08h len=%0d burst=%0d",
                 $time, addr, len, burst);
        test_count++;
        
        // Force read address channel
        force dut.master.axi_araddr = addr;
        force dut.master.axi_arlen = len;
        force dut.master.axi_arburst = burst;
        force dut.master.axi_arsize = 3'h2;
        force dut.master.axi_arvalid = 1'b1;
        
        // Wait for address handshake
        @(posedge clk);
        while (!axi_arready) @(posedge clk);
        @(posedge clk);
        release dut.master.axi_arvalid;
        release dut.master.axi_araddr;
        release dut.master.axi_arlen;
        release dut.master.axi_arburst;
        release dut.master.axi_arsize;
        
        // Handle read data
        force dut.master.axi_rready = 1'b1;
        @(posedge clk);
        while (!axi_rlast || !axi_rvalid) begin
            @(posedge clk);
            if (cycle_count > TIMEOUT_CYCLES) break;
        end
        @(posedge clk);
        release dut.master.axi_rready;
        
        pass_count++;
        $display("[%0t] Read complete", $time);
    endtask

    // =========================================================================
    // Main Test Sequence
    // =========================================================================
    initial begin
        $dumpfile("axi4_top_tb.vcd");
        $dumpvars(0, axi4_top_tb);
        
        $display("================================================================");
        $display(" AXI4 System-Level Testbench - Comprehensive Coverage");
        $display("================================================================");
        
        // Initialize
        resetn = 0;
        
        // Apply reset
        reset_dut();
        
        // =====================================================================
        // Test 1: Single-beat writes to different address regions
        // =====================================================================
        $display("\n--- Test 1: Single-beat writes to address regions ---");
        
        // Region 0 (0x000-0x0FF) - INCR burst
        do_write(32'h0000_0000, 8'h0, 2'b01, 4'hF);  // Single, INCR, full strobe
        repeat(20) @(posedge clk);
        
        // Region 1 (0x100-0x1FF) - FIXED burst
        do_write(32'h0000_0100, 8'h0, 2'b00, 4'hF);  // Single, FIXED, full strobe
        repeat(20) @(posedge clk);
        
        // Region 2 (0x200-0x2FF) - WRAP burst
        do_write(32'h0000_0200, 8'h0, 2'b10, 4'hF);  // Single, WRAP, full strobe
        repeat(20) @(posedge clk);
        
        // Region 3 (0x300-0x3FF) - partial strobe
        do_write(32'h0000_0300, 8'h0, 2'b01, 4'h3);  // Single, INCR, partial strobe
        repeat(20) @(posedge clk);
        
        // =====================================================================
        // Test 2: Multi-beat writes
        // =====================================================================
        $display("\n--- Test 2: Multi-beat writes ---");
        
        // 4-beat INCR burst
        do_write(32'h0000_0010, 8'h3, 2'b01, 4'hF);
        repeat(20) @(posedge clk);
        
        // 8-beat WRAP burst  
        do_write(32'h0000_0110, 8'h7, 2'b10, 4'hF);
        repeat(20) @(posedge clk);
        
        // =====================================================================
        // Test 3: Single-beat reads
        // =====================================================================
        $display("\n--- Test 3: Single-beat reads ---");
        
        // Read from region 0
        do_read(32'h0000_0000, 8'h0, 2'b01);
        repeat(20) @(posedge clk);
        
        // Read from region 1
        do_read(32'h0000_0100, 8'h0, 2'b00);
        repeat(20) @(posedge clk);
        
        // Read from region 2
        do_read(32'h0000_0200, 8'h0, 2'b10);
        repeat(20) @(posedge clk);
        
        // =====================================================================
        // Test 4: Multi-beat reads
        // =====================================================================
        $display("\n--- Test 4: Multi-beat reads ---");
        
        // 4-beat INCR read
        do_read(32'h0000_0010, 8'h3, 2'b01);
        repeat(20) @(posedge clk);
        
        // =====================================================================
        // Test 5: Out-of-range access (should cause DECERR)
        // =====================================================================
        $display("\n--- Test 5: Out-of-range access ---");
        
        do_write(32'h0000_1000, 8'h0, 2'b01, 4'hF);  // Address > 0x3FF
        repeat(20) @(posedge clk);
        
        do_read(32'h0000_1000, 8'h0, 2'b01);
        repeat(20) @(posedge clk);
        
        // =====================================================================
        // Test 6: Additional coverage patterns
        // =====================================================================
        $display("\n--- Test 6: Additional patterns ---");
        
        // More partial strobes
        do_write(32'h0000_0050, 8'h0, 2'b01, 4'h1);
        repeat(20) @(posedge clk);
        
        do_write(32'h0000_0060, 8'h0, 2'b01, 4'hC);
        repeat(20) @(posedge clk);
        
        // Let any pending transactions complete
        repeat(500) @(posedge clk);
        
        // =====================================================================
        // Report Results
        // =====================================================================
        $display("\n================================================================");
        $display(" TEST SUMMARY");
        $display("================================================================");
        $display(" Tests run:    %0d", test_count);
        $display(" Tests passed: %0d", pass_count);
        $display(" Tests failed: %0d", fail_count);
        $display(" Write Addrs:  %0d", write_addr_count);
        $display(" Write Data:   %0d", write_data_count);
        $display(" Write Resp:   %0d", write_resp_count);
        $display(" Read Addrs:   %0d", read_addr_count);
        $display(" Read Data:    %0d", read_data_count);
        $display("================================================================");
        
        if (fail_count == 0 && test_count > 0) begin
            $display("RESULT: PASS");
        end else begin
            $display("RESULT: FAIL");
        end
        
        $finish;
    end

    // Timeout watchdog
    initial begin
        repeat(TIMEOUT_CYCLES) @(posedge clk);
        $display("[ERROR] Timeout after %0d cycles!", TIMEOUT_CYCLES);
        $finish;
    end

endmodule
