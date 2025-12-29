// Verilator simulation main for AXI4 Slave Testbench
#include "Vaxi4_slave_tb.h"
#include "verilated.h"
#include <iostream>
#include <memory>

int main(int argc, char** argv) {
    // Create context
    const std::unique_ptr<VerilatedContext> contextp{new VerilatedContext};
    contextp->commandArgs(argc, argv);
    contextp->traceEverOn(true);
    
    // Create instance of the testbench
    const std::unique_ptr<Vaxi4_slave_tb> tb{new Vaxi4_slave_tb{contextp.get()}};
    
    // Simulation loop - run until $finish is called
    while (!contextp->gotFinish()) {
        // Evaluate the model
        tb->eval();
        
        // Advance time
        contextp->timeInc(1);
        
        // Safety limit
        if (contextp->time() > 10000000) {
            std::cerr << "Simulation timeout!" << std::endl;
            break;
        }
    }
    
    // Final evaluation
    tb->final();
    
    return 0;
}
