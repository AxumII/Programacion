#ifndef PLANTCONTROLLER_H
#define PLANTCONTROLLER_H

#include <Arduino.h>
#include "plantStatus.h"

enum ControlMode { CTRL_NONE, CTRL_PID_POSITION };

class plantController {
private:
    plantStatus* _planta;

    // Parámetros PID Forma Estándar
    float _K;   // Ganancia Proporcional
    float _Ti;  // Tao Integral (Tiempo)
    float _Td;  // Tao Derivativo (Tiempo)

    // Variables de Estado del Controlador
    float _setpointAngle;
    float _maxSpeedPWM;
    float _errorPrev;
    float _integral;
    uint32_t _lastTime;

    ControlMode _currentMode;

public:
    // Constructor recibe la planta para poder actuar sobre los motores
    plantController(plantStatus* plantaPtr);

    // Ajustar parámetros del controlador
    void setPID(float K, float Ti, float Td);
    
    // Iniciar el control hacia un ángulo con velocidad (PWM) máxima
    void setTarget(float targetAngle, float maxSpeedPWM);
    
    // Detener el lazo de control
    void stop();

    // Actualización del lazo (debe ir en el loop)
    void update();
};

#endif