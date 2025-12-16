// =============================================================================
// AXI4 Protocol Coverage Module (FIXED - Not modified by agents)
// =============================================================================
//
// This module contains FIXED coverpoints that measure the quality of agent-
// generated stimulus. Agents don't write these - they write stimulus that
// exercises these coverpoints.
//
// Usage in grading:
//   1. Compile with agent's testbench
//   2. Run simulation
//   3. Extract coverage with Verilator (--coverage) or "covered" tool
//   4. Grade = % of bins hit by agent's stimulus
//
// =============================================================================

module axi4_coverage #(
    parameter ADDR_WIDTH = 32,
    parameter DATA_WIDTH = 32
) (
    input logic clk,
    input logic resetn,
    
    // Write Address Channel
    input logic [ADDR_WIDTH-1:0] awaddr,
    input logic [7:0]            awlen,
    input logic [2:0]            awsize,
    input logic [1:0]            awburst,
    input logic                  awvalid,
    input logic                  awready,
    
    // Write Data Channel
    input logic [DATA_WIDTH-1:0] wdata,
    input logic [3:0]            wstrb,
    input logic                  wlast,
    input logic                  wvalid,
    input logic                  wready,
    
    // Write Response Channel
    input logic [1:0]            bresp,
    input logic                  bvalid,
    input logic                  bready,
    
    // Read Address Channel
    input logic [ADDR_WIDTH-1:0] araddr,
    input logic [7:0]            arlen,
    input logic [2:0]            arsize,
    input logic [1:0]            arburst,
    input logic                  arvalid,
    input logic                  arready,
    
    // Read Data Channel
    input logic [DATA_WIDTH-1:0] rdata,
    input logic [1:0]            rresp,
    input logic                  rlast,
    input logic                  rvalid,
    input logic                  rready
);

    // ==========================================================================
    // Coverage tracking counters (Verilator-friendly - no covergroups)
    // ==========================================================================
    
    // Burst type coverage
    int unsigned burst_fixed_count = 0;
    int unsigned burst_incr_count = 0;
    int unsigned burst_wrap_count = 0;
    
    // Burst length coverage
    int unsigned single_beat_write_count = 0;
    int unsigned multi_beat_write_count = 0;
    int unsigned single_beat_read_count = 0;
    int unsigned multi_beat_read_count = 0;
    
    // Response code coverage
    int unsigned resp_okay_count = 0;
    int unsigned resp_exokay_count = 0;
    int unsigned resp_slverr_count = 0;
    int unsigned resp_decerr_count = 0;
    
    // Channel activity coverage
    int unsigned aw_handshake_count = 0;
    int unsigned w_handshake_count = 0;
    int unsigned b_handshake_count = 0;
    int unsigned ar_handshake_count = 0;
    int unsigned r_handshake_count = 0;
    
    // Address range coverage (4 regions)
    int unsigned addr_region0_count = 0;  // 0x000 - 0x0FF
    int unsigned addr_region1_count = 0;  // 0x100 - 0x1FF
    int unsigned addr_region2_count = 0;  // 0x200 - 0x2FF
    int unsigned addr_region3_count = 0;  // 0x300 - 0x3FF
    int unsigned addr_out_of_range_count = 0;  // > 0x3FF (should cause DECERR)
    
    // Write strobe coverage
    int unsigned wstrb_full_count = 0;    // All bytes (4'hF)
    int unsigned wstrb_partial_count = 0; // Partial bytes
    
    // LAST signal coverage
    int unsigned wlast_asserted_count = 0;
    int unsigned rlast_asserted_count = 0;
    
    // Burst types
    localparam [1:0] FIXED = 2'b00;
    localparam [1:0] INCR  = 2'b01;
    localparam [1:0] WRAP  = 2'b10;
    
    // Response codes
    localparam [1:0] OKAY   = 2'b00;
    localparam [1:0] EXOKAY = 2'b01;
    localparam [1:0] SLVERR = 2'b10;
    localparam [1:0] DECERR = 2'b11;
    
    // ==========================================================================
    // Coverage Collection Logic
    // ==========================================================================
    
    // Write Address Channel Coverage
    always_ff @(posedge clk) begin
        if (resetn && awvalid && awready) begin
            aw_handshake_count <= aw_handshake_count + 1;
            
            // Burst type coverage
            case (awburst)
                FIXED: burst_fixed_count <= burst_fixed_count + 1;
                INCR:  burst_incr_count <= burst_incr_count + 1;
                WRAP:  burst_wrap_count <= burst_wrap_count + 1;
                default: ;
            endcase
            
            // Burst length coverage
            if (awlen == 0)
                single_beat_write_count <= single_beat_write_count + 1;
            else
                multi_beat_write_count <= multi_beat_write_count + 1;
            
            // Address range coverage
            if (awaddr < 32'h100)
                addr_region0_count <= addr_region0_count + 1;
            else if (awaddr < 32'h200)
                addr_region1_count <= addr_region1_count + 1;
            else if (awaddr < 32'h300)
                addr_region2_count <= addr_region2_count + 1;
            else if (awaddr < 32'h400)
                addr_region3_count <= addr_region3_count + 1;
            else
                addr_out_of_range_count <= addr_out_of_range_count + 1;
        end
    end
    
    // Write Data Channel Coverage
    always_ff @(posedge clk) begin
        if (resetn && wvalid && wready) begin
            w_handshake_count <= w_handshake_count + 1;
            
            // Write strobe coverage
            if (wstrb == 4'hF)
                wstrb_full_count <= wstrb_full_count + 1;
            else if (wstrb != 4'h0)
                wstrb_partial_count <= wstrb_partial_count + 1;
            
            // WLAST coverage
            if (wlast)
                wlast_asserted_count <= wlast_asserted_count + 1;
        end
    end
    
    // Write Response Channel Coverage
    always_ff @(posedge clk) begin
        if (resetn && bvalid && bready) begin
            b_handshake_count <= b_handshake_count + 1;
            
            // Response code coverage
            case (bresp)
                OKAY:   resp_okay_count <= resp_okay_count + 1;
                EXOKAY: resp_exokay_count <= resp_exokay_count + 1;
                SLVERR: resp_slverr_count <= resp_slverr_count + 1;
                DECERR: resp_decerr_count <= resp_decerr_count + 1;
            endcase
        end
    end
    
    // Read Address Channel Coverage
    always_ff @(posedge clk) begin
        if (resetn && arvalid && arready) begin
            ar_handshake_count <= ar_handshake_count + 1;
            
            // Burst length coverage
            if (arlen == 0)
                single_beat_read_count <= single_beat_read_count + 1;
            else
                multi_beat_read_count <= multi_beat_read_count + 1;
        end
    end
    
    // Read Data Channel Coverage
    always_ff @(posedge clk) begin
        if (resetn && rvalid && rready) begin
            r_handshake_count <= r_handshake_count + 1;
            
            // Response code coverage (read)
            case (rresp)
                OKAY:   resp_okay_count <= resp_okay_count + 1;
                EXOKAY: resp_exokay_count <= resp_exokay_count + 1;
                SLVERR: resp_slverr_count <= resp_slverr_count + 1;
                DECERR: resp_decerr_count <= resp_decerr_count + 1;
            endcase
            
            // RLAST coverage
            if (rlast)
                rlast_asserted_count <= rlast_asserted_count + 1;
        end
    end
    
    // ==========================================================================
    // Coverage Report (printed at end of simulation)
    // ==========================================================================
    
    // Coverage bin definitions (total bins = 24)
    localparam TOTAL_COVERAGE_BINS = 24;
    
    function automatic int get_bins_hit();
        int bins_hit = 0;
        
        // Channel coverage (5 bins) - each channel exercised
        if (aw_handshake_count > 0) bins_hit++;
        if (w_handshake_count > 0) bins_hit++;
        if (b_handshake_count > 0) bins_hit++;
        if (ar_handshake_count > 0) bins_hit++;
        if (r_handshake_count > 0) bins_hit++;
        
        // Burst type coverage (3 bins)
        if (burst_fixed_count > 0) bins_hit++;
        if (burst_incr_count > 0) bins_hit++;
        if (burst_wrap_count > 0) bins_hit++;
        
        // Burst length coverage (4 bins)
        if (single_beat_write_count > 0) bins_hit++;
        if (multi_beat_write_count > 0) bins_hit++;
        if (single_beat_read_count > 0) bins_hit++;
        if (multi_beat_read_count > 0) bins_hit++;
        
        // Response code coverage (4 bins)
        if (resp_okay_count > 0) bins_hit++;
        if (resp_exokay_count > 0) bins_hit++;
        if (resp_slverr_count > 0) bins_hit++;
        if (resp_decerr_count > 0) bins_hit++;
        
        // Address range coverage (5 bins)
        if (addr_region0_count > 0) bins_hit++;
        if (addr_region1_count > 0) bins_hit++;
        if (addr_region2_count > 0) bins_hit++;
        if (addr_region3_count > 0) bins_hit++;
        if (addr_out_of_range_count > 0) bins_hit++;
        
        // Write strobe coverage (2 bins)
        if (wstrb_full_count > 0) bins_hit++;
        if (wstrb_partial_count > 0) bins_hit++;
        
        // LAST signal coverage (2 bins) - WLAST exercised, not just asserted once
        if (wlast_asserted_count > 0) bins_hit++;
        if (rlast_asserted_count > 0) bins_hit++;
        
        return bins_hit;
    endfunction
    
    // Final coverage report
    final begin
        int bins_hit;
        real coverage_pct;
        
        bins_hit = get_bins_hit();
        coverage_pct = (bins_hit * 100.0) / TOTAL_COVERAGE_BINS;
        
        $display("");
        $display("============================================================");
        $display("FUNCTIONAL COVERAGE REPORT (Fixed Coverpoints)");
        $display("============================================================");
        $display("");
        $display("Channel Coverage:");
        $display("  AW handshakes: %0d", aw_handshake_count);
        $display("  W  handshakes: %0d", w_handshake_count);
        $display("  B  handshakes: %0d", b_handshake_count);
        $display("  AR handshakes: %0d", ar_handshake_count);
        $display("  R  handshakes: %0d", r_handshake_count);
        $display("");
        $display("Burst Type Coverage:");
        $display("  FIXED: %0d, INCR: %0d, WRAP: %0d", burst_fixed_count, burst_incr_count, burst_wrap_count);
        $display("");
        $display("Burst Length Coverage:");
        $display("  Single-beat writes: %0d, Multi-beat writes: %0d", single_beat_write_count, multi_beat_write_count);
        $display("  Single-beat reads: %0d, Multi-beat reads: %0d", single_beat_read_count, multi_beat_read_count);
        $display("");
        $display("Response Code Coverage:");
        $display("  OKAY: %0d, EXOKAY: %0d, SLVERR: %0d, DECERR: %0d", resp_okay_count, resp_exokay_count, resp_slverr_count, resp_decerr_count);
        $display("");
        $display("Address Range Coverage:");
        $display("  Region0 (0x000-0x0FF): %0d", addr_region0_count);
        $display("  Region1 (0x100-0x1FF): %0d", addr_region1_count);
        $display("  Region2 (0x200-0x2FF): %0d", addr_region2_count);
        $display("  Region3 (0x300-0x3FF): %0d", addr_region3_count);
        $display("  Out of range (>0x3FF): %0d", addr_out_of_range_count);
        $display("");
        $display("Write Strobe Coverage:");
        $display("  Full (4'hF): %0d, Partial: %0d", wstrb_full_count, wstrb_partial_count);
        $display("");
        $display("LAST Signal Coverage:");
        $display("  WLAST asserted: %0d, RLAST asserted: %0d", wlast_asserted_count, rlast_asserted_count);
        $display("");
        $display("============================================================");
        $display("COVERAGE SUMMARY: %0d/%0d bins hit (%.1f%%)", bins_hit, TOTAL_COVERAGE_BINS, coverage_pct);
        $display("============================================================");
        $display("");
        
        // Machine-readable output for grading
        $display("COVERAGE_BINS_HIT=%0d", bins_hit);
        $display("COVERAGE_BINS_TOTAL=%0d", TOTAL_COVERAGE_BINS);
        $display("COVERAGE_PERCENT=%.1f", coverage_pct);
    end

endmodule

