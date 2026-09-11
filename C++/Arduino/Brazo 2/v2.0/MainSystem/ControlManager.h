#ifndef CONTROLMANAGER_H
#define CONTROLMANAGER_H

#include "Kinematic.h"
#include "SystemConfig.h"
#include <ArduinoEigenDense.h> 

class ControlManager {
public:
    // Obligatorio para evitar colapsos de hardware por alineación de memoria en ESP32 con Eigen
    EIGEN_MAKE_ALIGNED_OPERATOR_NEW

private:
    Kinematic* _kinematic;
    SystemConfig* _sys; 

    float* sensor_q;
    float* sensor_q_dot;
    float* sensor_i_meas;
    float* sensor_v_batt;

    // --- Variables del Filtro de Kalman ---
    Eigen::Vector2f _x_est[4]; 
    Eigen::Matrix2f _P_cov[4]; 
    Eigen::Matrix2f _Q;        
    float _R;                  
    Eigen::Matrix<float, 1, 2> _H; 

public:
    ControlManager(Kinematic* kinPtr, SystemConfig* sysPtr);
    
    bool joinSensors(float* q_ptr, float* q_dot_ptr, float* i_meas_ptr, float* v_batt_ptr);
    void updateSensors(float dt);
    void updateVelocityKalman(int id, float z_measured, float dt);
    void setMotor(int id, int pwm, char dir);
};

#endif