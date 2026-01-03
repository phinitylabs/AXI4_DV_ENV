#include <verilated.h>
#include <verilated_cov.h>
#include "Vaxi4_top_tb.h"

int main(int argc, char** argv) {
    VerilatedContext* contextp = new VerilatedContext;
    contextp->commandArgs(argc, argv);
    
    Vaxi4_top_tb* top = new Vaxi4_top_tb{contextp};
    
    while (!contextp->gotFinish()) {
        contextp->timeInc(1);
        top->eval();
    }
    
    top->final();
    
    // Explicitly write coverage data
    VerilatedCov::write("coverage.dat");
    
    delete top;
    delete contextp;
    return 0;
}
