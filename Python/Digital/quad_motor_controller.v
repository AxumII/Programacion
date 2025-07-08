module quad_motor_controller(
    input clk,
    input rst,
    input  [7:0] sel,              // 4 motores × 2 bits
    output [7:0] sel_protected     // 4 salidas × 2 bits
);

    // Motor 0
    motor_controller motor0 (
        .clk(clk),
        .rst(rst),
        .sel(sel[1:0]),
        .sel_protected(sel_protected[1:0])
    );

    // Motor 1
    motor_controller motor1 (
        .clk(clk),
        .rst(rst),
        .sel(sel[3:2]),
        .sel_protected(sel_protected[3:2])
    );

    // Motor 2
    motor_controller motor2 (
        .clk(clk),
        .rst(rst),
        .sel(sel[5:4]),
        .sel_protected(sel_protected[5:4])
    );

    // Motor 3
    motor_controller motor3 (
        .clk(clk),
        .rst(rst),
        .sel(sel[7:6]),
        .sel_protected(sel_protected[7:6])
    );

endmodule
