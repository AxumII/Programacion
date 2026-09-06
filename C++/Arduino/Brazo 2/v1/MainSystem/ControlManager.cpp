#include "ControlManager.h"
#include <Arduino.h>     
#include <ArduinoEigenDense.h>
#include <cmath> // Necesario para fabs(), isnan(), isinf()
#include "Kinematic.h"

ControlManager::ControlManager(Kinematic* kinPtr) {
    _kinematic = kinPtr;
    sensor_q = nullptr;
    sensor_q_dot = nullptr;
    sensor_i_meas = nullptr;
    sensor_v_batt = nullptr;
}

bool ControlManager::joinSensors(float* q_ptr, float* q_dot_ptr, float* i_meas_ptr, float* v_batt_ptr) {
    if(!q_ptr || !q_dot_ptr || !i_meas_ptr || !v_batt_ptr) return false;
    sensor_q = q_ptr;
    sensor_q_dot = q_dot_ptr;
    sensor_i_meas = i_meas_ptr;
    sensor_v_batt = v_batt_ptr;
    return true;
}

bool ControlManager::setTargetCartesian(float x, float y, float z, float phi, bool use_phi) {
    final_target_XYZ << x, y, z;
    final_target_Phi = phi;
    use_phi_control = use_phi;
    return true;
}

bool ControlManager::setInterpolationActive(bool active) {
    enable_interpolation = active;
    return true;
}

// ==============================================================
// GESTOR PRINCIPAL EN CASCADA (Unificado)
// ==============================================================
bool ControlManager::CascadePlant() {
    if(!sensor_q || !sensor_q_dot || !sensor_i_meas || !sensor_v_batt || !_kinematic) {
        return false; 
    }

    unsigned long t_now = millis();
    bool status = true;

    // --- MODO AUTO-TUNING (Secuestra el control) ---
    if (is_tuning) {
        if (t_now - last_time_curr >= DT_CURR_MS) {
            // Pasamos el dt real para mayor precisión de la integral
            float dt_real = (t_now - last_time_curr) / 1000.0f;
            AutoTuneLoop(dt_real);
            last_time_curr = t_now;
        }
        return true; 
    }

    // --- MODO OPERACIÓN NORMAL ---
    // 1. Lazo de Posición Cartesiana e Interpolación (10 Hz)
    if (t_now - last_time_pos >= DT_POS_MS) {
        float dt_real = (t_now - last_time_pos) / 1000.0f;
        status &= PositionLoop(dt_real);
        last_time_pos = t_now;
    }

    // 2. Lazo de Velocidad (40 Hz)
    if (t_now - last_time_vel >= DT_VEL_MS) {
        float dt_real = (t_now - last_time_vel) / 1000.0f;
        status &= VelocityLoop(dt_real);
        last_time_vel = t_now;
    }

    // 3. Lazo de Corriente + Compensación Dinámica (200 Hz)
    if (t_now - last_time_curr >= DT_CURR_MS) {
        float dt_real = (t_now - last_time_curr) / 1000.0f;
        status &= CurrentLoop(dt_real);
        last_time_curr = t_now;
    }

    return status;
}

