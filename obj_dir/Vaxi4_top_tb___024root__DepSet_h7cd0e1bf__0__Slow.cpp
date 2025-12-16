// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vaxi4_top_tb.h for the primary calling header

#include "Vaxi4_top_tb__pch.h"
#include "Vaxi4_top_tb__Syms.h"
#include "Vaxi4_top_tb___024root.h"

VL_ATTR_COLD void Vaxi4_top_tb___024root___eval_initial__TOP(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval_initial__TOP\n"); );
    // Init
    VlWide<4>/*127:0*/ __Vtemp_1;
    // Body
    __Vtemp_1[0U] = 0x2e766364U;
    __Vtemp_1[1U] = 0x705f7462U;
    __Vtemp_1[2U] = 0x345f746fU;
    __Vtemp_1[3U] = 0x617869U;
    vlSymsp->_vm_contextp__->dumpfile(VL_CVT_PACK_STR_NW(4, __Vtemp_1));
    vlSymsp->_traceDumpOpen();
    VL_WRITEF("==========================================\nAXI4 Golden Testbench Started\n==========================================\n");
    vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__unnamedblk1__DOT__i = 0U;
    while (VL_GTS_III(32, 0x100U, vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__unnamedblk1__DOT__i)) {
        vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__memory[(0xffU 
                                                                & vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__unnamedblk1__DOT__i)] = 0U;
        vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__unnamedblk1__DOT__i 
            = ((IData)(1U) + vlSelf->axi4_top_tb__DOT__dut__DOT__slave__DOT__unnamedblk1__DOT__i);
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vaxi4_top_tb___024root___dump_triggers__stl(Vaxi4_top_tb___024root* vlSelf);
#endif  // VL_DEBUG

VL_ATTR_COLD void Vaxi4_top_tb___024root___eval_triggers__stl(Vaxi4_top_tb___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vaxi4_top_tb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vaxi4_top_tb___024root___eval_triggers__stl\n"); );
    // Body
    vlSelf->__VstlTriggered.set(0U, (IData)(vlSelf->__VstlFirstIteration));
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vaxi4_top_tb___024root___dump_triggers__stl(vlSelf);
    }
#endif
}
