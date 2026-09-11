#include <Arduino.h>
#include "SystemConfig.h"
#include "ControlManager.h"
#include "Kinematic.h"

// =================================================================
// 1. DEFINICIÓN DE PINES
// =================================================================
byte analogInputPin[]  = {10}; // Pin para V_BATT
byte PWMLeftPin[]      = {5, 7, 16, 18};
byte PWMRightPin[]     = {4, 6, 15, 17};
byte i2cPin[]          = {8, 9}; 
byte QEncoderAPin[]    = {11, 13, 48, 20};
byte QEncoderBPin[]    = {12, 14, 47, 19};

byte* digitalInputPin  = nullptr;
byte* digitalOutputPin = nullptr;
byte* spiPin           = nullptr; 
byte* csPin            = nullptr;

// =================================================================
// 2. PARÁMETROS FÍSICOS GENERALES
// =================================================================
const int PIN_V_BATT = 10;
const float F_BATT = 7.66;
const uint32_t PWM_FREQ = 20000;
const byte PWM_RES = 8;

// Límite de corriente para parada por colisión
const float LIMITES_CORRIENTE[4] = {6.5, 1.2, 1.2, 1.2}; 

const float l1 = 100.0, l2 = 150.0, l3 = 100.0, l4 = 50.0;
const float w1 = 0.0,   w2 = 0.0,   w3 = 0.0,   w4 = 0.0;

const bool INVERTIR_MOTOR[4]   = {true, false, true, true};
const bool INVERTIR_ENCODER[4] = {true, false, true, true};

const float RELACION_CAJA_M1  = 1154.0;
const float RELACION_CAJA_M24 = 1000.0;
const float ENCODER_31ZY_FACTOR = 5.0;
const float ENCODER_JGY370_FACTOR = 11.0;

const float PPR[4] = {
  ENCODER_31ZY_FACTOR * 4.0 * RELACION_CAJA_M1, 
  ENCODER_JGY370_FACTOR * 4.0 * RELACION_CAJA_M24,
  ENCODER_JGY370_FACTOR * 4.0 * RELACION_CAJA_M24,
  ENCODER_JGY370_FACTOR * 4.0 * RELACION_CAJA_M24 
};

float OFFSETS_IS[4] = {0.5876, 0.4674, 0, 0}; 
float FACTOR_M31ZY  = 20.0;   
float FACTOR_MJGY   = 13.6;  

// =================================================================
// 3. INSTANCIAS DEL FRAMEWORK Y MEMORIA GLOBAL
// =================================================================
SystemConfig sistema(
    sizeof(analogInputPin), analogInputPin,
    sizeof(PWMLeftPin), PWMLeftPin,
    sizeof(PWMRightPin), PWMRightPin,
    sizeof(i2cPin), i2cPin,
    sizeof(QEncoderAPin), QEncoderAPin,
    sizeof(QEncoderBPin), QEncoderBPin,
    115200, 0, nullptr, 0, nullptr, 0, nullptr, 0, nullptr                            
);

Kinematic* cinBrazo = nullptr;
ControlManager* robotControl = nullptr;
int typeDimensionsConfig = 4;

// Memoria compartida global
float sensor_q[4] = {0}, sensor_q_dot[4] = {0}, sensor_i_meas[4] = {0}, v_batt = 0;
unsigned long last_sensor_time = 0;

// Variables de control temporal
bool telemetriaActiva = true;
unsigned long ultimaTelemetria = 0;
unsigned long ultimaRevisionColision = 0;

// =================================================================
// 4. MÉTODOS TEMPORALES DE INTERFAZ SERIAL Y SEGURIDAD
// =================================================================

void imprimirTelemetria() {
    unsigned long msActual = millis();
    if (telemetriaActiva && (msActual - ultimaTelemetria >= 500)) {
        ultimaTelemetria = msActual;
        Serial.printf("\n[BAT: %.1fV]\n", v_batt);
        for(int i=0; i<4; i++) {
            // El Kalman devuelve radianes. Se convierte a grados para la impresión temporal.
            float anguloGrados = sensor_q[i] * 180.0 / PI; 
            Serial.printf("M%d -> Angulo: %6.1f° | Vel: %6.2f | Corr: %4.2fA\n", i+1, anguloGrados, sensor_q_dot[i], sensor_i_meas[i]);
        }
    }
}

void revisarColisiones() {
    unsigned long msActual = millis();
    if (msActual - ultimaRevisionColision >= 50) {
        ultimaRevisionColision = msActual;
        for(int i=0; i<4; i++) {
            if (sensor_i_meas[i] > LIMITES_CORRIENTE[i]) {
                robotControl->setMotor(i, 0, 'S'); // Esto fuerza el guardado en NVS desde SystemConfig
                Serial.printf("\n[!] ALARMA DE COLISIÓN M%d [!] Corriente: %.2fA. Motor bloqueado por seguridad.\n", i+1, sensor_i_meas[i]);
            }
        }
    }
}

