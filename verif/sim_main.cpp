#include <verilated.h>
#include "Vaxi4_top_tb.h"

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    Vaxi4_top_tb* top = new Vaxi4_top_tb;
    while (!Verilated::gotFinish()) {
        top->eval();
    }
    top->final();
    delete top;
    return 0;
}
