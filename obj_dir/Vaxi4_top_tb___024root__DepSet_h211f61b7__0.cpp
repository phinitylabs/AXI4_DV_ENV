// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vaxi4_top_tb.h for the primary calling header

#include "Vaxi4_top_tb__pch.h"
#include "Vaxi4_top_tb___024root.h"

VL_ATTR_COLD void Vaxi4_top_tb___024root___eval_initial__TOP(Vaxi4_top_tb___024root* vlSelf);
VlCoroutine Vaxi4_top_tb___024root___eval_initial__TOP__Vtiming__0(Vaxi4_top_tb___024root* vlSelf);
VlCoroutine Vaxi4_top_tb___024root___eval_initial__TOP__Vtiming__1(Vaxi4_top_tb___024root* vlSelf);

void Vaxi4_top_tb___024root___eval_initial(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval_initial\n"); );
    // Body
    Vaxi4_top_tb___024root___eval_initial__TOP(vlSelf);
    Vaxi4_top_tb___024root___eval_initial__TOP__Vtiming__0(vlSelf);
    Vaxi4_top_tb___024root___eval_initial__TOP__Vtiming__1(vlSelf);
    vlSelf->__Vtrigprevexpr___TOP__axi4_top_tb__DOT__clk__0 
        = vlSelf->axi4_top_tb__DOT__clk;
    vlSelf->__Vtrigprevexpr___TOP__axi4_top_tb__DOT__resetn__0 
        = vlSelf->axi4_top_tb__DOT__resetn;
}

VL_INLINE_OPT VlCoroutine Vaxi4_top_tb___024root___eval_initial__TOP__Vtiming__0(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval_initial__TOP__Vtiming__0\n"); );
    // Body
    vlSelf->axi4_top_tb__DOT__clk = 0U;
    while (1U) {
        co_await vlSelf->__VdlySched.delay(0x1388ULL, 
                                           nullptr, 
                                           "verif/axi4_top_tb.sv", 
                                           17);
        vlSelf->axi4_top_tb__DOT__clk = (1U & (~ (IData)(vlSelf->axi4_top_tb__DOT__clk)));
    }
}

VL_INLINE_OPT VlCoroutine Vaxi4_top_tb___024root___eval_initial__TOP__Vtiming__1(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval_initial__TOP__Vtiming__1\n"); );
    // Body
    vlSelf->axi4_top_tb__DOT__resetn = 0U;
    co_await vlSelf->__VdlySched.delay(0x186a0ULL, 
                                       nullptr, "verif/axi4_top_tb.sv", 
                                       23);
    vlSelf->axi4_top_tb__DOT__resetn = 1U;
    co_await vlSelf->__VdlySched.delay(0x989680ULL, 
                                       nullptr, "verif/axi4_top_tb.sv", 
                                       25);
    VL_WRITEF("==========================================\nSimulation Complete\n==========================================\nCoverage Summary:\n  Write Transactions: %0d\n  Read Transactions: %0d\n  Write Address Handshakes: %0d\n  Read Address Handshakes: %0d\n  Write Response Handshakes: %0d\n  Read Data Handshakes: %0d\n==========================================\n",
              32,vlSelf->axi4_top_tb__DOT__write_transaction_count,
              32,vlSelf->axi4_top_tb__DOT__read_transaction_count,
              32,vlSelf->axi4_top_tb__DOT__write_addr_handshake_count,
              32,vlSelf->axi4_top_tb__DOT__read_addr_handshake_count,
              32,vlSelf->axi4_top_tb__DOT__write_resp_handshake_count,
              32,vlSelf->axi4_top_tb__DOT__read_data_handshake_count);
    VL_FINISH_MT("verif/axi4_top_tb.sv", 37, "");
}

void Vaxi4_top_tb___024root___eval_act(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval_act\n"); );
}

extern const VlUnpacked<CData/*4:0*/, 128> Vaxi4_top_tb__ConstPool__TABLE_hc8079c3b_0;
extern const VlUnpacked<CData/*0:0*/, 128> Vaxi4_top_tb__ConstPool__TABLE_h0c95e6ed_0;
extern const VlUnpacked<CData/*0:0*/, 128> Vaxi4_top_tb__ConstPool__TABLE_h08698683_0;
extern const VlUnpacked<CData/*0:0*/, 128> Vaxi4_top_tb__ConstPool__TABLE_h2da5e280_0;
extern const VlUnpacked<CData/*0:0*/, 128> Vaxi4_top_tb__ConstPool__TABLE_h7f0673c1_0;
extern const VlUnpacked<CData/*0:0*/, 128> Vaxi4_top_tb__ConstPool__TABLE_ha332edba_0;

