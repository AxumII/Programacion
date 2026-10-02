#include "ControlManager.h"
#include <Arduino.h>     
#include <cmath>


ControlManager::ControlManager(Kinematic* kinPtr, SystemConfig* sysPtr) {
    _kinematic = kinPtr;
    _sys = sysPtr; 
    sensor_q = nullptr;
    sensor_q_dot = nullptr;
    sensor_i = nullptr;
    sensor_v_fuente = nullptr;

    / --- CONSTANTES DEL SISTEMA ---
    _dt_sensor_us = 100 //10000 Hz
    _dt_pos_us = 10000; // 100 Hz
    _dt_vel_us = 2500;  // 400 Hz
    _dt_tune_us = 5000; // 200 Hz 

    _max_vel_rad = 30.0f * (M_PI / 180.0f); 
    _max_pwm = 100.0f;       
    _max_int_pwm = 80.0f;  


    _encoder_res_rad_step_jgy = M_PI*(1/(4*11*1000))
    _encoder_res_rad_step_31zy = M_PI*(1/(4*5*1154))

    // Constantes de control 


    //Limites Angulares 
    _min_angles[0] = -175.0f * (M_PI / 180.0f); _max_angles[0] = 175.0f * (M_PI / 180.0f); 
    _min_angles[1] = -3.0f * (M_PI / 180.0f);   _max_angles[1] = 135.0f * (M_PI / 180.0f); 
    _min_angles[2] = -160.0f * (M_PI / 180.0f); _max_angles[2] = 160.0f * (M_PI / 180.0f); 
    _min_angles[3] = -100.0f * (M_PI / 180.0f); _max_angles[3] = 100.0f * (M_PI / 180.0f);


    //Parametros Kalman
    _H << 1.0f, 0.0f; 
    _R = ((_encoder_res_rad_step_31zy)**2/(12))f; 
    _Q << 0.001f, 0.0f, 0.0f, 0.01f;

    for(int i = 0; i < 4; i++) {
        _x_est[i] << 0.0f, 0.0f; 
        _P_cov[i] << 1.0f, 0.0f, 0.0f, 1.0f;
    }
}

bool ControlManager::joinSensors(float* q_ptr, float* q_dot_ptr, float* i_meas_ptr, float* v_fuente_ptr) {
    if(!q_ptr || !q_dot_ptr || !i_meas_ptr || !v_fuente_ptr) return false;
    sensor_q = q_ptr; sensor_q_dot = q_dot_ptr; sensor_i = i_meas_ptr; sensor_v_fuente = v_fuente_ptr;
    return true;
}

void ControlManager::updateVelocityKalman(int id, float z_measured) {
    Eigen::Matrix2f A; A << 1.0f,  _dt_sensor_us, 0.0f, 1.0f;
    Eigen::Vector2f x_pred = A * _x_est[id];
    Eigen::Matrix2f P_pred = A * _P_cov[id] * A.transpose() + _Q; 
    float y = z_measured - (_H * x_pred)(0, 0); 
    float S = (_H * P_pred * _H.transpose())(0, 0) + _R;
    Eigen::Vector2f K = P_pred * _H.transpose() / S;
    _x_est[id] = x_pred + K * y;
    Eigen::Matrix2f I = Eigen::Matrix2f::Identity();
    _P_cov[id] = (I - K * _H) * P_pred; 
}

void ControlManager::updateSensors() {
    if (!_sys || !sensor_q || !sensor_q_dot) return;
    for (int i = 0; i < 4; i++) {
        float q_raw = _sys->getAngle(i); 
        updateVelocityKalman(i, q_raw);
        sensor_q[i] = _x_est[i](0);       
        sensor_q_dot[i] = _x_est[i](1);   
    }
    static int adc_channel = 0;
    if (sensor_i) {
        sensor_i[adc_channel] = _sys->getCurrent(adc_channel);
        adc_channel = (adc_channel + 1) % 4;
    }
    if (sensor_v_fuente) *sensor_v_fuente = _sys->getSourceVoltage(); 
}


void ControlManager::setMotor(int id, float pwm, MotorDir dir) {
    if (!_sys) return;
    if (pwm > 0.0f) traj_space = 'M'; 
    if (dir == MotorDir::STOP) stopRobot();   
    
    // Evaluamos los límites físicos duros
    if (sensor_q && (dir == MotorDir::FORWARD || dir == MotorDir::REVERSE)) {
        if (sensor_q[id] >= _max_angles[id] && dir == MotorDir::FORWARD) { 
            pwm = 0.0f; 
            dir = MotorDir::STOP; 
        }
        else if (sensor_q[id] <= _min_angles[id] && dir == MotorDir::REVERSE) { 
            pwm = 0.0f; 
            dir = MotorDir::STOP; 
        }
    }
    _sys->applyMotor(id, pwm, dir);
}

void ControlManager::stopRobot() {
    is_tuning = false; 
    traj_space = 'S'; 
    enable_interpolation = false;
    
    for(int i = 0; i < 4; i++) {
        joints[i].q_dot_ref = 0.0f;
        // Ahora enviamos MotorDir::STOP en lugar de 'S'
        if (_sys) _sys->applyMotor(i, 0.0f, MotorDir::STOP); 
    }
}

void ControlManager::setProtectionMotor(float dt) {
    float margin = 1.5f * (M_PI / 180.0f); 
    bool limit_hit = false;
    
    for (int i = 0; i < 4; i++) {
        if ((sensor_q[i] >= (_max_angles[i] - margin) && joints[i].q_dot_ref > 0.0f) ||
            (sensor_q[i] <= (_min_angles[i] + margin) && joints[i].q_dot_ref < 0.0f)) {
            limit_hit = true; 
            break; 
        }
    }
    
    if (limit_hit) {
        stopRobot(); 
        Serial.println("\n[!] ALARMA: Pared virtual alcanzada. Trayectoria cancelada por seguridad.");
    }
}