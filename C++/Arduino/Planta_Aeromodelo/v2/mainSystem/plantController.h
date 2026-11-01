#ifndef PLANTCONTROLLER_H
#define PLANTCONTROLLER_H

#include <Arduino.h>
#include "plantStatus.h"

enum ControlMode { CTRL_NONE, CTRL_PID_POSITION };

class plantController {
private:
    plantStatus* _planta;

    float _K, _Ti, _Td;
    float _setpointAngle, _maxSpeedPWM, _errorPrev, _integral;
    uint32_t _lastTime;
    ControlMode _currentMode;

public:
    plantController(plantStatus* plantaPtr);
    void setPID(float K, float Ti, float Td);
    void setTarget(float targetAngle, float maxSpeedPWM);
    void stop();
    void update();
};

#endif