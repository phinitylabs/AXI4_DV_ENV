// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vaxi4_top_tb.h for the primary calling header

#include "Vaxi4_top_tb__pch.h"
#include "Vaxi4_top_tb___024root.h"

VL_ATTR_COLD void Vaxi4_top_tb___024root___eval_static__TOP(Vaxi4_top_tb___024root* vlSelf);

VL_ATTR_COLD void Vaxi4_top_tb___024root___eval_static(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval_static\n"); );
    // Body
    Vaxi4_top_tb___024root___eval_static__TOP(vlSelf);
    vlSelf->__Vm_traceActivity[2U] = 1U;
    vlSelf->__Vm_traceActivity[1U] = 1U;
    vlSelf->__Vm_traceActivity[0U] = 1U;
}

VL_ATTR_COLD void Vaxi4_top_tb___024root___eval_static__TOP(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval_static__TOP\n"); );
    // Body
    vlSelf->axi4_top_tb__DOT__write_transaction_count = 0U;
    vlSelf->axi4_top_tb__DOT__read_transaction_count = 0U;
    vlSelf->axi4_top_tb__DOT__write_addr_handshake_count = 0U;
    vlSelf->axi4_top_tb__DOT__read_addr_handshake_count = 0U;
    vlSelf->axi4_top_tb__DOT__write_resp_handshake_count = 0U;
    vlSelf->axi4_top_tb__DOT__read_data_handshake_count = 0U;
    vlSelf->axi4_top_tb__DOT__assertion_pass_count = 0U;
    vlSelf->axi4_top_tb__DOT__assertion_fail_count = 0U;
    vlSelf->axi4_top_tb__DOT__warmup_cycles = 0U;
    vlSelf->axi4_top_tb__DOT__total_aw_handshakes = 0U;
    vlSelf->axi4_top_tb__DOT__total_w_handshakes = 0U;
    vlSelf->axi4_top_tb__DOT__total_b_handshakes = 0U;
    vlSelf->axi4_top_tb__DOT__total_ar_handshakes = 0U;
    vlSelf->axi4_top_tb__DOT__total_r_handshakes = 0U;
    vlSelf->axi4_top_tb__DOT__total_wlast_seen = 0U;
    vlSelf->axi4_top_tb__DOT__total_rlast_seen = 0U;
    vlSelf->axi4_top_tb__DOT__awvalid_ever_seen = 0U;
    vlSelf->axi4_top_tb__DOT__arvalid_ever_seen = 0U;
    vlSelf->axi4_top_tb__DOT__wvalid_ever_seen = 0U;
    vlSelf->axi4_top_tb__DOT__bvalid_ever_seen = 0U;
    vlSelf->axi4_top_tb__DOT__rvalid_ever_seen = 0U;
    vlSelf->axi4_top_tb__DOT__write_beat_count = 0U;
    vlSelf->axi4_top_tb__DOT__write_burst_len = 0U;
    vlSelf->axi4_top_tb__DOT__write_burst_active = 0U;
    vlSelf->axi4_top_tb__DOT__read_beat_count = 0U;
    vlSelf->axi4_top_tb__DOT__read_burst_len = 0U;
    vlSelf->axi4_top_tb__DOT__read_burst_active = 0U;
    vlSelf->axi4_top_tb__DOT__aw_seen = 0U;
    vlSelf->axi4_top_tb__DOT__wlast_handshake_seen = 0U;
    vlSelf->axi4_top_tb__DOT__aw_timeout_counter = 0U;
    vlSelf->axi4_top_tb__DOT__w_timeout_counter = 0U;
    vlSelf->axi4_top_tb__DOT__pending_ar_count = 0U;
    vlSelf->axi4_top_tb__DOT__ar_no_data_counter = 0U;
    vlSelf->axi4_top_tb__DOT__ever_saw_rvalid = 0U;
    vlSelf->axi4_top_tb__DOT__ar_activity_counter = 0U;
    vlSelf->axi4_top_tb__DOT__aw_activity_counter = 0U;
    vlSelf->axi4_top_tb__DOT__ar_activity_checked = 0U;
    vlSelf->axi4_top_tb__DOT__aw_activity_checked = 0U;
    vlSelf->axi4_top_tb__DOT__reset_checked = 0U;
    vlSelf->axi4_top_tb__DOT__write_addr_low_count = 0U;
    vlSelf->axi4_top_tb__DOT__write_addr_mid_count = 0U;
    vlSelf->axi4_top_tb__DOT__write_addr_high_count = 0U;
    vlSelf->axi4_top_tb__DOT__write_burst_fixed_count = 0U;
    vlSelf->axi4_top_tb__DOT__write_burst_incr_count = 0U;
    vlSelf->axi4_top_tb__DOT__write_burst_wrap_count = 0U;
    vlSelf->axi4_top_tb__DOT__write_size_byte_count = 0U;
    vlSelf->axi4_top_tb__DOT__write_size_halfword_count = 0U;
    vlSelf->axi4_top_tb__DOT__write_size_word_count = 0U;
    vlSelf->axi4_top_tb__DOT__write_resp_okay_count = 0U;
    vlSelf->axi4_top_tb__DOT__write_resp_exokay_count = 0U;
    vlSelf->axi4_top_tb__DOT__write_resp_slverr_count = 0U;
    vlSelf->axi4_top_tb__DOT__write_resp_decerr_count = 0U;
    vlSelf->axi4_top_tb__DOT__read_addr_low_count = 0U;
    vlSelf->axi4_top_tb__DOT__read_addr_mid_count = 0U;
    vlSelf->axi4_top_tb__DOT__read_addr_high_count = 0U;
    vlSelf->axi4_top_tb__DOT__read_burst_fixed_count = 0U;
    vlSelf->axi4_top_tb__DOT__read_burst_incr_count = 0U;
    vlSelf->axi4_top_tb__DOT__read_burst_wrap_count = 0U;
    vlSelf->axi4_top_tb__DOT__read_resp_okay_count = 0U;
    vlSelf->axi4_top_tb__DOT__read_resp_exokay_count = 0U;
    vlSelf->axi4_top_tb__DOT__read_resp_slverr_count = 0U;
    vlSelf->axi4_top_tb__DOT__read_resp_decerr_count = 0U;
    vlSelf->axi4_top_tb__DOT__aw_handshake_valid_ready_count = 0U;
    vlSelf->axi4_top_tb__DOT__w_handshake_valid_ready_count = 0U;
    vlSelf->axi4_top_tb__DOT__b_handshake_valid_ready_count = 0U;
    vlSelf->axi4_top_tb__DOT__ar_handshake_valid_ready_count = 0U;
    vlSelf->axi4_top_tb__DOT__r_handshake_valid_ready_count = 0U;
    vlSelf->axi4_top_tb__DOT__interrupt_idle_count = 0U;
    vlSelf->axi4_top_tb__DOT__interrupt_pending_count = 0U;
    vlSelf->axi4_top_tb__DOT__interrupt_acknowledged_count = 0U;
    vlSelf->axi4_top_tb__DOT__interrupt_req_prev = 0U;
    vlSelf->axi4_top_tb__DOT__interrupt_ack_prev = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_fixed_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_incr_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_wrap_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__single_beat_write_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__multi_beat_write_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__single_beat_read_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__multi_beat_read_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_okay_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_exokay_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_slverr_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_decerr_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__aw_handshake_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__w_handshake_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__b_handshake_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__ar_handshake_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__r_handshake_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region0_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region1_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region2_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region3_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_out_of_range_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wstrb_full_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wstrb_partial_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wlast_asserted_count = 0U;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__rlast_asserted_count = 0U;
}

