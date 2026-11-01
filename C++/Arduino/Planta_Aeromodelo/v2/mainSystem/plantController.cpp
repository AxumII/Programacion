#include "plantController.h"

plantController::plantController(plantStatus* plantaPtr) {
    _planta = plantaPtr;
    _currentMode = CTRL_NONE;
    _K = 1.0; _Ti = 0.0; _Td = 0.0; 
    _errorPrev = 0; 
    _integral = 0;
}

void plantController::setPID(float K, float Ti, float Td) {
    _K = K; _Ti = Ti; _Td = Td;
}

void plantController::setTarget(float targetAngle, float maxSpeedPWM) {
    _setpointAngle = targetAngle;
    _maxSpeedPWM = (maxSpeedPWM > 100.0f) ? 100.0f : maxSpeedPWM;
    _errorPrev = _setpointAngle - _planta->angulo_as5600;
    _integral = 0; 
    _lastTime = micros();
    _currentMode = CTRL_PID_POSITION;
}

void plantController::stop() {
    _currentMode = CTRL_NONE;
    _planta->applyMotor(0.0, 0, false);
}

void plantController::update() {
    if (_currentMode != CTRL_PID_POSITION) return;

    uint32_t currentTime = micros();
    float dt = (currentTime - _lastTime) / 1000000.0f; 
    
    if (dt <= 0.0f || dt > 0.5f) {
        _lastTime = currentTime;
        return; 
    }
    _lastTime = currentTime;

    float error = _setpointAngle - _planta->angulo_as5600;
    
    // Si el error es mayor a 180, buscar el camino más corto (para sensores circulares 0-360)
    if (error > 180.0f) error -= 360.0f;
    if (error < -180.0f) error += 360.0f;

    float P = error;
    float I = 0;
    if (_Ti > 0.001f) { 
        _integral += error * dt;
        float max_integral = _maxSpeedPWM / _K; 
        if (_integral > max_integral) _integral = max_integral;
        if (_integral < -max_integral) _integral = -max_integral;
        I = _integral / _Ti;
    }

    float D = _Td * ((error - _errorPrev) / dt);
    _errorPrev = error;

    float u = _K * (P + I + D);
    float duty = abs(u);
    if (duty > _maxSpeedPWM) duty = _maxSpeedPWM;

    int direction = 0;
    if (u > 0.5f) direction = 1;        
    else if (u < -0.5f) direction = -1; 
    else duty = 0.0;                    

    _planta->applyMotor(duty, direction, false);
}