// ==============================================================
// LAZOS DE CONTROL
// ==============================================================
bool ControlManager::PositionLoop(float dt) {
    Eigen::Vector4f q_dot_target = Eigen::Vector4f::Zero();
    q_dot_target.setZero();

    if (enable_interpolation && traj_duration > 0.0f) {
        // Avanzar el reloj de la trayectoria
        traj_time += dt;
        float tau = traj_time / traj_duration;
        if (tau > 1.0f) tau = 1.0f; // Tope

        // Evaluar el polinomio elegido para obtener el porcentaje de avance (0.0 a 1.0)
        float s = evaluateProfile(traj_profile, tau);

        if (traj_space == 'C') {
            // INTERPOLACIÓN CARTESIANA
            current_interpolated_XYZ = start_XYZ + (final_target_XYZ - start_XYZ) * s;
            current_interpolated_Phi = start_Phi + (final_target_Phi - start_Phi) * s;

            Kinematic::Matrix4f T_current;
            _kinematic->angle2Pos(sensor_q[0], sensor_q[1], sensor_q[2], sensor_q[3], T_current);
            Eigen::Vector3f current_XYZ;
            current_XYZ << T_current(0,3), T_current(1,3), T_current(2,3);
            
            Eigen::Vector3f v_cartesian = Kp_pos_cartesian * (current_interpolated_XYZ - current_XYZ);

            // Jacobiano Inverso
            if (use_phi_control) {
                Eigen::MatrixXf J = _kinematic->Jacobian4x4(sensor_q[0], sensor_q[1], sensor_q[2], sensor_q[3]);
                Eigen::MatrixXf J_pinv = _kinematic->pseudoInverse(J);
                float current_Phi = sensor_q[1] + sensor_q[2] + sensor_q[3];
                float v_phi = Kp_pos_cartesian * (current_interpolated_Phi - current_Phi); 
                Eigen::VectorXf V4(4);
                V4 << v_cartesian(0), v_cartesian(1), v_cartesian(2), v_phi;
                q_dot_target = J_pinv * V4;
            } else {
                Eigen::MatrixXf J = _kinematic->Jacobian3x4(sensor_q[0], sensor_q[1], sensor_q[2], sensor_q[3]);
                Eigen::MatrixXf J_pinv = _kinematic->pseudoInverse(J);
                q_dot_target = J_pinv * v_cartesian;
            }
        } else {
            // INTERPOLACIÓN ANGULAR
            current_interpolated_Q = start_Q + (final_target_Q - start_Q) * s;
            for(int i=0; i<4; i++) {
                q_dot_target(i) = Kp_pos_cartesian * (current_interpolated_Q(i) - sensor_q[i]);
            }
        }
    } else {
        // SIN INTERPOLACIÓN
        for(int i=0; i<4; i++) {
            q_dot_target(i) = Kp_pos_cartesian * (final_target_Q(i) - sensor_q[i]);
        }
    }

    // Unroll explícito - Límite físico en GRADOS/S. 
    // CORRECCIÓN: Si 0.6 era en radianes, 60.0f grados es un buen límite seguro (aprox 10 RPM)
    float max_vel_deg = 60.0f; 
    joints[0].q_dot_ref = constrain(q_dot_target(0), -max_vel_deg, max_vel_deg);
    joints[1].q_dot_ref = constrain(q_dot_target(1), -max_vel_deg, max_vel_deg);
    joints[2].q_dot_ref = constrain(q_dot_target(2), -max_vel_deg, max_vel_deg);
    joints[3].q_dot_ref = constrain(q_dot_target(3), -max_vel_deg, max_vel_deg);

    return true;
}

inline bool ControlManager::processVelocityJoint(int id, float dt) {
    float error_vel = joints[id].q_dot_ref - sensor_q_dot[id];
    float int_vel_val = 0;
    
    // Límite de la integral virtual (Aprox 3 Amperios límite de corrección por velocidad)
    if(!simpson13(error_vel, joints[id].int_vel_state, dt, 3.0f, int_vel_val)) return false;
    
    joints[id].i_ref = (joints[id].Kp_vel * error_vel) + (joints[id].Ki_vel * int_vel_val);
    joints[id].i_ref = constrain(joints[id].i_ref, -5.0f, 5.0f); // 5 Amperios Max
    return true;
}

bool ControlManager::VelocityLoop(float dt) {
    bool ok = true;
    ok &= processVelocityJoint(0, dt);
    ok &= processVelocityJoint(1, dt);
    ok &= processVelocityJoint(2, dt);
    ok &= processVelocityJoint(3, dt);
    return ok;
}

inline bool ControlManager::processCurrentJoint(int id, float dt) {
    float current_meas = sensor_i_meas[id]; 
    float pwm_crudo = 0.0f;

    // 1. Solución del Lazo (Corriente Activa o Bypass de Voltaje)
    if (joints[id].enable_current_control) {
        float error_curr = joints[id].i_ref - current_meas;
        float int_curr_val = 0.0f;
        
        if(!simpson13(error_curr, joints[id].int_curr_state, dt, 150.0f, int_curr_val)) return false;
        pwm_crudo = (joints[id].Kp_curr * error_curr) + (joints[id].Ki_curr * int_curr_val);
    } else {
        pwm_crudo = joints[id].i_ref * 51.0f; 
    }

    // 2. Planta Dinámica: SIEMPRE calcular Gravedad (Evita caída en reposo)
    float pwm_grav = 0.0f;
    if (id > 0) {
        pwm_grav = joints[id].grav_comp * cos(sensor_q[id] * PI / 180.0f);
    }
    
    // 3. Zona Muerta (Fricción): Solo activa si hay intención de movimiento
    float pwm_fric = 0.0f;
    if (joints[id].q_dot_ref > 0.01f) {
        pwm_fric = joints[id].deadzone_up;
    } else if (joints[id].q_dot_ref < -0.01f) {
        pwm_fric = -joints[id].deadzone_down;
    }
    
    // 4. Normalización de Voltaje de Batería
    float v_b = *sensor_v_batt;
    if (v_b < 6.0f) v_b = 12.0f; 
    float batt_factor = 12.0f / v_b;

    // 5. Sumatoria final total (Sin el if restrictivo de velocidad anterior)
    float pwm_final_calc = (pwm_crudo + pwm_grav + pwm_fric) * batt_factor;

    // 6. Asignación Estricta al Formato de Salida
    if (pwm_final_calc > 1.0f) {
        joints[id].direction = 'R';
        joints[id].pwm_final = constrain((int)round(pwm_final_calc), 0, 255);
    } else if (pwm_final_calc < -1.0f) {
        joints[id].direction = 'L';
        joints[id].pwm_final = constrain((int)round(fabs(pwm_final_calc)), 0, 255); // CORRECCIÓN: Usar fabs()
    } else {
        joints[id].direction = 'S';
        joints[id].pwm_final = 0;
    }

    return true;
}

