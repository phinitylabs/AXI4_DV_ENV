// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vaxi4_top_tb.h for the primary calling header

#ifndef VERILATED_VAXI4_TOP_TB___024ROOT_H_
#define VERILATED_VAXI4_TOP_TB___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_timing.h"


class Vaxi4_top_tb__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vaxi4_top_tb___024root final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        CData/*0:0*/ axi4_top_tb__DOT__clk;
        CData/*0:0*/ axi4_top_tb__DOT__resetn;
        CData/*0:0*/ axi4_top_tb__DOT__awvalid_prev;
        CData/*0:0*/ axi4_top_tb__DOT__arvalid_prev;
        CData/*0:0*/ axi4_top_tb__DOT__wvalid_prev;
        CData/*0:0*/ axi4_top_tb__DOT__bvalid_prev;
        CData/*0:0*/ axi4_top_tb__DOT__rvalid_prev;
        CData/*0:0*/ axi4_top_tb__DOT__awready_prev;
        CData/*0:0*/ axi4_top_tb__DOT__arready_prev;
        CData/*0:0*/ axi4_top_tb__DOT__wready_prev;
        CData/*0:0*/ axi4_top_tb__DOT__bready_prev;
        CData/*0:0*/ axi4_top_tb__DOT__rready_prev;
        CData/*0:0*/ axi4_top_tb__DOT__awvalid_ever_seen;
        CData/*0:0*/ axi4_top_tb__DOT__arvalid_ever_seen;
        CData/*0:0*/ axi4_top_tb__DOT__wvalid_ever_seen;
        CData/*0:0*/ axi4_top_tb__DOT__bvalid_ever_seen;
        CData/*0:0*/ axi4_top_tb__DOT__rvalid_ever_seen;
        CData/*0:0*/ axi4_top_tb__DOT__write_burst_active;
        CData/*0:0*/ axi4_top_tb__DOT__read_burst_active;
        CData/*0:0*/ axi4_top_tb__DOT__aw_seen;
        CData/*0:0*/ axi4_top_tb__DOT__wlast_handshake_seen;
        CData/*0:0*/ axi4_top_tb__DOT__ever_saw_rvalid;
        CData/*0:0*/ axi4_top_tb__DOT__ar_activity_checked;
        CData/*0:0*/ axi4_top_tb__DOT__aw_activity_checked;
        CData/*0:0*/ axi4_top_tb__DOT__reset_checked;
        CData/*0:0*/ axi4_top_tb__DOT__interrupt_req_prev;
        CData/*0:0*/ axi4_top_tb__DOT__interrupt_ack_prev;
        CData/*7:0*/ axi4_top_tb__DOT__dut__DOT__axi_awlen;
        CData/*2:0*/ axi4_top_tb__DOT__dut__DOT__axi_awsize;
        CData/*1:0*/ axi4_top_tb__DOT__dut__DOT__axi_awburst;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__axi_awvalid;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__axi_awready;
        CData/*3:0*/ axi4_top_tb__DOT__dut__DOT__axi_wstrb;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__axi_wlast;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__axi_wvalid;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__axi_wready;
        CData/*1:0*/ axi4_top_tb__DOT__dut__DOT__axi_bresp;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__axi_bvalid;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__axi_bready;
        CData/*7:0*/ axi4_top_tb__DOT__dut__DOT__axi_arlen;
        CData/*2:0*/ axi4_top_tb__DOT__dut__DOT__axi_arsize;
        CData/*1:0*/ axi4_top_tb__DOT__dut__DOT__axi_arburst;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__axi_arvalid;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__axi_arready;
        CData/*1:0*/ axi4_top_tb__DOT__dut__DOT__axi_rresp;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__axi_rlast;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__axi_rvalid;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__axi_rready;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__interrupt_req;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__interrupt_ack;
        CData/*2:0*/ axi4_top_tb__DOT__dut__DOT__master__DOT__state;
        CData/*2:0*/ axi4_top_tb__DOT__dut__DOT__master__DOT__next_state;
        CData/*7:0*/ axi4_top_tb__DOT__dut__DOT__master__DOT__write_count;
        CData/*7:0*/ axi4_top_tb__DOT__dut__DOT__master__DOT__write_length;
        CData/*2:0*/ axi4_top_tb__DOT__dut__DOT__master__DOT__write_size;
        CData/*1:0*/ axi4_top_tb__DOT__dut__DOT__master__DOT__write_burst;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__master__DOT__write_in_progress;
        CData/*7:0*/ axi4_top_tb__DOT__dut__DOT__master__DOT__read_count;
        CData/*7:0*/ axi4_top_tb__DOT__dut__DOT__master__DOT__read_length;
        CData/*2:0*/ axi4_top_tb__DOT__dut__DOT__master__DOT__read_size;
        CData/*1:0*/ axi4_top_tb__DOT__dut__DOT__master__DOT__read_burst;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__master__DOT__read_in_progress;
        CData/*7:0*/ axi4_top_tb__DOT__dut__DOT__slave__DOT__write_len;
        CData/*2:0*/ axi4_top_tb__DOT__dut__DOT__slave__DOT__write_size;
    };
    struct {
        CData/*1:0*/ axi4_top_tb__DOT__dut__DOT__slave__DOT__write_burst;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr_accepted;
        CData/*7:0*/ axi4_top_tb__DOT__dut__DOT__slave__DOT__write_count;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__slave__DOT__write_in_progress;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__slave__DOT__write_data_accepted;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_pending;
        CData/*0:0*/ axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_ready;
        CData/*1:0*/ axi4_top_tb__DOT__dut__DOT__interrupt_ctrl__DOT__state;
        CData/*1:0*/ axi4_top_tb__DOT__dut__DOT__interrupt_ctrl__DOT__next_state;
        CData/*0:0*/ __VstlFirstIteration;
        CData/*0:0*/ __Vtrigprevexpr___TOP__axi4_top_tb__DOT__clk__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__axi4_top_tb__DOT__resetn__0;
        CData/*0:0*/ __VactContinue;
        IData/*31:0*/ axi4_top_tb__DOT__write_transaction_count;
        IData/*31:0*/ axi4_top_tb__DOT__read_transaction_count;
        IData/*31:0*/ axi4_top_tb__DOT__write_addr_handshake_count;
        IData/*31:0*/ axi4_top_tb__DOT__read_addr_handshake_count;
        IData/*31:0*/ axi4_top_tb__DOT__write_resp_handshake_count;
        IData/*31:0*/ axi4_top_tb__DOT__read_data_handshake_count;
        IData/*31:0*/ axi4_top_tb__DOT__assertion_pass_count;
        IData/*31:0*/ axi4_top_tb__DOT__assertion_fail_count;
        IData/*31:0*/ axi4_top_tb__DOT__warmup_cycles;
        IData/*31:0*/ axi4_top_tb__DOT__total_aw_handshakes;
        IData/*31:0*/ axi4_top_tb__DOT__total_w_handshakes;
        IData/*31:0*/ axi4_top_tb__DOT__total_b_handshakes;
        IData/*31:0*/ axi4_top_tb__DOT__total_ar_handshakes;
        IData/*31:0*/ axi4_top_tb__DOT__total_r_handshakes;
        IData/*31:0*/ axi4_top_tb__DOT__total_wlast_seen;
        IData/*31:0*/ axi4_top_tb__DOT__total_rlast_seen;
        IData/*31:0*/ axi4_top_tb__DOT__write_beat_count;
        IData/*31:0*/ axi4_top_tb__DOT__write_burst_len;
        IData/*31:0*/ axi4_top_tb__DOT__read_beat_count;
        IData/*31:0*/ axi4_top_tb__DOT__read_burst_len;
        IData/*31:0*/ axi4_top_tb__DOT__aw_timeout_counter;
        IData/*31:0*/ axi4_top_tb__DOT__w_timeout_counter;
        IData/*31:0*/ axi4_top_tb__DOT__pending_ar_count;
        IData/*31:0*/ axi4_top_tb__DOT__ar_no_data_counter;
        IData/*31:0*/ axi4_top_tb__DOT__ar_activity_counter;
        IData/*31:0*/ axi4_top_tb__DOT__aw_activity_counter;
        IData/*31:0*/ axi4_top_tb__DOT__write_addr_low_count;
        IData/*31:0*/ axi4_top_tb__DOT__write_addr_mid_count;
        IData/*31:0*/ axi4_top_tb__DOT__write_addr_high_count;
        IData/*31:0*/ axi4_top_tb__DOT__write_burst_fixed_count;
        IData/*31:0*/ axi4_top_tb__DOT__write_burst_incr_count;
        IData/*31:0*/ axi4_top_tb__DOT__write_burst_wrap_count;
        IData/*31:0*/ axi4_top_tb__DOT__write_size_byte_count;
        IData/*31:0*/ axi4_top_tb__DOT__write_size_halfword_count;
        IData/*31:0*/ axi4_top_tb__DOT__write_size_word_count;
        IData/*31:0*/ axi4_top_tb__DOT__write_resp_okay_count;
        IData/*31:0*/ axi4_top_tb__DOT__write_resp_exokay_count;
        IData/*31:0*/ axi4_top_tb__DOT__write_resp_slverr_count;
        IData/*31:0*/ axi4_top_tb__DOT__write_resp_decerr_count;
        IData/*31:0*/ axi4_top_tb__DOT__read_addr_low_count;
        IData/*31:0*/ axi4_top_tb__DOT__read_addr_mid_count;
        IData/*31:0*/ axi4_top_tb__DOT__read_addr_high_count;
        IData/*31:0*/ axi4_top_tb__DOT__read_burst_fixed_count;
        IData/*31:0*/ axi4_top_tb__DOT__read_burst_incr_count;
        IData/*31:0*/ axi4_top_tb__DOT__read_burst_wrap_count;
        IData/*31:0*/ axi4_top_tb__DOT__read_resp_okay_count;
        IData/*31:0*/ axi4_top_tb__DOT__read_resp_exokay_count;
        IData/*31:0*/ axi4_top_tb__DOT__read_resp_slverr_count;
        IData/*31:0*/ axi4_top_tb__DOT__read_resp_decerr_count;
        IData/*31:0*/ axi4_top_tb__DOT__aw_handshake_valid_ready_count;
        IData/*31:0*/ axi4_top_tb__DOT__w_handshake_valid_ready_count;
    };
    struct {
        IData/*31:0*/ axi4_top_tb__DOT__b_handshake_valid_ready_count;
        IData/*31:0*/ axi4_top_tb__DOT__ar_handshake_valid_ready_count;
        IData/*31:0*/ axi4_top_tb__DOT__r_handshake_valid_ready_count;
        IData/*31:0*/ axi4_top_tb__DOT__interrupt_idle_count;
        IData/*31:0*/ axi4_top_tb__DOT__interrupt_pending_count;
        IData/*31:0*/ axi4_top_tb__DOT__interrupt_acknowledged_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__axi_awaddr;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__axi_wdata;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__axi_araddr;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__axi_rdata;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__master__DOT__write_base_addr;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__master__DOT__read_base_addr;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__slave__DOT__current_addr;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__slave__DOT__addr_offset;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__slave__DOT__byte_size;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__slave__DOT__wrap_boundary;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__slave__DOT__aligned_addr;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__slave__DOT__mem_addr;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__slave__DOT__unnamedblk1__DOT__i;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__slave__DOT__unnamedblk2__DOT__read_addr;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_fixed_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_incr_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_wrap_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__single_beat_write_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__multi_beat_write_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__single_beat_read_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__multi_beat_read_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_okay_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_exokay_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_slverr_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_decerr_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__aw_handshake_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__w_handshake_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__b_handshake_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__ar_handshake_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__r_handshake_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region0_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region1_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region2_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region3_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_out_of_range_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wstrb_full_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wstrb_partial_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wlast_asserted_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__rlast_asserted_count;
        IData/*31:0*/ axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__unnamedblk1__DOT__bins_hit;
        IData/*31:0*/ __VactIterCount;
        VlUnpacked<IData/*31:0*/, 256> axi4_top_tb__DOT__dut__DOT__slave__DOT__memory;
        VlUnpacked<CData/*0:0*/, 3> __Vm_traceActivity;
    };
    double axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__unnamedblk1__DOT__coverage_pct;
    VlDelayScheduler __VdlySched;
    VlTriggerVec<1> __VstlTriggered;
    VlTriggerVec<3> __VactTriggered;
    VlTriggerVec<3> __VnbaTriggered;

    // INTERNAL VARIABLES
    Vaxi4_top_tb__Syms* const vlSymsp;

    // CONSTRUCTORS
    Vaxi4_top_tb___024root(Vaxi4_top_tb__Syms* symsp, const char* v__name);
    ~Vaxi4_top_tb___024root();
    VL_UNCOPYABLE(Vaxi4_top_tb___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
