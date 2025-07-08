module motor_controller(
    input clk,
    input rst,
    input wire [1:0] sel,
    output reg [1:0] sel_protected
);

    localparam IDLE                = 2'b00;
    localparam CLOCK_WISE         = 2'b01;
    localparam COUNTER_CLOCK_WISE = 2'b10;
    localparam PROTECTION         = 2'b11;

    reg [1:0] fsm_state, next_state;

    // Lógica de transición de estado sincronizada
    always @(negedge clk or posedge rst) begin
        if (rst)
            fsm_state <= IDLE;
        else
            fsm_state <= next_state;
    end

    // Lógica de próxima transición de estado
    always @(*) begin
        case (fsm_state)
            IDLE:               next_state = sel;
            CLOCK_WISE:         next_state = sel;
            COUNTER_CLOCK_WISE: next_state = sel;
            PROTECTION:         next_state = sel;
            default:            next_state = IDLE;
        endcase
    end

    // Lógica de salida
    always @(*) begin
        if (fsm_state == PROTECTION)
            sel_protected = 2'b00;
        else
            sel_protected = sel;
    end

endmodule