#ifndef MENUMANAGER_H
#define MENUMANAGER_H

#include <Arduino.h> // Necesario para reconocer Serial, String, millis(), etc.
#include "SystemConfig.h"
#include "ControlManager.h"

class MenuManager {
private:
    ControlManager* _robotControl;
    SystemConfig* _sistema;
    
    // Punteros a la memoria compartida de sensores
    float* sensor_q;
    float* sensor_q_dot;
    float* sensor_i_meas;
    float* sensor_v_fuente;
    
    const float* limites_corriente;

    // Variables de control de tiempo
    bool telemetriaActiva;
    unsigned long ultimaTelemetria;
    unsigned long ultimaRevisionColision;

public:
    // Constructor
    MenuManager(ControlManager* robotControl, SystemConfig* sistema, const float* limites);
    
    // Métodos
    void joinSensors(float* q, float* q_dot, float* i_meas, float* v_fuente);
    void procesarComandosSeriales();
    void revisarColisiones();
    void imprimirTelemetria();
    void run(); // Ejecuta las rutinas asíncronas
};

#endif