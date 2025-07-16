//========================================================
//  algorithmic_machine.sv — FSM de 17 estados (Mealy)
//========================================================
//  • Transición y salida dependen de «estado_actual» + bit
//    relevante del bus «sensor».  No usamos casez/unique; se
//    emplea un case clásico para mayor claridad didáctica.
//  • movement_sel: 4‑bit (0000‑1111) — códigos ejemplo (puedes
//    cambiarlos).
//========================================================

module algorithmic_machine (
    input  wire        clk,
    input  wire        rst,           // reset asíncrono activo en ‘1’
    input  wire [3:0]  sensor,        // {Left,Back,Right,Front} = {S3,S2,S1,S0}
    output reg  [3:0]  movement_sel   // 4‑bit código de movimiento
);

    //----------------------------------------------------//
    // 1) Estados (17 → 5 bits)
    //----------------------------------------------------//
    typedef enum logic [4:0] {
        IDLE    =  5'd0,
        // Orientación 1
        UP_1    =  5'd1,  RIGHT_1 = 5'd2,  DOWN_1 = 5'd3,  LEFT_1 = 5'd4,
        // Orientación 2
        UP_2    =  5'd5,  RIGHT_2 = 5'd6,  DOWN_2 = 5'd7,  LEFT_2 = 5'd8,
        // Orientación 3
        UP_3    =  5'd9,  RIGHT_3 = 5'd10, DOWN_3 = 5'd11, LEFT_3 = 5'd12,
        // Orientación 4
        UP_4    =  5'd13, RIGHT_4 = 5'd14, DOWN_4 = 5'd15, LEFT_4 = 5'd16
    } state_t;

    state_t estado_actual, estado_siguiente;

    //----------------------------------------------------//
    // 2) Registro de estado
    //----------------------------------------------------//
    always_ff @(posedge clk or posedge rst) begin
        if (rst)
            estado_actual <= IDLE;
        else
            estado_actual <= estado_siguiente;
    end

    //----------------------------------------------------//
    // 3) TRANSICIÓN DE ESTADO  (Mealy style)
    //    — Se comprueba *únicamente* el bit que le corresponde a
    //      cada orientación: S0 (Front) en UP, S1 (Right) en RIGHT…
    //----------------------------------------------------//
    always_comb begin
        case (estado_actual)
            //--------------------------------------------------
            // ORIENTACIÓN 1
            //--------------------------------------------------
            IDLE    : estado_siguiente = sensor[0] ? UP_1    : IDLE; // arranque
            UP_1    : estado_siguiente = sensor[0] ? RIGHT_1 : UP_1;
            RIGHT_1 : estado_siguiente = sensor[1] ? DOWN_1  : RIGHT_1;
            DOWN_1  : estado_siguiente = sensor[2] ? LEFT_1  : DOWN_1;
            LEFT_1  : estado_siguiente = sensor[3] ? UP_2    : LEFT_1;
            //--------------------------------------------------
            // ORIENTACIÓN 2
            //--------------------------------------------------
            UP_2    : estado_siguiente = sensor[0] ? RIGHT_2 : UP_2;
            RIGHT_2 : estado_siguiente = sensor[1] ? DOWN_2  : RIGHT_2;
            DOWN_2  : estado_siguiente = sensor[2] ? LEFT_2  : DOWN_2;
            LEFT_2  : estado_siguiente = sensor[3] ? UP_3    : LEFT_2;
            //--------------------------------------------------
            // ORIENTACIÓN 3
            //--------------------------------------------------
            UP_3    : estado_siguiente = sensor[0] ? RIGHT_3 : UP_3;
            RIGHT_3 : estado_siguiente = sensor[1] ? DOWN_3  : RIGHT_3;
            DOWN_3  : estado_siguiente = sensor[2] ? LEFT_3  : DOWN_3;
            LEFT_3  : estado_siguiente = sensor[3] ? UP_4    : LEFT_3;
            //--------------------------------------------------
            // ORIENTACIÓN 4
            //--------------------------------------------------
            UP_4    : estado_siguiente = sensor[0] ? RIGHT_4 : UP_4;
            RIGHT_4 : estado_siguiente = sensor[1] ? DOWN_4  : RIGHT_4;
            DOWN_4  : estado_siguiente = sensor[2] ? LEFT_4  : DOWN_4;
            LEFT_4  : estado_siguiente = sensor[3] ? UP_1    : LEFT_4;
            //--------------------------------------------------
            default : estado_siguiente = IDLE;
        endcase
    end

    //----------------------------------------------------//
    // 4) SALIDA MEALY — depende de estado y sensor
    //----------------------------------------------------//
    always_comb begin
        case (estado_actual)
            //------------- ORIENTACIÓN 1 -------------------
            UP_1   : movement_sel = sensor[0] ? 4'b0011 /*Right*/ : 4'b0001 /*Fw*/;
            RIGHT_1: movement_sel = sensor[1] ? 4'b0010 /*Back*/  : 4'b0011 /*Right*/;
            DOWN_1 : movement_sel = sensor[2] ? 4'b0100 /*Left*/  : 4'b0010 /*Back*/;
            LEFT_1 : movement_sel = sensor[3] ? 4'b0001 /*Fw*/    : 4'b0100 /*Left*/;
            //------------- ORIENTACIÓN 2 -------------------
            UP_2   : movement_sel = sensor[0] ? 4'b0011 : 4'b0001;
            RIGHT_2: movement_sel = sensor[1] ? 4'b0010 : 4'b0011;
            DOWN_2 : movement_sel = sensor[2] ? 4'b0100 : 4'b0010;
            LEFT_2 : movement_sel = sensor[3] ? 4'b0001 : 4'b0100;
            //------------- ORIENTACIÓN 3 -------------------
            UP_3   : movement_sel = sensor[0] ? 4'b0011 : 4'b0001;
            RIGHT_3: movement_sel = sensor[1] ? 4'b0010 : 4'b0011;
            DOWN_3 : movement_sel = sensor[2] ? 4'b0100 : 4'b0010;
            LEFT_3 : movement_sel = sensor[3] ? 4'b0001 : 4'b0100;
            //------------- ORIENTACIÓN 4 -------------------
            UP_4   : movement_sel = sensor[0] ? 4'b0011 : 4'b0001;
            RIGHT_4: movement_sel = sensor[1] ? 4'b0010 : 4'b0011;
            DOWN_4 : movement_sel = sensor[2] ? 4'b0100 : 4'b0010;
            LEFT_4 : movement_sel = sensor[3] ? 4'b0001 : 4'b0100;
            //------------- IDLE / DEFAULT ------------------
            default: movement_sel = 4'b0000; // Idle
        endcase
    end

endmodule
