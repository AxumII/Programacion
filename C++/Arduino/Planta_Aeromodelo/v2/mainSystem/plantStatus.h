#ifndef PLANTSTATUS_H
#define PLANTSTATUS_H

#include <Arduino.h>
#include <Wire.h>
#include "systemConfig.h"

// Enumerador para la máquina de estados de los perfiles
enum MotorProfile { PROFILE_NONE, PROFILE_STEP, PROFILE_RAMP };

class plantStatus {
private:
    SystemConfig* _sys; 

    // Variables para calibración (Zero offset)[cite: 7]
    float offset_angulo, offset_ax, offset_ay, offset_az, offset_gx, offset_gy, offset_gz;
    float currentDuty;
    // Ajustes PWM
    uint32_t currentFreq;

    // Variables para generador de perfiles
    MotorProfile _currentProfile;
    uint32_t _profileStartTime;
    uint32_t _profileDuration;
    float _profileStartDuty;
    float _profileEndDuty;
    int _profileDirection;

public:
    float angulo_as5600; 
    float ax, ay, az, gx, gy, gz; 

    plantStatus(SystemConfig* sysPtr); 
    
    // Control de Motor Integrado
    void applyMotor(float duty, int direction, bool eStop = false); //
    
    // Generador de Perfiles no bloqueantes
    void startStep(float targetDuty, int direction, uint32_t duration_ms);
    void startRamp(float startDuty, float endDuty, int direction, uint32_t duration_ms);
    void updateProfile();
    
    // Métodos de Sensores
    void readAS5600(); 
    void readMPU6050(); 
    void updateSensors(); 
    void calibrateSensors(); 

};

#endif