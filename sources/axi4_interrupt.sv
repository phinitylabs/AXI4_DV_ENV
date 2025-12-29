// AXI4 Interrupt Controller Module - Complete Implementation
// This module handles interrupt requests and acknowledgments

module axi4_interrupt (
    input logic clk,
    input logic resetn,
    input logic interrupt_req,
    output logic interrupt_ack
);

    // Interrupt controller state
    typedef enum logic [1:0] {
        IDLE,
        PENDING,
        ACKNOWLEDGED
    } interrupt_state_t;
    
    interrupt_state_t state, next_state;
    
    // Interrupt state machine
    always_ff @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            state <= IDLE;
            interrupt_ack <= 1'b0;
        end else begin
            state <= next_state;
            case (next_state)
                IDLE: interrupt_ack <= 1'b0;
                PENDING: interrupt_ack <= 1'b0;
                ACKNOWLEDGED: interrupt_ack <= 1'b1;
            endcase
        end
    end
    
    // Next state logic
    always_comb begin
        next_state = state;
        case (state)
            IDLE: begin
                if (interrupt_req) begin
                    next_state = PENDING;
                end
            end
            PENDING: begin
                // Acknowledge the interrupt
                next_state = ACKNOWLEDGED;
            end
            ACKNOWLEDGED: begin
                if (!interrupt_req) begin
                    next_state = IDLE;
                end
            end
        endcase
    end

endmodule

