// Verilator C++ wrapper for AXI4 Interrupt Testbench

#include "Vaxi4_top_tb.h"
#include "verilated.h"
#include "verilated_vcd_c.h"

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    
    VerilatedContext* contextp = new VerilatedContext;
    contextp->commandArgs(argc, argv);
    
    Vaxi4_top_tb* top = new Vaxi4_top_tb{contextp};
    
    VerilatedVcdC* tfp = nullptr;
    Verilated::traceEverOn(true);
    tfp = new VerilatedVcdC;
    top->trace(tfp, 99);
    tfp->open("axi4_top_tb.vcd");
    
    while (!contextp->gotFinish()) {
        contextp->timeInc(1);
        top->eval();
        if (tfp) tfp->dump(contextp->time());
    }
    
    if (tfp) {
        tfp->close();
        delete tfp;
    }
    
    // Write coverage data
    contextp->coveragep()->write("coverage.dat");
    
    delete top;
    delete contextp;
    
    return 0;
}