void procesarComandosSeriales() {
    if (Serial.available() > 0) {
        String cmd = Serial.readStringUntil('\n');
        cmd.trim(); cmd.toUpperCase();

        if (cmd == "S") {
            for(int i=0; i<4; i++) robotControl->setMotor(i, 0, 'S');
            Serial.println("\n[!!!] PARADA DE EMERGENCIA EJECUTADA Y POSICIÓN GUARDADA [!!!]");
        } 
        else if (cmd == "P") {
            telemetriaActiva = !telemetriaActiva;
        }
        else if (cmd == "D") {
            Serial.println("\n--- MODO DEBUG ANALÓGICO ---");
            for(int i=0; i<4; i++) {
                Serial.printf("Canal %d (Motor %d) Corriente actual: %.4f A\n", i, i+1, sensor_i_meas[i]);
            }
        }
        else if (cmd.startsWith("Z") && cmd.length() == 2) {
            int id = cmd.charAt(1) - '1';
            if(id >= 0 && id <= 3) {
                sistema.zeroEncoder(id); 
                Serial.printf(">> Cero (Offset) establecido para M%d\n", id+1);
            }
        }
        else if (cmd.startsWith("R") && cmd.length() == 3) {
            int id = cmd.charAt(1) - '1';
            bool estado = cmd.charAt(2) == '1';
            if (id >= 0 && id <= 3) {
                // Invertimos el estado por la lógica PCF original (activo en LOW típicamente)
                sistema.writeExpanderPin(id, !estado); 
                Serial.printf(">> Relay %d -> %s\n", id+1, estado ? "ON" : "OFF");
            }
        }
        else if (cmd.startsWith("T") && cmd.indexOf(',') > 0) {
            int id = cmd.charAt(1) - '1';
            char dir = cmd.charAt(2);
            int commaIdx = cmd.indexOf(',');
            
            if (id >= 0 && id <= 3 && (dir == 'H' || dir == 'A')) {
                int pot = cmd.substring(3, commaIdx).toInt();
                int ms = cmd.substring(commaIdx + 1).toInt();
                ms = constrain(ms, 5, 2000); 
                
                robotControl->setMotor(id, pot, dir);
                delay(ms); 
                robotControl->setMotor(id, 0, 'S'); // Detener y guardar NVS
            }
        }
        else if (cmd.length() >= 2) {
            int id = cmd.charAt(0) - '1';
            char dir = cmd.charAt(1);
            
            if (id >= 0 && id <= 3) {
                if (dir == 'S') {
                    robotControl->setMotor(id, 0, 'S'); // Detener y guardar NVS
                } else if (dir == 'H' || dir == 'A') {
                    int pot = cmd.substring(2).toInt();
                    robotControl->setMotor(id, pot, dir);
                }
            }
        }
    }
}

// =================================================================
// 5. SETUP Y LOOP
// =================================================================
void setup(){
    // Dar un respiro para que el Monitor Serial capture los primeros prints
    delay(1000); 

    // Inyección de parámetros hardware
    sistema.setInvMotor(INVERTIR_MOTOR);
    sistema.setEncoderParams(INVERTIR_ENCODER, PPR);
    sistema.setPWMParams(PWM_FREQ, PWM_RES);
    sistema.setADCParams(OFFSETS_IS, FACTOR_M31ZY, FACTOR_MJGY);
    sistema.setBatteryParams(PIN_V_BATT, F_BATT);

    switch (typeDimensionsConfig){
        default: {
            float lengthTool = 14, wTool = -6.5;
            cinBrazo = new Kinematic(40.04, 100.8, 55, 15.1, 1, -14, lengthTool, wTool);
            break;
        }
    }

    // Esto ejecutará todos los mensajes de inicio en la consola
    sistema.start();

    robotControl = new ControlManager(cinBrazo, &sistema);
    robotControl->joinSensors(sensor_q, sensor_q_dot, sensor_i_meas, &v_batt);
    
    // Forzar lectura inicial inmediata para que no aparezca en ceros absolutos si ya hay posición previa
    robotControl->updateSensors(0.01f);

    last_sensor_time = micros();
    
    Serial.println(F("=================================================="));
    Serial.println(F("  SISTEMA INICIADO: Kalman | NVS | Anti-Colisión  "));
    Serial.println(F("=================================================="));
}
void loop(){
    unsigned long now = micros();
    float dt = (now - last_sensor_time) / 1000000.0f; // dt en segundos

    // 1. Ciclo Crítico de Adquisición y Estimación (100Hz)
    if (dt >= 0.01f) {
        last_sensor_time = now;
        robotControl->updateSensors(dt); 
    }

    // 2. Procesos Asíncronos (Comandos, Seguridad y Reportes)
    revisarColisiones();
    procesarComandosSeriales();
    imprimirTelemetria();
}