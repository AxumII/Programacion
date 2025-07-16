//========================================================
//  algorithmic_machine.sv — FSM de 17 estados (Mealy)
//========================================================
//  • Transición y salida dependen de «estado_actual» + bit
//    relevante del bus «sensor». 
//  • movement_sel: 4‑bit 
//  • sensor: 4‑bit 
//========================================================

module algorithmic_machine (
    input  wire        clk,
    input  wire        rst,           // reset activo en ‘1’
    input  wire [3:0]  sensor,        // {Left,Back,Right,Front} = {S3,S2,S1,S0}
    output reg  [3:0]  movement_sel   // 4‑bit código de movimiento
);

    //----------------------------------------------------//
    // 1 Estados (17 → 5 bits)
    //----------------------------------------------------//
    parameter
        IDLE    =  5'd0,
        // Orientación 1
        UP_1    =  5'd1, 
        RIGHT_1 = 5'd2,  
        DOWN_1 = 5'd3,  
        LEFT_1 = 5'd4,
        // Orientación 2
        UP_2    =  5'd5,
        RIGHT_2 = 5'd6,  
        DOWN_2 = 5'd7,  
        LEFT_2 = 5'd8,
        // Orientación 3
        UP_3    =  5'd9,  
        RIGHT_3 = 5'd10, 
        DOWN_3 = 5'd11, 
        LEFT_3 = 5'd12,
        // Orientación 4
        UP_4    =  5'd13, 
        RIGHT_4 = 5'd14, 
        DOWN_4 = 5'd15, 
        LEFT_4 = 5'd16;



   reg [1:0] estado_actual, estado_siguiente;

    //----------------------------------------------------//
    // 2 Registro de estado
    //----------------------------------------------------//
    always @(posedge clk or posedge rst) begin
        if (rst)
            estado_actual <= IDLE;
        else
            estado_actual <= estado_siguiente;
    end

    //----------------------------------------------------//
    // 3 TRANSICIÓN DE ESTADO  (Mealy style)
    //----------------------------------------------------//
    always_comb begin
        case (estado_actual)
            //--------------------------------------------------
            // ORIENTACIÓN 1
            //--------------------------------------------------
            IDLE    : estado_siguiente = sensor[0] ? UP_1    : IDLE; // arranque, no va a afectar luego
            UP_1    : estado_siguiente = sensor[0] ? RIGHT_1 : UP_1;
            RIGHT_1 : estado_siguiente = sensor[1] ? DOWN_1  : UP_2;
            DOWN_1  : estado_siguiente = sensor[3] ? LEFT_1  : UP_4;
            LEFT_1  : estado_siguiente = sensor[2] ? UP_1    : UP_2;
            //--------------------------------------------------
            // ORIENTACIÓN 2
            //--------------------------------------------------
            UP_2    : estado_siguiente = sensor[1] ? RIGHT_2 : UP_2;
            RIGHT_2 : estado_siguiente = sensor[2] ? DOWN_2  : UP_3;
            DOWN_2  : estado_siguiente = sensor[0] ? LEFT_2  : UP_1;
            LEFT_2  : estado_siguiente = sensor[3] ? UP_2    : UP_3;
            //--------------------------------------------------
            // ORIENTACIÓN 3
            //--------------------------------------------------
            UP_3    : estado_siguiente = sensor[2] ? RIGHT_3 : UP_3;
            RIGHT_3 : estado_siguiente = sensor[3] ? DOWN_3  : UP_4;
            DOWN_3  : estado_siguiente = sensor[1] ? LEFT_3  : UP_2;
            LEFT_3  : estado_siguiente = sensor[0] ? UP_3    : UP_4;
            //--------------------------------------------------
            // ORIENTACIÓN 4
            //--------------------------------------------------
            UP_4    : estado_siguiente = sensor[3] ? RIGHT_4 : UP_4;
            RIGHT_4 : estado_siguiente = sensor[0] ? DOWN_4  : UP_1;
            DOWN_4  : estado_siguiente = sensor[2] ? LEFT_4  : UP_3;
            LEFT_4  : estado_siguiente = sensor[1] ? UP_4    : UP_1;
            //--------------------------------------------------
            default : estado_siguiente = IDLE;
        endcase
    end

    //----------------------------------------------------//
    // 4 SALIDA MEALY — depende de estado y sensor
    //----------------------------------------------------//
    always_comb begin
        case (estado_actual)

            //STATE:OUT = INPUT ? (Aca vale1) out : (Aca vale0) out2
            //------------- ORIENTACIÓN 1 -------------------
            IDLE   : movement_sel = sensor[0] ? 4'0000 : 4'b0000;
            UP_1   : movement_sel = sensor[0] ? 4'0000 : 4'b0001;
            RIGHT_1: movement_sel = sensor[1] ? 4'0000 : 4'b0000;
            DOWN_1 : movement_sel = sensor[3] ? 4'0000 : 4'b0000;
            LEFT_1 : movement_sel = sensor[2] ? 4'0000 : 4'b0000;
            //------------- ORIENTACIÓN 2 -------------------
            UP_2   : movement_sel = sensor[1] ? 4'0000 : 4'b0100;
            RIGHT_2: movement_sel = sensor[2] ? 4'0000 : 4'b0000;
            DOWN_2 : movement_sel = sensor[0] ? 4'0000 : 4'b0000;
            LEFT_2 : movement_sel = sensor[3] ? 4'0000 : 4'b0000;
            //------------- ORIENTACIÓN 3 -------------------
            UP_3   : movement_sel = sensor[2] ? 4'0000 : 4'b0010;
            RIGHT_3: movement_sel = sensor[3] ? 4'0000 : 4'b0000;
            DOWN_3 : movement_sel = sensor[1] ? 4'0000 : 4'b0000;
            LEFT_3 : movement_sel = sensor[0] ? 4'0000 : 4'b0000;
            //------------- ORIENTACIÓN 4 -------------------
            UP_4   : movement_sel = sensor[3] ? 4'0000 : 4'b0011;
            RIGHT_4: movement_sel = sensor[0] ? 4'0000 : 4'b0000;
            DOWN_4 : movement_sel = sensor[2] ? 4'0000 : 4'b0000;
            LEFT_4 : movement_sel = sensor[1] ? 4'0000 : 4'b0000;
            //------------- IDLE / DEFAULT ------------------
            default: movement_sel = 4'b0000; // Idle
        endcase
    end

endmodule
