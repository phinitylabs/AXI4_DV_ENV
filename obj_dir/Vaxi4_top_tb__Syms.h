// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VAXI4_TOP_TB__SYMS_H_
#define VERILATED_VAXI4_TOP_TB__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vaxi4_top_tb.h"

// INCLUDE MODULE CLASSES
#include "Vaxi4_top_tb___024root.h"

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES)Vaxi4_top_tb__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vaxi4_top_tb* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vaxi4_top_tb___024root         TOP;

    // CONSTRUCTORS
    Vaxi4_top_tb__Syms(VerilatedContext* contextp, const char* namep, Vaxi4_top_tb* modelp);
    ~Vaxi4_top_tb__Syms();

    // METHODS
    const char* name() { return TOP.name(); }
};

#endif  // guard
