#ifndef PLANTSTATUS_H
#define PLANTSTATUS_H

#include <Arduino.h>
#include <Wire.h>
#include "systemConfig.h"

class plantStatus {
private:
    SystemConfig* _sys; 

    // Variables para calibración (Zero offset)
    float offset_angulo, offset_ax, offset_ay, offset_az, offset_gx, offset_gy, offset_gz;

    // Ajustes PWM del motor
    uint8_t PWM_BITS;
    int PWM_MAX;
    uint32_t currentFreq;

public:
    float angulo_as5600;
    float ax, ay, az, gx, gy, gz;

    plantStatus(SystemConfig* sysPtr);
    
    // Control de Motor Integrado
    void motorCoast();
    void motorBrake();
    void motorSet(int speedPercent);
    
    // Métodos de Sensores
    void readAS5600();
    void readMPU6050();
    void updateSensors();
    void printData(); 
    void calibrateSensors();
    
    // Serial Terminal
    void serialMotorControl();
};

#endif