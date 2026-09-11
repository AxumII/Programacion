#ifndef CONTROLMANAGER_H
#define CONTROLMANAGER_H

#include <Arduino.h>     
#include <ArduinoEigenDense.h>
// CORRECCIÓN: Librerías agregadas para reconocer los punteros físicos
#include <ESP32Encoder.h>
#include <Adafruit_ADS1X15.h>
#include "Kinematic.h"

#define DT_CURR_MS 5    // 200 Hz
#define DT_VEL_MS  25   // 40 Hz
#define DT_POS_MS  100  // 10 Hz

struct IntegratorState {
    float e1 = 0.0f;      
    float e2 = 0.0f;      
    float I_prev = 0.0f;  
    float I_prev2 = 0.0f; 
};

struct JointData {
    float q_dot_ref = 0.0f; 
    float i_ref = 0.0f;     
    
    IntegratorState int_vel_state;
    IntegratorState int_curr_state;
    
    float Kp_vel = 1.5f, Ki_vel = 0.4f;
    float Kp_curr = 20.0f, Ki_curr = 5.0f;
    
    float deadzone_up = 0.0f;   
    float deadzone_down = 0.0f; 
    float grav_comp = 0.0f; 
    
    int pwm_final = 0;       
    char direction = 'S';
    
    // CORRECCIÓN: Atributo trasladado desde la clase principal hacia la estructura local
    bool enable_current_control = true; 
};

class ControlManager {
public:
    EIGEN_MAKE_ALIGNED_OPERATOR_NEW
    ControlManager(Kinematic* kinPtr);

    bool joinSensors(float* q_ptr, float* q_dot_ptr, float* i_meas_ptr, float* v_batt_ptr);
    bool tuneDeadzone(int joint, float up, float down);
    bool tuneGravity(int joint, float grav);
    bool setTargetCartesian(float x, float y, float z, float phi, bool use_phi);
    bool setInterpolationActive(bool active);
    bool setTarget(float x, float y, float z, float phi, bool use_phi, char space = 'A', char profile = '5', float duration_sec = 2.0f);
    bool CascadePlant();
    bool getPWMCommand(int motor_id, int &pwm_val, char &dir);
    

    void setEnableCurrentControl(bool state) { 
        for(int i = 0; i < 4; i++) joints[i].enable_current_control = state; 
    }

    // Vincula el control con el hardware y sus parámetros
    void bindHardware(ESP32Encoder* enc, Adafruit_ADS1115* ads, long* offsets, int battPin);
    void setSensorParams(const float* ppr, const float* off_is, float f_31zy, float f_jgy, float f_batt);
    
    // Método que realiza el "uso" de los sensores
    void readAndProcessSensors(float dt);

    bool startAutoTune(int joint);
    bool isTuningActive() { return is_tuning; }

    JointData joints[4];
    float Kp_pos_cartesian = 2.0f;
    bool enable_interpolation = true; 

private:
    Kinematic* _kinematic;
    
    float* sensor_q;
    float* sensor_q_dot;
    float* sensor_i_meas;
    float* sensor_v_batt;
    
    unsigned long last_time_pos = 0;
    unsigned long last_time_vel = 0;
    unsigned long last_time_curr = 0;
    
    // Generador de Trayectorias
    char traj_space = 'A';
    char traj_profile = '5';
    float traj_duration = 0.0f;
    float traj_time = 0.0f;

    Eigen::Vector3f start_XYZ;
    Eigen::Vector3f final_target_XYZ;
    float start_Phi = 0.0f;
    float final_target_Phi = 0.0f;

    Eigen::Vector4f start_Q;
    Eigen::Vector4f final_target_Q;

    Eigen::Vector3f current_interpolated_XYZ; 
    float current_interpolated_Phi = 0.0f;
    Eigen::Vector4f current_interpolated_Q;

    bool use_phi_control = false;

    // Variables de Estado de Auto-Sintonización
    bool is_tuning = false;
    int tune_joint = -1;
    int tune_state = 0;
    float tune_timer = 0.0f;
    float tune_pwm = 0.0f;
    float tune_max_vel = 0.0f;

    // Punteros al hardware físico inyectado
    ESP32Encoder* _encoders;
    Adafruit_ADS1115* _ads;
    long* _offsets_enc;
    int _batt_pin;

    // Parámetros de conversión
    const float* _PPR;
    const float* _OFFSETS_IS;
    float _FACTOR_M31ZY;
    float _FACTOR_MJGY;
    float _F_BATT;

    float evaluateProfile(char profile, float tau);
    bool simpson13(float current_err, IntegratorState &st, float dt, float limit, float &result);
    
    bool PositionLoop(float dt);
    bool VelocityLoop(float dt);
    bool CurrentLoop(float dt);
    bool AutoTuneLoop(float dt); 
    
    inline bool processVelocityJoint(int id, float dt);
    inline bool processCurrentJoint(int id, float dt);
};

#endif