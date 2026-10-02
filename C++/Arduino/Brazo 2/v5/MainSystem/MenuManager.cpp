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

        // ==========================================
        // COMANDOS DEL SISTEMA Y DEBUG
        // ==========================================
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
        
        // ==========================================
        // COMANDOS DE HARDWARE ADICIONAL
        // ==========================================
        else if (cmd == "E1" || cmd == "EH") {
            if (pinElevador != 255) {
                digitalWrite(pinElevador, HIGH);
                Serial.println(">> Elevador/Relé: ACTIVADO");
            }
        }
        else if (cmd == "E0" || cmd == "ED") {
            if (pinElevador != 255) {
                digitalWrite(pinElevador, LOW);
                Serial.println(">> Elevador/Relé: DESACTIVADO");
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

        // ==========================================
        // COMANDOS MANUALES DE MOTORES
        // ==========================================
        else if (cmd.startsWith("T") && cmd.indexOf(',') > 0) {
            int id = cmd.charAt(1) - '1';
            char dir = cmd.charAt(2);
            int commaIdx = cmd.indexOf(',');
            
            if (id >= 0 && id <= 3 && (dir == 'H' || dir == 'A')) {
                float pwm = cmd.substring(3, commaIdx).toFloat();
                int ms = cmd.substring(commaIdx + 1).toInt();
                
                // Llamada al nuevo método con temporización
                _robotControl->movMPWMT(id, pwm, dir, ms);
                Serial.printf(">> Motor temporizado: M%d -> Dir: %c | PWM: %.1f | ms: %d\n", id + 1, dir, pwm, ms);
            }
        }
        else if (cmd.length() >= 2 && cmd.charAt(0) >= '1' && cmd.charAt(0) <= '4') {
            int id = cmd.charAt(0) - '1'; // Convierte '1'-'4' a índice 0-3
            char dir = cmd.charAt(1);     // Obtiene la dirección 'H', 'A', o 'S'
            float pwm = 0.0f;
            
            // Extrae el valor PWM si la cadena incluye número
            if (cmd.length() > 2) {
                pwm = cmd.substring(2).toFloat(); 
            }
            
            // Llamada al nuevo método continuo
            if (dir == 'H' || dir == 'A' || dir == 'S') {
                _robotControl->movMPWM(id, pwm, dir);
                Serial.printf(">> Motor manual: M%d -> Dir: %c | PWM: %.1f\n", id + 1, dir, pwm);
            }
        }

        // ==========================================
        // COMANDOS DE LÍNEA Y CÍRCULO (IK Y DLS)
        // ==========================================
        else if (cmd.startsWith("MLJ ")) {
            float x, y, z, v, phi;
            int argsParsed = sscanf(cmd.c_str(), "MLJ %f %f %f %f %f", &x, &y, &z, &v, &phi);
            if (argsParsed == 4) { 
                _robotControl->movLJc(x, y, z, v); 
                Serial.printf(">> MovLJc (Auto): X=%.1f, Y=%.1f, Z=%.1f, Vel=%.1f\n", x, y, z, v); 
            } else if (argsParsed == 5) { 
                _robotControl->movLJc(x, y, z, v, phi * PI / 180.0f); 
                Serial.printf(">> MovLJc (Phi): X=%.1f, Y=%.1f, Z=%.1f, Vel=%.1f, Phi=%.1f°\n", x, y, z, v, phi); 
            }
        }
        else if (cmd.startsWith("ML ")) {
            float x, y, z, v, phi;
            int argsParsed = sscanf(cmd.c_str(), "ML %f %f %f %f %f", &x, &y, &z, &v, &phi);
            if (argsParsed == 4) { 
                _robotControl->movL(x, y, z, v); 
                Serial.printf(">> MovL (IK Auto): X=%.1f, Y=%.1f, Z=%.1f, Vel=%.1f\n", x, y, z, v); 
            } else if (argsParsed == 5) { 
                _robotControl->movL(x, y, z, v, (float)(phi * PI / 180.0f)); 
                Serial.printf(">> MovL (IK Phi): X=%.1f, Y=%.1f, Z=%.1f, Vel=%.1f, Phi=%.1f°\n", x, y, z, v, phi); 
            }
        }
        else if (cmd.startsWith("MJ ")) {
            float x, y, z, v, phi;
            int argsParsed = sscanf(cmd.c_str(), "MJ %f %f %f %f %f", &x, &y, &z, &v, &phi);
            if (argsParsed == 4) { 
                _robotControl->movJ(x, y, z, v); 
                Serial.printf(">> MovJ (Auto): X=%.1f, Y=%.1f, Z=%.1f, Vel=%.1f\n", x, y, z, v); 
            } else if (argsParsed == 5) { 
                _robotControl->movJ(x, y, z, v, (float)(phi * PI / 180.0f)); 
                Serial.printf(">> MovJ (Phi): X=%.1f, Y=%.1f, Z=%.1f, Vel=%.1f, Phi=%.1f°\n", x, y, z, v, phi); 
            }
        }
        else if (cmd.startsWith("MC ")) {
            float x1, y1, z1, x2, y2, z2, v, phi;
            int argsParsed = sscanf(cmd.c_str(), "MC %f %f %f %f %f %f %f %f", &x1, &y1, &z1, &x2, &y2, &z2, &v, &phi);
            if (argsParsed == 7) { 
                _robotControl->movC(x1, y1, z1, x2, y2, z2, v); 
                Serial.printf(">> MovC (IK): Via(%.1f, %.1f, %.1f) Fin(%.1f, %.1f, %.1f) V=%.1f\n", x1, y1, z1, x2, y2, z2, v); 
            } else if (argsParsed == 8) { 
                _robotControl->movC(x1, y1, z1, x2, y2, z2, v, (float)(phi * PI / 180.0f)); 
                Serial.printf(">> MovC (IK Phi): Via(%.1f,%.1f,%.1f) Fin(%.1f,%.1f,%.1f) V=%.1f Phi=%.1f°\n", x1, y1, z1, x2, y2, z2, v, phi); 
            }
        }
        else if (cmd.startsWith("MCJ ")) {
            float x1, y1, z1, x2, y2, z2, v, phi;
            int argsParsed = sscanf(cmd.c_str(), "MCJ %f %f %f %f %f %f %f %f", &x1, &y1, &z1, &x2, &y2, &z2, &v, &phi);
            if (argsParsed == 7) { 
                _robotControl->movCJc(x1, y1, z1, x2, y2, z2, v); 
                Serial.printf(">> MovCJc (DLS): Via(%.1f, %.1f, %.1f) Fin(%.1f, %.1f, %.1f) V=%.1f\n", x1, y1, z1, x2, y2, z2, v); 
            } else if (argsParsed == 8) { 
                _robotControl->movCJc(x1, y1, z1, x2, y2, z2, v, phi * PI / 180.0f); 
                Serial.printf(">> MovCJc (DLS Phi): Via(%.1f,%.1f,%.1f) Fin(%.1f,%.1f,%.1f) V=%.1f Phi=%.1f°\n", x1, y1, z1, x2, y2, z2, v, phi); 
            }
        }
        else if (cmd.startsWith("MA ")) {
            float q1, q2, q3, q4, v;
            if (sscanf(cmd.c_str(), "MA %f %f %f %f %f", &q1, &q2, &q3, &q4, &v) == 5) {
                _robotControl->movA(q1 * PI/180.0f, q2 * PI/180.0f, q3 * PI/180.0f, q4 * PI/180.0f, v);
                Serial.printf(">> Ejecutando MoveA: Q1=%.1f°, Q2=%.1f°, Q3=%.1f°, Q4=%.1f°, Vel=%.1f °/s\n", q1, q2, q3, q4, v);
            }
        }
        else if (cmd.startsWith("MZJ ")) {
            float z, v, phi;
            int argsParsed = sscanf(cmd.c_str(), "MZJ %f %f %f", &z, &v, &phi);
            if (argsParsed == 3) { 
                _robotControl->movZJc(z, v, phi * PI / 180.0f); 
                Serial.printf(">> MovZJc (DLS): Z=%.1f, Vel=%.1f, Phi=%.1f°\n", z, v, phi); 
            }
        }
        else if (cmd.startsWith("MZ ")) {
            float z, v, phi;
            int argsParsed = sscanf(cmd.c_str(), "MZ %f %f %f", &z, &v, &phi);
            if (argsParsed == 3) { 
                _robotControl->movZ(z, v, (float)(phi * PI / 180.0f)); 
                Serial.printf(">> MovZ (IK): Z=%.1f, Vel=%.1f, Phi=%.1f°\n", z, v, phi); 
            }
        }

        // --- NUEVOS COMANDOS HOME ---
        else if (cmd.startsWith("HZ")) {
            float v = 30.0f; // Velocidad por defecto
            if (sscanf(cmd.c_str(), "HOMZ %f", &v) == 1) {
                _robotControl->homZ(v);
            } else {
                _robotControl->homZ();
            }
            Serial.printf(">> Ejecutando HomZ: Q={0, 0, 0, 0}, Vel=%.1f °/s\n", v);
        }
        else if (cmd.startsWith("H") && cmd.indexOf("HOMZ") == -1) { 
            // Verificamos que no contenga "HOMZ" para no confundir los comandos
            float v = 30.0f; // Velocidad por defecto
            if (sscanf(cmd.c_str(), "HOM %f", &v) == 1) {
                _robotControl->hom(v);
            } else {
                _robotControl->hom();
            }
            Serial.printf(">> Ejecutando Hom: Q={90, -90, 90, -90}, Vel=%.1f °/s\n", v);
        }

        // ==========================================
        // COMANDOS DE SINTONIZACIÓN Y GANANCIAS
        // ==========================================
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
        // ==========================================
        // COMANDOS DE CAPTURA DINAMICA (OSCILOSCOPIO)
        // ==========================================
        else if (cmd.startsWith("LOG ")) {
            int tipo;
            unsigned long tiempo;
            // Sintaxis: LOG <tipo> <tiempo_ms> 
            // Tipos: 1 = Ángulos, 2 = Velocidad, 3 = Corriente
            if (sscanf(cmd.c_str(), "LOG %d %lu", &tipo, &tiempo) == 2) {
                if (tipo >= 1 && tipo <= 3) {
                    modoLogActivo = tipo;
                    duracionLog = tiempo;
                    inicioLog = millis();
                    ultimoMuestreoLog = inicioLog;
                    telemetriaActiva = false; // Pausar telemetría normal
                    
                    Serial.println("\n--- INICIANDO DATALOGGER ---");
                    if (tipo == 1) Serial.println("Tiempo(ms),Q1(deg),Q2(deg),Q3(deg),Q4(deg)");
                    else if (tipo == 2) Serial.println("Tiempo(ms),V1(rad_s),V2(rad_s),V3(rad_s),V4(rad_s)");
                    else if (tipo == 3) Serial.println("Tiempo(ms),I1(A),I2(A),I3(A),I4(A)");
                    // Ahora el sistema grabará en CSV lo que sea que hagas a continuación.
                }
            } else {
                Serial.println("[-] Uso: LOG <1=Pos_Angular, 2=Velocidad, 3=Corriente> <tiempo_ms>");
            }
        }
    }
}

