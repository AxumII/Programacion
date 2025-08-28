//========================================================
//  algorithmic_machine.sv — FSM de 16 estados (Mealy, sin IDLE)
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
    // 1 Estados (16 → 4 bits, sin IDLE)
    //----------------------------------------------------//
    parameter
        // Orientación 1
        UP_1    =  4'd0, 
        RIGHT_1 = 4'd1,  
        DOWN_1  = 4'd2,  
        LEFT_1  = 4'd3,
        // Orientación 2
        UP_2    =  4'd4,
        RIGHT_2 = 4'd5,  
        DOWN_2  = 4'd6,  
        LEFT_2  = 4'd7,
        // Orientación 3
        UP_3    =  4'd8,  
        RIGHT_3 = 4'd9, 
        DOWN_3  = 4'd10, 
        LEFT_3  = 4'd11,
        // Orientación 4
        UP_4    =  4'd12, 
        RIGHT_4 = 4'd13, 
        DOWN_4  = 4'd14, 
        LEFT_4  = 4'd15;

    reg [3:0] estado_actual, estado_siguiente;  // <--- Ahora 4 bits

    //----------------------------------------------------//
    // 2 Registro de estado
    //----------------------------------------------------//
    always @(posedge clk or posedge rst) begin
        if (rst)
            estado_actual <= UP_1; // Ahora el reset va a UP_1
        else
            estado_actual <= estado_siguiente;
    end

    //----------------------------------------------------//
    // 3 TRANSICIÓN DE ESTADO  (Mealy style)
    //----------------------------------------------------//
    always @(posedge clk) begin
        case (estado_actual)
            //--------------------------------------------------
            // ORIENTACIÓN 1
            //--------------------------------------------------
            UP_1    : estado_siguiente = sensor[0] ? RIGHT_1 : UP_1;
            RIGHT_1 : estado_siguiente = sensor[1] ? LEFT_1  : UP_2;
            LEFT_1  : estado_siguiente = sensor[3] ? DOWN_1  : UP_4;
            DOWN_1  : estado_siguiente = sensor[2] ? UP_1    : UP_2;
            //--------------------------------------------------
            // ORIENTACIÓN 2
            //--------------------------------------------------
            UP_2    : estado_siguiente = sensor[1] ? RIGHT_2 : UP_2;
            RIGHT_2 : estado_siguiente = sensor[2] ? LEFT_2  : UP_3;
            LEFT_2  : estado_siguiente = sensor[0] ? DOWN_2  : UP_1;
            DOWN_2  : estado_siguiente = sensor[3] ? UP_2    : UP_3;
            //--------------------------------------------------
            // ORIENTACIÓN 3
            //--------------------------------------------------
            UP_3    : estado_siguiente = sensor[2] ? RIGHT_3 : UP_3;
            RIGHT_3 : estado_siguiente = sensor[3] ? LEFT_3  : UP_4;
            LEFT_3  : estado_siguiente = sensor[1] ? DOWN_3  : UP_2;
            DOWN_3  : estado_siguiente = sensor[0] ? UP_3    : UP_4;
            //--------------------------------------------------
            // ORIENTACIÓN 4
            //--------------------------------------------------
            UP_4    : estado_siguiente = sensor[3] ? RIGHT_4 : UP_4;
            RIGHT_4 : estado_siguiente = sensor[0] ? LEFT_4  : UP_1;
            LEFT_4  : estado_siguiente = sensor[2] ? DOWN_4  : UP_3;
            DOWN_4  : estado_siguiente = sensor[1] ? UP_4    : UP_1;
            //--------------------------------------------------
            default : estado_siguiente = UP_1; // default ahora es UP_1
        endcase
    end

    //----------------------------------------------------//
    // 4 SALIDA MEALY — depende de estado y sensor
    //----------------------------------------------------//
    always @(posedge clk) begin
        case (estado_actual)
            //------------- ORIENTACIÓN 1 -------------------
            UP_1   : movement_sel = sensor[0] ? 4'b0000 : 4'b0001;
            RIGHT_1: movement_sel = sensor[1] ? 4'b0000 : 4'b0000;
            DOWN_1 : movement_sel = sensor[2] ? 4'b0000 : 4'b0000;
            LEFT_1 : movement_sel = sensor[3] ? 4'b0000 : 4'b0000;
            //------------- ORIENTACIÓN 2 -------------------
            UP_2   : movement_sel = sensor[1] ? 4'b0000 : 4'b0011;
            RIGHT_2: movement_sel = sensor[2] ? 4'b0000 : 4'b0000;
            DOWN_2 : movement_sel = sensor[3] ? 4'b0000 : 4'b0000;
            LEFT_2 : movement_sel = sensor[0] ? 4'b0000 : 4'b0000;
            //------------- ORIENTACIÓN 3 -------------------
            UP_3   : movement_sel = sensor[2] ? 4'b0000 : 4'b0010;
            RIGHT_3: movement_sel = sensor[3] ? 4'b0000 : 4'b0000;
            DOWN_3 : movement_sel = sensor[0] ? 4'b0000 : 4'b0000;
            LEFT_3 : movement_sel = sensor[1] ? 4'b0000 : 4'b0000;
            //------------- ORIENTACIÓN 4 -------------------
            UP_4   : movement_sel = sensor[3] ? 4'b0000 : 4'b0100;
            RIGHT_4: movement_sel = sensor[0] ? 4'b0000 : 4'b0000;
            DOWN_4 : movement_sel = sensor[1] ? 4'b0000 : 4'b0000;
            LEFT_4 : movement_sel = sensor[2] ? 4'b0000 : 4'b0000;
            //------------- DEFAULT ------------------
            default: movement_sel = 4'b0000; // Ahora default es UP_1
        endcase
    end

endmodule