#include "MenuManager.h"

MenuManager::MenuManager(ControlManager* robotControl, SystemConfig* sistema, const float* limites) {
    _robotControl = robotControl;
    _sistema = sistema;
    limites_corriente = limites;
    
    telemetriaActiva = true;
    ultimaTelemetria = 0;
    ultimaRevisionColision = 0;
}

void MenuManager::joinSensors(float* q, float* q_dot, float* i_meas, float* v_fuente) {
    sensor_q = q;
    sensor_q_dot = q_dot;
    sensor_i_meas = i_meas;
    sensor_v_fuente = v_fuente;
}

void MenuManager::imprimirTelemetria() {
    unsigned long msActual = millis();
    if (telemetriaActiva && (msActual - ultimaTelemetria >= 500)) {
        ultimaTelemetria = msActual;
        
        if (sensor_v_fuente != nullptr) {
            Serial.printf("\n[FUENTE: %.1fV]\n", *sensor_v_fuente);
        } else {
            Serial.printf("\n[FUENTE: N/A]\n");
        }
        
        for(int i=0; i<4; i++) {
            float anguloGrados = sensor_q[i] * 180.0 / PI; 
            // [MODIFICADO] %7.2f muestra 2 decimales, %7.3f para la velocidad
            Serial.printf("M%d -> Angulo: %7.2f° | Vel: %7.3f | Corr: %4.2fA\n", 
                          i+1, anguloGrados, sensor_q_dot[i], sensor_i_meas[i]);
        }
    }
}

void MenuManager::revisarColisiones() {
    unsigned long msActual = millis();
    if (msActual - ultimaRevisionColision >= 50) {
        ultimaRevisionColision = msActual;
        for(int i=0; i<4; i++) {
            if (sensor_i_meas[i] > limites_corriente[i]) {
                _robotControl->setMotor(i, 0, 'S'); // Forzará a su vez el guardado seguro en NVS
                Serial.printf("\n[!] ALARMA DE COLISIÓN M%d [!] Corriente: %.2fA. Motor bloqueado por seguridad.\n", i+1, sensor_i_meas[i]);
            }
        }
    }
}

