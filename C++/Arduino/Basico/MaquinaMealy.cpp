#include <Arduino.h>

// Definiciones teóricas (Alfabetos)
typedef char AlfabetoEntrada;
typedef String AlfabetoSalida;

class MaquinaMealy {
  private:
    // S: Conjunto de Estados
    enum Estado { S0, S1, S2, ERROR };
    Estado estadoActual; // s ∈ S

    // G: Función de Salida (Salida depende de Estado actual y Entrada)
    AlfabetoSalida funcionG(Estado s, AlfabetoEntrada sigma) {
      if (s == S0 && sigma == 'A') return "Transicion S0->S1";
      if (s == S1 && sigma == 'B') return "EXITO: Secuencia Detectada";
      if (sigma == 'X') return "RESET_SYSTEM";
      return "NULL_OUTPUT";
    }

    // T: Función de Transición de Estados
    Estado funcionT(Estado s, AlfabetoEntrada sigma) {
      switch (s) {
        case S0: return (sigma == 'A') ? S1 : S0;
        case S1: return (sigma == 'B') ? S2 : (sigma == 'A' ? S1 : S0);
        case S2: return S0; // Ciclo
        default: return S0;
      }
    }

  public:
    // Constructor define el Estado Inicial (s0)
    MaquinaMealy() {
      estadoActual = S0;
    }

    // El corazón de la máquina: Procesa el estímulo
    void transitar(AlfabetoEntrada sigma) {
      // 1. Calcular la salida basándose en el par (Estado actual, Entrada)
      // Teóricamente: Lambda_t = G(S_t, Sigma_t)
      AlfabetoSalida lambda = funcionG(estadoActual, sigma);
      
      // Ejecutar la salida (acción)
      emitirSalida(lambda);

      // 2. Calcular el siguiente estado
      // Teóricamente: S_{t+1} = T(S_t, Sigma_t)
      estadoActual = funcionT(estadoActual, sigma);
    }

    void emitirSalida(AlfabetoSalida lambda) {
      if (lambda != "NULL_OUTPUT") {
        Serial.print("Salida Emitida (Lambda): ");
        Serial.println(lambda);
      }
    }

    Estado obtenerEstadoActual() { return estadoActual; }
};

// --- Ejecución ---

MaquinaMealy maquina;

void setup() {
  Serial.begin(9600);
  Serial.println("Maquina de Mealy Inicializada.");
}

void loop() {
  if (Serial.available() > 0) {
    AlfabetoEntrada sigma = Serial.read();
    if (sigma != '\n' && sigma != '\r') {
      Serial.print("Entrada (Sigma): "); Serial.println(sigma);
      maquina.transitar(sigma);
    }
  }
}