#include "ControlManager.h"
#include <Arduino.h>     
#include <cmath>

ControlManager::ControlManager(Kinematic* kinPtr, SystemConfig* sysPtr) {
    _kinematic = kinPtr;
    _sys = sysPtr; 
    sensor_q = nullptr;
    sensor_q_dot = nullptr;
    sensor_i_meas = nullptr;
    sensor_v_batt = nullptr;

    // --- Inicialización del Filtro de Kalman ---
    _H << 1.0f, 0.0f; // Solo observamos la posición

    // Varianza del sensor (Ruido de medición). Ajusta según el PPR de tu encoder.
    _R = 0.01f; 

    // Matriz de ruido del proceso. 
    // Valores más altos confían más en la medida cruda; valores bajos filtran más pero añaden lag.
    _Q << 0.001f, 0.0f,
          0.0f,   0.01f;

    for(int i = 0; i < 4; i++) {
        _x_est[i] << 0.0f, 0.0f; 
        _P_cov[i] << 1.0f, 0.0f, 
                 0.0f, 1.0f;
    }
}

bool ControlManager::joinSensors(float* q_ptr, float* q_dot_ptr, float* i_meas_ptr, float* v_batt_ptr) {
    if(!q_ptr || !q_dot_ptr || !i_meas_ptr || !v_batt_ptr) return false;
    sensor_q = q_ptr;
    sensor_q_dot = q_dot_ptr;
    sensor_i_meas = i_meas_ptr;
    sensor_v_batt = v_batt_ptr;
    return true;
}

void ControlManager::updateVelocityKalman(int id, float z_measured, float dt) {
    Eigen::Matrix2f A;
    A << 1.0f, dt,
         0.0f, 1.0f;

    // --- PREDICCIÓN ---
    Eigen::Vector2f x_pred = A * _x_est[id];
    Eigen::Matrix2f P_pred = A * _P_cov[id] * A.transpose() + _Q; 

    // --- ACTUALIZACIÓN ---
    float y = z_measured - (_H * x_pred)(0, 0); 
    float S = (_H * P_pred * _H.transpose())(0, 0) + _R;
    Eigen::Vector2f K = P_pred * _H.transpose() / S;

    _x_est[id] = x_pred + K * y;
    
    Eigen::Matrix2f I = Eigen::Matrix2f::Identity();
    _P_cov[id] = (I - K * _H) * P_pred; 
}

void ControlManager::updateSensors(float dt) {
    if (dt <= 0.0001f || !_sys || !sensor_q || !sensor_q_dot) return;

    for (int i = 0; i < 4; i++) {
        // Obtenemos la medida cruda[cite: 17, 19]
        float q_raw = _sys->getAngle(i);

        // Pasamos la medida por el filtro de Kalman
        updateVelocityKalman(i, q_raw, dt);

        // Guardamos los valores filtrados en la memoria compartida
        sensor_q[i] = _x_est[i](0);       // Ángulo óptimo estimado
        sensor_q_dot[i] = _x_est[i](1);   // Velocidad óptima estimada

        // Corriente del Motor[cite: 17]
        if (sensor_i_meas) {
            sensor_i_meas[i] = _sys->getCurrent(i);
        }
    }

    // Voltaje de Batería[cite: 17]
    if (sensor_v_batt) {
        *sensor_v_batt = _sys->getBatteryVoltage();
    }
}

void ControlManager::setMotor(int id, int pwm, char dir) {
    if (_sys) {
        _sys->applyMotor(id, pwm, dir);
    }
}