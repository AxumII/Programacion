module mealy_fsm_template(
    input clk,
    input rst,
    input x,
    output reg z
);
  
  // Definición de estados
  parameter A = 2'b00,
            B = 2'b01,
            C = 2'b10;

  reg [1:0] estado_actual, estado_siguiente;

  // Lógica secuencial
  always @(posedge clk or posedge rst) begin
      if (rst) estado_actual <= A;
      else     estado_actual <= estado_siguiente;
  end

  // Lógica combinacional para el próximo estado
  always @(*) begin
      case (estado_actual)
          A: estado_siguiente = x ? B : A;
          B: estado_siguiente = x ? A : C;
          C: estado_siguiente = x ? C : B;
          default: estado_siguiente = A;
      endcase
  end

  // Lógica combinacional para la salida Mealy
  always @(*) begin
      case (estado_actual)
          A: z = x ? 1'b1 : 1'b0;
          B: z = x ? 1'b1 : 1'b0;
          C: z = x ? 1'b0 : 1'b1;
          default: z = 1'b0;
      endcase
  end

endmodule