VL_INLINE_OPT void Vaxi4_top_tb___024root___nba_sequent__TOP__0(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___nba_sequent__TOP__0\n"); );
    // Init
    CData/*6:0*/ __Vtableidx1;
    __Vtableidx1 = 0;
    IData/*31:0*/ __Vdly__axi4_top_tb__DOT__warmup_cycles;
    __Vdly__axi4_top_tb__DOT__warmup_cycles = 0;
    CData/*0:0*/ __Vdly__axi4_top_tb__DOT__write_burst_active;
    __Vdly__axi4_top_tb__DOT__write_burst_active = 0;
    IData/*31:0*/ __Vdly__axi4_top_tb__DOT__write_burst_len;
    __Vdly__axi4_top_tb__DOT__write_burst_len = 0;
    IData/*31:0*/ __Vdly__axi4_top_tb__DOT__write_beat_count;
    __Vdly__axi4_top_tb__DOT__write_beat_count = 0;
    CData/*0:0*/ __Vdly__axi4_top_tb__DOT__read_burst_active;
    __Vdly__axi4_top_tb__DOT__read_burst_active = 0;
    IData/*31:0*/ __Vdly__axi4_top_tb__DOT__read_burst_len;
    __Vdly__axi4_top_tb__DOT__read_burst_len = 0;
    IData/*31:0*/ __Vdly__axi4_top_tb__DOT__read_beat_count;
    __Vdly__axi4_top_tb__DOT__read_beat_count = 0;
    CData/*0:0*/ __Vdly__axi4_top_tb__DOT__aw_seen;
    __Vdly__axi4_top_tb__DOT__aw_seen = 0;
    IData/*31:0*/ __Vdly__axi4_top_tb__DOT__aw_timeout_counter;
    __Vdly__axi4_top_tb__DOT__aw_timeout_counter = 0;
    CData/*0:0*/ __Vdly__axi4_top_tb__DOT__wlast_handshake_seen;
    __Vdly__axi4_top_tb__DOT__wlast_handshake_seen = 0;
    IData/*31:0*/ __Vdly__axi4_top_tb__DOT__w_timeout_counter;
    __Vdly__axi4_top_tb__DOT__w_timeout_counter = 0;
    IData/*31:0*/ __Vdly__axi4_top_tb__DOT__pending_ar_count;
    __Vdly__axi4_top_tb__DOT__pending_ar_count = 0;
    IData/*31:0*/ __Vdly__axi4_top_tb__DOT__ar_no_data_counter;
    __Vdly__axi4_top_tb__DOT__ar_no_data_counter = 0;
    IData/*31:0*/ __Vdly__axi4_top_tb__DOT__ar_activity_counter;
    __Vdly__axi4_top_tb__DOT__ar_activity_counter = 0;
    IData/*31:0*/ __Vdly__axi4_top_tb__DOT__aw_activity_counter;
    __Vdly__axi4_top_tb__DOT__aw_activity_counter = 0;
    IData/*31:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_slverr_count;
    __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_slverr_count = 0;
    IData/*31:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_exokay_count;
    __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_exokay_count = 0;
    IData/*31:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_okay_count;
    __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_okay_count = 0;
    IData/*31:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_decerr_count;
    __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_decerr_count = 0;
    // Body
    __Vdly__axi4_top_tb__DOT__warmup_cycles = vlSelf->axi4_top_tb__DOT__warmup_cycles;
    __Vdly__axi4_top_tb__DOT__aw_activity_counter = vlSelf->axi4_top_tb__DOT__aw_activity_counter;
    __Vdly__axi4_top_tb__DOT__ar_activity_counter = vlSelf->axi4_top_tb__DOT__ar_activity_counter;
    __Vdly__axi4_top_tb__DOT__w_timeout_counter = vlSelf->axi4_top_tb__DOT__w_timeout_counter;
    __Vdly__axi4_top_tb__DOT__wlast_handshake_seen 
        = vlSelf->axi4_top_tb__DOT__wlast_handshake_seen;
    __Vdly__axi4_top_tb__DOT__aw_timeout_counter = vlSelf->axi4_top_tb__DOT__aw_timeout_counter;
    __Vdly__axi4_top_tb__DOT__aw_seen = vlSelf->axi4_top_tb__DOT__aw_seen;
    __Vdly__axi4_top_tb__DOT__write_beat_count = vlSelf->axi4_top_tb__DOT__write_beat_count;
    __Vdly__axi4_top_tb__DOT__write_burst_len = vlSelf->axi4_top_tb__DOT__write_burst_len;
    __Vdly__axi4_top_tb__DOT__write_burst_active = vlSelf->axi4_top_tb__DOT__write_burst_active;
    __Vdly__axi4_top_tb__DOT__ar_no_data_counter = vlSelf->axi4_top_tb__DOT__ar_no_data_counter;
    __Vdly__axi4_top_tb__DOT__pending_ar_count = vlSelf->axi4_top_tb__DOT__pending_ar_count;
    if ((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
          & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid)) 
         & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wready))) {
        if (vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wlast) {
            VL_WRITEF("[%0t] Write Data (LAST): 0x%08x\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      32,vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wdata);
        } else {
            VL_WRITEF("[%0t] Write Data: 0x%08x\n",
                      64,VL_TIME_UNITED_Q(1000),-9,
                      32,vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wdata);
        }
    }
    __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_decerr_count 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_decerr_count;
    __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_okay_count 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_okay_count;
    __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_exokay_count 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_exokay_count;
    __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_slverr_count 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_slverr_count;
    __Vdly__axi4_top_tb__DOT__read_beat_count = vlSelf->axi4_top_tb__DOT__read_beat_count;
    __Vdly__axi4_top_tb__DOT__read_burst_len = vlSelf->axi4_top_tb__DOT__read_burst_len;
    __Vdly__axi4_top_tb__DOT__read_burst_active = vlSelf->axi4_top_tb__DOT__read_burst_active;
    if (((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
         & (1U <= vlSelf->axi4_top_tb__DOT__warmup_cycles))) {
        if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bready))) {
            vlSelf->axi4_top_tb__DOT__total_b_handshakes 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__total_b_handshakes);
        }
        if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready))) {
            vlSelf->axi4_top_tb__DOT__total_r_handshakes 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__total_r_handshakes);
        }
        if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arready))) {
            vlSelf->axi4_top_tb__DOT__total_ar_handshakes 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__total_ar_handshakes);
        }
        if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awready))) {
            vlSelf->axi4_top_tb__DOT__total_aw_handshakes 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__total_aw_handshakes);
        }
        if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wready))) {
            vlSelf->axi4_top_tb__DOT__total_w_handshakes 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__total_w_handshakes);
        }
        if ((((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid) 
              & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wready)) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wlast))) {
            vlSelf->axi4_top_tb__DOT__total_wlast_seen 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__total_wlast_seen);
        }
    }
    if ((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
          & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid)) 
         & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bready))) {
        if ((2U & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bresp))) {
            if ((1U & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bresp))) {
                vlSelf->axi4_top_tb__DOT__write_resp_decerr_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__write_resp_decerr_count);
            }
            if ((1U & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bresp)))) {
                vlSelf->axi4_top_tb__DOT__write_resp_slverr_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__write_resp_slverr_count);
            }
        }
        if ((1U & (~ ((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bresp) 
                      >> 1U)))) {
            if ((1U & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bresp))) {
                vlSelf->axi4_top_tb__DOT__write_resp_exokay_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__write_resp_exokay_count);
            }
            if ((1U & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bresp)))) {
                vlSelf->axi4_top_tb__DOT__write_resp_okay_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__write_resp_okay_count);
            }
        }
    }
    if (vlSelf->axi4_top_tb__DOT__resetn) {
        if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bready))) {
            vlSelf->axi4_top_tb__DOT__b_handshake_valid_ready_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__b_handshake_valid_ready_count);
        }
        if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready))) {
            vlSelf->axi4_top_tb__DOT__r_handshake_valid_ready_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__r_handshake_valid_ready_count);
        }
        if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arready))) {
            vlSelf->axi4_top_tb__DOT__ar_handshake_valid_ready_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__ar_handshake_valid_ready_count);
        }
        if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awready))) {
            vlSelf->axi4_top_tb__DOT__aw_handshake_valid_ready_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__aw_handshake_valid_ready_count);
        }
        if ((0U == (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_req) 
                     << 1U) | (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ack)))) {
            vlSelf->axi4_top_tb__DOT__interrupt_idle_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__interrupt_idle_count);
        }
        if ((0U != (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_req) 
                     << 1U) | (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ack)))) {
            if ((2U == (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_req) 
                         << 1U) | (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ack)))) {
                vlSelf->axi4_top_tb__DOT__interrupt_pending_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__interrupt_pending_count);
            }
            if ((2U != (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_req) 
                         << 1U) | (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ack)))) {
                if ((3U == (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_req) 
                             << 1U) | (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ack)))) {
                    vlSelf->axi4_top_tb__DOT__interrupt_acknowledged_count 
                        = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__interrupt_acknowledged_count);
                }
            }
        }
        if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wready))) {
            vlSelf->axi4_top_tb__DOT__w_handshake_valid_ready_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__w_handshake_valid_ready_count);
        }
    }
    if (VL_UNLIKELY((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
                      & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid)) 
                     & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bready)))) {
        vlSelf->axi4_top_tb__DOT__write_resp_handshake_count 
            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__write_resp_handshake_count);
        VL_WRITEF("[%0t] Write Response: BRESP=0x%02x\n",
                  64,VL_TIME_UNITED_Q(1000),-9,2,(IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bresp));
    }
    if (VL_UNLIKELY(((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
                       & (1U <= vlSelf->axi4_top_tb__DOT__warmup_cycles)) 
                      & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid)) 
                     & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bready)))) {
        vlSelf->axi4_top_tb__DOT__assertion_pass_count 
            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_pass_count);
        VL_WRITEF("ASSERTION PASSED: Valid BRESP (%b)\n",
                  2,vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bresp);
    }
    if (((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
         & (1U <= vlSelf->axi4_top_tb__DOT__warmup_cycles))) {
        if (VL_UNLIKELY((((IData)(vlSelf->axi4_top_tb__DOT__bvalid_prev) 
                          & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid))) 
                         & (~ (IData)(vlSelf->axi4_top_tb__DOT__bready_prev))))) {
            vlSelf->axi4_top_tb__DOT__assertion_fail_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_fail_count);
            VL_WRITEF("ASSERTION FAILED: BVALID not stable until BREADY\n");
        } else if (VL_UNLIKELY(((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid) 
                                & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bready)))) {
            VL_WRITEF("ASSERTION PASSED: BVALID/BREADY handshake\n");
            vlSelf->axi4_top_tb__DOT__assertion_pass_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_pass_count);
        }
    }
    if (((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
         & (1U <= vlSelf->axi4_top_tb__DOT__warmup_cycles))) {
        if (VL_UNLIKELY((((IData)(vlSelf->axi4_top_tb__DOT__rvalid_prev) 
                          & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid))) 
                         & (~ (IData)(vlSelf->axi4_top_tb__DOT__rready_prev))))) {
            vlSelf->axi4_top_tb__DOT__assertion_fail_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_fail_count);
            VL_WRITEF("ASSERTION FAILED: RVALID not stable until RREADY\n");
        } else if (VL_UNLIKELY(((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid) 
                                & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready)))) {
            VL_WRITEF("ASSERTION PASSED: RVALID/RREADY handshake\n");
            vlSelf->axi4_top_tb__DOT__assertion_pass_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_pass_count);
        }
    }
    if (((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
         & (1U <= vlSelf->axi4_top_tb__DOT__warmup_cycles))) {
        if (VL_UNLIKELY((((IData)(vlSelf->axi4_top_tb__DOT__arvalid_prev) 
                          & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid))) 
                         & (~ (IData)(vlSelf->axi4_top_tb__DOT__arready_prev))))) {
            vlSelf->axi4_top_tb__DOT__assertion_fail_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_fail_count);
            VL_WRITEF("ASSERTION FAILED: ARVALID not stable until ARREADY\n");
        } else if (VL_UNLIKELY(((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid) 
                                & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arready)))) {
            VL_WRITEF("ASSERTION PASSED: ARVALID/ARREADY handshake\n");
            vlSelf->axi4_top_tb__DOT__assertion_pass_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_pass_count);
        }
    }
    if (((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
         & (1U <= vlSelf->axi4_top_tb__DOT__warmup_cycles))) {
        if (VL_UNLIKELY((((IData)(vlSelf->axi4_top_tb__DOT__awvalid_prev) 
                          & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid))) 
                         & (~ (IData)(vlSelf->axi4_top_tb__DOT__awready_prev))))) {
            vlSelf->axi4_top_tb__DOT__assertion_fail_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_fail_count);
            VL_WRITEF("ASSERTION FAILED: AWVALID not stable until AWREADY\n");
        } else if (VL_UNLIKELY(((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid) 
                                & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awready)))) {
            VL_WRITEF("ASSERTION PASSED: AWVALID/AWREADY handshake\n");
            vlSelf->axi4_top_tb__DOT__assertion_pass_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_pass_count);
        }
    }
    if ((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
          & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid)) 
         & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arready))) {
        if ((0U != (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arburst))) {
            if ((1U != (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arburst))) {
                if ((2U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arburst))) {
                    vlSelf->axi4_top_tb__DOT__read_burst_wrap_count 
                        = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__read_burst_wrap_count);
                }
            }
            if ((1U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arburst))) {
                vlSelf->axi4_top_tb__DOT__read_burst_incr_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__read_burst_incr_count);
            }
        }
        if ((0U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arburst))) {
            vlSelf->axi4_top_tb__DOT__read_burst_fixed_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__read_burst_fixed_count);
        }
        if ((0xfffffffU >= vlSelf->axi4_top_tb__DOT__dut__DOT__axi_araddr)) {
            vlSelf->axi4_top_tb__DOT__read_addr_low_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__read_addr_low_count);
        }
        if ((0xfffffffU < vlSelf->axi4_top_tb__DOT__dut__DOT__axi_araddr)) {
            if (((0x10000000U <= vlSelf->axi4_top_tb__DOT__dut__DOT__axi_araddr) 
                 & (0x1fffffffU >= vlSelf->axi4_top_tb__DOT__dut__DOT__axi_araddr))) {
                vlSelf->axi4_top_tb__DOT__read_addr_mid_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__read_addr_mid_count);
            }
            if ((1U & (~ ((0x10000000U <= vlSelf->axi4_top_tb__DOT__dut__DOT__axi_araddr) 
                          & (0x1fffffffU >= vlSelf->axi4_top_tb__DOT__dut__DOT__axi_araddr))))) {
                vlSelf->axi4_top_tb__DOT__read_addr_high_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__read_addr_high_count);
            }
        }
    }
    if ((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
          & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid)) 
         & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awready))) {
        if ((0U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awsize))) {
            vlSelf->axi4_top_tb__DOT__write_size_byte_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__write_size_byte_count);
        }
        if ((0U != (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awsize))) {
            if ((1U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awsize))) {
                vlSelf->axi4_top_tb__DOT__write_size_halfword_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__write_size_halfword_count);
            }
            if ((1U != (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awsize))) {
                if ((2U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awsize))) {
                    vlSelf->axi4_top_tb__DOT__write_size_word_count 
                        = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__write_size_word_count);
                }
            }
        }
        if ((0U != (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awburst))) {
            if ((1U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awburst))) {
                vlSelf->axi4_top_tb__DOT__write_burst_incr_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__write_burst_incr_count);
            }
            if ((1U != (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awburst))) {
                if ((2U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awburst))) {
                    vlSelf->axi4_top_tb__DOT__write_burst_wrap_count 
                        = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__write_burst_wrap_count);
                }
            }
        }
        if ((0U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awburst))) {
            vlSelf->axi4_top_tb__DOT__write_burst_fixed_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__write_burst_fixed_count);
        }
        if ((0xfffffffU < vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr)) {
            if ((1U & (~ ((0x10000000U <= vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr) 
                          & (0x1fffffffU >= vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr))))) {
                vlSelf->axi4_top_tb__DOT__write_addr_high_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__write_addr_high_count);
            }
            if (((0x10000000U <= vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr) 
                 & (0x1fffffffU >= vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr))) {
                vlSelf->axi4_top_tb__DOT__write_addr_mid_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__write_addr_mid_count);
            }
        }
        if ((0xfffffffU >= vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr)) {
            vlSelf->axi4_top_tb__DOT__write_addr_low_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__write_addr_low_count);
        }
    }
    if (((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
         & (1U <= vlSelf->axi4_top_tb__DOT__warmup_cycles))) {
        if (VL_UNLIKELY((((IData)(vlSelf->axi4_top_tb__DOT__wvalid_prev) 
                          & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid))) 
                         & (~ (IData)(vlSelf->axi4_top_tb__DOT__wready_prev))))) {
            vlSelf->axi4_top_tb__DOT__assertion_fail_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_fail_count);
            VL_WRITEF("ASSERTION FAILED: WVALID not stable until WREADY\n");
        } else if (VL_UNLIKELY(((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid) 
                                & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wready)))) {
            VL_WRITEF("ASSERTION PASSED: WVALID/WREADY handshake\n");
            vlSelf->axi4_top_tb__DOT__assertion_pass_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_pass_count);
        }
    }
    if (((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
         & (1U <= vlSelf->axi4_top_tb__DOT__warmup_cycles))) {
        if ((((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid) 
              & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready)) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rlast))) {
            vlSelf->axi4_top_tb__DOT__total_rlast_seen 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__total_rlast_seen);
        }
    }
    if ((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
          & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid)) 
         & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready))) {
        if ((2U & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rresp))) {
            if ((1U & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rresp))) {
                vlSelf->axi4_top_tb__DOT__read_resp_decerr_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__read_resp_decerr_count);
            }
            if ((1U & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rresp)))) {
                vlSelf->axi4_top_tb__DOT__read_resp_slverr_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__read_resp_slverr_count);
            }
        }
        if ((1U & (~ ((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rresp) 
                      >> 1U)))) {
            if ((1U & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rresp))) {
                vlSelf->axi4_top_tb__DOT__read_resp_exokay_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__read_resp_exokay_count);
            }
            if ((1U & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rresp)))) {
                vlSelf->axi4_top_tb__DOT__read_resp_okay_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__read_resp_okay_count);
            }
        }
    }
    if (VL_UNLIKELY(((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
                       & (1U <= vlSelf->axi4_top_tb__DOT__warmup_cycles)) 
                      & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid)) 
                     & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready)))) {
        vlSelf->axi4_top_tb__DOT__assertion_pass_count 
            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_pass_count);
        VL_WRITEF("ASSERTION PASSED: Valid RRESP (%b)\n",
                  2,vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rresp);
    }
    if (VL_UNLIKELY((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
                      & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid)) 
                     & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arready)))) {
        vlSelf->axi4_top_tb__DOT__read_addr_handshake_count 
            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__read_addr_handshake_count);
        vlSelf->axi4_top_tb__DOT__read_transaction_count 
            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__read_transaction_count);
        VL_WRITEF("[%0t] Read Address: 0x%08x, LEN=%0#\n",
                  64,VL_TIME_UNITED_Q(1000),-9,32,vlSelf->axi4_top_tb__DOT__dut__DOT__axi_araddr,
                  8,(IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arlen));
    }
    if (VL_UNLIKELY((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
                      & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid)) 
                     & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awready)))) {
        vlSelf->axi4_top_tb__DOT__write_addr_handshake_count 
            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__write_addr_handshake_count);
        vlSelf->axi4_top_tb__DOT__write_transaction_count 
            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__write_transaction_count);
        VL_WRITEF("[%0t] Write Address: 0x%08x, LEN=%0#\n",
                  64,VL_TIME_UNITED_Q(1000),-9,32,vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr,
                  8,(IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awlen));
    }
    if (VL_UNLIKELY((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
                      & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid)) 
                     & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready)))) {
        vlSelf->axi4_top_tb__DOT__read_data_handshake_count 
            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__read_data_handshake_count);
        VL_WRITEF("[%0t] Read Data: 0x%08x, RLAST=%0#\n",
                  64,VL_TIME_UNITED_Q(1000),-9,32,vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rdata,
                  1,(IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rlast));
    }
    if (vlSelf->axi4_top_tb__DOT__resetn) {
        if ((1U > vlSelf->axi4_top_tb__DOT__warmup_cycles)) {
            __Vdly__axi4_top_tb__DOT__warmup_cycles 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__warmup_cycles);
        }
    } else {
        __Vdly__axi4_top_tb__DOT__warmup_cycles = 0U;
    }
    if (VL_UNLIKELY(((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
                     & (~ (IData)(vlSelf->axi4_top_tb__DOT__reset_checked))))) {
        vlSelf->axi4_top_tb__DOT__assertion_pass_count 
            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_pass_count);
        VL_WRITEF("ASSERTION PASSED: Reset released\n");
        vlSelf->axi4_top_tb__DOT__reset_checked = 1U;
    }
    if ((1U & (~ (IData)(vlSelf->axi4_top_tb__DOT__resetn)))) {
        vlSelf->axi4_top_tb__DOT__reset_checked = 0U;
    }
    if ((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
          & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid)) 
         & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bready))) {
        vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__b_handshake_count 
            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__b_handshake_count);
    }
    if ((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
          & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid)) 
         & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready))) {
        vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__r_handshake_count 
            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__r_handshake_count);
    }
    if (vlSelf->axi4_top_tb__DOT__resetn) {
        if (((1U <= vlSelf->axi4_top_tb__DOT__warmup_cycles) 
             & (~ (IData)(vlSelf->axi4_top_tb__DOT__aw_activity_checked)))) {
            __Vdly__axi4_top_tb__DOT__aw_activity_counter 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__aw_activity_counter);
            if (VL_UNLIKELY(VL_LTS_III(32, 0U, vlSelf->axi4_top_tb__DOT__total_aw_handshakes))) {
                vlSelf->axi4_top_tb__DOT__assertion_pass_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_pass_count);
                VL_WRITEF("ASSERTION PASSED: AWVALID activity detected\n");
                vlSelf->axi4_top_tb__DOT__aw_activity_checked = 1U;
            }
            if (VL_UNLIKELY((VL_LTES_III(32, 0x1f4U, vlSelf->axi4_top_tb__DOT__aw_activity_counter) 
                             & (0U == vlSelf->axi4_top_tb__DOT__total_aw_handshakes)))) {
                VL_WRITEF("ASSERTION FAILED: AWVALID never asserted - write address channel stuck\n");
                vlSelf->axi4_top_tb__DOT__assertion_fail_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_fail_count);
                vlSelf->axi4_top_tb__DOT__aw_activity_checked = 1U;
            }
        }
    } else {
        __Vdly__axi4_top_tb__DOT__aw_activity_counter = 0U;
        vlSelf->axi4_top_tb__DOT__aw_activity_checked = 0U;
    }
    if (vlSelf->axi4_top_tb__DOT__resetn) {
        if (((1U <= vlSelf->axi4_top_tb__DOT__warmup_cycles) 
             & (~ (IData)(vlSelf->axi4_top_tb__DOT__ar_activity_checked)))) {
            __Vdly__axi4_top_tb__DOT__ar_activity_counter 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__ar_activity_counter);
            if (VL_UNLIKELY(VL_LTS_III(32, 0U, vlSelf->axi4_top_tb__DOT__total_ar_handshakes))) {
                vlSelf->axi4_top_tb__DOT__assertion_pass_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_pass_count);
                VL_WRITEF("ASSERTION PASSED: ARVALID activity detected\n");
                vlSelf->axi4_top_tb__DOT__ar_activity_checked = 1U;
            }
            if (VL_UNLIKELY((VL_LTES_III(32, 0x1f4U, vlSelf->axi4_top_tb__DOT__ar_activity_counter) 
                             & (0U == vlSelf->axi4_top_tb__DOT__total_ar_handshakes)))) {
                VL_WRITEF("ASSERTION FAILED: ARVALID never asserted - read address channel stuck\n");
                vlSelf->axi4_top_tb__DOT__assertion_fail_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_fail_count);
                vlSelf->axi4_top_tb__DOT__ar_activity_checked = 1U;
            }
        }
    } else {
        __Vdly__axi4_top_tb__DOT__ar_activity_counter = 0U;
        vlSelf->axi4_top_tb__DOT__ar_activity_checked = 0U;
    }
    if ((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
          & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid)) 
         & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arready))) {
        vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__ar_handshake_count 
            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__ar_handshake_count);
    }
    if ((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
          & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid)) 
         & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awready))) {
        vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__aw_handshake_count 
            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__aw_handshake_count);
    }
    if (vlSelf->axi4_top_tb__DOT__resetn) {
        if (VL_UNLIKELY(((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_req) 
                         & (~ (IData)(vlSelf->axi4_top_tb__DOT__interrupt_req_prev))))) {
            VL_WRITEF("[%0t] Interrupt Request\n",64,
                      VL_TIME_UNITED_Q(1000),-9);
        }
        if (VL_UNLIKELY(((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ack) 
                         & (~ (IData)(vlSelf->axi4_top_tb__DOT__interrupt_ack_prev))))) {
            VL_WRITEF("[%0t] Interrupt Ack\n",64,VL_TIME_UNITED_Q(1000),
                      -9);
        }
        vlSelf->axi4_top_tb__DOT__interrupt_req_prev 
            = vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_req;
        vlSelf->axi4_top_tb__DOT__interrupt_ack_prev 
            = vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ack;
    } else {
        vlSelf->axi4_top_tb__DOT__interrupt_req_prev = 0U;
        vlSelf->axi4_top_tb__DOT__interrupt_ack_prev = 0U;
    }
    if ((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
          & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid)) 
         & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wready))) {
        vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__w_handshake_count 
            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__w_handshake_count);
        if (vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wlast) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wlast_asserted_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wlast_asserted_count);
        }
    }
    if (vlSelf->axi4_top_tb__DOT__resetn) {
        if ((1U <= vlSelf->axi4_top_tb__DOT__warmup_cycles)) {
            if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid) 
                 & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awready))) {
                __Vdly__axi4_top_tb__DOT__aw_seen = 1U;
                __Vdly__axi4_top_tb__DOT__aw_timeout_counter = 0U;
            } else if (((IData)(vlSelf->axi4_top_tb__DOT__aw_seen) 
                        & (~ (IData)(vlSelf->axi4_top_tb__DOT__wlast_handshake_seen)))) {
                __Vdly__axi4_top_tb__DOT__aw_timeout_counter 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__aw_timeout_counter);
            }
            if ((((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid) 
                  & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wready)) 
                 & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wlast))) {
                __Vdly__axi4_top_tb__DOT__wlast_handshake_seen = 1U;
                __Vdly__axi4_top_tb__DOT__w_timeout_counter = 0U;
            } else if (vlSelf->axi4_top_tb__DOT__wlast_handshake_seen) {
                __Vdly__axi4_top_tb__DOT__w_timeout_counter 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__w_timeout_counter);
            }
            if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid) 
                 & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bready))) {
                if (VL_UNLIKELY(((IData)(vlSelf->axi4_top_tb__DOT__wlast_handshake_seen) 
                                 | (IData)(vlSelf->axi4_top_tb__DOT__aw_seen)))) {
                    vlSelf->axi4_top_tb__DOT__assertion_pass_count 
                        = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_pass_count);
                    VL_WRITEF("ASSERTION PASSED: Write response follows write data\n");
                }
                __Vdly__axi4_top_tb__DOT__aw_seen = 0U;
                __Vdly__axi4_top_tb__DOT__wlast_handshake_seen = 0U;
            }
            if (VL_UNLIKELY(((IData)(vlSelf->axi4_top_tb__DOT__wlast_handshake_seen) 
                             & VL_LTS_III(32, 0x64U, vlSelf->axi4_top_tb__DOT__w_timeout_counter)))) {
                VL_WRITEF("ASSERTION FAILED: Write response timeout after WLAST\n");
                vlSelf->axi4_top_tb__DOT__assertion_fail_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_fail_count);
                __Vdly__axi4_top_tb__DOT__wlast_handshake_seen = 0U;
                __Vdly__axi4_top_tb__DOT__w_timeout_counter = 0U;
            }
        }
    } else {
        __Vdly__axi4_top_tb__DOT__aw_seen = 0U;
        __Vdly__axi4_top_tb__DOT__wlast_handshake_seen = 0U;
        __Vdly__axi4_top_tb__DOT__aw_timeout_counter = 0U;
        __Vdly__axi4_top_tb__DOT__w_timeout_counter = 0U;
    }
    if ((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
          & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid)) 
         & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awready))) {
        if ((0U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awlen))) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__single_beat_write_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__single_beat_write_count);
        }
        if ((0U != (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awlen))) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__multi_beat_write_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__multi_beat_write_count);
        }
        if ((0U != (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awburst))) {
            if ((1U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awburst))) {
                vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_incr_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_incr_count);
            }
            if ((1U != (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awburst))) {
                if ((2U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awburst))) {
                    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_wrap_count 
                        = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_wrap_count);
                }
            }
        }
        if ((0U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awburst))) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_fixed_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__burst_fixed_count);
        }
        if ((0x100U <= vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr)) {
            if ((0x200U > vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr)) {
                vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region1_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region1_count);
            }
            if ((0x200U <= vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr)) {
                if ((0x300U <= vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr)) {
                    if ((0x400U > vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr)) {
                        vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region3_count 
                            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region3_count);
                    }
                    if ((0x400U <= vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr)) {
                        vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_out_of_range_count 
                            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_out_of_range_count);
                    }
                }
                if ((0x300U > vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr)) {
                    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region2_count 
                        = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region2_count);
                }
            }
        }
        if ((0x100U > vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr)) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region0_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__addr_region0_count);
        }
    }
    if ((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
          & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid)) 
         & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arready))) {
        if ((0U != (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arlen))) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__multi_beat_read_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__multi_beat_read_count);
        }
        if ((0U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arlen))) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__single_beat_read_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__single_beat_read_count);
        }
    }
    if (vlSelf->axi4_top_tb__DOT__resetn) {
        if ((1U <= vlSelf->axi4_top_tb__DOT__warmup_cycles)) {
            if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid) 
                 & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awready))) {
                __Vdly__axi4_top_tb__DOT__write_burst_active = 1U;
                __Vdly__axi4_top_tb__DOT__write_burst_len 
                    = ((IData)(1U) + (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awlen));
                __Vdly__axi4_top_tb__DOT__write_beat_count = 0U;
            }
            if ((((IData)(vlSelf->axi4_top_tb__DOT__write_burst_active) 
                  & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid)) 
                 & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wready))) {
                __Vdly__axi4_top_tb__DOT__write_beat_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__write_beat_count);
                if (vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wlast) {
                    if (VL_UNLIKELY((((IData)(1U) + vlSelf->axi4_top_tb__DOT__write_beat_count) 
                                     == vlSelf->axi4_top_tb__DOT__write_burst_len))) {
                        vlSelf->axi4_top_tb__DOT__assertion_pass_count 
                            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_pass_count);
                        VL_WRITEF("ASSERTION PASSED: WLAST asserted on final beat\n");
                    }
                    __Vdly__axi4_top_tb__DOT__write_burst_active = 0U;
                } else if (VL_UNLIKELY((((IData)(1U) 
                                         + vlSelf->axi4_top_tb__DOT__write_beat_count) 
                                        == vlSelf->axi4_top_tb__DOT__write_burst_len))) {
                    VL_WRITEF("ASSERTION FAILED: WLAST not asserted on final beat\n");
                    vlSelf->axi4_top_tb__DOT__assertion_fail_count 
                        = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_fail_count);
                    __Vdly__axi4_top_tb__DOT__write_burst_active = 0U;
                }
            }
        }
    } else {
        __Vdly__axi4_top_tb__DOT__write_beat_count = 0U;
        __Vdly__axi4_top_tb__DOT__write_burst_active = 0U;
        __Vdly__axi4_top_tb__DOT__write_burst_len = 0U;
    }
    if ((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
          & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid)) 
         & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bready))) {
        if ((2U & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bresp))) {
            if ((1U & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bresp))) {
                __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_decerr_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_decerr_count);
            }
            if ((1U & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bresp)))) {
                __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_slverr_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_slverr_count);
            }
        }
        if ((1U & (~ ((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bresp) 
                      >> 1U)))) {
            if ((1U & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bresp)))) {
                __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_okay_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_okay_count);
            }
            if ((1U & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bresp))) {
                __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_exokay_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_exokay_count);
            }
        }
    }
    if ((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
          & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid)) 
         & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wready))) {
        if ((0xfU == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wstrb))) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wstrb_full_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wstrb_full_count);
        }
        if ((0xfU != (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wstrb))) {
            if ((0U != (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wstrb))) {
                vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wstrb_partial_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__wstrb_partial_count);
            }
        }
    }
    if ((((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
          & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid)) 
         & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready))) {
        if (vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rlast) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__rlast_asserted_count 
                = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__rlast_asserted_count);
        }
        if ((2U & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rresp))) {
            if ((1U & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rresp))) {
                __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_decerr_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_decerr_count);
            }
            if ((1U & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rresp)))) {
                __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_slverr_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_slverr_count);
            }
        }
        if ((1U & (~ ((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rresp) 
                      >> 1U)))) {
            if ((1U & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rresp)))) {
                __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_okay_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_okay_count);
            }
            if ((1U & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rresp))) {
                __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_exokay_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_exokay_count);
            }
        }
    }
    if (vlSelf->axi4_top_tb__DOT__resetn) {
        if ((1U <= vlSelf->axi4_top_tb__DOT__warmup_cycles)) {
            if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid) 
                 & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arready))) {
                __Vdly__axi4_top_tb__DOT__read_burst_active = 1U;
                __Vdly__axi4_top_tb__DOT__read_burst_len 
                    = ((IData)(1U) + (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arlen));
                __Vdly__axi4_top_tb__DOT__read_beat_count = 0U;
            }
            if ((((IData)(vlSelf->axi4_top_tb__DOT__read_burst_active) 
                  & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid)) 
                 & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready))) {
                __Vdly__axi4_top_tb__DOT__read_beat_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__read_beat_count);
                if (vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rlast) {
                    if (VL_UNLIKELY((((IData)(1U) + vlSelf->axi4_top_tb__DOT__read_beat_count) 
                                     == vlSelf->axi4_top_tb__DOT__read_burst_len))) {
                        vlSelf->axi4_top_tb__DOT__assertion_pass_count 
                            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_pass_count);
                        VL_WRITEF("ASSERTION PASSED: RLAST asserted on final beat\n");
                    }
                    __Vdly__axi4_top_tb__DOT__read_burst_active = 0U;
                } else if (VL_UNLIKELY((((IData)(1U) 
                                         + vlSelf->axi4_top_tb__DOT__read_beat_count) 
                                        == vlSelf->axi4_top_tb__DOT__read_burst_len))) {
                    VL_WRITEF("ASSERTION FAILED: RLAST not asserted on final beat\n");
                    vlSelf->axi4_top_tb__DOT__assertion_fail_count 
                        = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_fail_count);
                    __Vdly__axi4_top_tb__DOT__read_burst_active = 0U;
                }
            }
        }
    } else {
        __Vdly__axi4_top_tb__DOT__read_beat_count = 0U;
        __Vdly__axi4_top_tb__DOT__read_burst_active = 0U;
        __Vdly__axi4_top_tb__DOT__read_burst_len = 0U;
    }
    __Vtableidx1 = (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid) 
                     << 6U) | (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid) 
                                << 5U) | (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid) 
                                           << 4U) | 
                                          (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid) 
                                            << 3U) 
                                           | (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid) 
                                               << 2U) 
                                              | (((1U 
                                                   <= vlSelf->axi4_top_tb__DOT__warmup_cycles) 
                                                  << 1U) 
                                                 | (IData)(vlSelf->axi4_top_tb__DOT__resetn)))))));
    if ((1U & Vaxi4_top_tb__ConstPool__TABLE_hc8079c3b_0
         [__Vtableidx1])) {
        vlSelf->axi4_top_tb__DOT__awvalid_ever_seen 
            = Vaxi4_top_tb__ConstPool__TABLE_h0c95e6ed_0
            [__Vtableidx1];
    }
    if ((2U & Vaxi4_top_tb__ConstPool__TABLE_hc8079c3b_0
         [__Vtableidx1])) {
        vlSelf->axi4_top_tb__DOT__arvalid_ever_seen 
            = Vaxi4_top_tb__ConstPool__TABLE_h08698683_0
            [__Vtableidx1];
    }
    if ((4U & Vaxi4_top_tb__ConstPool__TABLE_hc8079c3b_0
         [__Vtableidx1])) {
        vlSelf->axi4_top_tb__DOT__wvalid_ever_seen 
            = Vaxi4_top_tb__ConstPool__TABLE_h2da5e280_0
            [__Vtableidx1];
    }
    if ((8U & Vaxi4_top_tb__ConstPool__TABLE_hc8079c3b_0
         [__Vtableidx1])) {
        vlSelf->axi4_top_tb__DOT__bvalid_ever_seen 
            = Vaxi4_top_tb__ConstPool__TABLE_h7f0673c1_0
            [__Vtableidx1];
    }
    if ((0x10U & Vaxi4_top_tb__ConstPool__TABLE_hc8079c3b_0
         [__Vtableidx1])) {
        vlSelf->axi4_top_tb__DOT__rvalid_ever_seen 
            = Vaxi4_top_tb__ConstPool__TABLE_ha332edba_0
            [__Vtableidx1];
    }
    if (vlSelf->axi4_top_tb__DOT__resetn) {
        if ((1U <= vlSelf->axi4_top_tb__DOT__warmup_cycles)) {
            if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid) 
                 & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arready))) {
                __Vdly__axi4_top_tb__DOT__pending_ar_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__pending_ar_count);
            }
            if (vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid) {
                vlSelf->axi4_top_tb__DOT__ever_saw_rvalid = 1U;
            }
            if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid) 
                 & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready))) {
                if (VL_UNLIKELY(VL_LTS_III(32, 0U, vlSelf->axi4_top_tb__DOT__pending_ar_count))) {
                    vlSelf->axi4_top_tb__DOT__assertion_pass_count 
                        = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_pass_count);
                    VL_WRITEF("ASSERTION PASSED: Read data follows read address\n");
                }
                if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rlast) 
                     & VL_LTS_III(32, 0U, vlSelf->axi4_top_tb__DOT__pending_ar_count))) {
                    __Vdly__axi4_top_tb__DOT__pending_ar_count 
                        = (vlSelf->axi4_top_tb__DOT__pending_ar_count 
                           - (IData)(1U));
                }
            }
            __Vdly__axi4_top_tb__DOT__ar_no_data_counter 
                = ((VL_LTS_III(32, 0U, vlSelf->axi4_top_tb__DOT__pending_ar_count) 
                    & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid)))
                    ? ((IData)(1U) + vlSelf->axi4_top_tb__DOT__ar_no_data_counter)
                    : 0U);
            if (VL_UNLIKELY((VL_LTS_III(32, 0U, vlSelf->axi4_top_tb__DOT__pending_ar_count) 
                             & VL_LTS_III(32, 0x64U, vlSelf->axi4_top_tb__DOT__ar_no_data_counter)))) {
                VL_WRITEF("ASSERTION FAILED: RVALID not asserted after ARVALID - read data timeout\n");
                vlSelf->axi4_top_tb__DOT__assertion_fail_count 
                    = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__assertion_fail_count);
                __Vdly__axi4_top_tb__DOT__ar_no_data_counter = 0U;
            }
        }
    } else {
        __Vdly__axi4_top_tb__DOT__pending_ar_count = 0U;
        __Vdly__axi4_top_tb__DOT__ar_no_data_counter = 0U;
        vlSelf->axi4_top_tb__DOT__ever_saw_rvalid = 0U;
    }
    vlSelf->axi4_top_tb__DOT__aw_activity_counter = __Vdly__axi4_top_tb__DOT__aw_activity_counter;
    vlSelf->axi4_top_tb__DOT__ar_activity_counter = __Vdly__axi4_top_tb__DOT__ar_activity_counter;
    vlSelf->axi4_top_tb__DOT__aw_seen = __Vdly__axi4_top_tb__DOT__aw_seen;
    vlSelf->axi4_top_tb__DOT__aw_timeout_counter = __Vdly__axi4_top_tb__DOT__aw_timeout_counter;
    vlSelf->axi4_top_tb__DOT__wlast_handshake_seen 
        = __Vdly__axi4_top_tb__DOT__wlast_handshake_seen;
    vlSelf->axi4_top_tb__DOT__w_timeout_counter = __Vdly__axi4_top_tb__DOT__w_timeout_counter;
    vlSelf->axi4_top_tb__DOT__write_burst_active = __Vdly__axi4_top_tb__DOT__write_burst_active;
    vlSelf->axi4_top_tb__DOT__write_burst_len = __Vdly__axi4_top_tb__DOT__write_burst_len;
    vlSelf->axi4_top_tb__DOT__write_beat_count = __Vdly__axi4_top_tb__DOT__write_beat_count;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_decerr_count 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_decerr_count;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_okay_count 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_okay_count;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_exokay_count 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_exokay_count;
    vlSelf->axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_slverr_count 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__coverage_monitor__DOT__resp_slverr_count;
    vlSelf->axi4_top_tb__DOT__read_burst_active = __Vdly__axi4_top_tb__DOT__read_burst_active;
    vlSelf->axi4_top_tb__DOT__read_burst_len = __Vdly__axi4_top_tb__DOT__read_burst_len;
    vlSelf->axi4_top_tb__DOT__read_beat_count = __Vdly__axi4_top_tb__DOT__read_beat_count;
    vlSelf->axi4_top_tb__DOT__bready_prev = ((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
                                             && (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bready));
    vlSelf->axi4_top_tb__DOT__bvalid_prev = ((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
                                             && (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid));
    vlSelf->axi4_top_tb__DOT__rready_prev = ((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
                                             && (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready));
    vlSelf->axi4_top_tb__DOT__rvalid_prev = ((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
                                             && (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid));
    vlSelf->axi4_top_tb__DOT__arvalid_prev = ((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
                                              && (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid));
    vlSelf->axi4_top_tb__DOT__arready_prev = ((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
                                              && (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arready));
    vlSelf->axi4_top_tb__DOT__awready_prev = ((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
                                              && (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awready));
    vlSelf->axi4_top_tb__DOT__awvalid_prev = ((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
                                              && (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid));
    vlSelf->axi4_top_tb__DOT__wvalid_prev = ((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
                                             && (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid));
    vlSelf->axi4_top_tb__DOT__wready_prev = ((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
                                             && (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wready));
    vlSelf->axi4_top_tb__DOT__pending_ar_count = __Vdly__axi4_top_tb__DOT__pending_ar_count;
    vlSelf->axi4_top_tb__DOT__ar_no_data_counter = __Vdly__axi4_top_tb__DOT__ar_no_data_counter;
    vlSelf->axi4_top_tb__DOT__warmup_cycles = __Vdly__axi4_top_tb__DOT__warmup_cycles;
}

extern const VlUnpacked<CData/*1:0*/, 8> Vaxi4_top_tb__ConstPool__TABLE_h8f7a1049_0;
extern const VlUnpacked<CData/*1:0*/, 8> Vaxi4_top_tb__ConstPool__TABLE_h85139238_0;
extern const VlUnpacked<CData/*0:0*/, 8> Vaxi4_top_tb__ConstPool__TABLE_h70de94fd_0;
extern const VlUnpacked<CData/*1:0*/, 8> Vaxi4_top_tb__ConstPool__TABLE_h166b8ba2_0;

VL_INLINE_OPT void Vaxi4_top_tb___024root___nba_sequent__TOP__1(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___nba_sequent__TOP__1\n"); );
    // Init
    CData/*2:0*/ __Vtableidx2;
    __Vtableidx2 = 0;
    CData/*2:0*/ __Vtableidx3;
    __Vtableidx3 = 0;
    CData/*0:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__axi_awvalid;
    __Vdly__axi4_top_tb__DOT__dut__DOT__axi_awvalid = 0;
    CData/*0:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__write_in_progress;
    __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__write_in_progress = 0;
    CData/*0:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__axi_wlast;
    __Vdly__axi4_top_tb__DOT__dut__DOT__axi_wlast = 0;
    CData/*0:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__axi_wvalid;
    __Vdly__axi4_top_tb__DOT__dut__DOT__axi_wvalid = 0;
    CData/*7:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__write_count;
    __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__write_count = 0;
    CData/*0:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__axi_bready;
    __Vdly__axi4_top_tb__DOT__dut__DOT__axi_bready = 0;
    CData/*0:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__axi_arvalid;
    __Vdly__axi4_top_tb__DOT__dut__DOT__axi_arvalid = 0;
    CData/*0:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__read_in_progress;
    __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__read_in_progress = 0;
    CData/*0:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__axi_rready;
    __Vdly__axi4_top_tb__DOT__dut__DOT__axi_rready = 0;
    CData/*7:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__read_count;
    __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__read_count = 0;
    IData/*31:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr;
    __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr = 0;
    CData/*7:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_count;
    __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_count = 0;
    CData/*0:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_in_progress;
    __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_in_progress = 0;
    CData/*0:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__axi_awready;
    __Vdly__axi4_top_tb__DOT__dut__DOT__axi_awready = 0;
    CData/*7:0*/ __Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0;
    __Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0 = 0;
    CData/*4:0*/ __Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0;
    __Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0 = 0;
    CData/*7:0*/ __Vdlyvval__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0;
    __Vdlyvval__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0 = 0;
    CData/*0:0*/ __Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0;
    __Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0 = 0;
    CData/*7:0*/ __Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1;
    __Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1 = 0;
    CData/*4:0*/ __Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1;
    __Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1 = 0;
    CData/*7:0*/ __Vdlyvval__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1;
    __Vdlyvval__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1 = 0;
    CData/*0:0*/ __Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1;
    __Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1 = 0;
    CData/*7:0*/ __Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2;
    __Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2 = 0;
    CData/*4:0*/ __Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2;
    __Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2 = 0;
    CData/*7:0*/ __Vdlyvval__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2;
    __Vdlyvval__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2 = 0;
    CData/*0:0*/ __Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2;
    __Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2 = 0;
    CData/*7:0*/ __Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3;
    __Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3 = 0;
    CData/*4:0*/ __Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3;
    __Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3 = 0;
    CData/*7:0*/ __Vdlyvval__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3;
    __Vdlyvval__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3 = 0;
    CData/*0:0*/ __Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3;
    __Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3 = 0;
    CData/*0:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_data_accepted;
    __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_data_accepted = 0;
    CData/*0:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_pending;
    __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_pending = 0;
    CData/*0:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__axi_bvalid;
    __Vdly__axi4_top_tb__DOT__dut__DOT__axi_bvalid = 0;
    CData/*0:0*/ __Vdly__axi4_top_tb__DOT__dut__DOT__axi_rvalid;
    __Vdly__axi4_top_tb__DOT__dut__DOT__axi_rvalid = 0;
    // Body
    __Vdly__axi4_top_tb__DOT__dut__DOT__axi_bvalid 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid;
    __Vdly__axi4_top_tb__DOT__dut__DOT__axi_bready 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bready;
    __Vdly__axi4_top_tb__DOT__dut__DOT__axi_arvalid 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid;
    __Vdly__axi4_top_tb__DOT__dut__DOT__axi_awvalid 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid;
    __Vdly__axi4_top_tb__DOT__dut__DOT__axi_rvalid 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid;
    __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__write_in_progress 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_in_progress;
    __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__write_count 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_count;
    __Vdly__axi4_top_tb__DOT__dut__DOT__axi_wvalid 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid;
    __Vdly__axi4_top_tb__DOT__dut__DOT__axi_wlast = vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wlast;
    __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__read_count 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_count;
    __Vdly__axi4_top_tb__DOT__dut__DOT__axi_rready 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready;
    __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__read_in_progress 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_in_progress;
    __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_in_progress 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_in_progress;
    __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr;
    __Vdly__axi4_top_tb__DOT__dut__DOT__axi_awready 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awready;
    __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_pending 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_pending;
    __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_data_accepted 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_data_accepted;
    __Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0 = 0U;
    __Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1 = 0U;
    __Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2 = 0U;
    __Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3 = 0U;
    __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_count 
        = vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_count;
    if (vlSelf->axi4_top_tb__DOT__resetn) {
        if ((3U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__state))) {
            __Vdly__axi4_top_tb__DOT__dut__DOT__axi_bready = 1U;
        } else if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid) 
                    & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bready))) {
            __Vdly__axi4_top_tb__DOT__dut__DOT__axi_bready = 0U;
            __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__write_in_progress = 0U;
        }
        if ((5U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__state))) {
            __Vdly__axi4_top_tb__DOT__dut__DOT__axi_rready = 1U;
        } else if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid) 
                    & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready))) {
            if (vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rlast) {
                __Vdly__axi4_top_tb__DOT__dut__DOT__axi_rready = 0U;
                __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__read_in_progress = 0U;
                __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__read_count = 0U;
            } else {
                __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__read_count 
                    = (0xffU & ((IData)(1U) + (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_count)));
            }
        }
        if ((((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid) 
              & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wready)) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_in_progress))) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__byte_size 
                = ((IData)(1U) << (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_size));
            vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__addr_offset 
                = ((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_count) 
                   * vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__byte_size);
            if ((0U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_burst))) {
                vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__current_addr 
                    = vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr;
            } else if ((1U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_burst))) {
                vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__current_addr 
                    = (vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr 
                       + vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__addr_offset);
            } else if ((2U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_burst))) {
                vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__aligned_addr 
                    = ((vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr 
                        >> (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_size)) 
                       << (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_size));
                vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__wrap_boundary 
                    = (vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__aligned_addr 
                       + (((IData)(1U) + (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_len)) 
                          << (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_size)));
                vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__current_addr 
                    = (vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__aligned_addr 
                       + VL_MODDIV_III(32, ((vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr 
                                             + vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__addr_offset) 
                                            - vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__aligned_addr), vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__wrap_boundary));
            } else {
                vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__current_addr 
                    = vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr;
            }
            if ((0x400U > vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__current_addr)) {
                vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__mem_addr 
                    = VL_SHIFTR_III(32,32,32, vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__current_addr, 2U);
                if ((1U & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wstrb))) {
                    __Vdlyvval__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0 
                        = (0xffU & vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wdata);
                    __Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0 = 1U;
                    __Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0 = 0U;
                    __Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0 
                        = (0xffU & vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__mem_addr);
                }
                if ((2U & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wstrb))) {
                    __Vdlyvval__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1 
                        = (0xffU & (vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wdata 
                                    >> 8U));
                    __Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1 = 1U;
                    __Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1 = 8U;
                    __Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1 
                        = (0xffU & vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__mem_addr);
                }
                if ((4U & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wstrb))) {
                    __Vdlyvval__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2 
                        = (0xffU & (vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wdata 
                                    >> 0x10U));
                    __Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2 = 1U;
                    __Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2 = 0x10U;
                    __Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2 
                        = (0xffU & vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__mem_addr);
                }
                if ((8U & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wstrb))) {
                    __Vdlyvval__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3 
                        = (vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wdata 
                           >> 0x18U);
                    __Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3 = 1U;
                    __Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3 = 0x18U;
                    __Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3 
                        = (0xffU & vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__mem_addr);
                }
            }
            if (vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wlast) {
                __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_count = 0U;
                __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_data_accepted = 1U;
                __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_pending = 1U;
            } else {
                __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_count 
                    = (0xffU & ((IData)(1U) + (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_count)));
            }
        }
        if ((((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid) 
              & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arready)) 
             & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid)))) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__unnamedblk2__DOT__read_addr 
                = VL_SHIFTR_III(32,32,32, vlSelf->axi4_top_tb__DOT__dut__DOT__axi_araddr, 2U);
            if ((0x100U > vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__unnamedblk2__DOT__read_addr)) {
                vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rdata 
                    = vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__memory
                    [(0xffU & vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__unnamedblk2__DOT__read_addr)];
                vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rresp = 0U;
            } else {
                vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rdata = 0U;
                vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rresp = 3U;
            }
            vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rlast = 1U;
            __Vdly__axi4_top_tb__DOT__dut__DOT__axi_rvalid = 1U;
        }
        if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready))) {
            __Vdly__axi4_top_tb__DOT__dut__DOT__axi_rvalid = 0U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rlast = 0U;
        }
        if (((2U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__state)) 
             & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid)))) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wdata 
                = ((IData)(0xdeadbeefU) + (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_count));
            vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wstrb = 0xfU;
            __Vdly__axi4_top_tb__DOT__dut__DOT__axi_wlast 
                = ((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_count) 
                   == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_length));
            __Vdly__axi4_top_tb__DOT__dut__DOT__axi_wvalid = 1U;
        } else if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid) 
                    & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wready))) {
            if (vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wlast) {
                __Vdly__axi4_top_tb__DOT__dut__DOT__axi_wvalid = 0U;
                __Vdly__axi4_top_tb__DOT__dut__DOT__axi_wlast = 0U;
                __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__write_count = 0U;
            } else {
                __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__write_count 
                    = (0xffU & ((IData)(1U) + (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_count)));
                vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wdata 
                    = ((IData)(0xdeadbef0U) + (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_count));
                __Vdly__axi4_top_tb__DOT__dut__DOT__axi_wlast 
                    = (((IData)(1U) + (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_count)) 
                       == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_length));
            }
        }
        if ((((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid) 
              & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awready)) 
             & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_in_progress)))) {
            __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr 
                = vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr;
            vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_len 
                = vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awlen;
            vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_size 
                = vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awsize;
            vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_burst 
                = vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awburst;
            vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr_accepted = 1U;
            __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_count = 0U;
            __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_in_progress = 1U;
        }
        if ((((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_ready) 
              & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid)) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bready))) {
            __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_data_accepted = 0U;
            __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_pending = 0U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr_accepted = 0U;
            __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_in_progress = 0U;
        }
        if ((1U & ((~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_in_progress)) 
                   & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_pending))))) {
            __Vdly__axi4_top_tb__DOT__dut__DOT__axi_awready = 1U;
        } else if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid) 
                    & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awready))) {
            __Vdly__axi4_top_tb__DOT__dut__DOT__axi_awready = 0U;
        }
        if ((((0U == (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__state)) 
              & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_in_progress))) 
             & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_in_progress)))) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__axi_araddr = 0x10000000U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arlen = 0U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arsize = 2U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arburst = 1U;
            __Vdly__axi4_top_tb__DOT__dut__DOT__axi_arvalid = 1U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_base_addr = 0x10000000U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_length = 0U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_size = 2U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_burst = 1U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr = 0x10000000U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awlen = 3U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awsize = 2U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awburst = 1U;
            __Vdly__axi4_top_tb__DOT__dut__DOT__axi_awvalid = 1U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_base_addr = 0x10000000U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_length = 3U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_size = 2U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_burst = 1U;
        } else {
            if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid) 
                 & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arready))) {
                __Vdly__axi4_top_tb__DOT__dut__DOT__axi_arvalid = 0U;
                __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__read_in_progress = 1U;
            }
            if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid) 
                 & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awready))) {
                __Vdly__axi4_top_tb__DOT__dut__DOT__axi_awvalid = 0U;
                __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__write_in_progress = 1U;
            }
        }
        if ((((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_pending) 
              & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_data_accepted)) 
             & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid)))) {
            vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bresp 
                = ((0x400U > vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr)
                    ? 0U : 3U);
            __Vdly__axi4_top_tb__DOT__dut__DOT__axi_bvalid = 1U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_ready = 1U;
        }
        if (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid) 
             & (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bready))) {
            __Vdly__axi4_top_tb__DOT__dut__DOT__axi_bvalid = 0U;
            vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_ready = 0U;
        }
        vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__state 
            = vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__next_state;
    } else {
        __Vdly__axi4_top_tb__DOT__dut__DOT__axi_bready = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__write_in_progress = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__axi_rready = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__read_in_progress = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__read_count = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_data_accepted = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_pending = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__axi_rvalid = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rdata = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rresp = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rlast = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__axi_wvalid = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wdata = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wstrb = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__axi_wlast = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__write_count = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__axi_awready = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr_accepted = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_len = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_size = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_burst = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_count = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_in_progress = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__axi_arvalid = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__axi_araddr = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arlen = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arsize = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arburst = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_base_addr = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_length = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_size = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_burst = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__read_in_progress = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__axi_bvalid = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bresp = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_ready = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__axi_awvalid = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awaddr = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awlen = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awsize = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awburst = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_base_addr = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_length = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_size = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_burst = 0U;
        __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__write_in_progress = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__state = 0U;
    }
    __Vtableidx2 = (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ctrl__DOT__next_state) 
                     << 1U) | (IData)(vlSelf->axi4_top_tb__DOT__resetn));
    vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ctrl__DOT__state 
        = Vaxi4_top_tb__ConstPool__TABLE_h8f7a1049_0
        [__Vtableidx2];
    if ((2U & Vaxi4_top_tb__ConstPool__TABLE_h85139238_0
         [__Vtableidx2])) {
        vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ack 
            = Vaxi4_top_tb__ConstPool__TABLE_h70de94fd_0
            [__Vtableidx2];
    }
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_count 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__read_count;
    __Vtableidx3 = (((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_req) 
                     << 2U) | (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ctrl__DOT__state));
    vlSelf->axi4_top_tb__DOT__dut__DOT__interrupt_ctrl__DOT__next_state 
        = Vaxi4_top_tb__ConstPool__TABLE_h166b8ba2_0
        [__Vtableidx3];
    if (__Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0) {
        vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__memory[__Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0] 
            = (((~ ((IData)(0xffU) << (IData)(__Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0))) 
                & vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__memory
                [__Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0]) 
               | (0xffffffffULL & ((IData)(__Vdlyvval__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0) 
                                   << (IData)(__Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v0))));
    }
    if (__Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1) {
        vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__memory[__Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1] 
            = (((~ ((IData)(0xffU) << (IData)(__Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1))) 
                & vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__memory
                [__Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1]) 
               | (0xffffffffULL & ((IData)(__Vdlyvval__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1) 
                                   << (IData)(__Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v1))));
    }
    if (__Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2) {
        vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__memory[__Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2] 
            = (((~ ((IData)(0xffU) << (IData)(__Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2))) 
                & vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__memory
                [__Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2]) 
               | (0xffffffffULL & ((IData)(__Vdlyvval__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2) 
                                   << (IData)(__Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v2))));
    }
    if (__Vdlyvset__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3) {
        vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__memory[__Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3] 
            = (((~ ((IData)(0xffU) << (IData)(__Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3))) 
                & vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__memory
                [__Vdlyvdim0__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3]) 
               | (0xffffffffULL & ((IData)(__Vdlyvval__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3) 
                                   << (IData)(__Vdlyvlsb__axi4_top_tb__DOT__dut__DOT__slave__DOT__memory__v3))));
    }
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rready 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__axi_rready;
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_rvalid 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__axi_rvalid;
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_count 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__write_count;
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wlast = __Vdly__axi4_top_tb__DOT__dut__DOT__axi_wlast;
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wvalid 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__axi_wvalid;
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_count 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_count;
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_wready 
        = ((IData)(vlSelf->axi4_top_tb__DOT__resetn) 
           && ((IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_in_progress) 
               & (~ (IData)(vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_pending))));
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arvalid 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__axi_arvalid;
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_in_progress 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_in_progress;
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_data_accepted 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_data_accepted;
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_addr;
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_pending 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__slave__DOT__write_response_pending;
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bready 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__axi_bready;
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_bvalid 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__axi_bvalid;
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awready 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__axi_awready;
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_awvalid 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__axi_awvalid;
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__write_in_progress 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__write_in_progress;
    vlSelf->axi4_top_tb__DOT__dut__DOT__master__DOT__read_in_progress 
        = __Vdly__axi4_top_tb__DOT__dut__DOT__master__DOT__read_in_progress;
    vlSelf->axi4_top_tb__DOT__dut__DOT__axi_arready = 1U;
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