VL_ATTR_COLD void Vaxi4_top_tb___024root___eval_final__TOP(Vaxi4_top_tb___024root* vlSelf);

VL_ATTR_COLD void Vaxi4_top_tb___024root___eval_final(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval_final\n"); );
    // Body
    Vaxi4_top_tb___024root___eval_final__TOP(vlSelf);
    vlSelf->__Vm_traceActivity[2U] = 1U;
    vlSelf->__Vm_traceActivity[1U] = 1U;
    vlSelf->__Vm_traceActivity[0U] = 1U;
}

VL_ATTR_COLD void Vaxi4_top_tb___024root___eval_final__TOP(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval_final__TOP\n"); );
    // Init
    IData/*31:0*/ __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__Vfuncout;
    __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__Vfuncout = 0;
    IData/*31:0*/ __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit;
    __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit = 0;
    // Body
    VL_WRITEF("==========================================\nFinal Report\n==========================================\nTransactions: Write=%0d, Read=%0d\nHandshakes: AW=%0d, W=%0d, B=%0d, AR=%0d, R=%0d\nLAST signals: WLAST=%0d, RLAST=%0d\nChecks: pass_count=%0d, error_count=%0d\n==========================================\n",
              32,vlSelf->axi4_top_tb__DOT__write_transaction_count,
              32,vlSelf->axi4_top_tb__DOT__read_transaction_count,
              32,vlSelf->axi4_top_tb__DOT__total_aw_handshakes,
              32,vlSelf->axi4_top_tb__DOT__total_w_handshakes,
              32,vlSelf->axi4_top_tb__DOT__total_b_handshakes,
              32,vlSelf->axi4_top_tb__DOT__total_ar_handshakes,
              32,vlSelf->axi4_top_tb__DOT__total_r_handshakes,
              32,vlSelf->axi4_top_tb__DOT__total_wlast_seen,
              32,vlSelf->axi4_top_tb__DOT__total_rlast_seen,
              32,vlSelf->axi4_top_tb__DOT__assertion_pass_count,
              32,vlSelf->axi4_top_tb__DOT__assertion_fail_count);
    __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit = 0U;
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__aw_handshake_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__w_handshake_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__b_handshake_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__ar_handshake_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__r_handshake_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_fixed_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_incr_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_wrap_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__single_beat_write_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__multi_beat_write_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__single_beat_read_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__multi_beat_read_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_okay_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_exokay_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_slverr_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_decerr_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region0_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region1_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region2_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region3_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_out_of_range_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wstrb_full_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wstrb_partial_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wlast_asserted_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    if ((0U < vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__rlast_asserted_count)) {
        __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit 
            = ((IData)(1U) + __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit);
    }
    __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__Vfuncout 
        = __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__bins_hit;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__unnamedblk1__DOT__bins_hit 
        = __Vfunc_axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__get_bins_hit__0__Vfuncout;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__unnamedblk1__DOT__coverage_pct 
        = ((100.0 * VL_ISTOR_D_I(32, vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__unnamedblk1__DOT__bins_hit)) 
           / 24.0);
    VL_WRITEF("\n============================================================\nFUNCTIONAL COVERAGE REPORT (Fixed Coverpoints)\n============================================================\n\nChannel Coverage:\n  AW handshakes: %0#\n  W  handshakes: %0#\n  B  handshakes: %0#\n  AR handshakes: %0#\n  R  handshakes: %0#\n\nBurst Type Coverage:\n  FIXED: %0#, INCR: %0#, WRAP: %0#\n\nBurst Length Coverage:\n  Single-beat writes: %0#, Multi-beat writes: %0#\n  Single-beat reads: %0#, Multi-beat reads: %0#\n\nResponse Code Coverage:\n",
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__aw_handshake_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__w_handshake_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__b_handshake_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__ar_handshake_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__r_handshake_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_fixed_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_incr_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_wrap_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__single_beat_write_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__multi_beat_write_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__single_beat_read_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__multi_beat_read_count);
    VL_WRITEF("  OKAY: %0#, EXOKAY: %0#, SLVERR: %0#, DECERR: %0#\n\nAddress Range Coverage:\n  Region0 (0x000-0x0FF): %0#\n  Region1 (0x100-0x1FF): %0#\n  Region2 (0x200-0x2FF): %0#\n  Region3 (0x300-0x3FF): %0#\n  Out of range (>0x3FF): %0#\n\nWrite Strobe Coverage:\n  Full (4'hF): %0#, Partial: %0#\n\nLAST Signal Coverage:\n  WLAST asserted: %0#, RLAST asserted: %0#\n\n============================================================\nCOVERAGE SUMMARY: %0d/24 bins hit (%.1f%%)\n",
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_okay_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_exokay_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_slverr_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_decerr_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region0_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region1_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region2_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region3_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_out_of_range_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wstrb_full_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wstrb_partial_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wlast_asserted_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__rlast_asserted_count,
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__unnamedblk1__DOT__bins_hit,
              64,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__unnamedblk1__DOT__coverage_pct);
    VL_WRITEF("============================================================\n\nCOVERAGE_BINS_HIT=%0d\nCOVERAGE_BINS_TOTAL=24\nCOVERAGE_PERCENT=%.1f\n",
              32,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__unnamedblk1__DOT__bins_hit,
              64,vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__unnamedblk1__DOT__coverage_pct);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vaxi4_top_tb___024root___dump_triggers__stl(Vaxi4_top_tb___024root* vlSelf);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vaxi4_top_tb___024root___eval_phase__stl(Vaxi4_top_tb___024root* vlSelf);

VL_ATTR_COLD void Vaxi4_top_tb___024root___eval_settle(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval_settle\n"); );
    // Init
    IData/*31:0*/ __VstlIterCount;
    CData/*0:0*/ __VstlContinue;
    // Body
    __VstlIterCount = 0U;
    vlSelf->__VstlFirstIteration = 1U;
    __VstlContinue = 1U;
    while (__VstlContinue) {
        if (VL_UNLIKELY((0x64U < __VstlIterCount))) {
#ifdef VL_DEBUG
            Vaxi4_top_tb___024root___dump_triggers__stl(vlSelf);
#endif
            VL_FATAL_MT("verif/axi4_top_tb.sv", 8, "", "Settle region did not converge.");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        __VstlContinue = 0U;
        if (Vaxi4_top_tb___024root___eval_phase__stl(vlSelf)) {
            __VstlContinue = 1U;
        }
        vlSelf->__VstlFirstIteration = 0U;
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vaxi4_top_tb___024root___dump_triggers__stl(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(vlSelf->__VstlTriggered.any())))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelf->__VstlTriggered.word(0U))) {
        VL_DBG_MSGF("         'stl' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

extern const VlUnpacked<CData/*1:0*/, 8> Vaxi4_top_tb__ConstPool__TABLE_h166b8ba2_0;

VL_ATTR_COLD void Vaxi4_top_tb___024root___stl_sequent__TOP__0(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___stl_sequent__TOP__0\n"); );
    // Init
    CData/*2:0*/ __Vtableidx3;
    __Vtableidx3 = 0;
    // Body
    __Vtableidx3 = (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_req) 
                     << 2U) | (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ctrl__DOT__state));
    vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ctrl__DOT__next_state 
        = Vaxi4_top_tb__ConstPool__TABLE_h166b8ba2_0
        [__Vtableidx3];
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__next_state 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__state;
    if ((0U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__state))) {
        vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__next_state = 0U;
    } else if ((1U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__state))) {
        if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awready))) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__next_state = 2U;
        }
    } else if ((2U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__state))) {
        if ((((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid) 
              & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wready)) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wlast))) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__next_state = 3U;
        }
    } else if ((3U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__state))) {
        if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bready))) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__next_state = 0U;
        }
    } else if ((4U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__state))) {
        if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arready))) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__next_state = 5U;
        }
    } else if ((5U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__state))) {
        if ((((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid) 
              & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready)) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rlast))) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__next_state = 0U;
        }
    }
}

