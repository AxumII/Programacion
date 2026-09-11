#ifndef MENUMANAGER_H
#define MENUMANAGER_H

#include <Arduino.h>
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

    int modoLogActivo = 0; 
    unsigned long inicioLog = 0;
    unsigned long ultimoMuestreoLog = 0;
    unsigned long duracionLog = 0;
    
    // Pin asignado para el relé/elevador
    byte pinElevador = 255; 

public:
    MenuManager(ControlManager* robotControl, SystemConfig* sistema, const float* limites);
    
    void joinSensors(float* q, float* q_dot, float* i_meas, float* v_fuente);
    
    // Método para inyectar el pin desde el MainSystem
    void setPinElevador(byte pin) { pinElevador = pin; }
    
    void procesarComandosSeriales();
    void revisarColisiones();
    void imprimirTelemetria();
    void ejecutarLogDinamico(); 
    void run();
};

#endif