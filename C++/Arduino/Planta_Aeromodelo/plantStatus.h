#ifndef PLANTSTATUS_H
#define PLANTSTATUS_H

#include <Arduino.h>
#include <Wire.h>
#include "systemConfig.h"
#include "driver/mcpwm.h"

class plantStatus {
private:
    SystemConfig* _sys;
    float* sensor_q;
    float* sensor_q_dot;

    unsigned long _dt_vel_us;
    float _max_angle_rad;
    float _max_pwm;

public:
    // Variables públicas para almacenar los datos leídos
    float angulo_as5600;
    float ax, ay, az, gx, gy, gz;

    plantStatus(SystemConfig* sysPtr);
    
    // Control de motor mediante MCPWM
    void applyMotor(float porcentaje, char dir);
    
    // Lectura de sensores I2C
    void initMPU6050();
    void readAS5600();
    void readMPU6050();
    void updateSensors();
};

#endif