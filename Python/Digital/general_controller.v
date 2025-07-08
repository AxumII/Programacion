module top_level_controller (
    input clk,
    input rst,
    input [3:0] movement_sel,  // Entrada de movimiento
    output [7:0] sel_protected  // Salida protegida de los motores
);

    // Señales intermedias para conectar la salida de move_machine a motor_controller
    wire [7:0] sel;

    // Instanciar el módulo move_machine (motor_controller)
    move_machine move_machine_instance (
        .clk(clk),
        .rst(rst),
        .movement_sel(movement_sel),
        .sel(sel)
    );

    // Instanciar el módulo quad_motor_controller
    quad_motor_controller quad_motor_instance (
        .clk(clk),
        .rst(rst),
        .sel(sel),              // Conectamos la salida de move_machine a la entrada de quad_motor_controller
        .sel_protected(sel_protected) // Salida protegida de los motores
    );

endmodule
