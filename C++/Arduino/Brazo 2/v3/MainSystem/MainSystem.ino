#include <Arduino.h>
#include "SystemConfig.h"
#include "ControlManager.h"
#include "Kinematic.h"
#include "MenuManager.h"

// =================================================================
// 1. DEFINICIÓN DE PINES
// =================================================================
byte analogInputPin[]  = {10}; 
byte PWMLeftPin[]      = {7, 5, 16, 18};
byte PWMRightPin[]     = {6, 4, 15, 17};
byte i2cPin[]          = {8, 9}; 
byte QEncoderAPin[]    = {13, 11, 48, 20};
byte QEncoderBPin[]    = {14, 12, 47, 19};

byte* digitalInputPin  = nullptr;
byte* digitalOutputPin = nullptr;
byte* spiPin           = nullptr; 
byte* csPin            = nullptr;

// =================================================================
// 2. PARÁMETROS FÍSICOS GENERALES
// =================================================================
const uint32_t PWM_FREQ = 20000;
const byte PWM_RES = 10;

const float l1 = 116.0 + 16, l2 = 304.3, l3 = 218.0, l4 = 103.0;
const float w1 = 4.75,   w2 = -27.0,   w3 = -30.0,   w4 = -3.0;

const bool INVERTIR_MOTOR[4]   = {true, false, false, true};
const bool INVERTIR_ENCODER[4] = {false, true, false, true};

// Límite de corriente para parada por colisión
const float LIMITES_CORRIENTE[4] = {1.0, 3, 1.0, 1.0}; 

const float RELACION_CAJA_M1  = 1154.0;
const float RELACION_CAJA_M24 = 1000.0;
const float ENCODER_31ZY_FACTOR = 5.0;
const float ENCODER_JGY370_FACTOR = 11.0;

const float PPR[4] = {
  ENCODER_JGY370_FACTOR * 4.0 * RELACION_CAJA_M24, // Índice 0: Base (Motor físico 2)
  ENCODER_31ZY_FACTOR * 4.0 * RELACION_CAJA_M1,    // Índice 1: Hombro (Motor físico 1)
  ENCODER_JGY370_FACTOR * 4.0 * RELACION_CAJA_M24, // Índice 2: Codo
  ENCODER_JGY370_FACTOR * 4.0 * RELACION_CAJA_M24  // Índice 3: Muñeca
};

// =================================================================
// 3. INSTANCIAS DEL FRAMEWORK Y MEMORIA GLOBAL
// =================================================================
SystemConfig sistema(
    0, nullptr, // ADC deshabilitado
    sizeof(PWMLeftPin), PWMLeftPin,
    sizeof(PWMRightPin), PWMRightPin,
    sizeof(i2cPin), i2cPin,
    sizeof(QEncoderAPin), QEncoderAPin,
    sizeof(QEncoderBPin), QEncoderBPin,
    115200, 0, nullptr, 0, nullptr, 0, nullptr, 0, nullptr                            
);

Kinematic* cinBrazo = nullptr;
ControlManager* robotControl = nullptr;
MenuManager* menu = nullptr; 

// Selección de herramienta activa (0 = Sin herramienta, 1 al 5 = Herramientas personalizadas)
int typeDimensionsConfig = 1; 

// Memoria compartida global
float sensor_q[4] = {0}, sensor_q_dot[4] = {0}, sensor_i_meas[4] = {0};
float sensor_v_fuente = 0.0f;
unsigned long last_sensor_time = 0;

// =================================================================
// 4. SETUP Y LOOP
// =================================================================
void setup(){
    delay(1000); 

    sistema.setInvMotor(INVERTIR_MOTOR);
    sistema.setEncoderParams(INVERTIR_ENCODER, PPR);
    sistema.setPWMParams(PWM_FREQ, PWM_RES);

    float lengthTool = 0.0;
    float wTool = 0.0;

    // Configuración del TCP según la herramienta seleccionada
    switch (typeDimensionsConfig){
        case 1:
            // Herramienta 1 (Tool Calibracion)
            lengthTool = 24.0;
            wTool = 0.0;
            break;
        case 2:
            // Herramienta 2 Gripper
            lengthTool = 120.0; 
            wTool = 0.0;
            break;
        case 3:
            // Herramienta 3 Electroiman
            lengthTool = 60.0; 
            wTool = 0.0;
            break;
        default:
            // Sin herramienta: El TCP coincide con la brida/eslabón final
            lengthTool = 0.0;
            wTool = 0.0;
            break;
    }

    cinBrazo = new Kinematic(l1, l2, l3, w1, w2, w3, l4 + lengthTool,  w4 + wTool);
    sistema.setPowerParams(analogInputPin[0], 7.66);
    sistema.start();

    // Inicializar Control y Menú enlazando sensores. (Se pasa nullptr en lugar de v_batt)
    robotControl = new ControlManager(cinBrazo, &sistema);
    robotControl->joinSensors(sensor_q, sensor_q_dot, sensor_i_meas, &sensor_v_fuente);
    robotControl->loadAllGains();
    
    menu = new MenuManager(robotControl, &sistema, LIMITES_CORRIENTE);
    menu->joinSensors(sensor_q, sensor_q_dot, sensor_i_meas, &sensor_v_fuente);
    
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

    // --- ¡AQUÍ SE EJECUTA EL CEREBRO DEL CONTROL! ---
    robotControl->CascadeControl();

    // 2. Procesos Asíncronos extraídos al MenuManager
    menu->run();

    // 3. Guardado Periódico de NVS
    sistema.savePositionsPeriodically(5000); 
}