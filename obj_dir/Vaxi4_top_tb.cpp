// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vaxi4_top_tb__pch.h"

//============================================================
// Constructors

Vaxi4_top_tb::Vaxi4_top_tb(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vaxi4_top_tb__Syms(contextp(), _vcname__, this)}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vaxi4_top_tb::Vaxi4_top_tb(const char* _vcname__)
    : Vaxi4_top_tb(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vaxi4_top_tb::~Vaxi4_top_tb() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vaxi4_top_tb___024root___eval_debug_assertions(Vaxi4_top_tb___024root* vlSelf);
#endif  // VL_DEBUG
void Vaxi4_top_tb___024root___eval_static(Vaxi4_top_tb___024root* vlSelf);
void Vaxi4_top_tb___024root___eval_initial(Vaxi4_top_tb___024root* vlSelf);
void Vaxi4_top_tb___024root___eval_settle(Vaxi4_top_tb___024root* vlSelf);
void Vaxi4_top_tb___024root___eval(Vaxi4_top_tb___024root* vlSelf);

void Vaxi4_top_tb::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vaxi4_top_tb::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vaxi4_top_tb___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        vlSymsp->__Vm_didInit = true;
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vaxi4_top_tb___024root___eval_static(&(vlSymsp->TOP));
        Vaxi4_top_tb___024root___eval_initial(&(vlSymsp->TOP));
        Vaxi4_top_tb___024root___eval_settle(&(vlSymsp->TOP));
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vaxi4_top_tb___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vaxi4_top_tb::eventsPending() { return !vlSymsp->TOP.__VdlySched.empty(); }

uint64_t Vaxi4_top_tb::nextTimeSlot() { return vlSymsp->TOP.__VdlySched.nextTimeSlot(); }

//============================================================
// Utilities

const char* Vaxi4_top_tb::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vaxi4_top_tb___024root___eval_final(Vaxi4_top_tb___024root* vlSelf);

VL_ATTR_COLD void Vaxi4_top_tb::final() {
    Vaxi4_top_tb___024root___eval_final(&(vlSymsp->TOP));
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vaxi4_top_tb::hierName() const { return vlSymsp->name(); }
const char* Vaxi4_top_tb::modelName() const { return "Vaxi4_top_tb"; }
unsigned Vaxi4_top_tb::threads() const { return 1; }
void Vaxi4_top_tb::prepareClone() const { contextp()->prepareClone(); }
void Vaxi4_top_tb::atClone() const {
    contextp()->threadPoolpOnClone();
}

//============================================================
// Trace configuration

VL_ATTR_COLD void Vaxi4_top_tb::trace(VerilatedVcdC* tfp, int levels, int options) {
    vl_fatal(__FILE__, __LINE__, __FILE__,"'Vaxi4_top_tb::trace()' called on model that was Verilated without --trace option");
}
