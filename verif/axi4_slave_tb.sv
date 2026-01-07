// =============================================================================
// AXI4 Burst Boundary Assertion Testbench - Starter Template
// Task: Add SVA assertions for burst address calculation verification
// =============================================================================
//
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// !! CRITICAL WARNING - READ BEFORE WRITING ASSERTIONS !!
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// !!
// !! DO NOT use hierarchical references to DUT internal signals!
// !!
// !! WRONG (will result in 0 points):
// !!   dut.u_write_channel.current_addr
// !!   dut.u_read_channel.beat_count
// !!   dut.u_write_channel.burst_type
// !!   or any dut.* internal signal access
// !!
// !! CORRECT: Use ONLY the testbench tracking signals provided below:
// !!   wr_in_burst, wr_current_addr, wr_beat_count, etc.
// !!   rd_in_burst, rd_current_addr, rd_beat_count, etc.
// !!
// !! The tracking logic is already implemented for you.
// !! Your job is to write assertions using these signals.
// !!
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

`timescale 1ns/1ps

module axi4_slave_tb;

    // Parameters
    parameter ADDR_WIDTH = 32;
    parameter DATA_WIDTH = 32;
    parameter ID_WIDTH   = 4;
    parameter STRB_WIDTH = DATA_WIDTH / 8;
    parameter CLK_PERIOD = 10;

    // Burst type constants
    localparam BURST_FIXED = 2'b00;
    localparam BURST_INCR  = 2'b01;
    localparam BURST_WRAP  = 2'b10;

    // Signals
    logic aclk;
    logic aresetn;

    // Write Address Channel
    logic [ID_WIDTH-1:0]   awid;
    logic [ADDR_WIDTH-1:0] awaddr;
    logic [7:0]            awlen;
    logic [2:0]            awsize;
    logic [1:0]            awburst;
    logic                  awvalid;
    logic                  awready;

    // Write Data Channel
    logic [DATA_WIDTH-1:0] wdata;
    logic [STRB_WIDTH-1:0] wstrb;
    logic                  wlast;
    logic                  wvalid;
    logic                  wready;

    // Write Response Channel
    logic [ID_WIDTH-1:0]   bid;
    logic [1:0]            bresp;
    logic                  bvalid;
    logic                  bready;

    // Read Address Channel
    logic [ID_WIDTH-1:0]   arid;
    logic [ADDR_WIDTH-1:0] araddr;
    logic [7:0]            arlen;
    logic [2:0]            arsize;
    logic [1:0]            arburst;
    logic                  arvalid;
    logic                  arready;

    // Read Data Channel
    logic [ID_WIDTH-1:0]   rid;
    logic [DATA_WIDTH-1:0] rdata;
    logic [1:0]            rresp;
    logic                  rlast;
    logic                  rvalid;
    logic                  rready;

    // Test Counters
    int test_count = 0;
    int pass_count = 0;
    int fail_count = 0;

    // Clock Generation
    initial begin
        aclk = 0;
        forever #(CLK_PERIOD/2) aclk = ~aclk;
    end

    // DUT Instantiation
    axi4_slave_top #(
        .ADDR_WIDTH(ADDR_WIDTH),
        .DATA_WIDTH(DATA_WIDTH),
        .ID_WIDTH(ID_WIDTH)
    ) dut (
        .aclk    (aclk),
        .aresetn (aresetn),
        .awid    (awid),
        .awaddr  (awaddr),
        .awlen   (awlen),
        .awsize  (awsize),
        .awburst (awburst),
        .awvalid (awvalid),
        .awready (awready),
        .wdata   (wdata),
        .wstrb   (wstrb),
        .wlast   (wlast),
        .wvalid  (wvalid),
        .wready  (wready),
        .bid     (bid),
        .bresp   (bresp),
        .bvalid  (bvalid),
        .bready  (bready),
        .arid    (arid),
        .araddr  (araddr),
        .arlen   (arlen),
        .arsize  (arsize),
        .arburst (arburst),
        .arvalid (arvalid),
        .arready (arready),
        .rid     (rid),
        .rdata   (rdata),
        .rresp   (rresp),
        .rlast   (rlast),
        .rvalid  (rvalid),
        .rready  (rready)
    );

    // =========================================================================
    // BURST STATE TRACKING - ALREADY IMPLEMENTED FOR YOU
    // Use these signals in your assertions (NOT dut.* internal signals!)
    // =========================================================================
    
    // Write burst tracking signals
    logic        wr_in_burst;
    logic [31:0] wr_start_addr;
    logic [31:0] wr_current_addr;
    logic [31:0] wr_prev_addr;
    logic [7:0]  wr_beat_count;
    logic [7:0]  wr_total_beats;
    logic [2:0]  wr_burst_size;
    logic [1:0]  wr_burst_type;
    logic [31:0] wr_wrap_boundary;
    logic [31:0] wr_wrap_size;
    logic [31:0] wr_addr_incr;
    
    // Read burst tracking signals
    logic        rd_in_burst;
    logic [31:0] rd_start_addr;
    logic [31:0] rd_current_addr;
    logic [31:0] rd_prev_addr;
    logic [7:0]  rd_beat_count;
    logic [7:0]  rd_total_beats;
    logic [2:0]  rd_burst_size;
    logic [1:0]  rd_burst_type;
    logic [31:0] rd_wrap_boundary;
    logic [31:0] rd_wrap_size;
    logic [31:0] rd_addr_incr;

    // =========================================================================
    // WRITE BURST TRACKING LOGIC (Pre-implemented - do not modify)
    // =========================================================================
    always_ff @(posedge aclk or negedge aresetn) begin
        if (!aresetn) begin
            wr_in_burst     <= 1'b0;
            wr_start_addr   <= '0;
            wr_current_addr <= '0;
            wr_prev_addr    <= '0;
            wr_beat_count   <= '0;
            wr_total_beats  <= '0;
            wr_burst_size   <= '0;
            wr_burst_type   <= '0;
            wr_wrap_boundary <= '0;
            wr_wrap_size    <= '0;
            wr_addr_incr    <= '0;
        end else begin
            // Capture burst parameters on address handshake
            if (awvalid && awready) begin
                wr_in_burst     <= 1'b1;
                wr_start_addr   <= awaddr;
                wr_current_addr <= awaddr;
                wr_prev_addr    <= awaddr;
                wr_beat_count   <= '0;
                wr_total_beats  <= awlen + 1;
                wr_burst_size   <= awsize;
                wr_burst_type   <= awburst;
                wr_addr_incr    <= (1 << awsize);
                wr_wrap_size    <= (awlen + 1) << awsize;
                wr_wrap_boundary <= awaddr & ~(((awlen + 1) << awsize) - 1);
            end
            // Update tracking on each data beat
            else if (wr_in_burst && wvalid && wready) begin
                wr_beat_count <= wr_beat_count + 1;
                wr_prev_addr  <= wr_current_addr;
                
                // Calculate next address based on burst type
                case (wr_burst_type)
                    BURST_FIXED: begin
                        wr_current_addr <= wr_start_addr; // Address stays same
                    end
                    BURST_INCR: begin
                        wr_current_addr <= wr_current_addr + wr_addr_incr;
                    end
                    BURST_WRAP: begin
                        if ((wr_current_addr + wr_addr_incr) >= (wr_wrap_boundary + wr_wrap_size))
                            wr_current_addr <= wr_wrap_boundary;
                        else
                            wr_current_addr <= wr_current_addr + wr_addr_incr;
                    end
                    default: begin
                        wr_current_addr <= wr_current_addr + wr_addr_incr;
                    end
                endcase
                
                // End burst on wlast
                if (wlast) begin
                    wr_in_burst <= 1'b0;
                end
            end
        end
    end

    // =========================================================================
    // READ BURST TRACKING LOGIC (Pre-implemented - do not modify)
    // =========================================================================
    always_ff @(posedge aclk or negedge aresetn) begin
        if (!aresetn) begin
            rd_in_burst     <= 1'b0;
            rd_start_addr   <= '0;
            rd_current_addr <= '0;
            rd_prev_addr    <= '0;
            rd_beat_count   <= '0;
            rd_total_beats  <= '0;
            rd_burst_size   <= '0;
            rd_burst_type   <= '0;
            rd_wrap_boundary <= '0;
            rd_wrap_size    <= '0;
            rd_addr_incr    <= '0;
        end else begin
            // Capture burst parameters on address handshake
            if (arvalid && arready) begin
                rd_in_burst     <= 1'b1;
                rd_start_addr   <= araddr;
                rd_current_addr <= araddr;
                rd_prev_addr    <= araddr;
                rd_beat_count   <= '0;
                rd_total_beats  <= arlen + 1;
                rd_burst_size   <= arsize;
                rd_burst_type   <= arburst;
                rd_addr_incr    <= (1 << arsize);
                rd_wrap_size    <= (arlen + 1) << arsize;
                rd_wrap_boundary <= araddr & ~(((arlen + 1) << arsize) - 1);
            end
            // Update tracking on each data beat
            else if (rd_in_burst && rvalid && rready) begin
                rd_beat_count <= rd_beat_count + 1;
                rd_prev_addr  <= rd_current_addr;
                
                // Calculate next address based on burst type
                case (rd_burst_type)
                    BURST_FIXED: begin
                        rd_current_addr <= rd_start_addr; // Address stays same
                    end
                    BURST_INCR: begin
                        rd_current_addr <= rd_current_addr + rd_addr_incr;
                    end
                    BURST_WRAP: begin
                        if ((rd_current_addr + rd_addr_incr) >= (rd_wrap_boundary + rd_wrap_size))
                            rd_current_addr <= rd_wrap_boundary;
                        else
                            rd_current_addr <= rd_current_addr + rd_addr_incr;
                    end
                    default: begin
                        rd_current_addr <= rd_current_addr + rd_addr_incr;
                    end
                endcase
                
                // End burst on rlast
                if (rlast) begin
                    rd_in_burst <= 1'b0;
                end
            end
        end
    end

    // =========================================================================
    // ADD YOUR BURST BOUNDARY ASSERTIONS HERE (Simplified - just 2 types needed)
    // =========================================================================
    //
    // TASK: Write at least 2 assertions using the tracking signals above.
    //       DO NOT use hierarchical references like dut.u_write_channel.*
    //
    // Required assertions (pick 2 or more):
    //
    // 1. INCR address increment verification
    //    - Check that address increments correctly for INCR bursts
    //
    // 2. WLAST/RLAST timing correctness  
    //    - Check that wlast/rlast signals burst end correctly
    //
    // =========================================================================
    // EXAMPLE ASSERTION (already provided - you need to add at least 1 more):
    // =========================================================================
    
    // Example: INCR Write Address Increment Check
    property p_incr_wr_addr;
        @(posedge aclk) disable iff (!aresetn)
        (wr_in_burst && wvalid && wready && wr_burst_type == BURST_INCR && wr_beat_count > 0)
        |-> (wr_current_addr == wr_prev_addr + wr_addr_incr);
    endproperty
    assert property (p_incr_wr_addr) 
        else $error("ASSERTION FAILED: INCR write address increment mismatch");

    // =========================================================================
    // AGENT-ADDED ASSERTIONS (GOLDEN SOLUTION)
    // =========================================================================

    // INCR Read Address Increment Check
    property p_incr_rd_addr;
        @(posedge aclk) disable iff (!aresetn)
        (rd_in_burst && rvalid && rready && rd_burst_type == BURST_INCR && rd_beat_count > 0)
        |-> (rd_current_addr == rd_prev_addr + rd_addr_incr);
    endproperty
    assert property (p_incr_rd_addr)
        else $error("ASSERTION FAILED: INCR read burst address increment mismatch");

    // 2. INCR Address Increment Assertion (Read)
    property p_incr_rd_addr_increment;
        @(posedge aclk) disable iff (!aresetn)
        (rd_in_burst && rvalid && rready && rd_burst_type == BURST_INCR && rd_beat_count > 0)
        |-> (rd_current_addr == rd_prev_addr + rd_addr_incr);
    endproperty
    
    assert property (p_incr_rd_addr_increment)
        else $error("ASSERTION FAILED: INCR read burst address increment mismatch");

    // 3. FIXED Address Stability Assertion (Write)
    property p_fixed_wr_addr_stable;
        @(posedge aclk) disable iff (!aresetn)
        (wr_in_burst && wvalid && wready && wr_burst_type == BURST_FIXED)
        |-> (wr_current_addr == wr_start_addr);
    endproperty
    
    assert property (p_fixed_wr_addr_stable)
        else $error("ASSERTION FAILED: FIXED write burst address changed");

    // 4. FIXED Address Stability Assertion (Read)
    property p_fixed_rd_addr_stable;
        @(posedge aclk) disable iff (!aresetn)
        (rd_in_burst && rvalid && rready && rd_burst_type == BURST_FIXED)
        |-> (rd_current_addr == rd_start_addr);
    endproperty
    
    assert property (p_fixed_rd_addr_stable)
        else $error("ASSERTION FAILED: FIXED read burst address changed");

    // 5. WRAP Boundary Assertion (Write)
    property p_wrap_wr_boundary;
        @(posedge aclk) disable iff (!aresetn)
        (wr_in_burst && wvalid && wready && wr_burst_type == BURST_WRAP)
        |-> (wr_current_addr >= wr_wrap_boundary && wr_current_addr < wr_wrap_boundary + wr_wrap_size);
    endproperty
    
    assert property (p_wrap_wr_boundary)
        else $error("ASSERTION FAILED: WRAP write address outside boundary");

    // 6. WRAP Boundary Assertion (Read)
    property p_wrap_rd_boundary;
        @(posedge aclk) disable iff (!aresetn)
        (rd_in_burst && rvalid && rready && rd_burst_type == BURST_WRAP)
        |-> (rd_current_addr >= rd_wrap_boundary && rd_current_addr < rd_wrap_boundary + rd_wrap_size);
    endproperty
    
    assert property (p_wrap_rd_boundary)
        else $error("ASSERTION FAILED: WRAP read address outside boundary");

    // Helper signals for 4KB boundary check
    logic [31:0] wr_end_addr;
    logic [31:0] rd_end_addr;
    assign wr_end_addr = awaddr + ((awlen + 1) << awsize) - 1;
    assign rd_end_addr = araddr + ((arlen + 1) << arsize) - 1;

    // 7. 4KB Boundary Check (Write)
    property p_4kb_wr_boundary;
        @(posedge aclk) disable iff (!aresetn)
        (awvalid && awready)
        |-> (awaddr[31:12] == wr_end_addr[31:12]);
    endproperty
    
    assert property (p_4kb_wr_boundary)
        else $error("ASSERTION FAILED: Write burst crosses 4KB boundary");

    // 8. 4KB Boundary Check (Read)
    property p_4kb_rd_boundary;
        @(posedge aclk) disable iff (!aresetn)
        (arvalid && arready)
        |-> (araddr[31:12] == rd_end_addr[31:12]);
    endproperty
    
    assert property (p_4kb_rd_boundary)
        else $error("ASSERTION FAILED: Read burst crosses 4KB boundary");

    // 9. WLAST Ends Burst
    property p_wlast_ends_burst;
        @(posedge aclk) disable iff (!aresetn)
        (wr_in_burst && wvalid && wready && wlast)
        |=> (!wr_in_burst);
    endproperty
    
    assert property (p_wlast_ends_burst)
        else $error("ASSERTION FAILED: WLAST did not end burst");

    // 10. RLAST Ends Burst
    property p_rlast_ends_burst;
        @(posedge aclk) disable iff (!aresetn)
        (rd_in_burst && rvalid && rready && rlast)
        |=> (!rd_in_burst);
    endproperty
    
    assert property (p_rlast_ends_burst)
        else $error("ASSERTION FAILED: RLAST did not end burst");

    // =========================================================================
    // END OF ASSERTION SECTION
    // =========================================================================

    // Reset Task
    task automatic reset_dut();
        aresetn = 0;
        awid = 0; awaddr = 0; awlen = 0; awsize = 3'b010; awburst = 2'b01; awvalid = 0;
        wdata = 0; wstrb = 0; wlast = 0; wvalid = 0;
        bready = 1;
        arid = 0; araddr = 0; arlen = 0; arsize = 3'b010; arburst = 2'b01; arvalid = 0;
        rready = 1;
        repeat(10) @(posedge aclk);
        aresetn = 1;
        repeat(5) @(posedge aclk);
    endtask

    // AXI Write Task
    task automatic axi_write(
        input logic [ADDR_WIDTH-1:0] addr,
        input logic [DATA_WIDTH-1:0] data,
        input logic [ID_WIDTH-1:0]   id,
        input logic [7:0]            len,
        input logic [1:0]            burst,
        input logic [3:0]            strb,
        output logic [1:0]           resp
    );
        int timeout_cnt;
        awid = id; awaddr = addr; awlen = len;
        awburst = burst; awsize = 3'b010; awvalid = 1'b1;
        
        timeout_cnt = 0;
        while (!awready && timeout_cnt < 100) begin
            @(posedge aclk);
            timeout_cnt++;
        end
        @(posedge aclk);
        awvalid = 1'b0;
        
        for (int i = 0; i <= len; i++) begin
            wdata = data + i;
            wstrb = strb;
            wlast = (i == len);
            wvalid = 1'b1;
            timeout_cnt = 0;
            while (!wready && timeout_cnt < 100) begin
                @(posedge aclk);
                timeout_cnt++;
            end
            @(posedge aclk);
        end
        wvalid = 1'b0;
        wlast = 1'b0;
        
        timeout_cnt = 0;
        while (!bvalid && timeout_cnt < 100) begin
            @(posedge aclk);
            timeout_cnt++;
        end
        resp = bresp;
        @(posedge aclk);
    endtask

    // AXI Read Task
    task automatic axi_read(
        input logic [ADDR_WIDTH-1:0]  addr,
        input logic [ID_WIDTH-1:0]    id,
        input logic [7:0]             len,
        input logic [1:0]             burst,
        output logic [DATA_WIDTH-1:0] data_out,
        output logic [1:0]            resp
    );
        logic [DATA_WIDTH-1:0] read_data[$];
        int timeout_cnt;
        logic got_rlast;

        read_data.delete();
        arid = id; araddr = addr; arlen = len;
        arburst = burst; arsize = 3'b010; arvalid = 1'b1;

        timeout_cnt = 0;
        while (!arready && timeout_cnt < 100) begin
            @(posedge aclk);
            timeout_cnt++;
        end
        @(posedge aclk);
        arvalid = 1'b0;

        got_rlast = 0;
        while (!got_rlast) begin
            timeout_cnt = 0;
            while (!rvalid && timeout_cnt < 100) begin
                @(posedge aclk);
                timeout_cnt++;
            end
            if (rvalid) begin
                read_data.push_back(rdata);
                resp = rresp;
                got_rlast = rlast;
                @(posedge aclk);
            end else break;
        end
        data_out = (read_data.size() > 0) ? read_data[0] : '0;
        @(posedge aclk);
    endtask

    // Simple Write/Read Tasks
    task automatic axi_write_simple(input logic [ADDR_WIDTH-1:0] addr, input logic [DATA_WIDTH-1:0] data);
        logic [1:0] resp;
        axi_write(addr, data, 0, 0, BURST_INCR, 4'b1111, resp);
    endtask

    task automatic axi_read_simple(input logic [ADDR_WIDTH-1:0] addr, output logic [DATA_WIDTH-1:0] data);
        logic [1:0] resp;
        axi_read(addr, 0, 0, BURST_INCR, data, resp);
    endtask

    // Test Cases
    task automatic test_single_write_read();
        logic [DATA_WIDTH-1:0] wr_data, rd_data;
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] Single Write/Read", test_count);
        wr_data = 32'hDEAD_BEEF;
        axi_write(32'h0000_1000, wr_data, 0, 0, BURST_INCR, 4'b1111, resp);
        axi_read(32'h0000_1000, 0, 0, BURST_INCR, rd_data, resp);
        if (rd_data !== wr_data) begin fail_count++; $display("  FAIL"); end
        else begin pass_count++; $display("  PASS"); end
    endtask

    task automatic test_incr_burst();
        logic [DATA_WIDTH-1:0] rd_data;
        logic [1:0] resp;
        logic [31:0] expected_addr;
        int errors;
        test_count++;
        errors = 0;
        $display("\n[TEST %0d] INCR Burst (4 beats) with data integrity verification", test_count);
        // Write unique data per beat: 0xBEEF_0000, 0xBEEF_0001, 0xBEEF_0002, 0xBEEF_0003
        axi_write(32'h0000_2000, 32'hBEEF_0000, 0, 3, BURST_INCR, 4'b1111, resp);
        // Verify each beat was written to the correct address by reading individually
        for (int i = 0; i < 4; i++) begin
            expected_addr = 32'h0000_2000 + (i * 4);  // INCR increments by transfer size
            axi_read_simple(expected_addr, rd_data);
            if (rd_data !== (32'hBEEF_0000 + i)) begin
                $error("ASSERTION FAILED: INCR burst data mismatch at addr=%h, expected=%h, got=%h", 
                       expected_addr, 32'hBEEF_0000 + i, rd_data);
                errors++;
            end
        end
        if (errors == 0) begin pass_count++; $display("  PASS"); end
        else begin fail_count++; $display("  FAIL"); end
    endtask

    task automatic test_fixed_burst();
        logic [DATA_WIDTH-1:0] rd_data;
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] FIXED Burst (address should stay same)", test_count);
        // For FIXED burst, all beats write to the same address
        // Only the last value should be retained
        axi_write(32'h0000_3000, 32'hF12D_0000, 0, 3, BURST_FIXED, 4'b1111, resp);
        axi_read_simple(32'h0000_3000, rd_data);
        // Last beat value is base + 3 = 0xF12D_0003
        if (rd_data !== 32'hF12D_0003) begin
            $error("ASSERTION FAILED: FIXED burst - expected last written value=%h, got=%h", 
                   32'hF12D_0003, rd_data);
            fail_count++; $display("  FAIL");
        end else begin
            pass_count++; $display("  PASS");
        end
    endtask

    task automatic test_wrap_burst();
        logic [DATA_WIDTH-1:0] rd_data;
        logic [1:0] resp;
        logic [31:0] wrap_boundary;
        logic [31:0] wrap_size;
        logic [31:0] expected_addr;
        logic [31:0] current_addr;
        int errors;
        test_count++;
        errors = 0;
        $display("\n[TEST %0d] WRAP Burst (4 beats) with wrap boundary verification", test_count);
        // WRAP burst starting at offset 0x4008 with len=3 (4 beats), size=4 bytes
        // Wrap boundary = 0x4000 (aligned to 16-byte wrap size)
        // Wrap size = 4 * 4 = 16 bytes
        // Addresses: 0x4008, 0x400C, 0x4000 (wrap!), 0x4004
        axi_write(32'h0000_4008, 32'hABCD_0000, 0, 3, BURST_WRAP, 4'b1111, resp);
        
        // Verify data at expected wrap addresses
        wrap_boundary = 32'h0000_4000;
        wrap_size = 16;
        current_addr = 32'h0000_4008;
        
        for (int i = 0; i < 4; i++) begin
            axi_read_simple(current_addr, rd_data);
            if (rd_data !== (32'hABCD_0000 + i)) begin
                $error("ASSERTION FAILED: WRAP burst data mismatch at addr=%h, expected=%h, got=%h", 
                       current_addr, 32'hABCD_0000 + i, rd_data);
                errors++;
            end
            // Calculate next address with wrap
            if ((current_addr + 4) >= (wrap_boundary + wrap_size))
                current_addr = wrap_boundary;
            else
                current_addr = current_addr + 4;
        end
        if (errors == 0) begin pass_count++; $display("  PASS"); end
        else begin fail_count++; $display("  FAIL"); end
    endtask

    task automatic test_decode_error();
        logic [1:0] resp;
        test_count++;
        $display("\n[TEST %0d] Decode Error (out of range)", test_count);
        axi_write(32'h0001_0000, 32'hDEAD, 0, 0, BURST_INCR, 4'b1111, resp);
        if (resp !== 2'b11) begin fail_count++; $display("  FAIL"); end
        else begin pass_count++; $display("  PASS"); end
    endtask

    // Main Test Sequence
    initial begin
        $dumpfile("axi4_slave_tb.vcd");
        $dumpvars(0, axi4_slave_tb);
        $display("================================================================");
        $display(" AXI4 Burst Boundary Assertion Testbench");
        $display("================================================================");
        reset_dut();
        test_single_write_read();
        test_incr_burst();
        test_fixed_burst();
        test_wrap_burst();
        test_decode_error();
        repeat(100) @(posedge aclk);
        $display("\n================================================================");
        $display(" Total: %0d, PASSED: %0d, FAILED: %0d", test_count, pass_count, fail_count);
        $display("================================================================");
        $finish;
    end

    initial begin
        #5000000;
        $display("ERROR: Timeout!");
        $finish;
    end

endmodule
