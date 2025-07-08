module motor_controller(
    input clk,
    input rst,
    input wire [3:0] movement_sel,
    output reg [7:0] sel
);

    localparam IDLE                             = 4'b0000;
    localparam FORWARD                          = 4'b0001;
    localparam BACK                             = 4'b0010;
    localparam RIGHT                            = 4'b0011;
    localparam LEFT                             = 4'b0100;
    localparam RIGHT_UPPER_DIAGONAL             = 4'b0101;
    localparam RIGHT_DOWN_DIAGONAL              = 4'b0110;
    localparam LEFT_UPPER_DIAGONAL              = 4'b0111;
    localparam LEFT_DOWN_DIAGONAL               = 4'b1000;
    localparam RADIUS_VERT_ROT_CLOCKWISE        = 4'b1001;
    localparam RADIUS_VERT_ROT_COUNTERCLOCKWISE = 4'b1010;
    localparam RADIUS_HORIZ_ROT_CLOCKWISE       = 4'b1011;
    localparam RADIUS_HORIZ_ROT_COUNTERCLOCKWISE= 4'b1100;
    localparam CENTER_ROT_CLOCKWISE             = 4'b1101;
    localparam CENTER_ROT_COUNTERCLOCKWISE      = 4'b1110;

    reg [3:0] fsm_state, next_state;

    // Lógica de transición de estado sincronizada
    always @(posedge clk or posedge rst) begin
        if (rst)
            fsm_state <= IDLE;
        else
            fsm_state <= next_state;
    end

    // Lógica para determinar el próximo estado según la entrada
    always @(*) begin
        case (movement_sel)
            IDLE:                             next_state = IDLE;
            FORWARD:                          next_state = FORWARD;
            BACK:                             next_state = BACK;
            RIGHT:                            next_state = RIGHT;
            LEFT:                             next_state = LEFT;
            RIGHT_UPPER_DIAGONAL:             next_state = RIGHT_UPPER_DIAGONAL;
            RIGHT_DOWN_DIAGONAL:              next_state = RIGHT_DOWN_DIAGONAL;
            LEFT_UPPER_DIAGONAL:              next_state = LEFT_UPPER_DIAGONAL;
            LEFT_DOWN_DIAGONAL:               next_state = LEFT_DOWN_DIAGONAL;
            RADIUS_VERT_ROT_CLOCKWISE:        next_state = RADIUS_VERT_ROT_CLOCKWISE;
            RADIUS_VERT_ROT_COUNTERCLOCKWISE: next_state = RADIUS_VERT_ROT_COUNTERCLOCKWISE;
            RADIUS_HORIZ_ROT_CLOCKWISE:       next_state = RADIUS_HORIZ_ROT_CLOCKWISE;
            RADIUS_HORIZ_ROT_COUNTERCLOCKWISE:next_state = RADIUS_HORIZ_ROT_COUNTERCLOCKWISE;
            CENTER_ROT_CLOCKWISE:             next_state = CENTER_ROT_CLOCKWISE;
            CENTER_ROT_COUNTERCLOCKWISE:      next_state = CENTER_ROT_COUNTERCLOCKWISE;
            default:                          next_state = IDLE;
        endcase
    end

    // Lógica de salida para cada estado de la FSM
    always @(*) begin
        case (fsm_state)
            IDLE:                              sel = 8'b0000_0000; // Motores apagados
            FORWARD:                           sel = 8'b0101_0101; // Avanzar recto
            BACK:                              sel = 8'b1010_1010; // Retroceder recto
            RIGHT:                             sel = 8'b0110_1001; // Girar derecha
            LEFT:                              sel = 8'b1001_0110; // Girar izquierda
            RIGHT_UPPER_DIAGONAL:              sel = 8'b0100_0001; // Diagonal sup derecha
            RIGHT_DOWN_DIAGONAL:               sel = 8'b0010_1000; // Diagonal inf derecha
            LEFT_UPPER_DIAGONAL:               sel = 8'b1000_0010; // Diagonal sup izquierda
            LEFT_DOWN_DIAGONAL:                sel = 8'b1001_0100; // Diagonal inf izquierda
            RADIUS_VERT_ROT_CLOCKWISE:         sel = 8'b0001_0001; // Rotar vertical, reloj
            RADIUS_VERT_ROT_COUNTERCLOCKWISE:  sel = 8'b0100_0100; // Rotar vertical, antirrel.
            RADIUS_HORIZ_ROT_CLOCKWISE:        sel = 8'b0000_0101; // Rotar horizontal, reloj
            RADIUS_HORIZ_ROT_COUNTERCLOCKWISE: sel = 8'b1001_1010; // Rotar horizontal, antirrel.
            CENTER_ROT_CLOCKWISE:              sel = 8'b1001_1001; // Giro centro, reloj
            CENTER_ROT_COUNTERCLOCKWISE:       sel = 8'b0110_0110; // Giro centro, antirrel.
            default:                           sel = 8'b0000_0000; // Por si las moscas
        endcase
    end

endmodule