bool ControlManager::CurrentLoop(float dt) {
    bool ok = true;
    ok &= processCurrentJoint(0, dt);
    ok &= processCurrentJoint(1, dt);
    ok &= processCurrentJoint(2, dt);
    ok &= processCurrentJoint(3, dt);
    return ok;
}

bool ControlManager::getPWMCommand(int motor_id, int &pwm_val, char &dir) {
    if (motor_id < 0 || motor_id > 3) return false;
    pwm_val = joints[motor_id].pwm_final;
    dir = joints[motor_id].direction;
    return true;
}

// ==============================================================
// MATEMÁTICAS Y HERRAMIENTAS
// ==============================================================
bool ControlManager::simpson13(float current_err, IntegratorState &st, float dt, float limit, float &result) {
    float I_new = st.I_prev2 + (dt / 3.0f) * (current_err + 4.0f * st.e1 + st.e2);
    
    if (std::isnan(I_new) || std::isinf(I_new)) return false;
    I_new = constrain(I_new, -limit, limit);
    
    st.I_prev2 = st.I_prev;
    st.I_prev  = I_new;
    st.e2 = st.e1;
    st.e1 = current_err;
    
    result = I_new;
    return true;
}

float ControlManager::evaluateProfile(char profile, float tau) {
    tau = constrain(tau, 0.0f, 1.0f); 
    switch(profile) {
        case 'l': case '1': 
            return tau; 
        case 's': 
            return 0.5f * (1.0f - cos(PI * tau)); 
        case '2': case 'q': 
            if (profile == 'q') return tau; 
            return (tau < 0.5f) ? 2.0f * tau * tau : 1.0f - pow(-2.0f * tau + 2.0f, 2.0f) / 2.0f;
        case '3': case 'c': 
            return tau * tau * (3.0f - 2.0f * tau);
        case '4': case 't': 
            return (tau < 0.5f) ? 8.0f * tau * tau * tau * tau : 1.0f - pow(-2.0f * tau + 2.0f, 4.0f) / 2.0f;
        case '5': case 'i': 
            return tau * tau * tau * (tau * (tau * 6.0f - 15.0f) + 10.0f);
        default: 
            return tau;
    }
}

bool ControlManager::setTarget(float x, float y, float z, float phi, bool use_phi, char space, char profile, float duration_sec) {
    if(!sensor_q || !_kinematic) return false;

    use_phi_control = use_phi;
    traj_space = space;
    traj_profile = profile;
    traj_duration = duration_sec;
    traj_time = 0.0f;

    Kinematic::Matrix4f T_current;
    if (_kinematic->angle2Pos(sensor_q[0], sensor_q[1], sensor_q[2], sensor_q[3], T_current)) {
        start_XYZ << T_current(0,3), T_current(1,3), T_current(2,3);
    } else {
        start_XYZ = current_interpolated_XYZ; 
    }
    start_Phi = sensor_q[1] + sensor_q[2] + sensor_q[3]; 

    final_target_XYZ << x, y, z;
    final_target_Phi = phi;

    start_Q << sensor_q[0], sensor_q[1], sensor_q[2], sensor_q[3];
    current_interpolated_Q = start_Q;

    float th1=0, th2=0, th3=0, th4=0;
    bool ik_ok = false;
    
    if (use_phi) {
        ik_ok = _kinematic->pos2Angle(x, y, z, th1, th2, th3, th4, phi);
    } else {
        ik_ok = _kinematic->pos2Angle(x, y, z, th1, th2, th3, 0.0f);
        th4 = sensor_q[3]; 
    }

    if (ik_ok) {
        final_target_Q << th1, th2, th3, th4;
    } else {
        final_target_Q = start_Q; 
        if(space == 'A') return false; 
    }

    return true;
}

