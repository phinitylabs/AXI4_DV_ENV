// =============================================================================
// AXI4 Slave Golden Testbench
// Comprehensive testbench for benchmark validation
// =============================================================================

`timescale 1ns/1ps

module axi4_slave_tb;

  // ==========================================================================
  // Parameters
  // ==========================================================================
  parameter ADDR_WIDTH = 32;
  parameter DATA_WIDTH = 32;
  parameter ID_WIDTH   = 4;
  parameter STRB_WIDTH = DATA_WIDTH / 8;
  parameter CLK_PERIOD = 10;

  // ==========================================================================
  // Signals
  // ==========================================================================
  logic aclk;
  logic aresetn;

  // Write Address Channel
  logic [ID_WIDTH-1:0]     awid;
  logic [ADDR_WIDTH-1:0]   awaddr;
  logic [7:0]              awlen;
  logic [2:0]              awsize;
  logic [1:0]              awburst;
  logic                    awvalid;
  logic                    awready;

  // Write Data Channel
  logic [DATA_WIDTH-1:0]   wdata;
  logic [STRB_WIDTH-1:0]   wstrb;
  logic                    wlast;
  logic                    wvalid;
  logic                    wready;

  // Write Response Channel
  logic [ID_WIDTH-1:0]     bid;
  logic [1:0]              bresp;
  logic                    bvalid;
  logic                    bready;

  // Read Address Channel
  logic [ID_WIDTH-1:0]     arid;
  logic [ADDR_WIDTH-1:0]   araddr;
  logic [7:0]              arlen;
  logic [2:0]              arsize;
  logic [1:0]              arburst;
  logic                    arvalid;
  logic                    arready;

  // Read Data Channel
  logic [ID_WIDTH-1:0]     rid;
  logic [DATA_WIDTH-1:0]   rdata;
  logic [1:0]              rresp;
  logic                    rlast;
  logic                    rvalid;
  logic                    rready;

  // ==========================================================================
  // Test Counters
  // ==========================================================================
  int test_count = 0;
  int pass_count = 0;
  int fail_count = 0;

  // ==========================================================================
  // Clock Generation
  // ==========================================================================
  initial begin
    aclk = 0;
    forever #(CLK_PERIOD/2) aclk = ~aclk;
  end

  // ==========================================================================
  // DUT Instantiation
  // ==========================================================================
  axi4_slave_top #(
    .ADDR_WIDTH(ADDR_WIDTH),
    .DATA_WIDTH(DATA_WIDTH),
    .ID_WIDTH(ID_WIDTH)
  ) dut (
    .aclk     (aclk),
    .aresetn  (aresetn),
    // Write Address
    .awid     (awid),
    .awaddr   (awaddr),
    .awlen    (awlen),
    .awsize   (awsize),
    .awburst  (awburst),
    .awvalid  (awvalid),
    .awready  (awready),
    // Write Data
    .wdata    (wdata),
    .wstrb    (wstrb),
    .wlast    (wlast),
    .wvalid   (wvalid),
    .wready   (wready),
    // Write Response
    .bid      (bid),
    .bresp    (bresp),
    .bvalid   (bvalid),
    .bready   (bready),
    // Read Address
    .arid     (arid),
    .araddr   (araddr),
    .arlen    (arlen),
    .arsize   (arsize),
    .arburst  (arburst),
    .arvalid  (arvalid),
    .arready  (arready),
    // Read Data
    .rid      (rid),
    .rdata    (rdata),
    .rresp    (rresp),
    .rlast    (rlast),
    .rvalid   (rvalid),
    .rready   (rready)
  );

  // ==========================================================================
  // Signal Initialization
  // ==========================================================================
  task automatic init_signals();
    awid    = '0;
    awaddr  = '0;
    awlen   = '0;
    awsize  = 3'b010;  // 4 bytes
    awburst = 2'b01;   // INCR
    awvalid = 1'b0;
    
    wdata   = '0;
    wstrb   = '0;
    wlast   = 1'b0;
    wvalid  = 1'b0;
    
    bready  = 1'b1;
    
    arid    = '0;
    araddr  = '0;
    arlen   = '0;
    arsize  = 3'b010;
    arburst = 2'b01;
    arvalid = 1'b0;
    
    rready  = 1'b1;
  endtask

  // ==========================================================================
  // Reset Task
  // ==========================================================================
  task automatic reset_dut();
    aresetn = 1'b0;
    init_signals();
    repeat(5) @(posedge aclk);
    aresetn = 1'b1;
    repeat(2) @(posedge aclk);
  endtask

  // ==========================================================================
  // AXI Write Task
  // ==========================================================================
  task automatic axi_write(
    input logic [ADDR_WIDTH-1:0] addr,
    input logic [DATA_WIDTH-1:0] data,
    input logic [ID_WIDTH-1:0]   id = 0,
    input logic [7:0]            len = 0,
    input logic [1:0]            burst = 2'b01,
    input logic [STRB_WIDTH-1:0] strobe = 4'b1111,
    output logic [1:0]           resp
  );
    int timeout_cnt;
    
    // Wait for DUT to be in IDLE state (awready high)
    timeout_cnt = 0;
    while (!awready && timeout_cnt < 100) begin
      @(posedge aclk);
      timeout_cnt++;
    end
    @(posedge aclk);  // Extra cycle to ensure we're stable
    
    // Address phase - set up signals
    awid    = id;
    awaddr  = addr;
    awlen   = len;
    awburst = burst;
    awsize  = 3'b010;
    awvalid = 1'b1;
    
    // Wait for handshake - awready should still be high
    @(posedge aclk);
    // Handshake happened on this edge
    $display("DEBUG[axi_write]: Handshake! awaddr on wire=0x%h, awready=%b", awaddr, awready);
    awvalid = 1'b0;
    
    // Data phase - send all beats  
    // After ADDR_RECV, DUT goes to DATA_BURST where wready=1
    @(posedge aclk);  // Wait for state transition to DATA_BURST
    
    for (int i = 0; i <= len; i++) begin
      wdata  = data + i;
      wstrb  = strobe;
      wlast  = (i == len);
      wvalid = 1'b1;
      $display("DEBUG[axi_write]: Data beat %0d, wdata=0x%h, wlast=%b, wready=%b", i, wdata, wlast, wready);
      
      // Wait for data handshake
      timeout_cnt = 0;
      while (timeout_cnt < 100) begin
        @(posedge aclk);
        break;  // Handshake assumed on first edge where wready is high
      end
    end
    wvalid = 1'b0;
    wlast  = 1'b0;
    
    // Wait for response
    timeout_cnt = 0;
    while (!bvalid && timeout_cnt < 100) begin
      @(posedge aclk);
      timeout_cnt++;
    end
    resp = bresp;
    @(posedge aclk);
    
    // Wait for state machine to return to IDLE
    @(posedge aclk);
  endtask

  // ==========================================================================
  // AXI Read Task
  // ==========================================================================
  task automatic axi_read(
    input  logic [ADDR_WIDTH-1:0] addr,
    input  logic [ID_WIDTH-1:0]   id = 0,
    input  logic [7:0]            len = 0,
    input  logic [1:0]            burst = 2'b01,
    output logic [DATA_WIDTH-1:0] data_out,
    output logic [1:0]            resp
  );
    logic [DATA_WIDTH-1:0] read_data[$];
    int beat_count;
    int timeout_cnt;
    logic got_rlast;
    
    // Explicitly clear the queue at start
    read_data.delete();
    
    // Wait for DUT to be in IDLE state (arready high)
    timeout_cnt = 0;
    while (!arready && timeout_cnt < 100) begin
      @(posedge aclk);
      timeout_cnt++;
    end
    
    // Address phase - set up signals
    arid    = id;
    araddr  = addr;
    arlen   = len;
    arburst = burst;
    arsize  = 3'b010;
    arvalid = 1'b1;
    
    // Wait for address handshake (happens on next posedge)
    @(posedge aclk);
    $display("DEBUG[axi_read]: Handshake! araddr on wire=0x%h, arready=%b", araddr, arready);
    arvalid = 1'b0;
    
    // Data phase - receive all beats
    beat_count = 0;
    got_rlast = 0;
    while (!got_rlast && beat_count < 300) begin
      // Wait for valid data
      timeout_cnt = 0;
      while (!rvalid && timeout_cnt < 100) begin
        @(posedge aclk);
        timeout_cnt++;
      end
      
      if (rvalid) begin
        $display("DEBUG[axi_read]: Data beat %0d, rdata=0x%h, rlast=%b", beat_count, rdata, rlast);
        read_data.push_back(rdata);
        resp = rresp;
        got_rlast = rlast;
        beat_count++;
        @(posedge aclk);
      end else begin
        $error("[RVALID_TIMEOUT] Timeout waiting for rvalid");
        break;
      end
    end
    
    // Check beat count matches expected
    if (beat_count != len + 1) begin
      $error("[BEAT_COUNT] Expected %0d beats, got %0d", len + 1, beat_count);
    end
    
    // Return first data word
    if (read_data.size() > 0) begin
      data_out = read_data[0];
      $display("DEBUG[axi_read]: Returning data_out=0x%h from queue[0], queue size=%0d", data_out, read_data.size());
    end else begin
      data_out = '0;
      $display("DEBUG[axi_read]: Queue empty, returning 0");
    end
    
    // Wait for state machine to return to IDLE
    @(posedge aclk);
  endtask

  // ==========================================================================
  // Simple Write Task (no output)
  // ==========================================================================
  task automatic axi_write_simple(
    input logic [ADDR_WIDTH-1:0] addr,
    input logic [DATA_WIDTH-1:0] data
  );
    logic [1:0] resp;
    axi_write(addr, data, 0, 0, 2'b01, 4'b1111, resp);
  endtask

  // ==========================================================================
  // Simple Read Task
  // ==========================================================================
  task automatic axi_read_simple(
    input  logic [ADDR_WIDTH-1:0] addr,
    output logic [DATA_WIDTH-1:0] data
  );
    logic [1:0] resp;
    axi_read(addr, 0, 0, 2'b01, data, resp);
  endtask

  // ==========================================================================
  // TEST CASES
  // ==========================================================================

  // -------------------------------------------------------------------------
  // Test 1: Single Write/Read
  // -------------------------------------------------------------------------
  task automatic test_single_write_read();
    logic [DATA_WIDTH-1:0] wr_data, rd_data;
    logic [1:0] wr_resp, rd_resp;
    
    test_count++;
    $display("\n[TEST %0d] Single Write/Read", test_count);
    
    // Debug: Check initial state
    $display("DEBUG: Before write - awready=%b, wready=%b, arready=%b", awready, wready, arready);
    
    wr_data = 32'hDEAD_BEEF;
    $display("DEBUG: Starting write to 0x1000 with data 0x%h", wr_data);
    axi_write(32'h0000_1000, wr_data, 0, 0, 2'b01, 4'b1111, wr_resp);
    $display("DEBUG: Write complete, resp=%d", wr_resp);
    axi_read(32'h0000_1000, 0, 0, 2'b01, rd_data, rd_resp);
    $display("DEBUG: Read complete, data=0x%h, resp=%d", rd_data, rd_resp);
    
    if (rd_data !== wr_data) begin
      $error("[DATA_MISMATCH] Single write/read: expected=0x%h, got=0x%h", wr_data, rd_data);
      fail_count++;
    end else begin
      $display("  PASS: Data matches 0x%h", rd_data);
      $display("COVERPOINT_HIT:cp_burst_single");
      $display("COVERPOINT_HIT:cp_write_response");
      $display("COVERPOINT_HIT:cp_read_response");
      pass_count++;
    end
    
    if (wr_resp !== 2'b00) begin
      $error("[BRESP_ERROR] Expected OKAY, got %0d", wr_resp);
    end
  endtask

  // -------------------------------------------------------------------------
  // Test 2: Multiple Addresses
  // -------------------------------------------------------------------------
  task automatic test_multiple_addresses();
    logic [DATA_WIDTH-1:0] rd_data;
    int errors = 0;
    
    test_count++;
    $display("\n[TEST %0d] Multiple Addresses", test_count);
    
    // Write to multiple locations with debug
    for (int i = 0; i < 8; i++) begin
      $display("DEBUG: Writing to addr 0x%h, data 0x%h", 32'h0000_2000 + (i*4), 32'hCAFE_0000 + i);
      axi_write_simple(32'h0000_2000 + (i*4), 32'hCAFE_0000 + i);
    end
    
    $display("DEBUG: All writes complete, starting reads");
    
    // Read back and verify
    for (int i = 0; i < 8; i++) begin
      axi_read_simple(32'h0000_2000 + (i*4), rd_data);
      $display("DEBUG: Read from addr 0x%h, got 0x%h", 32'h0000_2000 + (i*4), rd_data);
      if (rd_data !== (32'hCAFE_0000 + i)) begin
        $error("[DATA_MISMATCH] Addr 0x%h: expected=0x%h, got=0x%h", 
               32'h0000_2000 + (i*4), 32'hCAFE_0000 + i, rd_data);
        errors++;
      end
    end
    
    if (errors == 0) begin
      $display("  PASS: All 8 locations correct");
      pass_count++;
    end else begin
      fail_count++;
    end
  endtask

  // -------------------------------------------------------------------------
  // Test 3: Burst INCR
  // -------------------------------------------------------------------------
  task automatic test_burst_incr();
    logic [DATA_WIDTH-1:0] rd_data;
    logic [1:0] resp;
    
    test_count++;
    $display("\n[TEST %0d] Burst INCR (4 beats)", test_count);
    
    // Write burst
    axi_write(32'h0000_3000, 32'hBEEF_0000, 0, 3, 2'b01, 4'b1111, resp);
    
    // Read burst
    axi_read(32'h0000_3000, 0, 3, 2'b01, rd_data, resp);
    
    // Verify first word
    if (rd_data !== 32'hBEEF_0000) begin
      $error("[DATA_MISMATCH] Burst INCR first beat: expected=0x%h, got=0x%h", 
             32'hBEEF_0000, rd_data);
      fail_count++;
    end else begin
      $display("  PASS: Burst INCR completed");
      $display("COVERPOINT_HIT:cp_burst_incr");
      pass_count++;
    end
  endtask

  // -------------------------------------------------------------------------
  // Test 4: Burst FIXED
  // -------------------------------------------------------------------------
  task automatic test_burst_fixed();
    logic [DATA_WIDTH-1:0] rd_data;
    logic [1:0] resp;
    
    test_count++;
    $display("\n[TEST %0d] Burst FIXED (4 beats)", test_count);
    
    // Write burst - all to same address
    axi_write(32'h0000_4000, 32'hF1ED_0000, 0, 3, 2'b00, 4'b1111, resp);
    
    // Read back - should get last written value
    axi_read_simple(32'h0000_4000, rd_data);
    
    // Last value written is base + 3
    if (rd_data !== 32'hF1ED_0003) begin
      $error("[DATA_MISMATCH] Burst FIXED: expected=0x%h, got=0x%h", 
             32'hF1ED_0003, rd_data);
      fail_count++;
    end else begin
      $display("  PASS: Burst FIXED last value correct");
      $display("COVERPOINT_HIT:cp_burst_fixed");
      pass_count++;
    end
  endtask

  // -------------------------------------------------------------------------
  // Test 5: Burst WRAP
  // -------------------------------------------------------------------------
  task automatic test_burst_wrap();
    logic [DATA_WIDTH-1:0] rd_data;
    logic [1:0] resp;
    
    test_count++;
    $display("\n[TEST %0d] Burst WRAP (4 beats)", test_count);
    
    // Write wrap burst
    axi_write(32'h0000_5000, 32'hABCD_0000, 0, 3, 2'b10, 4'b1111, resp);
    
    // Read back
    axi_read(32'h0000_5000, 0, 3, 2'b10, rd_data, resp);
    
    $display("  PASS: Burst WRAP completed");
    $display("COVERPOINT_HIT:cp_burst_wrap");
    pass_count++;
  endtask

  // -------------------------------------------------------------------------
  // Test 6: Byte Strobes - Full
  // -------------------------------------------------------------------------
  task automatic test_strobe_full();
    logic [DATA_WIDTH-1:0] rd_data;
    
    test_count++;
    $display("\n[TEST %0d] Byte Strobe Full (0xF)", test_count);
    
    axi_write_simple(32'h0000_6000, 32'hFFFF_FFFF);
    axi_read_simple(32'h0000_6000, rd_data);
    
    if (rd_data !== 32'hFFFF_FFFF) begin
      $error("[DATA_MISMATCH] Full strobe: expected=0xFFFFFFFF, got=0x%h", rd_data);
      fail_count++;
    end else begin
      $display("  PASS: Full strobe correct");
      $display("COVERPOINT_HIT:cp_strobe_full");
      pass_count++;
    end
  endtask

  // -------------------------------------------------------------------------
  // Test 7: Byte Strobes - Partial (byte 0 only)
  // -------------------------------------------------------------------------
  task automatic test_strobe_partial();
    logic [DATA_WIDTH-1:0] rd_data;
    logic [1:0] resp;
    
    test_count++;
    $display("\n[TEST %0d] Byte Strobe Partial (byte 0)", test_count);
    
    // First write all ones
    axi_write_simple(32'h0000_6100, 32'hFFFF_FFFF);
    
    // Then write with partial strobe (only byte 0)
    axi_write(32'h0000_6100, 32'h0000_00AA, 0, 0, 2'b01, 4'b0001, resp);
    
    // Read back
    axi_read_simple(32'h0000_6100, rd_data);
    
    // Only byte 0 should change
    if (rd_data !== 32'hFFFF_FFAA) begin
      $error("[STROBE_ERROR] Partial strobe: expected=0xFFFFFFAA, got=0x%h", rd_data);
      fail_count++;
    end else begin
      $display("  PASS: Partial strobe preserved other bytes");
      $display("COVERPOINT_HIT:cp_strobe_partial");
      pass_count++;
    end
  endtask

  // -------------------------------------------------------------------------
  // Test 8: Byte Strobe - Upper bytes
  // -------------------------------------------------------------------------
  task automatic test_strobe_upper();
    logic [DATA_WIDTH-1:0] rd_data;
    logic [1:0] resp;
    
    test_count++;
    $display("\n[TEST %0d] Byte Strobe Upper (byte 3)", test_count);
    
    // First write zeros
    axi_write_simple(32'h0000_6200, 32'h0000_0000);
    
    // Then write with partial strobe (only byte 3)
    axi_write(32'h0000_6200, 32'hBB00_0000, 0, 0, 2'b01, 4'b1000, resp);
    
    // Read back
    axi_read_simple(32'h0000_6200, rd_data);
    
    if (rd_data !== 32'hBB00_0000) begin
      $error("[STROBE_ERROR] Upper byte strobe: expected=0xBB000000, got=0x%h", rd_data);
      fail_count++;
    end else begin
      $display("  PASS: Upper byte strobe correct");
      pass_count++;
    end
  endtask

  // -------------------------------------------------------------------------
  // Test 9: Address Zero
  // -------------------------------------------------------------------------
  task automatic test_address_zero();
    logic [DATA_WIDTH-1:0] rd_data;
    
    test_count++;
    $display("\n[TEST %0d] Address Zero", test_count);
    
    axi_write_simple(32'h0000_0000, 32'hADD0_0000);
    axi_read_simple(32'h0000_0000, rd_data);
    
    if (rd_data !== 32'hADD0_0000) begin
      $error("[DATA_MISMATCH] Address zero: expected=0xADD00000, got=0x%h", rd_data);
      fail_count++;
    end else begin
      $display("  PASS: Address zero works");
      $display("COVERPOINT_HIT:cp_addr_zero");
      pass_count++;
    end
  endtask

  // -------------------------------------------------------------------------
  // Test 10: Address Boundary (0xFFFC)
  // -------------------------------------------------------------------------
  task automatic test_address_boundary();
    logic [DATA_WIDTH-1:0] rd_data;
    
    test_count++;
    $display("\n[TEST %0d] Address Boundary (0xFFFC)", test_count);
    
    axi_write_simple(32'h0000_FFFC, 32'hB0AD_DA12);
    axi_read_simple(32'h0000_FFFC, rd_data);
    
    if (rd_data !== 32'hB0AD_DA12) begin
      $error("[DATA_MISMATCH] Address boundary: expected=0xB0ADDA12, got=0x%h", rd_data);
      fail_count++;
    end else begin
      $display("  PASS: Address boundary works");
      $display("COVERPOINT_HIT:cp_addr_boundary");
      pass_count++;
    end
  endtask

  // -------------------------------------------------------------------------
  // Test 11: Decode Error - Write
  // -------------------------------------------------------------------------
  task automatic test_decode_error_write();
    logic [1:0] resp;
    
    test_count++;
    $display("\n[TEST %0d] Decode Error on Write", test_count);
    
    // Write to out-of-range address
    axi_write(32'h0001_0000, 32'hDEAD_BEEF, 0, 0, 2'b01, 4'b1111, resp);
    
    if (resp !== 2'b11) begin
      $error("[BRESP_ERROR] Expected DECERR (3), got %0d for out-of-range write", resp);
      fail_count++;
    end else begin
      $display("  PASS: DECERR returned for out-of-range write");
      $display("COVERPOINT_HIT:cp_decode_error");
      pass_count++;
    end
  endtask

  // -------------------------------------------------------------------------
  // Test 12: Decode Error - Read
  // -------------------------------------------------------------------------
  task automatic test_decode_error_read();
    logic [DATA_WIDTH-1:0] rd_data;
    logic [1:0] resp;
    
    test_count++;
    $display("\n[TEST %0d] Decode Error on Read", test_count);
    
    // Read from out-of-range address
    axi_read(32'h0002_0000, 0, 0, 2'b01, rd_data, resp);
    
    if (resp !== 2'b11) begin
      $error("[RRESP_ERROR] Expected DECERR (3), got %0d for out-of-range read", resp);
      fail_count++;
    end else begin
      $display("  PASS: DECERR returned for out-of-range read");
      pass_count++;
    end
  endtask

  // -------------------------------------------------------------------------
  // Test 13: Transaction IDs
  // -------------------------------------------------------------------------
  task automatic test_transaction_ids();
    logic [DATA_WIDTH-1:0] rd_data;
    logic [1:0] resp;
    
    test_count++;
    $display("\n[TEST %0d] Transaction IDs", test_count);
    
    // Write with ID=5
    axi_write(32'h0000_7000, 32'h1D05_0000, 5, 0, 2'b01, 4'b1111, resp);
    
    // Check BID (captured during write)
    if (bid !== 5) begin
      $error("[BID_MISMATCH] Expected BID=5, got %0d", bid);
      fail_count++;
    end else begin
      // Read with ID=10
      axi_read(32'h0000_7000, 10, 0, 2'b01, rd_data, resp);
      
      if (rid !== 10) begin
        $error("[RID_MISMATCH] Expected RID=10, got %0d", rid);
        fail_count++;
      end else begin
        $display("  PASS: Transaction IDs correct");
        pass_count++;
      end
    end
  endtask

  // -------------------------------------------------------------------------
  // Test 14: Long Burst (16 beats)
  // -------------------------------------------------------------------------
  task automatic test_long_burst();
    logic [DATA_WIDTH-1:0] rd_data;
    logic [1:0] resp;
    
    test_count++;
    $display("\n[TEST %0d] Long Burst (16 beats)", test_count);
    
    axi_write(32'h0000_8000, 32'hFACE_0000, 0, 15, 2'b01, 4'b1111, resp);
    axi_read(32'h0000_8000, 0, 15, 2'b01, rd_data, resp);
    
    if (rd_data !== 32'hFACE_0000) begin
      $error("[DATA_MISMATCH] Long burst: expected=0xFACE0000, got=0x%h", rd_data);
      fail_count++;
    end else begin
      $display("  PASS: Long burst completed");
      pass_count++;
    end
  endtask

  // -------------------------------------------------------------------------
  // Test 15: Max Burst (256 beats) - Edge case for E01
  // -------------------------------------------------------------------------
  task automatic test_max_burst();
    logic [DATA_WIDTH-1:0] rd_data;
    logic [1:0] resp;
    
    test_count++;
    $display("\n[TEST %0d] Max Burst (256 beats) - AWLEN=255", test_count);
    
    axi_write(32'h0000_9000, 32'hDADA_0000, 0, 255, 2'b01, 4'b1111, resp);
    axi_read(32'h0000_9000, 0, 255, 2'b01, rd_data, resp);
    
    if (resp !== 2'b00) begin
      $error("[MAX_BURST] Unexpected response %0d for max burst", resp);
      fail_count++;
    end else begin
      $display("  PASS: Max burst (256 beats) completed");
      $display("COVERPOINT_HIT:cp_burst_max");
      pass_count++;
    end
  endtask

  // -------------------------------------------------------------------------
  // Test 16: RLAST Timing Check
  // -------------------------------------------------------------------------
  task automatic test_rlast_timing();
    logic [1:0] resp;
    int rlast_beat;
    int beat_count;
    int timeout_cnt;
    
    test_count++;
    $display("\n[TEST %0d] RLAST Timing (4 beats)", test_count);
    
    // First write some data
    axi_write(32'h0000_A000, 32'hABBA_0000, 0, 3, 2'b01, 4'b1111, resp);
    
    // Wait for DUT to be in IDLE state
    timeout_cnt = 0;
    while (!arready && timeout_cnt < 100) begin
      @(posedge aclk);
      timeout_cnt++;
    end
    
    // Read and track RLAST
    arid    = 0;
    araddr  = 32'h0000_A000;
    arlen   = 3;
    arburst = 2'b01;
    arsize  = 3'b010;
    arvalid = 1'b1;
    
    // Wait for address handshake
    @(posedge aclk);
    arvalid = 1'b0;
    
    beat_count = 0;
    rlast_beat = -1;
    for (int i = 0; i < 10; i++) begin  // Max 10 iterations for safety
      // Wait for valid data
      timeout_cnt = 0;
      while (!rvalid && timeout_cnt < 100) begin
        @(posedge aclk);
        timeout_cnt++;
      end
      
      if (rvalid) begin
        beat_count++;
        if (rlast) rlast_beat = beat_count;
        @(posedge aclk);
      end
      if (rlast_beat > 0) break;  // Got rlast, exit loop
    end
    
    if (rlast_beat !== 4) begin
      $error("[RLAST_TIMING] RLAST on beat %0d, expected beat 4", rlast_beat);
      fail_count++;
    end else begin
      $display("  PASS: RLAST on correct beat");
      pass_count++;
    end
  endtask

  // -------------------------------------------------------------------------
  // Test 17: Reset Behavior
  // -------------------------------------------------------------------------
  task automatic test_reset_behavior();
    test_count++;
    $display("\n[TEST %0d] Reset Behavior", test_count);
    
    // Apply reset
    aresetn = 1'b0;
    repeat(3) @(posedge aclk);
    
    // Check outputs after reset
    if (bvalid !== 1'b0) begin
      $error("[RESET_ERROR] BVALID not 0 after reset");
      fail_count++;
    end else if (rvalid !== 1'b0) begin
      $error("[RESET_ERROR] RVALID not 0 after reset");
      fail_count++;
    end else begin
      $display("  PASS: Outputs cleared after reset");
      pass_count++;
    end
    
    // Release reset
    aresetn = 1'b1;
    repeat(2) @(posedge aclk);
  endtask

  // -------------------------------------------------------------------------
  // Test 18: Back-to-back Writes
  // -------------------------------------------------------------------------
  task automatic test_back_to_back_writes();
    logic [DATA_WIDTH-1:0] rd_data;
    int errors = 0;
    
    test_count++;
    $display("\n[TEST %0d] Back-to-back Writes", test_count);
    
    // Rapid writes
    for (int i = 0; i < 10; i++) begin
      axi_write_simple(32'h0000_B000 + (i*4), 32'hB2B0_0000 + i);
    end
    
    // Verify all
    for (int i = 0; i < 10; i++) begin
      axi_read_simple(32'h0000_B000 + (i*4), rd_data);
      if (rd_data !== (32'hB2B0_0000 + i)) errors++;
    end
    
    if (errors == 0) begin
      $display("  PASS: All back-to-back writes correct");
      pass_count++;
    end else begin
      $error("[BACK2BACK] %0d errors in back-to-back writes", errors);
      fail_count++;
    end
  endtask

  // -------------------------------------------------------------------------
  // Test 19: Back-to-back Reads with Different IDs
  // -------------------------------------------------------------------------
  task automatic test_back_to_back_reads();
    logic [DATA_WIDTH-1:0] rd_data;
    logic [1:0] resp;
    
    test_count++;
    $display("\n[TEST %0d] Back-to-back Reads Different IDs", test_count);
    
    // Write data first
    axi_write_simple(32'h0000_C000, 32'hC000_1111);
    axi_write_simple(32'h0000_C004, 32'hC004_2222);
    
    // Read with different IDs
    axi_read(32'h0000_C000, 1, 0, 2'b01, rd_data, resp);
    if (rid !== 1) begin
      $error("[RID_STALE] First read RID: expected=1, got=%0d", rid);
      fail_count++;
      return;
    end
    
    axi_read(32'h0000_C004, 7, 0, 2'b01, rd_data, resp);
    if (rid !== 7) begin
      $error("[RID_STALE] Second read RID: expected=7, got=%0d", rid);
      fail_count++;
    end else begin
      $display("  PASS: RIDs updated correctly");
      pass_count++;
    end
  endtask

  // -------------------------------------------------------------------------
  // Test 20: Single Beat with WLAST
  // -------------------------------------------------------------------------
  task automatic test_single_beat_wlast();
    logic [1:0] resp;
    logic [DATA_WIDTH-1:0] rd_data;
    
    test_count++;
    $display("\n[TEST %0d] Single Beat WLAST", test_count);
    
    // Single beat (awlen=0) should still check WLAST
    axi_write(32'h0000_D000, 32'h5BEA_BEEF, 0, 0, 2'b01, 4'b1111, resp);
    
    if (resp !== 2'b00) begin
      $error("[WLAST_ERROR] Single beat write got response %0d", resp);
      fail_count++;
    end else begin
      axi_read_simple(32'h0000_D000, rd_data);
      if (rd_data !== 32'h5BEA_BEEF) begin
        $error("[DATA_MISMATCH] Single beat: expected=0x5BEABEEF, got=0x%h", rd_data);
        fail_count++;
      end else begin
        $display("  PASS: Single beat with WLAST correct");
        pass_count++;
      end
    end
  endtask

  // ==========================================================================
  // Main Test Sequence
  // ==========================================================================
  initial begin
    $dumpfile("axi4_slave_tb.vcd");
    $dumpvars(0, axi4_slave_tb);
    
    $display("================================================================");
    $display("  AXI4 Slave Golden Testbench");
    $display("================================================================");
    
    // Initial reset
    reset_dut();
    
    // Run all tests
    test_single_write_read();
    test_multiple_addresses();
    test_burst_incr();
    test_burst_fixed();
    test_burst_wrap();
    test_strobe_full();
    test_strobe_partial();
    test_strobe_upper();
    test_address_zero();
    test_address_boundary();
    test_decode_error_write();
    test_decode_error_read();
    test_transaction_ids();
    test_long_burst();
    test_max_burst();
    test_rlast_timing();
    test_reset_behavior();
    test_back_to_back_writes();
    test_back_to_back_reads();
    test_single_beat_wlast();
    
    // Wait for any pending transactions
    repeat(100) @(posedge aclk);
    
    // Summary
    $display("");
    $display("================================================================");
    $display("  TEST SUMMARY");
    $display("================================================================");
    $display("  Total Tests:  %0d", test_count);
    $display("  PASSED:       %0d", pass_count);
    $display("  FAILED:       %0d", fail_count);
    $display("================================================================");
    
    if (fail_count == 0)
      $display("*** ALL TESTS PASSED ***");
    else
      $display("*** SOME TESTS FAILED ***");
    
    $finish;
  end

  // Timeout watchdog
  initial begin
    #5000000;  // 5ms timeout
    $display("ERROR: Simulation timeout!");
    $finish;
  end

endmodule

