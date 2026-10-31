#include "syncMenu.h"

SyncMenu::SyncMenu(plantStatus* plantaPtr, plantController* ctrlPtr) {
    _planta = plantaPtr;
    _controlador = ctrlPtr;
    _lastTxTime = 0;
}

// ... [Mantén processSerialCommands y transmitData exactamente igual] ...

void SyncMenu::executeCommand(String input) {
    input.trim();
    char cmd = input.charAt(0);
    
    if (cmd == 'Z' || cmd == 'z') {
        _planta->calibrateSensors();
    }
    else if (cmd == 'S' || cmd == 's') { 
        _controlador->stop(); // Desactiva PID si estaba prendido
        _planta->applyMotor(0.0, 0, false);
    }
    else if (cmd == 'E' || cmd == 'e') { 
        _controlador->stop();
        _planta->applyMotor(0.0, 0, true);
    }
    // NUEVO: Comando PID P<angulo>,<velocidad_maxima>
    else if (cmd == 'P' || cmd == 'p') {
        int comaIdx = input.indexOf(',');
        float target = 0;
        float maxPWM = 100.0; // Velocidad por defecto

        if (comaIdx != -1) { // Si se proveyó una coma P90,50
            target = input.substring(1, comaIdx).toFloat();
            maxPWM = input.substring(comaIdx + 1).toFloat();
        } else { // Si solo se puso el angulo P90
            target = input.substring(1).toFloat();
        }
        _controlador->setTarget(target, maxPWM);
    }
    else if (cmd == 'H' || cmd == 'h' || cmd == 'A' || cmd == 'a') {
        _controlador->stop(); // Si ordenas manual, el PID se detiene
        if (input.length() > 1) {
            float pwr = input.substring(1).toFloat();
            int dir = (cmd == 'H' || cmd == 'h') ? 1 : -1;
            _planta->applyMotor(pwr, dir, false);
        }
    }
}