// =================================================================
// OSCILOSCOPIO DIGITAL PARA EVALUAR SOBREIMPULSO Y ESTABILIDAD
// =================================================================
void MenuManager::ejecutarLogDinamico() {
    if (modoLogActivo == 0) return;
    
    unsigned long t_actual = millis();
    unsigned long t_transcurrido = t_actual - inicioLog;
    
    // Muestreo a 100 Hz (cada 10 ms)
    if (t_actual - ultimoMuestreoLog >= 10) {
        ultimoMuestreoLog = t_actual;
        
        if (modoLogActivo == 1) { // Control Angular (Posición de las articulaciones)
            Serial.printf("%lu,%.2f,%.2f,%.2f,%.2f\n", t_transcurrido, 
                sensor_q[0]*180.0f/PI, sensor_q[1]*180.0f/PI, 
                sensor_q[2]*180.0f/PI, sensor_q[3]*180.0f/PI);
        } 
        else if (modoLogActivo == 2) { // Control de Velocidad
            Serial.printf("%lu,%.3f,%.3f,%.3f,%.3f\n", t_transcurrido, 
                sensor_q_dot[0], sensor_q_dot[1], sensor_q_dot[2], sensor_q_dot[3]);
        } 
        else if (modoLogActivo == 3) { // Esfuerzo de Control (Corriente)
            Serial.printf("%lu,%.3f,%.3f,%.3f,%.3f\n", t_transcurrido, 
                sensor_i_meas[0], sensor_i_meas[1], sensor_i_meas[2], sensor_i_meas[3]);
        }
    }
    
    // Terminar la captura automáticamente
    if (t_transcurrido >= duracionLog) {
        modoLogActivo = 0;
        telemetriaActiva = true; // Restaurar telemetría
        Serial.println("--- FIN DEL REGISTRO. Copia los datos para graficar ---");
    }
}

void MenuManager::run() {
    revisarColisiones();
    procesarComandosSeriales();
    
    // Solo imprimir telemetría si no estamos haciendo un test ni grabando un log
    if (modoLogActivo == 0) { 
        imprimirTelemetria(); 
    }
    
    ejecutarLogDinamico();
}