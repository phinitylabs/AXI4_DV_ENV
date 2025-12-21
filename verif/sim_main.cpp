// Verilator simulation main wrapper for timing-enabled simulation
// Compatible with Verilator 5.x --timing flag
#include "Vaxi4_slave_tb.h"
#include "verilated.h"
#include "verilated_cov.h"  // For coverage

int main(int argc, char** argv) {
    // Initialize Verilator context
    VerilatedContext* contextp = new VerilatedContext;
    contextp->commandArgs(argc, argv);
    contextp->debug(0);
    contextp->randReset(2);
    contextp->traceEverOn(false);  // Disable VCD for performance
    
    // Create instance of our module
    Vaxi4_slave_tb* top = new Vaxi4_slave_tb{contextp};
    
    // Main simulation loop for --timing enabled designs
    // Process events and advance time based on scheduled events
    while (!contextp->gotFinish()) {
        // Process all events at current time
        top->eval_step();
        
        // Check if there are more events pending
        if (top->eventsPending()) {
            // Advance time to the next scheduled event
            contextp->time(top->nextTimeSlot());
        } else {
            // No more events - simulation should be finishing
            break;
        }
    }
    
    // Final cleanup
    top->final();
    
    // Write coverage data
    VerilatedCov::write("coverage.dat");
    
    delete top;
    delete contextp;
    
    return 0;
}
