//================ algorithmic_machine.v ================//
module algorithmic_machine (
    input  wire        clk,
    input  wire        rst,           // reset global activo en ‘1’
    input  wire [3:0]  sensor,        // bus compartido
    output reg  [3:0]  movement_sel   // salida combinada
);

    //--------------------------------------------------------//
    // 1) Estados de la FSM codificados (el subindice dice que grupo pertenece)
    //--------------------------------------------------------//
    parameter           IDLE = 5 b0000
                    UP_1    = 5'b0000,
                      RIGHT_1 = 5'b,
                      DOWN_1  = 5'b,
                      LEFT_1  = 5'b,
                      UP_2    = 5'b,
                      RIGHT_2 = 5'b,
                      DOWN_2  = 5'b,
                      LEFT_2  = 5'b,
                      UP_3    = 5'b,
                      RIGHT_3 = 5'b,
                      DOWN_3  = 5'b,
                      LEFT_3  = 5'b,
                      UP_4    = 5'b,
                      RIGHT_4 = 5'b,
                      DOWN_4  = 5'b,
                      LEFT_4  = 5'b;    
                      ;

    reg [1:0] estado_actual, estado_siguiente;

    //--------------------------------------------------------//
    // 2) Conexiones con otros modulos
    //--------------------------------------------------------//
 

    //--------------------------------------------------------//
    // 3) Registro de estado (máquina principal)
    //--------------------------------------------------------//
          always @(posedge clk or posedge rst) begin
        if (rst)
            estado_actual <= IDLE;       
        else
            estado_actual <= estado_siguiente;
    end
    //--------------------------------------------------------//
    // 4) Lógica de transición
    //   
    //--------------------------------------------------------//
    always @(*) begin
        case (estado_actual)
            UP:    estado_siguiente = sensor[0] ? RIGHT : UP;
            RIGHT: estado_siguiente = sensor[1] ? DOWN  : RIGHT;
            DOWN:  estado_siguiente = sensor[2] ? LEFT  : DOWN;
            LEFT:  estado_siguiente = sensor[3] ? UP    : LEFT;
            default: estado_siguiente = UP;
        endcase
    end
    //--------------------------------------------------------//
    // 5) Salida: copia la de la máquina actualmente activa
    //--------------------------------------------------------//
    always @(*) begin
        // Valores por defecto 
        movement_sel  = 4'b0000;

        case (estado_actual)
            
        endcase
    end

endmodule