void MenuManager::procesarComandosSeriales() {
    if (Serial.available() > 0) {
        String cmd = Serial.readStringUntil('\n');
        cmd.trim(); cmd.toUpperCase();

        if (cmd == "S") {
            for(int i=0; i<4; i++) _robotControl->setMotor(i, 0, 'S');
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
                _sistema->zeroEncoder(id); 
                Serial.printf(">> Cero (Offset) establecido para M%d\n", id+1);
            }
        }
        else if (cmd.startsWith("R") && cmd.length() == 3) {
            int id = cmd.charAt(1) - '1';
            bool estado = cmd.charAt(2) == '1';
            if (id >= 0 && id <= 3) {
                _sistema->writeExpanderPin(id, !estado); 
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
                
                _robotControl->setMotor(id, pot, dir);
                delay(ms); 
                _robotControl->setMotor(id, 0, 'S'); // Se detiene y guarda en NVS
            }
        }
        else if (cmd.length() >= 2 && cmd.charAt(0) >= '1' && cmd.charAt(0) <= '4') {
            int id = cmd.charAt(0) - '1';
            char dir = cmd.charAt(1);
            
            if (dir == 'S') {
                _robotControl->setMotor(id, 0, 'S'); 
            } else if (dir == 'H' || dir == 'A') {
                int pot = cmd.substring(2).toInt();
                _robotControl->setMotor(id, pot, dir);
            }
        }

        else if (cmd.startsWith("ML ")) {
            float x, y, z, v, phi;
            int argsParsed = sscanf(cmd.c_str(), "ML %f %f %f %f %f", &x, &y, &z, &v, &phi);
            
            if (argsParsed == 4) {
                _robotControl->moveL(x, y, z, v);
                Serial.printf(">> Ejecutando MoveL (Auto): X=%.1f, Y=%.1f, Z=%.1f, Vel=%.1f mm/s\n", x, y, z, v);
            } else if (argsParsed == 5) {
                float phi_rad = phi * PI / 180.0f; 
                _robotControl->moveL(x, y, z, v, phi_rad);
                Serial.printf(">> Ejecutando MoveL (Phi): X=%.1f, Y=%.1f, Z=%.1f, Vel=%.1f mm/s, Phi=%.1f°\n", x, y, z, v, phi);
            } else {
                Serial.println("[-] Error sintaxis. Uso: ML X Y Z V [Phi_grados]");
            }
        }
        else if (cmd.startsWith("MJ ")) {
            float x, y, z, v, phi;
            int argsParsed = sscanf(cmd.c_str(), "MJ %f %f %f %f %f", &x, &y, &z, &v, &phi);
            
            if (argsParsed == 4) {
                _robotControl->moveJ(x, y, z, v);
                Serial.printf(">> Ejecutando MoveJ (Auto): X=%.1f, Y=%.1f, Z=%.1f, Vel=%.1f mm/s\n", x, y, z, v);
            } else if (argsParsed == 5) {
                float phi_rad = phi * PI / 180.0f; 
                _robotControl->moveJ(x, y, z, v, phi_rad);
                Serial.printf(">> Ejecutando MoveJ (Phi): X=%.1f, Y=%.1f, Z=%.1f, Vel=%.1f mm/s, Phi=%.1f°\n", x, y, z, v, phi);
            } else {
                Serial.println("[-] Error sintaxis. Uso: MJ X Y Z V [Phi_grados]");
            }
        }
        else if (cmd.startsWith("MA ")) {
            float q1, q2, q3, q4, v;
            int argsParsed = sscanf(cmd.c_str(), "MA %f %f %f %f %f", &q1, &q2, &q3, &q4, &v);
            
            if (argsParsed == 5) {
                _robotControl->moveA(q1 * PI/180.0f, q2 * PI/180.0f, q3 * PI/180.0f, q4 * PI/180.0f, v);
                Serial.printf(">> Ejecutando MoveA: Q1=%.1f°, Q2=%.1f°, Q3=%.1f°, Q4=%.1f°, Vel=%.1f °/s\n", q1, q2, q3, q4, v);
            } else {
                Serial.println("[-] Error sintaxis. Uso: MA Q1 Q2 Q3 Q4 V");
            }
        }
        else if (cmd == "TUNE") {
            telemetriaActiva = false; // <-- APAGA LA TELEMETRÍA PARA NO COLISIONAR
            
            Serial.println("\n=================================================");
            Serial.println(" [!] COMANDO TUNE RECIBIDO");
            Serial.println(" [!] TELEMETRIA PAUSADA PARA EVITAR COLISIONES");
            Serial.println("=================================================\n");
            
            _robotControl->startAutoTune();
        }
        else if (cmd.startsWith("SETGAIN ")) {
            int id;
            float kp, ki, fup, fdown;
            if (sscanf(cmd.c_str(), "SETGAIN %d %f %f %f %f", &id, &kp, &ki, &fup, &fdown) == 5) {
                if (id >= 1 && id <= 4) {
                    _robotControl->setGains(id - 1, kp, ki, fup, fdown);
                    Serial.printf(">> Ganancias M%d actualizadas: Kp=%.2f, Ki=%.2f, F_Up=%.1f, F_Dn=%.1f\n", id, kp, ki, fup, fdown);
                }
            } else {
                Serial.println("[-] Error sintaxis. Uso: SETGAIN <M1-4> <Kp> <Ki> <F_up> <F_down>");
            }
        }
        else if (cmd == "GETGAINS") {
            _robotControl->printGains();
        }
    }
}

void MenuManager::run() {
    revisarColisiones();
    procesarComandosSeriales();
    imprimirTelemetria();
}