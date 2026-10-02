#ifndef WIFIMANAGER_H
#define WIFIMANAGER_H

#include <Arduino.h>
#include <WiFi.h>
#include "SystemConfig.h"
#include "ControlManager.h"

class WiFiManager {
private:
    ControlManager* _control;
    SystemConfig* _sistema;
    const float* _limitesCorriente;
    
    // Servidor TCP en el puerto 8080 (puedes cambiarlo)
    WiFiServer _server;
    WiFiClient _client;

    // Punteros a la memoria global compartida
    float* _q;
    float* _q_dot;
    float* _i_meas;
    float* _v_fuente;
    byte _pinElevador = 255;

    // Método interno para procesar la cadena de texto recibida
    void processCommand(String cmd);

public:
    // Constructor
    WiFiManager(ControlManager* control, SystemConfig* sistema, const float* limitesCorriente, uint16_t port = 8080);
    
    // Inicializa el servidor TCP
    void begin();
    
    // Rutina de ejecución asíncrona (debe ir en el loop)
    void run();
    
    // Métodos de vinculación de memoria
    void joinSensors(float* q, float* q_dot, float* i_meas, float* v_fuente);
    void setPinElevador(byte pin);
};

#endif