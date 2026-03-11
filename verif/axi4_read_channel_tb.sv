// =============================================================================
// AXI4 Read Channel Testbench - GOLDEN Solution
// Complete verification with BOTH tests AND SVA assertions
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
    // MEMORY MODEL
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
    // TRACKING SIGNALS FOR ASSERTIONS
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
    
    // Track previous rvalid for handshake check
    logic prev_rvalid, prev_rready;
    always_ff @(posedge clk or negedge aresetn) begin
        if (!aresetn) begin
            prev_rvalid <= 1'b0;
            prev_rready <= 1'b0;
        end else begin
            prev_rvalid <= rvalid;
            prev_rready <= rready;
        end
    end

    // =========================================================================
    // GOLDEN SVA ASSERTIONS
    // =========================================================================
    
    // Assertion 1: RLAST asserts on final beat
    property p_rlast_on_final_beat;
        @(posedge clk) disable iff (!aresetn)
        (rvalid && rready && rd_in_burst && (rd_beat_count == rd_total_beats - 1))
        |-> rlast;
    endproperty
    
    assert property (p_rlast_on_final_beat)
        else $error("ASSERTION FAILED: RLAST should assert on final beat");
    
    // Assertion 2: RLAST only on final beat (not early)
    property p_rlast_not_early;
        @(posedge clk) disable iff (!aresetn)
        (rvalid && rready && rd_in_burst && (rd_beat_count < rd_total_beats - 1) && (rd_total_beats > 1))
        |-> !rlast;
    endproperty
    
    assert property (p_rlast_not_early)
        else $error("ASSERTION FAILED: RLAST asserted too early");
    
    // Assertion 3: RVALID stays high until RREADY (handshake)
    property p_rvalid_stable;
        @(posedge clk) disable iff (!aresetn)
        (prev_rvalid && !prev_rready)
        |-> rvalid;
    endproperty
    
    assert property (p_rvalid_stable)
        else $error("ASSERTION FAILED: RVALID dropped before RREADY");
    
    // Assertion 4: Normal response when no decode error
    property p_rresp_okay;
        @(posedge clk) disable iff (!aresetn)
        (rvalid && !decode_error)
        |-> (rresp == RESP_OKAY);
    endproperty
    
    assert property (p_rresp_okay)
        else $error("ASSERTION FAILED: RRESP should be OKAY for valid addresses");

    // =========================================================================
    // GOLDEN TEST TASKS
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

    // Test 1: Single beat read
    task automatic test_single_read();
        test_count++;
        $display("\n[TEST %0d] Single Beat Read", test_count);
        
        // Issue read address
        araddr = 32'h0000_0100;
        arlen = 0;  // 1 beat
        arid = 4'h1;
        arburst = BURST_INCR;
        arvalid = 1;
        
        wait(arready);
        @(posedge clk);
        arvalid = 0;
        
        // Collect response
        rready = 1;
        wait(rvalid);
        
        // araddr=0x100 → word index 0x100>>2=0x40=64; expected data = 32'hDADA_0000+64
        if (!rlast) begin
            $error("ASSERTION FAILED: RLAST should be high for single beat");
            fail_count++;
        end else if (rresp !== RESP_OKAY) begin
            $error("ASSERTION FAILED: Expected OKAY response");
            fail_count++;
        end else if (rdata !== (32'hDADA_0000 + 32'd64)) begin
            $error("ASSERTION FAILED: Data mismatch: got 0x%08h, expected 0x%08h",
                   rdata, 32'hDADA_0000 + 32'd64);
            fail_count++;
        end else begin
            $display("  PASS: Single read completed, data=0x%08h", rdata);
            pass_count++;
        end
        
        @(posedge clk);
        #1; // avoid race: let DUT's always_ff process handshake before deasserting rready
        rready = 0;
        repeat(5) @(posedge clk);
    endtask

    // Test 2: 4-beat INCR burst read
    task automatic test_burst_read();
        int beat;
        test_count++;
        $display("\n[TEST %0d] 4-Beat INCR Burst Read", test_count);
        
        // Issue read address
        araddr = 32'h0000_0200;
        arlen = 3;  // 4 beats
        arid = 4'h2;
        arburst = BURST_INCR;
        arsize = 2;  // 4 bytes
        arvalid = 1;
        
        wait(arready);
        @(posedge clk);
        arvalid = 0;
        
        // Collect responses
        rready = 1;
        beat = 0;
        
        // araddr=0x200 → word index 0x200>>2=0x80=128; beat i at word (128+i)
        while (beat < 4) begin
            wait(rvalid);
            $display("  Beat %0d: data=0x%08h, rlast=%b", beat, rdata, rlast);

            if (beat == 3 && !rlast) begin
                $error("ASSERTION FAILED: RLAST not high on final beat");
                fail_count++;
                break;
            end else if (beat < 3 && rlast) begin
                $error("ASSERTION FAILED: RLAST high too early at beat %0d", beat);
                fail_count++;
                break;
            end else if (rdata !== (32'hDADA_0000 + 32'd128 + beat)) begin
                $error("ASSERTION FAILED: Burst beat %0d data mismatch: got 0x%08h, expected 0x%08h",
                       beat, rdata, 32'hDADA_0000 + 32'd128 + beat);
                fail_count++;
                break;
            end

            beat++;
            @(posedge clk);
            #1; // avoid race: let DUT's always_ff update rdata/rvalid before next wait(rvalid)
        end

        if (beat == 4) begin
            $display("  PASS: Burst read completed correctly");
            pass_count++;
        end

        #1; // avoid race: let DUT's always_ff process last handshake before deasserting rready
        rready = 0;
        repeat(5) @(posedge clk);
    endtask

    // Test 3: RVALID/RREADY handshake
    task automatic test_handshake();
        test_count++;
        $display("\n[TEST %0d] RVALID/RREADY Handshake", test_count);
        
        // Issue read
        araddr = 32'h0000_0300;
        arlen = 0;
        arvalid = 1;
        
        wait(arready);
        @(posedge clk);
        arvalid = 0;
        
        // Don't assert rready immediately
        rready = 0;
        wait(rvalid);
        $display("  RVALID asserted, holding RREADY low");
        
        // Wait a few cycles with rready low
        repeat(3) begin
            @(posedge clk);
            if (!rvalid) begin
                $error("ASSERTION FAILED: RVALID dropped before RREADY");
                fail_count++;
                rready = 1;
                @(posedge clk);
                rready = 0;
                return;
            end
        end
        
        // Now assert rready
        rready = 1;
        @(posedge clk);
        $display("  PASS: RVALID held stable until RREADY");
        pass_count++;

        #1; // avoid race: let DUT's always_ff process handshake before deasserting rready
        rready = 0;
        repeat(5) @(posedge clk);
    endtask

    // =========================================================================
    // END OF TEST SECTION
    // =========================================================================

    // Main test sequence
    initial begin
        $dumpfile("axi4_read_channel_tb.vcd");
        $dumpvars(0, axi4_read_channel_tb);
        
        $display("================================================================");
        $display(" AXI4 Read Channel Testbench - GOLDEN");
        $display("================================================================");

        reset_dut();

        test_single_read();
        test_burst_read();
        test_handshake();

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
        $error("TESTBENCH TIMEOUT: simulation exceeded time limit");
        $finish;
    end

endmodule
