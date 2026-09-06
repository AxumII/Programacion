
#include <Arduino.h>
#include "SystemConfig.h"
#include "ControlManager.h"
#include "Kinematic.h"

// =================================================================
// 1. DEFINICIÓN DE PINES
// =================================================================
byte analogInputPin[] = {10};
byte digitalInputPin[] = {};
byte digitalOutputPin[] = {};
byte PWMLeftPin[] = {5, 7, 16, 18};
byte PWMRightPin[] = {4, 6, 15, 17};
byte i2cPin[] = {8, 9}; 
byte spiPin[] = {}; 
byte csPin[] = {}; 
byte QEncoderAPin[] = {11, 13, 48, 20};
byte QEncoderBPin[] = {12, 14, 47, 19};

// =================================================================
// 2. PARÁMETROS FÍSICOS GENERALES
// =================================================================
const float F_BATT = 7.66;
const float l1 = 100.0, l2 = 150.0, l3 = 100.0, l4 = 50.0;
const float w1 = 0.0,   w2 = 0.0,   w3 = 0.0,   w4 = 0.0;

const bool INVERTIR_MOTOR[4]   = {true, false, true, true};
const bool INVERTIR_ENCODER[4] = {true, false, true, true};

const float RELACION_CAJA_M1  = 1154.0;
const float RELACION_CAJA_M24 = 1000.0;
const float PPR[4] = {
  5.0 * 4 * RELACION_CAJA_M1, 
  11.0 * 4 * RELACION_CAJA_M24,
  11.0 * 4 * RELACION_CAJA_M24,
  11.0 * 4 * RELACION_CAJA_M24 
};
float OFFSETS_IS[4] = {0.5876, 0.4674, 0, 0}; 
float FACTOR_M31ZY  = 20.0;   
float FACTOR_MJGY   = 13.6;  

// =================================================================
// 3. INSTANCIAS DEL FRAMEWORK
// =================================================================
SystemConfig sysConfig;
Kinematic robotKinematic(l1, l2, l3, w1, w2, w3, l4, w4);
ControlManager* robotControl;

// Variables de estado
float sensor_q[4] = {0}, sensor_q_dot[4] = {0}, sensor_i_meas[4] = {0}, v_batt = 0;
unsigned long last_sensor_time = 0;

/*
void setup() {
    delay(3000);
    // A. ENLAZAR Y ARRANCAR SISTEMA (Dueño de los sensores)
    sysConfig.bindPins(
        analogInputPin, 1,
        nullptr, 0,  // Sin inputs digitales
        nullptr, 0,  // Sin outputs digitales
        PWMLeftPin, PWMRightPin, 4,
        i2cPin, 2,
        nullptr, 0,  // Sin SPI
        QEncoderAPin, QEncoderBPin, 4
    );
    sysConfig.setInversions(INVERTIR_MOTOR, INVERTIR_ENCODER);
    sysConfig.start(); // Inicializa encoders, ADS y Memoria.

    // B. ENLAZAR Y ARRANCAR CONTROL (Dueño del uso y la matemática)
    robotControl.joinSensors(sensor_q, sensor_q_dot, sensor_i_meas, &v_batt);
    robotControl.bindHardware(sysConfig.encoders, &sysConfig.ads, sysConfig.offsets_enc, analogInputPin[0]);
    robotControl.setSensorParams(PPR, OFFSETS_IS, FACTOR_M31ZY, FACTOR_MJGY, F_BATT);
    
    robotControl.setInterpolationActive(true);
    robotControl.setEnableCurrentControl(false);
}
*/

void setup() {
    delay(3000); // Esperar a que el USB esté listo
    Serial.begin(115200);
    Serial.println("\n[1] Iniciando setup...");

    Serial.println("[2.1] Intentando bindPins...");
    sysConfig.bindPins(
        analogInputPin, sizeof(analogInputPin)/sizeof(analogInputPin[0]),
        digitalInputPin, sizeof(digitalInputPin)/sizeof(digitalInputPin[0]),
        digitalOutputPin, sizeof(digitalOutputPin)/sizeof(digitalOutputPin[0]),
        PWMLeftPin, PWMRightPin, sizeof(PWMLeftPin)/sizeof(PWMLeftPin[0]),
        i2cPin, sizeof(i2cPin)/sizeof(i2cPin[0]),
        spiPin, sizeof(spiPin)/sizeof(spiPin[0]),
        QEncoderAPin, QEncoderBPin, sizeof(QEncoderAPin)/sizeof(QEncoderAPin[0])
    );
    Serial.println("[2.2] bindPins OK.");

    Serial.println("[3.1] Intentando setInversions...");
    sysConfig.setInversions(INVERTIR_MOTOR, INVERTIR_ENCODER);
    Serial.println("[3.2] setInversions OK.");

    Serial.println("[4.1] Intentando sysConfig.start()...");
    sysConfig.start(); 
    Serial.println("[4.2] sysConfig.start() OK.");

    Serial.println("[5] ¡Todo el hardware inicializado correctamente!");
}