// ==============================================================
// RUTINA DE AUTO-SINTONIZACIÓN (Identificación de Planta)
// ==============================================================
bool ControlManager::startAutoTune(int joint) {
    if (joint < 0 || joint > 3) return false;
    
    is_tuning = true;
    tune_joint = joint;
    tune_state = 1; 
    tune_timer = 0.0f;
    tune_pwm = 0.0f;
    tune_max_vel = 0.0f;
    
    for(int i=0; i<4; i++) {
        joints[i].pwm_final = 0;
        joints[i].direction = 'S';
    }
    return true;
}

bool ControlManager::AutoTuneLoop(float dt) {
    if (tune_joint < 0 || tune_joint > 3) return false;
    
    int id = tune_joint;
    tune_timer += dt;
    
    switch(tune_state) {
        case 1: 
            tune_pwm += 15.0f * dt; 
            joints[id].pwm_final = (int)tune_pwm;
            joints[id].direction = 'R';
            
            if (sensor_q_dot[id] > 0.05f) { 
                joints[id].deadzone_up = tune_pwm;
                tune_state = 2; tune_timer = 0; tune_pwm = 0;
                joints[id].direction = 'S'; joints[id].pwm_final = 0; 
            }
            if (tune_pwm > 180.0f) tune_state = 0; 
            break;
            
        case 2: 
            if (tune_timer > 1.0f) { 
                tune_state = 3; tune_timer = 0; 
            }
            break;
            
        case 3: 
            tune_pwm += 15.0f * dt; 
            joints[id].pwm_final = (int)tune_pwm;
            joints[id].direction = 'L'; 
            
            if (sensor_q_dot[id] < -0.05f) { 
                joints[id].deadzone_down = tune_pwm;
                tune_state = 4; tune_timer = 0; tune_pwm = 0;
                joints[id].direction = 'S'; joints[id].pwm_final = 0;
            }
            if (tune_pwm > 180.0f) tune_state = 0; 
            break;
            
        case 4: 
            if (tune_timer > 1.0f) { 
                tune_state = 5; tune_timer = 0; tune_max_vel = 0.0f; 
            }
            break;
            
        case 5: 
            joints[id].pwm_final = constrain((int)(joints[id].deadzone_up + 40.0f), 0, 255);
            joints[id].direction = 'R';
            
            // CORRECCIÓN: fabs() para capturar velocidades correctamente
            if (fabs(sensor_q_dot[id]) > tune_max_vel) {
                tune_max_vel = fabs(sensor_q_dot[id]);
            }
            
            if (tune_timer > 0.6f) { 
                if (tune_max_vel > 0.01f) {
                    joints[id].Kp_vel = (40.0f / tune_max_vel) * 0.6f;
                    joints[id].Ki_vel = joints[id].Kp_vel * 0.25f; 
                }
                
                tune_state = 0; 
                is_tuning = false;
                joints[id].direction = 'S'; 
                joints[id].pwm_final = 0;
            }
            break;
    }
    return true;
}

// ==============================================================
// GESTIÓN DE HARDWARE Y SENSORES
// ==============================================================
void ControlManager::bindHardware(ESP32Encoder* enc, Adafruit_ADS1115* ads, long* offsets, int battPin) {
    _encoders = enc;
    _ads = ads;
    _offsets_enc = offsets;
    _batt_pin = battPin;
}

void ControlManager::setSensorParams(const float* ppr, const float* off_is, float f_31zy, float f_jgy, float f_batt) {
    _PPR = ppr;
    _OFFSETS_IS = off_is;
    _FACTOR_M31ZY = f_31zy;
    _FACTOR_MJGY = f_jgy;
    _F_BATT = f_batt;
}
void ControlManager::readAndProcessSensors(float dt) {
    if(!sensor_q || !_encoders || !_ads) return;

    if (sensor_v_batt) {
        *sensor_v_batt = (analogRead(_batt_pin) / 4095.0f) * 3.3f * _F_BATT;
    }

    for (int i = 0; i < 4; i++) {
        float prev_q = sensor_q[i];
        
        sensor_q[i] = ((_encoders[i].getCount() - _offsets_enc[i]) / _PPR[i]) * 360.0f; 
        sensor_q_dot[i] = (sensor_q[i] - prev_q) / dt;
        
        // Verificación extra para _ads por si no está conectado físicamente
        if (_OFFSETS_IS[i] > 0.0f && _ads != nullptr) {
            float vMedido = _ads->computeVolts(_ads->readADC_SingleEnded(i));
            float vSinRuido = vMedido - _OFFSETS_IS[i];
            float factor = (i == 0) ? _FACTOR_M31ZY : _FACTOR_MJGY;
            
            sensor_i_meas[i] = (fabs(vSinRuido) > 0.03f) ? (vSinRuido * factor) : 0.0f;
        } else {
            sensor_i_meas[i] = 0.0f;
        }
    }
}