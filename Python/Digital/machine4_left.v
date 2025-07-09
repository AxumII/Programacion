module machine4_left(
    input clk,
    input rst,
    input wire [3:0] sensor,
    output reg [1:0] state_control,
    output reg [3:0] movement_sel,
);
  
  //----------------------//
    //  Codificación estados

    localparam [1:0]  UP    = 2'b00,
                      RIGHT = 2'b01,
                      DOWN  = 2'b10,
                      LEFT  = 2'b11;

    reg [1:0] estado_actual, estado_siguiente;

    //------------------------------//
    //  Registro de estado (FF-D)
    //------------------------------//
    always @(posedge clk or posedge rst) begin
        if (rst)
            estado_actual <= UP;       
        else
            estado_actual <= estado_siguiente;
    end

    //---------------------------------------------------//
    //  Próximo estado  

    always @(*) begin
        case (estado_actual)
            UP:    estado_siguiente = sensor[0] ? RIGHT : UP;
            RIGHT: estado_siguiente = sensor[1] ? DOWN  : RIGHT;
            DOWN:  estado_siguiente = sensor[2] ? LEFT  : DOWN;
            LEFT:  estado_siguiente = sensor[3] ? UP    : LEFT;
            default: estado_siguiente = UP;
        endcase
    end

    //---------------------------------------------------//
    //  Salidas

    always @(*) begin
        // Valores por defecto 
        state_control = 2'b00;
        movement_sel  = 4'b0000;

        case (estado_actual)
            //-----------  UP  -----------
            UP: begin
                if (sensor[3]) begin               // bit = 1
                    state_control = 2'b00;         // 0
                    movement_sel  = 4'b0000;       // 0
                end else begin                     // bit = 0
                    state_control = 2'b00;         // 0
                    movement_sel  = 4'b0011;       // 3
                end
            end
            //-----------  RIGHT -----------
            RIGHT: begin
                if (sensor[0]) begin
                    state_control = 2'b00;         // 0
                    movement_sel  = 4'b0000;       // 0
                end else begin
                    state_control = 2'b01;         // 1
                    movement_sel  = 4'b0010;       // 2
                end
            end
            //-----------  DOWN -----------
            DOWN: begin
                if (sensor[1]) begin
                    state_control = 2'b00;         // 0
                    movement_sel  = 4'b0000;       // 0
                end else begin
                    state_control = 2'b01;         // 1
                    movement_sel  = 4'b0000;       // 0
                end
            end
            //-----------  LEFT -----------
            LEFT: begin
                if (sensor[2]) begin
                    state_control = 2'b00;         // 0
                    movement_sel  = 4'b0000;       // 0
                end else begin
                    state_control = 2'b10;         // 2
                    movement_sel  = 4'b0001;       // 1
                end
            end
        endcase
    end

endmodule