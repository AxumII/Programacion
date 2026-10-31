#include "plantController.h"

plantController::plantController(plantStatus* plantaPtr) {
    _planta = plantaPtr;
    _currentMode = CTRL_NONE;
    _K = 1.0; _Ti = 0.0; _Td = 0.0; 
    _errorPrev = 0; 
    _integral = 0;
}

void plantController::setPID(float K, float Ti, float Td) {
    _K = K;
    _Ti = Ti;
    _Td = Td;
}

void plantController::setTarget(float targetAngle, float maxSpeedPWM) {
    _setpointAngle = targetAngle;
    _maxSpeedPWM = (maxSpeedPWM > 100.0f) ? 100.0f : maxSpeedPWM;
    
    // Resetear estados al iniciar un nuevo movimiento
    _errorPrev = _setpointAngle - _planta->angulo_as5600;
    _integral = 0; 
    _lastTime = micros();
    _currentMode = CTRL_PID_POSITION;
}

void plantController::stop() {
    _currentMode = CTRL_NONE;
    _planta->applyMotor(0.0, 0, false); // Apagar motor
}

void plantController::update() {
    if (_currentMode != CTRL_PID_POSITION) return;

    uint32_t currentTime = micros();
    float dt = (currentTime - _lastTime) / 1000000.0f; // Delta de tiempo en segundos
    
    // Seguridad para ciclos ultra rápidos o bloqueos temporales
    if (dt <= 0.0f || dt > 0.5f) {
        _lastTime = currentTime;
        return; 
    }

    _lastTime = currentTime;

    // 1. Calcular Error
    float error = _setpointAngle - _planta->angulo_as5600;

    // 2. Término Proporcional
    float P = error;

    // 3. Término Integral (con Anti-Windup)
    float I = 0;
    if (_Ti > 0.001f) { // Si el Tao Integral no es cero
        _integral += error * dt;
        
        // Anti-Windup: No permitir que la integral supere la velocidad máxima posible
        float max_integral = _maxSpeedPWM / _K; 
        if (_integral > max_integral) _integral = max_integral;
        if (_integral < -max_integral) _integral = -max_integral;
        
        I = _integral / _Ti;
    }

    // 4. Término Derivativo
    float D = _Td * ((error - _errorPrev) / dt);
    _errorPrev = error;

    // 5. Señal de Control (PID Estándar)
    float u = _K * (P + I + D);

    // 6. Saturación de Velocidad Máxima (PWM límite)
    float duty = abs(u);
    if (duty > _maxSpeedPWM) duty = _maxSpeedPWM;

    // 7. Dirección
    int direction = 0;
    if (u > 0.5f) direction = 1;        // Horario
    else if (u < -0.5f) direction = -1; // Antihorario
    else duty = 0.0;                    // Dentro del umbral muerto

    // 8. Aplicar a la planta física
    _planta->applyMotor(duty, direction, false);
}