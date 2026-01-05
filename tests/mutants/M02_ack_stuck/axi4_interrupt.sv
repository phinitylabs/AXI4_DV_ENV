// MUTANT M02: Acknowledge Stuck High Bug
// Bug: interrupt_ack stays HIGH after request deasserts

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
            case (next_state)
                IDLE: interrupt_ack <= interrupt_ack;  // BUG: Should be 0
                PENDING: interrupt_ack <= 1'b0;
                ACKNOWLEDGED: interrupt_ack <= 1'b1;
            endcase
        end
    end
    
    always_comb begin
        next_state = state;
        case (state)
            IDLE: begin
                if (interrupt_req) next_state = PENDING;
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

