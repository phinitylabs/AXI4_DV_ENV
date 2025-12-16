// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vaxi4_top_tb.h for the primary calling header

#include "Vaxi4_top_tb__pch.h"
#include "Vaxi4_top_tb__Syms.h"
#include "Vaxi4_top_tb___024root.h"

#ifdef VL_DEBUG
VL_ATTR_COLD void Vaxi4_top_tb___024root___dump_triggers__act(Vaxi4_top_tb___024root* vlSelf);
#endif  // VL_DEBUG

void Vaxi4_top_tb___024root___eval_triggers__act(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval_triggers__act\n"); );
    // Body
    vlSelf->__VactTriggered.set(0U, ((IData)(vlSelf->axi4_top_tb__DOT__clk) 
                                     & (~ (IData)(vlSelf->__Vtrigprevexpr___TOP__axi4_top_tb__DOT__clk__0))));
    vlSelf->__VactTriggered.set(1U, (((IData)(vlSelf->axi4_top_tb__DOT__clk) 
                                      & (~ (IData)(vlSelf->__Vtrigprevexpr___TOP__axi4_top_tb__DOT__clk__0))) 
                                     | ((~ (IData)(vlSelf->axi4_top_tb__DOT__resetn)) 
                                        & (IData)(vlSelf->__Vtrigprevexpr___TOP__axi4_top_tb__DOT__resetn__0))));
    vlSelf->__VactTriggered.set(2U, vlSelf->__VdlySched.awaitingCurrentTime());
    vlSelf->__Vtrigprevexpr___TOP__axi4_top_tb__DOT__clk__0 
        = vlSelf->axi4_top_tb__DOT__clk;
    vlSelf->__Vtrigprevexpr___TOP__axi4_top_tb__DOT__resetn__0 
        = vlSelf->axi4_top_tb__DOT__resetn;
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vaxi4_top_tb___024root___dump_triggers__act(vlSelf);
    }
#endif
}
