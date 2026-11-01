#include "syncMenu.h"

// Actualizado para recibir _controlador
SyncMenu::SyncMenu(plantStatus* plantaPtr, plantController* ctrlPtr) {
    _planta = plantaPtr;
    _controlador = ctrlPtr;
    _lastTxTime = 0;
}

void SyncMenu::processSerialCommands() {
    static String inputBuffer = ""; 
    
    while (Serial.available() > 0) {
        char c = (char)Serial.read();
        
        if (c == '\n' || c == '\r') {
            if (inputBuffer.length() > 0) {
                executeCommand(inputBuffer);
                inputBuffer = ""; 
            }
        } else {
            inputBuffer += c; 
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
        _controlador->stop(); // Frena el PID
        _planta->applyMotor(0.0, 0, false);
    }
    else if (cmd == 'E' || cmd == 'e') { 
        _controlador->stop(); // Frena el PID
        _planta->applyMotor(0.0, 0, true);
    }
    else if (cmd == 'P' || cmd == 'p') { // Comando PID
        int comaIdx = input.indexOf(',');
        float target = 0;
        float maxPWM = 100.0;
        if (comaIdx != -1) {
            target = input.substring(1, comaIdx).toFloat();
            maxPWM = input.substring(comaIdx + 1).toFloat();
        } else {
            target = input.substring(1).toFloat();
        }
        _controlador->setTarget(target, maxPWM);
    }
    else if (cmd == 'H' || cmd == 'h' || cmd == 'A' || cmd == 'a') {
        _controlador->stop(); // Si envías comando manual, el PID se desactiva
        if (input.length() > 1) {
            float pwr = input.substring(1).toFloat();
            int dir = (cmd == 'H' || cmd == 'h') ? 1 : -1;
            _planta->applyMotor(pwr, dir, false);
        }
    }
}

void SyncMenu::transmitData(uint32_t frequencyHz) {
    uint32_t interval = 1000000 / frequencyHz; 
    uint32_t currentMicros = micros();

    if (currentMicros - _lastTxTime >= interval) {
        _lastTxTime = currentMicros;

        SensorDataPacket packet;
        packet.header[0] = 0xAA; 
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

        Serial.write((uint8_t*)&packet, sizeof(packet));
    }
}