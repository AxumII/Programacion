//================ principal_machine_search.v ================//
module principal_machine_search (
    input  wire        clk,
    input  wire        rst,           // reset global activo en ‘1’
    input  wire [3:0]  sensor,        // bus compartido
    output reg  [3:0]  movement_sel   // salida combinada
);

    //--------------------------------------------------------//
    // 1) Estados de la FSM principal (una por cada sub-máquina)
    //--------------------------------------------------------//
    localparam [1:0] M1 = 2'b00,
                     M2 = 2'b01,
                     M3 = 2'b10,
                     M4 = 2'b11;

    reg  [1:0] state_cur, state_nxt;

    //--------------------------------------------------------//
    // 2) Conexiones a las cuatro sub-máquinas
    //--------------------------------------------------------//
    wire [1:0] sc_M1, sc_M2, sc_M3, sc_M4;   // state_control
    wire [3:0] mv_M1, mv_M2, mv_M3, mv_M4;   // movement_sel

    machine1_up     u_M1 (.clk(clk), .rst(rst), .sensor(sensor),
                          .state_control(sc_M1), .movement_sel(mv_M1));

    machine2_right  u_M2 (.clk(clk), .rst(rst), .sensor(sensor),
                          .state_control(sc_M2), .movement_sel(mv_M2));

    machine3_down   u_M3 (.clk(clk), .rst(rst), .sensor(sensor),
                          .state_control(sc_M3), .movement_sel(mv_M3));

    machine4_left   u_M4 (.clk(clk), .rst(rst), .sensor(sensor),
                          .state_control(sc_M4), .movement_sel(mv_M4));

    //--------------------------------------------------------//
    // 3) Registro de estado (máquina principal)
    //--------------------------------------------------------//
    always @(posedge clk or posedge rst) begin
        if (rst)
            state_cur <= M1;          // arranque en M1
        else
            state_cur <= state_nxt;
    end

    //--------------------------------------------------------//
    // 4) Lógica de transición
    //    0 = quedarse | 1 = siguiente | 2 = anterior (wrap)
    //--------------------------------------------------------//
    always @(*) begin
        state_nxt = state_cur;        // valor por defecto

        case (state_cur)
            //----------------------------------------------//
            M1: case (sc_M1)
                    2'b01: state_nxt = M2;    // siguiente
                    2'b10: state_nxt = M4;    // anterior (wrap-back)
                 endcase
            //----------------------------------------------//
            M2: case (sc_M2)
                    2'b01: state_nxt = M3;
                    2'b10: state_nxt = M1;
                 endcase
            //----------------------------------------------//
            M3: case (sc_M3)
                    2'b01: state_nxt = M4;
                    2'b10: state_nxt = M2;
                 endcase
            //----------------------------------------------//
            M4: case (sc_M4)
                    2'b01: state_nxt = M1;    // wrap-forward
                    2'b10: state_nxt = M3;
                 endcase
        endcase
    end

    //--------------------------------------------------------//
    // 5) Salida: copia la de la máquina actualmente activa
    //--------------------------------------------------------//
    always @(*) begin
        case (state_cur)
            M1: movement_sel = mv_M1;
            M2: movement_sel = mv_M2;
            M3: movement_sel = mv_M3;
            M4: movement_sel = mv_M4;
            default: movement_sel = 4'b0000;
        endcase
    end

endmodule
