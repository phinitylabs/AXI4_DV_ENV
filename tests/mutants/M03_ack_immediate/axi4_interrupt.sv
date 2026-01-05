// MUTANT M03: Immediate Acknowledge Bug
// Bug: interrupt_ack asserts immediately without PENDING state

module axi4_interrupt (
    input logic clk,
    input logic resetn,
    input logic interrupt_req,
    output logic interrupt_ack
);

    typedef enum logic [1:0] {
        IDLE,
        PENDING,
        ACKNOWLEDGED
    } interrupt_state_t;
    
    interrupt_state_t state, next_state;
    
    always_ff @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            state <= IDLE;
            interrupt_ack <= 1'b0;
        end else begin
            state <= next_state;
            // BUG: Acknowledge immediately on request (skips PENDING)
            interrupt_ack <= interrupt_req;  // BUG: Should follow state machine
        end
    end
    
    always_comb begin
        next_state = state;
        case (state)
            IDLE: begin
                if (interrupt_req) next_state = ACKNOWLEDGED;  // BUG: Skips PENDING
            end
            PENDING: begin
                next_state = ACKNOWLEDGED;
            end
            ACKNOWLEDGED: begin
                if (!interrupt_req) next_state = IDLE;
            end
        endcase
    end

endmodule

