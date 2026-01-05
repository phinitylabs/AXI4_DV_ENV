// Verilator C++ wrapper for AXI4 Interrupt Testbench

#include "Vaxi4_top_tb.h"
#include "verilated.h"

#if VM_TRACE
#include "verilated_vcd_c.h"
#endif

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    
    VerilatedContext* contextp = new VerilatedContext;
    contextp->commandArgs(argc, argv);
    
    Vaxi4_top_tb* top = new Vaxi4_top_tb{contextp};

#if VM_TRACE
    VerilatedVcdC* tfp = nullptr;
    Verilated::traceEverOn(true);
    tfp = new VerilatedVcdC;
    top->trace(tfp, 99);
    tfp->open("axi4_top_tb.vcd");
#endif
    
    while (!contextp->gotFinish()) {
        contextp->timeInc(1);
        top->eval();
#if VM_TRACE
        if (tfp) tfp->dump(contextp->time());
#endif
    }

#if VM_TRACE
    if (tfp) {
        tfp->close();
        delete tfp;
    }
#endif

#if VM_COVERAGE
    // Write coverage data
    contextp->coveragep()->write("coverage.dat");
#endif
    
    delete top;
    delete contextp;
    
    return 0;
}