VL_ATTR_COLD void Vaxi4_top_tb___024root___eval_stl(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval_stl\n"); );
    // Body
    if ((1ULL & vlSelf->__VstlTriggered.word(0U))) {
        Vaxi4_top_tb___024root___stl_sequent__TOP__0(vlSelf);
        vlSelf->__Vm_traceActivity[2U] = 1U;
        vlSelf->__Vm_traceActivity[1U] = 1U;
        vlSelf->__Vm_traceActivity[0U] = 1U;
    }
}

VL_ATTR_COLD void Vaxi4_top_tb___024root___eval_triggers__stl(Vaxi4_top_tb___024root* vlSelf);

VL_ATTR_COLD bool Vaxi4_top_tb___024root___eval_phase__stl(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval_phase__stl\n"); );
    // Init
    CData/*0:0*/ __VstlExecute;
    // Body
    Vaxi4_top_tb___024root___eval_triggers__stl(vlSelf);
    __VstlExecute = vlSelf->__VstlTriggered.any();
    if (__VstlExecute) {
        Vaxi4_top_tb___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vaxi4_top_tb___024root___dump_triggers__act(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(vlSelf->__VactTriggered.any())))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelf->__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 0 is active: @(posedge axi4_top_tb.clk)\n");
    }
    if ((2ULL & vlSelf->__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 1 is active: @(posedge axi4_top_tb.clk or negedge axi4_top_tb.resetn)\n");
    }
    if ((4ULL & vlSelf->__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 2 is active: @([true] __VdlySched.awaitingCurrentTime())\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void Vaxi4_top_tb___024root___dump_triggers__nba(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___dump_triggers__nba\n"); );
    // Body
    if ((1U & (~ (IData)(vlSelf->__VnbaTriggered.any())))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelf->__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 0 is active: @(posedge axi4_top_tb.clk)\n");
    }
    if ((2ULL & vlSelf->__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 1 is active: @(posedge axi4_top_tb.clk or negedge axi4_top_tb.resetn)\n");
    }
    if ((4ULL & vlSelf->__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 2 is active: @([true] __VdlySched.awaitingCurrentTime())\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vaxi4_top_tb___024root___ctor_var_reset(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___ctor_var_reset\n"); );
    // Body
    vlSelf->axi4_top_tb__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__resetn = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__write_transaction_count = 0;
    vlSelf->axi4_top_tb__DOT__read_transaction_count = 0;
    vlSelf->axi4_top_tb__DOT__write_addr_handshake_count = 0;
    vlSelf->axi4_top_tb__DOT__read_addr_handshake_count = 0;
    vlSelf->axi4_top_tb__DOT__write_resp_handshake_count = 0;
    vlSelf->axi4_top_tb__DOT__read_data_handshake_count = 0;
    vlSelf->axi4_top_tb__DOT__assertion_pass_count = 0;
    vlSelf->axi4_top_tb__DOT__assertion_fail_count = 0;
    vlSelf->axi4_top_tb__DOT__warmup_cycles = 0;
    vlSelf->axi4_top_tb__DOT__awvalid_prev = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__arvalid_prev = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__wvalid_prev = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__bvalid_prev = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__rvalid_prev = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__awready_prev = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__arready_prev = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__wready_prev = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__bready_prev = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__rready_prev = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__total_aw_handshakes = 0;
    vlSelf->axi4_top_tb__DOT__total_w_handshakes = 0;
    vlSelf->axi4_top_tb__DOT__total_b_handshakes = 0;
    vlSelf->axi4_top_tb__DOT__total_ar_handshakes = 0;
    vlSelf->axi4_top_tb__DOT__total_r_handshakes = 0;
    vlSelf->axi4_top_tb__DOT__total_wlast_seen = 0;
    vlSelf->axi4_top_tb__DOT__total_rlast_seen = 0;
    vlSelf->axi4_top_tb__DOT__awvalid_ever_seen = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__arvalid_ever_seen = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__wvalid_ever_seen = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__bvalid_ever_seen = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__rvalid_ever_seen = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__write_beat_count = 0;
    vlSelf->axi4_top_tb__DOT__write_burst_len = 0;
    vlSelf->axi4_top_tb__DOT__write_burst_active = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__read_beat_count = 0;
    vlSelf->axi4_top_tb__DOT__read_burst_len = 0;
    vlSelf->axi4_top_tb__DOT__read_burst_active = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__aw_seen = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__wlast_handshake_seen = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__aw_timeout_counter = 0;
    vlSelf->axi4_top_tb__DOT__w_timeout_counter = 0;
    vlSelf->axi4_top_tb__DOT__pending_ar_count = 0;
    vlSelf->axi4_top_tb__DOT__ar_no_data_counter = 0;
    vlSelf->axi4_top_tb__DOT__ever_saw_rvalid = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__ar_activity_counter = 0;
    vlSelf->axi4_top_tb__DOT__aw_activity_counter = 0;
    vlSelf->axi4_top_tb__DOT__ar_activity_checked = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__aw_activity_checked = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__reset_checked = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__write_addr_low_count = 0;
    vlSelf->axi4_top_tb__DOT__write_addr_mid_count = 0;
    vlSelf->axi4_top_tb__DOT__write_addr_high_count = 0;
    vlSelf->axi4_top_tb__DOT__write_burst_fixed_count = 0;
    vlSelf->axi4_top_tb__DOT__write_burst_incr_count = 0;
    vlSelf->axi4_top_tb__DOT__write_burst_wrap_count = 0;
    vlSelf->axi4_top_tb__DOT__write_size_byte_count = 0;
    vlSelf->axi4_top_tb__DOT__write_size_halfword_count = 0;
    vlSelf->axi4_top_tb__DOT__write_size_word_count = 0;
    vlSelf->axi4_top_tb__DOT__write_resp_okay_count = 0;
    vlSelf->axi4_top_tb__DOT__write_resp_exokay_count = 0;
    vlSelf->axi4_top_tb__DOT__write_resp_slverr_count = 0;
    vlSelf->axi4_top_tb__DOT__write_resp_decerr_count = 0;
    vlSelf->axi4_top_tb__DOT__read_addr_low_count = 0;
    vlSelf->axi4_top_tb__DOT__read_addr_mid_count = 0;
    vlSelf->axi4_top_tb__DOT__read_addr_high_count = 0;
    vlSelf->axi4_top_tb__DOT__read_burst_fixed_count = 0;
    vlSelf->axi4_top_tb__DOT__read_burst_incr_count = 0;
    vlSelf->axi4_top_tb__DOT__read_burst_wrap_count = 0;
    vlSelf->axi4_top_tb__DOT__read_resp_okay_count = 0;
    vlSelf->axi4_top_tb__DOT__read_resp_exokay_count = 0;
    vlSelf->axi4_top_tb__DOT__read_resp_slverr_count = 0;
    vlSelf->axi4_top_tb__DOT__read_resp_decerr_count = 0;
    vlSelf->axi4_top_tb__DOT__aw_handshake_valid_ready_count = 0;
    vlSelf->axi4_top_tb__DOT__w_handshake_valid_ready_count = 0;
    vlSelf->axi4_top_tb__DOT__b_handshake_valid_ready_count = 0;
    vlSelf->axi4_top_tb__DOT__ar_handshake_valid_ready_count = 0;
    vlSelf->axi4_top_tb__DOT__r_handshake_valid_ready_count = 0;
    vlSelf->axi4_top_tb__DOT__interrupt_idle_count = 0;
    vlSelf->axi4_top_tb__DOT__interrupt_pending_count = 0;
    vlSelf->axi4_top_tb__DOT__interrupt_acknowledged_count = 0;
    vlSelf->axi4_top_tb__DOT__interrupt_req_prev = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__interrupt_ack_prev = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr = VL_RAND_RESET_I(32);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awlen = VL_RAND_RESET_I(8);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awsize = VL_RAND_RESET_I(3);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awburst = VL_RAND_RESET_I(2);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awready = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wdata = VL_RAND_RESET_I(32);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wstrb = VL_RAND_RESET_I(4);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wlast = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wready = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bresp = VL_RAND_RESET_I(2);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bready = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_araddr = VL_RAND_RESET_I(32);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arlen = VL_RAND_RESET_I(8);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arsize = VL_RAND_RESET_I(3);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arburst = VL_RAND_RESET_I(2);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arready = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rdata = VL_RAND_RESET_I(32);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rresp = VL_RAND_RESET_I(2);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rlast = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_req = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ack = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__state = VL_RAND_RESET_I(3);
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__next_state = VL_RAND_RESET_I(3);
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_count = VL_RAND_RESET_I(8);
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_base_addr = VL_RAND_RESET_I(32);
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_length = VL_RAND_RESET_I(8);
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_size = VL_RAND_RESET_I(3);
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_burst = VL_RAND_RESET_I(2);
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_in_progress = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_count = VL_RAND_RESET_I(8);
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_base_addr = VL_RAND_RESET_I(32);
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_length = VL_RAND_RESET_I(8);
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_size = VL_RAND_RESET_I(3);
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_burst = VL_RAND_RESET_I(2);
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_in_progress = VL_RAND_RESET_I(1);
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__memory[__Vi0] = VL_RAND_RESET_I(32);
    }
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr = VL_RAND_RESET_I(32);
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_len = VL_RAND_RESET_I(8);
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_size = VL_RAND_RESET_I(3);
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_burst = VL_RAND_RESET_I(2);
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr_accepted = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_count = VL_RAND_RESET_I(8);
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_in_progress = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_data_accepted = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_pending = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_ready = VL_RAND_RESET_I(1);
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__current_addr = VL_RAND_RESET_I(32);
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__addr_offset = VL_RAND_RESET_I(32);
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__byte_size = VL_RAND_RESET_I(32);
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__wrap_boundary = VL_RAND_RESET_I(32);
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__aligned_addr = VL_RAND_RESET_I(32);
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__mem_addr = VL_RAND_RESET_I(32);
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__unnamedblk1__DOT__i = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__unnamedblk2__DOT__read_addr = VL_RAND_RESET_I(32);
    vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ctrl__DOT__state = VL_RAND_RESET_I(2);
    vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ctrl__DOT__next_state = VL_RAND_RESET_I(2);
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_fixed_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_incr_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_wrap_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__single_beat_write_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__multi_beat_write_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__single_beat_read_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__multi_beat_read_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_okay_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_exokay_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_slverr_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_decerr_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__aw_handshake_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__w_handshake_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__b_handshake_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__ar_handshake_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__r_handshake_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region0_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region1_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region2_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region3_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_out_of_range_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wstrb_full_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wstrb_partial_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wlast_asserted_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__rlast_asserted_count = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__unnamedblk1__DOT__bins_hit = 0;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__unnamedblk1__DOT__coverage_pct = 0;
    vlSelf->__Vtrigprevexpr___TOP__axi4_top_tb__DOT__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__axi4_top_tb__DOT__resetn__0 = VL_RAND_RESET_I(1);
    for (int __Vi0 = 0; __Vi0 < 3; ++__Vi0) {
        vlSelf->__Vm_traceActivity[__Vi0] = 0;
    }
}
