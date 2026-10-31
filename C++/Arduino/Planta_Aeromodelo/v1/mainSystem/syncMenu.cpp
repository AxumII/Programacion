#include "syncMenu.h"

SyncMenu::SyncMenu(plantStatus* plantaPtr) {
    _planta = plantaPtr;
    _lastTxTime = 0;
}

// ---------- Manejo de comunicación serial (NO BLOQUEANTE) ----------

void SyncMenu::processSerialCommands() {
    static String inputBuffer = ""; // Búfer que persiste entre ciclos
    
    // Leemos todo lo disponible sin esperar (sin timeout)
    while (Serial.available() > 0) {
        char c = (char)Serial.read();
        
        if (c == '\n' || c == '\r') {
            if (inputBuffer.length() > 0) {
                executeCommand(inputBuffer);
                inputBuffer = ""; // Limpiar para el siguiente comando
            }
        } else {
            inputBuffer += c; // Ensamblar el comando
        }
    }
}

void SyncMenu::executeCommand(String input) {
    input.trim();
    char cmd = input.charAt(0);
    
    if (cmd == 'Z' || cmd == 'z') {
        _planta->calibrateSensors();
    }
    else if (cmd == 'S' || cmd == 's') { 
        _planta->applyMotor(0.0, 0, false);
    }
    else if (cmd == 'E' || cmd == 'e') { 
        _planta->applyMotor(0.0, 0, true);
    }
    else if (cmd == 'H' || cmd == 'h' || cmd == 'A' || cmd == 'a') {
        if (input.length() > 1) {
            float pwr = input.substring(1).toFloat();
            int dir = (cmd == 'H' || cmd == 'h') ? 1 : -1;
            _planta->applyMotor(pwr, dir, false);
        }
    }
    // Nota: Eliminamos los Serial.println() dentro de los comandos para no corromper la trama binaria.
}

// ---------- Envío Binario a Alta Frecuencia ----------

void SyncMenu::transmitData(uint32_t frequencyHz) {
    uint32_t interval = 1000000 / frequencyHz; // Intervalo en microsegundos
    uint32_t currentMicros = micros();

    if (currentMicros - _lastTxTime >= interval) {
        _lastTxTime = currentMicros;

        SensorDataPacket packet;
        packet.header[0] = 0xAA; // Cabecera para identificar en Python/MATLAB
        packet.header[1] = 0xBB;
        packet.timestamp = currentMicros;
        packet.pwm = _planta->currentDuty;
        packet.angulo = _planta->angulo_as5600;
        packet.ax = _planta->ax;
        packet.ay = _planta->ay;
        packet.az = _planta->az;
        packet.gx = _planta->gx;
        packet.gy = _planta->gy;
        packet.gz = _planta->gz;
        packet.footer = 0xCC;

        // Escribimos los 39 bytes directamente en el hardware de una sola vez
        Serial.write((uint8_t*)&packet, sizeof(packet));
    }
}