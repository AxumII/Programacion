#include "plantStatus.h"

plantStatus::plantStatus(SystemConfig* sysPtr){
    _sys = sysPtr; 
    sensor_q = nullptr;
    sensor_q_dot = nullptr;

    // --- CONSTANTES DEL SISTEMA ---
    _dt_vel_us = 2500;  // 400 Hz
    _max_angle_rad = 90.0f * (M_PI / 180.0f); 
    _max_pwm = 100.0f;  
}

// Inicializar el MPU6050 (Necesario para sacarlo del modo sleep)
void plantStatus::initMPU6050() {
    Wire.beginTransmission(0x68); // Dirección I2C del MPU6050
    Wire.write(0x6B);             // Registro PWR_MGMT_1
    Wire.write(0x00);             // Escribir 0 para despertar el sensor
    Wire.endTransmission(true);
}

// Control del motor usando MCPWM en el Unit 0, Timer 0
void plantStatus::applyMotor(float porcentaje, char dir) {
    // Restringir el porcentaje entre 0 y 100%
    porcentaje = constrain(porcentaje, 0.0f, 100.0f);

    // Detener motor
    if (porcentaje == 0.0f || dir == 'S') {
        mcpwm_set_duty(MCPWM_UNIT_0, MCPWM_TIMER_0, MCPWM_OPR_A, 0);
        mcpwm_set_duty(MCPWM_UNIT_0, MCPWM_TIMER_0, MCPWM_OPR_B, 0);
    } 
    // Movimiento hacia adelante / Horario
    else if (dir == 'H' || dir == 'R') {
        mcpwm_set_duty(MCPWM_UNIT_0, MCPWM_TIMER_0, MCPWM_OPR_B, 0);
        mcpwm_set_duty(MCPWM_UNIT_0, MCPWM_TIMER_0, MCPWM_OPR_A, porcentaje);
    } 
    // Movimiento hacia atrás / Antihorario
    else if (dir == 'A' || dir == 'L') {
        mcpwm_set_duty(MCPWM_UNIT_0, MCPWM_TIMER_0, MCPWM_OPR_A, 0);
        mcpwm_set_duty(MCPWM_UNIT_0, MCPWM_TIMER_0, MCPWM_OPR_B, porcentaje);
    }
}

// Leer ángulo del AS5600
void plantStatus::readAS5600() {
    Wire.beginTransmission(0x36); // Dirección I2C por defecto del AS5600
    Wire.write(0x0E);             // Registro de ángulo raw (0x0E y 0x0F)
    Wire.endTransmission(false);
    Wire.requestFrom(0x36, 2, true);
    
    if (Wire.available() == 2) {
        uint16_t rawAngle = Wire.read() << 8;
        rawAngle |= Wire.read();
        
        // Convertir el valor raw (0-4095) a grados (0-360)
        angulo_as5600 = (rawAngle * 360.0f) / 4096.0f;
    }
}

// Leer Acelerómetro y Giroscopio del MPU6050
void plantStatus::readMPU6050() {
    Wire.beginTransmission(0x68);
    Wire.write(0x3B);  // Registro inicial de aceleración (ACCEL_XOUT_H)
    Wire.endTransmission(false);
    Wire.requestFrom(0x68, 14, true);  // Solicitar 14 bytes
    
    if (Wire.available() == 14) {
        // Acelerómetro (Divisor 16384.0 para rango de +/- 2g por defecto)
        ax = (int16_t)(Wire.read() << 8 | Wire.read()) / 16384.0f;  
        ay = (int16_t)(Wire.read() << 8 | Wire.read()) / 16384.0f;  
        az = (int16_t)(Wire.read() << 8 | Wire.read()) / 16384.0f;  
        
        // Temperatura (La ignoramos pero leemos los bytes para avanzar el buffer)
        Wire.read(); Wire.read();
        
        // Giroscopio (Divisor 131.0 para rango de +/- 250 grados/s por defecto)
        gx = (int16_t)(Wire.read() << 8 | Wire.read()) / 131.0f;  
        gy = (int16_t)(Wire.read() << 8 | Wire.read()) / 131.0f;  
        gz = (int16_t)(Wire.read() << 8 | Wire.read()) / 131.0f;  
    }
}

// Función maestra para actualizar ambos sensores a la vez
void plantStatus::updateSensors() {
    readAS5600();
    readMPU6050();
}