void Vaxi4_top_tb___024root___eval_nba(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval_nba\n"); );
    // Body
    if ((1ULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vaxi4_top_tb___024root___nba_sequent__TOP__0(vlSelf);
        vlSelf->__Vm_traceActivity[1U] = 1U;
    }
    if ((2ULL & vlSelf->__VnbaTriggered.word(0U))) {
        Vaxi4_top_tb___024root___nba_sequent__TOP__1(vlSelf);
        vlSelf->__Vm_traceActivity[2U] = 1U;
    }
}

void Vaxi4_top_tb___024root___timing_resume(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___timing_resume\n"); );
    // Body
    if ((4ULL & vlSelf->__VactTriggered.word(0U))) {
        vlSelf->__VdlySched.resume();
    }
}

void Vaxi4_top_tb___024root___eval_triggers__act(Vaxi4_top_tb___024root* vlSelf);

bool Vaxi4_top_tb___024root___eval_phase__act(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval_phase__act\n"); );
    // Init
    VlTriggerVec<3> __VpreTriggered;
    CData/*0:0*/ __VactExecute;
    // Body
    Vaxi4_top_tb___024root___eval_triggers__act(vlSelf);
    __VactExecute = vlSelf->__VactTriggered.any();
    if (__VactExecute) {
        __VpreTriggered.andNot(vlSelf->__VactTriggered, vlSelf->__VnbaTriggered);
        vlSelf->__VnbaTriggered.thisOr(vlSelf->__VactTriggered);
        Vaxi4_top_tb___024root___timing_resume(vlSelf);
        Vaxi4_top_tb___024root___eval_act(vlSelf);
    }
    return (__VactExecute);
}

bool Vaxi4_top_tb___024root___eval_phase__nba(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval_phase__nba\n"); );
    // Init
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = vlSelf->__VnbaTriggered.any();
    if (__VnbaExecute) {
        Vaxi4_top_tb___024root___eval_nba(vlSelf);
        vlSelf->__VnbaTriggered.clear();
    }
    return (__VnbaExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vaxi4_top_tb___024root___dump_triggers__nba(Vaxi4_top_tb___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void Vaxi4_top_tb___024root___dump_triggers__act(Vaxi4_top_tb___024root* vlSelf);
#endif  // VL_DEBUG

void Vaxi4_top_tb___024root___eval(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval\n"); );
    // Init
    IData/*31:0*/ __VnbaIterCount;
    CData/*0:0*/ __VnbaContinue;
    // Body
    __VnbaIterCount = 0U;
    __VnbaContinue = 1U;
    while (__VnbaContinue) {
        if (VL_UNLIKELY((0x64U < __VnbaIterCount))) {
#ifdef VL_DEBUG
            Vaxi4_top_tb___024root___dump_triggers__nba(vlSelf);
#endif
            VL_FATAL_MT("verif/axi4_top_tb.sv", 8, "", "NBA region did not converge.");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        __VnbaContinue = 0U;
        vlSelf->__VactIterCount = 0U;
        vlSelf->__VactContinue = 1U;
        while (vlSelf->__VactContinue) {
            if (VL_UNLIKELY((0x64U < vlSelf->__VactIterCount))) {
#ifdef VL_DEBUG
                Vaxi4_top_tb___024root___dump_triggers__act(vlSelf);
#endif
                VL_FATAL_MT("verif/axi4_top_tb.sv", 8, "", "Active region did not converge.");
            }
            vlSelf->__VactIterCount = ((IData)(1U) 
                                       + vlSelf->__VactIterCount);
            vlSelf->__VactContinue = 0U;
            if (Vaxi4_top_tb___024root___eval_phase__act(vlSelf)) {
                vlSelf->__VactContinue = 1U;
            }
        }
        if (Vaxi4_top_tb___024root___eval_phase__nba(vlSelf)) {
            __VnbaContinue = 1U;
        }
    }
}

#ifdef VL_DEBUG
void Vaxi4_top_tb___024root___eval_debug_assertions(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval_debug_assertions\n"); );
}
#endif  // VL_DEBUG