void loop() {
    unsigned long msActual = millis();
    float dt = (msActual - last_sensor_time) / 1000.0f;

    // 1. El controlador "usa" los sensores para calcular estado
    if (dt >= 0.005f) {
        last_sensor_time = msActual;
        robotControl->readAndProcessSensors(dt);
    }

    // 2. Ejecutar Planta de control Matemática
    robotControl->CascadePlant();

    // 3. Traducir matemáticas a hardware físico
    for(int i = 0; i < 4; i++) {
        int pwm_val = 0;
        char dir = 'S';
        
        if (robotControl->getPWMCommand(i, pwm_val, dir)) {
            sysConfig.applyMotor(i, pwm_val, dir); 
        }
    }

// =================================================================
    // 4. MÉTODOS DE MOVIMIENTO Y COMUNICACIÓN SERIAL
    // =================================================================
    static unsigned long last_telemetry_time = 0;
    static bool telemetry_active = true;

    if (Serial.available() > 0) {
        String cmd = Serial.readStringUntil('\n');
        cmd.trim();
        cmd.toUpperCase();

        // [COMANDO S] Parada de Emergencia
        if (cmd == "S") {
            robotControl->setTarget(0, 0, 0, 0, false, 'A', '1', 0.0f); // Purga la trayectoria actual
            for(int i = 0; i < 4; i++) {
                sysConfig.applyMotor(i, 0, 'S'); // Corta la energía en la capa de hardware
            }
            Serial.println("\n[!!!] PARADA DE EMERGENCIA EJECUTADA [!!!]");
        }
        
        // [COMANDO P] Alternar Telemetría
        else if (cmd == "P") {
            telemetry_active = !telemetry_active;
            Serial.println(telemetry_active ? "\n[+] Telemetría Activada" : "\n[-] Telemetría Desactivada");
        }
        
        // [COMANDO AUTO] Iniciar Auto-Sintonización (Ej: "AUTO 0" para Motor 1)
        else if (cmd.startsWith("AUTO ")) {
            int id = cmd.substring(5).toInt();
            if (id >= 0 && id <= 3) {
                robotControl->startAutoTune(id);
                Serial.printf("\n[*] Iniciando Auto-Sintonización en Motor %d\n", id + 1);
            }
        }
        
        // [COMANDO G] Movimiento Cartesiano: G <X> <Y> <Z> <PHI> <DURACION_SEGUNDOS>
        // Ejemplo: G 150.0 50.0 100.0 90.0 2.5
        else if (cmd.startsWith("G ")) {
            int espacios[5];
            int pos = 0;
            
            // Buscar los espacios separadores
            for(int i = 0; i < 5; i++) {
                pos = cmd.indexOf(' ', pos + 1);
                espacios[i] = pos;
            }

            if (espacios[0] > 0 && espacios[1] > 0 && espacios[2] > 0 && espacios[3] > 0 && espacios[4] > 0) {
                float x = cmd.substring(espacios[0] + 1, espacios[1]).toFloat();
                float y = cmd.substring(espacios[1] + 1, espacios[2]).toFloat();
                float z = cmd.substring(espacios[2] + 1, espacios[3]).toFloat();
                float phi = cmd.substring(espacios[3] + 1, espacios[4]).toFloat();
                float dur = cmd.substring(espacios[4] + 1).toFloat();

                // Intentar calcular la cinemática inversa y trazar ruta
                // Usamos 'C' (Cartesiano) y perfil '5' (Quíntico - Zero Jerk)
                bool ik_ok = robotControl->setTarget(x, y, z, phi, true, 'C', '5', dur);
                
                if (ik_ok) {
                    Serial.printf("\n[+] Moviendo a -> X:%.1f Y:%.1f Z:%.1f Phi:%.1f | Tiempo: %.1fs\n", x, y, z, phi, dur);
                } else {
                    Serial.println("\n[-] ERROR: Posición Inalcanzable (Singularidad o fuera de espacio de trabajo)");
                }
            } else {
                Serial.println("\n[-] Formato incorrecto. Usa: G X Y Z PHI DURACION");
            }
        }
    }

// =================================================================
    // 5. TELEMETRÍA (10 Hz)
    // =================================================================
    if (telemetry_active && (msActual - last_telemetry_time >= 100)) {
        last_telemetry_time = msActual;
        
        Serial.printf("[BAT: %.2fV] ", v_batt);
        for(int i = 0; i < 4; i++) {
            // Muestra: Motor[Ángulo | Corriente | Referencia Velocidad]
            Serial.printf("M%d[%6.1f° %4.2fA %.2frad/s] ", 
                          i+1, 
                          sensor_q[i], 
                          sensor_i_meas[i],
                          robotControl->joints[i].q_dot_ref);
        }
        Serial.println();
    }
} 