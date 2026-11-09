#ifndef CONTROLMANAGER_H
#define CONTROLMANAGER_H

#include "Kinematic.h"
#include "SystemConfig.h"
#include <ArduinoEigenDense.h> 

struct IntegratorState {
    float I_prev = 0.0f;
    float e1 = 0.0f;
};

struct JointState {
    float q_dot_ref = 0.0f;
    float Kp_ang = 5.0f;
    float Kp_vel = 1.0f;
    float Ki_vel = 0.5f;
    float fric_up_pwm = 0.0f;
    float fric_down_pwm = 0.0f;
    IntegratorState int_vel_state;
};

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
    float* sensor_v_fuente;

    // --- Variables del Filtro de Kalman ---
    Eigen::Vector2f _x_est[4]; 
    Eigen::Matrix2f _P_cov[4]; 
    Eigen::Matrix2f _Q;        
    float _R;                  
    Eigen::Matrix<float, 1, 2> _H; 

    // --- Constantes y Tiempos del Sistema ---
    unsigned long _dt_pos_us;
    unsigned long _dt_vel_us;
    unsigned long _dt_tune_us;
    
    float _max_vel_rad;
    float _max_pwm;
    float _max_int_pwm;
    float _k_grav_hombro;
    float _k_grav_codo;
    float _k_grav_mun;
    float _min_angles[4];
    float _max_angles[4];

    // --- Variables de Estado y Control ---
    char traj_space = 'S'; 
    bool enable_interpolation = false;
    JointState joints[4];
    int control_mode = 0;
    
    bool is_tuning = false;
    unsigned long last_time_tune = 0;
    unsigned long last_time_pos = 0;
    unsigned long last_time_vel = 0;

    // --- Trayectorias ---
    float traj_duration = 0.0f;
    float traj_time = 0.0f;
    char traj_profile = 'i';
    
    Eigen::Vector3f start_XYZ;
    Eigen::Vector3f final_target_XYZ;
    float start_Phi = 0.0f;
    float final_target_Phi = 0.0f;
    float Kp_pos_cartesian = 2.0f;
    float Kp_pos_phi = 1.0f;       
    float Kp_pos_theta4 = 1.0f;    

    // --- Geometría Circular ---
    Eigen::Vector3f circ_center;
    Eigen::Vector3f circ_vx;
    Eigen::Vector3f circ_vy;
    float circ_radius = 0.0f;
    float circ_total_angle = 0.0f;

    bool setupCircleMath(Eigen::Vector3f P1, Eigen::Vector3f P2, Eigen::Vector3f P3);
    
    float start_Q[4] = {0};
    float final_target_Q[4] = {0};

    // --- Métodos Privados ---
    bool angleLimits();
    void applyVirtualWalls(float dt);
    bool integrateTrapezoidal(float current_err, IntegratorState &st, float dt, float limit, float &result);
    float evaluateProfile(char profile, float tau);
    float computeGravityPWM(int id, float* q);
    void AutoTuneLoop(float dt);
    
    bool PositionLoop(float dt);
    bool AngleLoop(float dt);
    bool VelocityLoop(float dt);

    bool traj_maintain_phi = true; 
    float start_Theta4 = 0.0f;
    float final_target_Theta4 = 0.0f;

    bool modoTestStep = false;

public:
    ControlManager(Kinematic* kinPtr, SystemConfig* sysPtr);
    
    bool joinSensors(float* q_ptr, float* q_dot_ptr, float* i_meas_ptr, float* v_fuente_ptr);
    void updateSensors(float dt);
    void updateVelocityKalman(int id, float z_measured, float dt);
    void setMotor(int id, float pwm, char dir);

    void startAutoTune() { is_tuning = true; last_time_tune = micros(); }
    void setGains(int id, float kp, float ki, float fup, float fdown);
    void loadAllGains();
    void printGains();

    void movMPWM(int id, float pwm, char dir);
    void movMPWMT(int id, float pwm, char dir, int ms);

    void stopRobot();
    bool CascadeControl();
    
    float evaluateVelocityProfile(char profile, float tau, float duration);
    bool movA(float q1, float q2, float q3, float q4, float speed_deg_s);
    
    // --- Comandos MoveLJc (Línea Jacobiano DLS) ---
    bool movLJc(float x, float y, float z, float speed_mm_s);    
    bool movLJc(float x, float y, float z, float speed_mm_s, float phi_val);

    // --- Comandos MoveJ (Articular Pura) ---
    bool movJ(float x, float y, float z, float speed_mm_s, bool elbowUp = true);    
    bool movJ(float x, float y, float z, float speed_mm_s, float phi_val, bool elbowUp = true);

    // --- Comandos MovL (Línea Recta por IK Continua) ---
    bool movL(float x, float y, float z, float speed_mm_s, bool elbowUp = true);    
    bool movL(float x, float y, float z, float speed_mm_s, float phi_val, bool elbowUp = true);

    // --- Comandos MovCJc (Círculo resuelto por Jacobiano DLS) ---
    bool movCJc(float x_via, float y_via, float z_via, float x_end, float y_end, float z_end, float speed_mm_s);
    bool movCJc(float x_via, float y_via, float z_via, float x_end, float y_end, float z_end, float speed_mm_s, float phi_val);

    // --- Comandos MovC (Círculo resuelto por IK Continua) ---
    bool movC(float x_via, float y_via, float z_via, float x_end, float y_end, float z_end, float speed_mm_s, bool elbowUp = true);
    bool movC(float x_via, float y_via, float z_via, float x_end, float y_end, float z_end, float speed_mm_s, float phi_val, bool elbowUp = true);

    // --- Comandos MovZ (Movimiento vertical exclusivo) ---
    bool movZ(float z, float speed_mm_s, float phi_val);
    bool movZJc(float z, float speed_mm_s, float phi_val);

    // --- Comandos Home ---
    bool homZ(float speed_deg_s = 30.0f);
    bool hom(float speed_deg_s = 30.0f);
};

#endif