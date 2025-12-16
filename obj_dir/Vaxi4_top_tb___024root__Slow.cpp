// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vaxi4_top_tb.h for the primary calling header

#include "Vaxi4_top_tb__pch.h"
#include "Vaxi4_top_tb__Syms.h"
#include "Vaxi4_top_tb___024root.h"

void Vaxi4_top_tb___024root___ctor_var_reset(Vaxi4_top_tb___024root* vlSelf);

Vaxi4_top_tb___024root::Vaxi4_top_tb___024root(Vaxi4_top_tb__Syms* symsp, const char* v__name)
    : VerilatedModule{v__name}
    , __VdlySched{*symsp->_vm_contextp__}
    , vlSymsp{symsp}
 {
    // Reset structure values
    Vaxi4_top_tb___024root___ctor_var_reset(this);
}

void Vaxi4_top_tb___024root::__Vconfigure(bool first) {
    if (false && first) {}  // Prevent unused
}

Vaxi4_top_tb___024root::~Vaxi4_top_tb___024root() {
}
