#include "MenuManager.h"

MenuManager::MenuManager(SystemConfig* sys, ServoControlling* servo) {
    _sys = sys;
    _servo = servo;
}

void MenuManager::update() {
    procesarComandosSeriales();
}

void MenuManager::procesarComandosSeriales() {
    if (Serial.available() > 0) {
        String cmd = Serial.readStringUntil('\n');
        cmd.trim(); cmd.toUpperCase();

        if (cmd == "S") {
            Servo1.stop(); Servo2.stop(); Servo3.stop(); 
            if (_servo->isServo4) Servo4.stop();
            Servo5.stop(); // Detiene también el Gripper
            Serial.println("\n[!!!] PARADA DE EMERGENCIA EJECUTADA [!!!]");
        } 
        else if (cmd == "RUTINA") {
            rutinaPickAndPlace();
        }
        else if (cmd.startsWith("G ")) { // Comando manual para el gripper
            float gAng;
            if (sscanf(cmd.c_str(), "G %f", &gAng) == 1) {
                _servo->setGripperAngle(gAng);
                Serial.printf(">> Gripper (Servo 5) movido a: %.1f°\n", gAng);
            }
        }
        else if (cmd.startsWith("MA ")) {
            float q1, q2, q3, q4, v;
            if (sscanf(cmd.c_str(), "MA %f %f %f %f %f", &q1, &q2, &q3, &q4, &v) == 5) {
                _servo->ReachForAnglesAndStop(q1, q2, q3, q4, (int)v);
                Serial.printf(">> MoveA: Q1=%.1f°, Q2=%.1f°, Q3=%.1f°, Q4=%.1f°, Vel=%.1f\n", q1, q2, q3, q4, v);
            }
        }
        else if (cmd.startsWith("MJ ")) {
            float x, y, z, v, phi;
            int argsParsed = sscanf(cmd.c_str(), "MJ %f %f %f %f %f", &x, &y, &z, &v, &phi);
            
            if (argsParsed == 5) { 
                _servo->moveJ(Eigen::Vector3f(x, y, z), (int)v, phi, 0.0f); 
                Serial.printf(">> MovJ: X=%.1f, Y=%.1f, Z=%.1f, Vel=%.1f, Phi=%.1f°\n", x, y, z, v, phi); 
            } else if (argsParsed == 4) {
                _servo->moveJ(Eigen::Vector3f(x, y, z), (int)v); 
                Serial.printf(">> MovJ: X=%.1f, Y=%.1f, Z=%.1f, Vel=%.1f\n", x, y, z, v); 
            }
        }
        else if (cmd == "HZ") {
            _servo->goExtendedHome();
            Serial.println(">> Ejecutando Extended Home (0, 0, 0, 0)");
        }
        else if (cmd == "H") { 
            _servo->goHome();
            Serial.println(">> Ejecutando Home (0, 90, -90, 0)");
        }
    }
}

bool MenuManager::esperarPasoRutina(unsigned long tiempoEspera_ms) {
    unsigned long inicio = millis();
    while (millis() - inicio < tiempoEspera_ms) {
        if (Serial.available() > 0) {
            String cmd = Serial.readStringUntil('\n');
            cmd.trim(); cmd.toUpperCase();
            if (cmd == "S") {
                Servo1.stop(); Servo2.stop(); Servo3.stop(); 
                if (_servo->isServo4) Servo4.stop();
                Servo5.stop();
                Serial.println("\n[!!!] PARADA DE EMERGENCIA - RUTINA ABORTADA [!!!]");
                return false; 
            }
        }
        yield(); 
    }
    return true; 
}

void MenuManager::rutinaPickAndPlace() {
    Serial.println("\n>> [RUTINA] Iniciando Pick & Place. Envíe 'S' para abortar.");
    bool ejecutando = true;
    
    int v_mm = 60;   
    float phi_down = -90.0f; 

    while (ejecutando) {
        Serial.println("-> Ejecutando: Home");
        _servo->goHome();
        if (!esperarPasoRutina(4000)) break;

        Serial.println("-> Ejecutando: Aproximación a recogida (MovJ)");
        if (!_servo->moveJ(Eigen::Vector3f(200.0f, 50.0f, 150.0f), v_mm, phi_down, 0.0f)) {
            Serial.println("[!] ERROR IK: Punto inalcanzable.");
        }
        if (!esperarPasoRutina(3000)) break;

        Serial.println("-> Ejecutando: Bajando a recoger (MovJ)");
        _servo->moveJ(Eigen::Vector3f(200.0f, 50.0f, 50.0f), v_mm, phi_down, 0.0f);
        if (!esperarPasoRutina(2000)) break;

        Serial.println("-> Ejecutando: Subiendo con carga (MovJ)");
        _servo->moveJ(Eigen::Vector3f(200.0f, 50.0f, 150.0f), v_mm, phi_down, 0.0f);
        if (!esperarPasoRutina(2000)) break;

        Serial.println("-> Ejecutando: Traslado a destino (MovJ)");
        _servo->moveJ(Eigen::Vector3f(200.0f, -50.0f, 150.0f), v_mm, phi_down, 0.0f);
        if (!esperarPasoRutina(3500)) break;

        Serial.println("\n>> [RUTINA] Ciclo completado. Reiniciando...\n");
    }
}