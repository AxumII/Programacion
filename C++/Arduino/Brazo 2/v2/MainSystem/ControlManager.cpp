#include "ControlManager.h"
#include <Arduino.h>     
#include <cmath>

ControlManager::ControlManager(Kinematic* kinPtr, SystemConfig* sysPtr) {
    _kinematic = kinPtr;
    _sys = sysPtr; 
    sensor_q = nullptr;
    sensor_q_dot = nullptr;
    sensor_i_meas = nullptr;
    sensor_v_fuente = nullptr;
    
    // --- CONSTANTES DEL SISTEMA ---
    _dt_pos_us = 10000; // 100 Hz
    _dt_vel_us = 2500;  // 400 Hz
    _dt_tune_us = 5000; // 200 Hz 
    
    _max_vel_rad = 30.0f * (M_PI / 180.0f); 
    _max_pwm = 100.0f;       // [MODIFICADO] Ahora el PID satura al 100%
    _max_int_pwm = 80.0f;    // [MODIFICADO] 20% (Equivale al viejo 50 de 255)
    _k_grav_hombro = 15.6f;  // [MODIFICADO] Escalado al 100%
    _k_grav_codo = 9.8f;     // [MODIFICADO] Escalado al 100%
    _k_grav_mun = 9.8f;     // [MODIFICADO] Escalado al 100%

    // =========================================================
    // VALORES BASELINE (Se usarán si la NVS está vacía)
    // =========================================================
// Articulación 1 (M1)
    joints[0].Kp_vel = 20.67f; 
    joints[0].Ki_vel = 6.17f; 
    joints[0].fric_up_pwm = 23.6f; 
    joints[0].fric_down_pwm = 15.8f; 
    joints[0].Kp_ang = 1.2f; // M1: Mayor inercia

    // Articulación 2 (M2)
    joints[1].Kp_vel = 16.14f; 
    joints[1].Ki_vel = 4.82f; 
    joints[1].fric_up_pwm = 21.8f; 
    joints[1].fric_down_pwm = 22.4f; 
    joints[1].Kp_ang = 2.5f; // M2: Mayor inercia

    // Articulación 3 (M3)
    joints[2].Kp_vel = 19.23f; 
    joints[2].Ki_vel = 5.74f; 
    joints[2].fric_up_pwm = 14.6f; 
    joints[2].fric_down_pwm = 16.3f; 
    joints[2].Kp_ang = 1.2f;

    // Articulación 4 (M4)
    joints[3].Kp_vel = 18.85f; 
    joints[3].Ki_vel = 5.63f; 
    joints[3].fric_up_pwm = 15.8f; 
    joints[3].fric_down_pwm = 14.3f;
    joints[3].Kp_ang = 1.2f;
    // =========================================================


    _min_angles[0] = -175.0f * (M_PI / 180.0f); _max_angles[0] = 175.0f * (M_PI / 180.0f); // Base
    _min_angles[1] = -3.0f * (M_PI / 180.0f);   _max_angles[1] = 135.0f * (M_PI / 180.0f); // Hombro
    _min_angles[2] = -160.0f * (M_PI / 180.0f); _max_angles[2] = 160.0f * (M_PI / 180.0f); 
    _min_angles[3] = -100.0f * (M_PI / 180.0f); _max_angles[3] = 100.0f * (M_PI / 180.0f);

    _H << 1.0f, 0.0f; 
    _R = 0.01f; 
    _Q << 0.001f, 0.0f, 0.0f, 0.01f;

    for(int i = 0; i < 4; i++) {
        _x_est[i] << 0.0f, 0.0f; 
        _P_cov[i] << 1.0f, 0.0f, 0.0f, 1.0f;
    }
}

// =================================================================
// Acople Sensores y Filtros
// =================================================================
bool ControlManager::joinSensors(float* q_ptr, float* q_dot_ptr, float* i_meas_ptr, float* v_fuente_ptr) {
    if(!q_ptr || !q_dot_ptr || !i_meas_ptr || !v_fuente_ptr) return false;
    sensor_q = q_ptr;
    sensor_q_dot = q_dot_ptr;
    sensor_i_meas = i_meas_ptr;
    sensor_v_fuente = v_fuente_ptr;
    return true;
}

void ControlManager::updateVelocityKalman(int id, float z_measured, float dt) {
    Eigen::Matrix2f A;
    A << 1.0f, dt,
         0.0f, 1.0f;

    Eigen::Vector2f x_pred = A * _x_est[id];
    Eigen::Matrix2f P_pred = A * _P_cov[id] * A.transpose() + _Q; 

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
        float q_raw = _sys->getAngle(i); 
        updateVelocityKalman(i, q_raw, dt);
        sensor_q[i] = _x_est[i](0);       
        sensor_q_dot[i] = _x_est[i](1);   
    }

    static int adc_channel = 0;
    if (sensor_i_meas) {
        sensor_i_meas[adc_channel] = _sys->getCurrent(adc_channel);
        adc_channel = (adc_channel + 1) % 4;
    }
    if (sensor_v_fuente) {
        *sensor_v_fuente = _sys->getSourceVoltage(); 
    }
}

// =================================================================
// Movimiento Motor y Seguridad
// =================================================================
void ControlManager::setMotor(int id, float pwm, char dir) {
    if (!_sys) return;
    if (pwm > 0.0f) traj_space = 'M'; 
    if (dir == 'S') stopRobot();   
    
    // [NUEVO] PROTECCIÓN ABSOLUTA EN COMANDOS MANUALES O DE EMERGENCIA
    if (sensor_q && (dir == 'H' || dir == 'A')) {
        if (sensor_q[id] >= _max_angles[id] && dir == 'H') {
            pwm = 0.0f; dir = 'S';
            Serial.printf("\n[!] BLOQUEO M%d: Limite superior alcanzado. Solo se permite reversa (A).\n", id + 1);
        }
        else if (sensor_q[id] <= _min_angles[id] && dir == 'A') {
            pwm = 0.0f; dir = 'S';
            Serial.printf("\n[!] BLOQUEO M%d: Limite inferior alcanzado. Solo se permite reversa (H).\n", id + 1);
        }
    }

    _sys->applyMotor(id, pwm, dir);
}

bool ControlManager::angleLimits() {
    if (!sensor_q) return false;
    for (int i = 0; i < 4; i++) {
        if (sensor_q[i] < _min_angles[i] || sensor_q[i] > _max_angles[i]) {
            return false; 
        }
    }
    return true;
}

void ControlManager::stopRobot() {
    is_tuning = false;       
    traj_space = 'S';
    enable_interpolation = false;
    for(int i = 0; i < 4; i++) {
        joints[i].q_dot_ref = 0.0f;
        // Apagado forzoso directo al hardware
        if (_sys) _sys->applyMotor(i, 0.0f, 'S'); 
    }
}

void ControlManager::applyVirtualWalls(float dt) {
    // Margen de seguridad estricto de 1.5 grados antes del límite real
    float margin = 1.5f * (M_PI / 180.0f); 

    for (int i = 0; i < 4; i++) {
        // Si se acerca al límite superior e intenta avanzar más (velocidad positiva)
        if (sensor_q[i] >= (_max_angles[i] - margin) && joints[i].q_dot_ref > 0.0f) {
            joints[i].q_dot_ref = 0.0f;
            joints[i].int_vel_state.I_prev = 0.0f; 
            enable_interpolation = false; // [CRUCIAL] Mata la trayectoria para que deje de exigir el objetivo prohibido
        } 
        // Si se acerca al límite inferior e intenta retroceder más (velocidad negativa)
        else if (sensor_q[i] <= (_min_angles[i] + margin) && joints[i].q_dot_ref < 0.0f) {
            joints[i].q_dot_ref = 0.0f;
            joints[i].int_vel_state.I_prev = 0.0f; 
            enable_interpolation = false; // [CRUCIAL] Mata la trayectoria activa
        }
    }
}

// =================================================================
// Controlador Maestro en Cascada
// =================================================================
bool ControlManager::CascadeControl() {
    if(!sensor_q || !sensor_q_dot || !_kinematic) return false;

    unsigned long t_now = micros(); 
    bool status = true;

    if (is_tuning) {
        if (t_now - last_time_tune >= _dt_tune_us) {
            float dt_real = (t_now - last_time_tune) / 1000000.0f;
            AutoTuneLoop(dt_real);
            last_time_tune = t_now;
        }
        return true; 
    }

    if (traj_space == 'M') {
        return true; 
    }

    // 1. Lazo Externo: Generador de Velocidades
    if (t_now - last_time_pos >= _dt_pos_us) {
        float dt_real = (t_now - last_time_pos) / 1000000.0f;
        
        if (traj_space == 'C') {
            status &= PositionLoop(dt_real); 
        } 
        else if (traj_space == 'Q') {
            status &= AngleLoop(dt_real);    
        } 
        else {
            for(int i = 0; i < 4; i++) { joints[i].q_dot_ref = 0.0f; }
        }
        
        // Las paredes virtuales ahora gestionan la frontera sin colapsar el programa
        applyVirtualWalls(dt_real);
        last_time_pos = t_now;
    }

    // 2. Lazo Interno: Ejecutor de Velocidad a PWM
    // Al no haber "return false" previo, este lazo aplicará el bloqueo físico siempre
    if (t_now - last_time_vel >= _dt_vel_us) {
        float dt_real = (t_now - last_time_vel) / 1000000.0f;
        status &= VelocityLoop(dt_real);
        last_time_vel = t_now;
    }

    return status;
}

// Lazo: Posición Cartesiana -> Velocidades (rad/s)
bool ControlManager::PositionLoop(float dt) {
    Eigen::Vector4f q_dot_target = Eigen::Vector4f::Zero();

    if (enable_interpolation && traj_duration > 0.0f) {
        traj_time += dt; 
        if (traj_time >= traj_duration) {
            traj_time = traj_duration;
            enable_interpolation = false; 
        }
        
        float tau = traj_time / traj_duration;
        float s = evaluateProfile(traj_profile, tau); 
        float ds_dt = evaluateVelocityProfile(traj_profile, tau, traj_duration); // Feedforward

        Eigen::Vector3f current_interpolated_XYZ = start_XYZ + (final_target_XYZ - start_XYZ) * s;
        Eigen::Vector3f v_ff_XYZ = (final_target_XYZ - start_XYZ) * ds_dt; // Vector Velocidad Pura
        
        // ¡BUG SOLUCIONADO! Convertimos Radianes a Grados para la Cinemática
        float q0_deg = sensor_q[0] * 180.0f / M_PI;
        float q1_deg = sensor_q[1] * 180.0f / M_PI;
        float q2_deg = sensor_q[2] * 180.0f / M_PI;
        float q3_deg = sensor_q[3] * 180.0f / M_PI;

        Kinematic::Matrix4f T_current;
        _kinematic->angle2Pos(q0_deg, q1_deg, q2_deg, q3_deg, T_current); 
        Eigen::Vector3f current_XYZ;
        current_XYZ << T_current(0,3), T_current(1,3), T_current(2,3);

        // Control Vectorial: Velocidad Prealimentada + Corrección P
        Eigen::Vector3f v_cartesian = v_ff_XYZ + Kp_pos_cartesian * (current_interpolated_XYZ - current_XYZ);

        if (control_mode == 1) {
            float current_interpolated_Phi = start_Phi + (final_target_Phi - start_Phi) * s;
            float v_ff_phi = (final_target_Phi - start_Phi) * ds_dt;
            float current_Phi = sensor_q[1] + sensor_q[2] + sensor_q[3];
            float v_phi = v_ff_phi + (Kp_pos_phi * (current_interpolated_Phi - current_Phi));
            
            // ¡BUG SOLUCIONADO! Pasamos Grados al Jacobiano
            Eigen::MatrixXf J4x4 = _kinematic->Jacobian4x4(q0_deg, q1_deg, q2_deg, q3_deg);
            Eigen::MatrixXf J4x4_pinv = _kinematic->pseudoInverse(J4x4);
            
            Eigen::Vector4f V_cart_4D;
            V_cart_4D << v_cartesian(0), v_cartesian(1), v_cartesian(2), v_phi;
            q_dot_target = J4x4_pinv * V_cart_4D;
        } 
        else if (control_mode == 2) {
            // ... Mismo procedimiento, pasando grados a Jacobian3x4 y sumando feedforward a v_theta4
            float current_interpolated_Theta4 = start_Theta4 + (final_target_Theta4 - start_Theta4) * s;
            float v_ff_theta4 = (final_target_Theta4 - start_Theta4) * ds_dt;
            float v_theta4 = v_ff_theta4 + Kp_pos_theta4 * (current_interpolated_Theta4 - sensor_q[3]);
            
            q_dot_target(3) = v_theta4;
            Eigen::MatrixXf J3x4 = _kinematic->Jacobian3x4(q0_deg, q1_deg, q2_deg, q3_deg);
            Eigen::MatrixXf J3x3 = J3x4.block<3,3>(0,0); 
            Eigen::MatrixXf J3x3_pinv = _kinematic->pseudoInverse(J3x3);

            Eigen::Vector3f J_col4 = J3x4.col(3);
            Eigen::Vector3f v_compensated = v_cartesian - (J_col4 * q_dot_target(3));
            
            Eigen::Vector3f q_dot_123 = J3x3_pinv * v_compensated;
            q_dot_target(0) = q_dot_123(0); q_dot_target(1) = q_dot_123(1); q_dot_target(2) = q_dot_123(2);
        }
        else {
            // ==========================================
            // CASO 3: Theta4 Óptimo Automático por Jacobiano (3x4)
            // ==========================================
            // Al usar únicamente la pseudoinversa del Jacobiano 3x4 directamente 
            // sobre la velocidad cartesiana XYZ, el sistema resuelve la cinemática 
            // diferencial minimizando la norma de las velocidades articulares, 
            // encontrando de forma natural el movimiento óptimo para el motor 4.
            Eigen::MatrixXf J3x4 = _kinematic->Jacobian3x4(sensor_q[0], sensor_q[1], sensor_q[2], sensor_q[3]);
            Eigen::MatrixXf J3x4_pinv = _kinematic->pseudoInverse(J3x4);
            
            q_dot_target = J3x4_pinv * v_cartesian;
        }
    } 

    for(int i = 0; i < 4; i++) {
        joints[i].q_dot_ref = constrain(q_dot_target(i), -_max_vel_rad, _max_vel_rad);
    }
    return true;
}

// Lazo: Ángulos Articulares -> Velocidades (rad/s)
bool ControlManager::AngleLoop(float dt) {
    float s = 1.0f; 
    float ds_dt = 0.0f; 
    
    if (enable_interpolation && traj_duration > 0.0f) {
        traj_time += dt;
        if (traj_time >= traj_duration) {
            traj_time = traj_duration;
            enable_interpolation = false;
        }
        float tau = traj_time / traj_duration;
        s = evaluateProfile(traj_profile, tau);
        ds_dt = evaluateVelocityProfile(traj_profile, tau, traj_duration);
    }

    for(int i = 0; i < 4; i++) {
        float current_interpolated_Q = start_Q[i] + (final_target_Q[i] - start_Q[i]) * s;
        float error_pos = current_interpolated_Q - sensor_q[i];
        
        // Tolerancia basada en tu resolución mecánica extrema (0.05 grados)
        float tolerancia_rad = 0.05f * M_PI / 180.0f; 
        
        // Si el perfil terminó y el error es minúsculo, apagamos la velocidad de referencia
        if (!enable_interpolation && std::abs(error_pos) < tolerancia_rad) {
            joints[i].q_dot_ref = 0.0f;
            joints[i].int_vel_state.I_prev = 0.0f; // Previene "hunting"
        } else {
            float v_ff = (final_target_Q[i] - start_Q[i]) * ds_dt; 
            float q_dot_target = v_ff + (joints[i].Kp_ang * error_pos);
            joints[i].q_dot_ref = constrain(q_dot_target, -_max_vel_rad, _max_vel_rad);
        }
    }
    return true;
}
// Lazo: Velocidad -> PWM
bool ControlManager::VelocityLoop(float dt) {
    bool status = true;

    for(int i = 0; i < 4; i++) {
        float error_vel = joints[i].q_dot_ref - sensor_q_dot[i];
        float int_vel_val = 0;
        
        if(!integrateTrapezoidal(error_vel, joints[i].int_vel_state, dt, _max_int_pwm, int_vel_val)) {
            status = false; 
        }

        float pwm_crudo = (joints[i].Kp_vel * error_vel) + (joints[i].Ki_vel * int_vel_val);
        float pwm_grav = 0.0f;
        float pwm_fric = 0.0f;
        
        // ============================================================
        // SUAVIZADOR DE FRICCIÓN (Elimina vibración al arrancar)
        // ============================================================
        if (std::abs(joints[i].q_dot_ref) > 0.0f) {
            pwm_grav = computeGravityPWM(i, sensor_q); 
            
            float Fs = (joints[i].q_dot_ref > 0) ? joints[i].fric_up_pwm : joints[i].fric_down_pwm;
            float Fc = Fs * 0.75f; 
            float ws = 0.15f; 
            float f_stribeck = Fc + (Fs - Fc) * exp(-pow(std::abs(joints[i].q_dot_ref) / ws, 2));
            
            // Rampamos la fricción de 0% a 100% en los primeros 0.05 rad/s
            float suavizador = std::min(1.0f, std::abs(joints[i].q_dot_ref) / 0.05f);
            float fric_pura = (joints[i].q_dot_ref > 0) ? f_stribeck : -f_stribeck;
            
            pwm_fric = fric_pura * suavizador;
        }

        float pwm_final = pwm_crudo + pwm_grav + pwm_fric;
        
        // ============================================================
        // CORTE DEFINITIVO (Elimina vibración de 20s en estático)
        // ============================================================
        if (joints[i].q_dot_ref == 0.0f) {
            pwm_final = 0.0f; 
            joints[i].int_vel_state.I_prev = 0.0f; // Asesina la memoria del ruido
        }

        float pwm_out = constrain(std::abs(pwm_final), 0.0f, _max_pwm);
        char dir = (pwm_final >= 0) ? 'H' : 'A'; 
        
        // LÍMITES FÍSICOS ABSOLUTOS
        if (sensor_q[i] >= _max_angles[i] && pwm_final > 0.0f) { 
            pwm_out = 0.0f; dir = 'S'; 
            joints[i].int_vel_state.I_prev = 0.0f; 
        }
        if (sensor_q[i] <= _min_angles[i] && pwm_final < 0.0f) { 
            pwm_out = 0.0f; dir = 'S'; 
            joints[i].int_vel_state.I_prev = 0.0f; 
        }

        if (_sys) _sys->applyMotor(i, pwm_out, dir);
    }
    return status;
}


// =================================================================
// Auxiliares Matemáticos
// =================================================================
bool ControlManager::integrateTrapezoidal(float current_err, IntegratorState &st, float dt, float limit, float &result) {
    float I_new = st.I_prev + (dt / 2.0f) * (current_err + st.e1);
    
    if (std::isnan(I_new) || std::isinf(I_new)) return false;
    I_new = constrain(I_new, -limit, limit);
    
    st.I_prev = I_new;
    st.e1 = current_err;
    
    result = I_new;
    return true;
}

float ControlManager::evaluateProfile(char profile, float tau) {
    tau = constrain(tau, 0.0f, 1.0f); 
    switch(profile) {
        case 's': 
            return 0.5f * (1.0f - cos(M_PI * tau)); 
        case 'c': 
            return tau * tau * (3.0f - 2.0f * tau);
        case 'i': 
            return tau * tau * tau * (tau * (tau * 6.0f - 15.0f) + 10.0f);
        default: 
            return tau; // 'l' lineal
    }
}

float ControlManager::computeGravityPWM(int id, float* q) {
    // q[1], q[2] y q[3] ya están expresados directamente en radianes
    if (id == 1) return _k_grav_hombro * cos(q[1]);
    if (id == 2) return _k_grav_codo * cos(q[1] + q[2]);
    if (id == 3) return _k_grav_mun * cos(q[1] + q[2] + q[3]); 
    
    return 0.0f; 
}

float ControlManager::evaluateVelocityProfile(char profile, float tau, float duration) {
    if (duration <= 0.0001f) return 0.0f;
    tau = constrain(tau, 0.0f, 1.0f); 
    float ds_dtau = 1.0f;
    switch(profile) {
        case 's': ds_dtau = 0.5f * M_PI * sin(M_PI * tau); break;
        case 'c': ds_dtau = 6.0f * tau * (1.0f - tau); break;
        case 'i': ds_dtau = 30.0f * tau * tau * (1.0f - 2.0f*tau + tau*tau); break;
        default:  ds_dtau = 1.0f; break; // lineal
    }
    return ds_dtau / duration; // Retorna ds/dt
}

// =================================================================
// Sintonizador Automático 
// =================================================================
void ControlManager::AutoTuneLoop(float dt) {
    static int state = 0;
    static int last_state = -1; // <-- NUEVO: Para evitar spam de prints
    static int motor = 0;
    static float timer_tune = 0.0f;
    
    static float test_pwm = 0.0f;
    static float fric_up = 0.0f;
    static float fric_down = 0.0f;
    
    const float ramp_rate = 10.0f; 
    const float vel_threshold = 0.03f; 

    // --- Variables del Relé ---
    const float relay_d = 20.0f;    
    const float hysteresis = 0.02f; 
    static int relay_state = 1;     
    static float peak_max = 0.0f, peak_min = 0.0f;
    static float sum_amp = 0.0f, sum_period = 0.0f;
    static int cycle_count = 0;
    static unsigned long last_switch_time = 0;

    if (!angleLimits()) {
        is_tuning = false; state = 0; motor = 0; stopRobot();
        Serial.println("\n[-] [AUTO-TUNE] ABORTADO: Limite articular excedido.");
        return;
    }

    bool limite_peligroso = (sensor_q[motor] >= _max_angles[motor] - 0.15f) || 
                        (sensor_q[motor] <= _min_angles[motor] + 0.15f);
                        

    // =========================================================
    // IMPRESIÓN LIMPIA (Solo una vez por cada cambio de fase)
    // =========================================================
    if (state != last_state) {
        Serial.printf("\n[TUNE] M%d | ", motor + 1);
        switch(state) {
            case 0: Serial.print("Iniciando..."); break;
            case 1: Serial.print("Estabilizando..."); break;
            case 2: Serial.print("Buscando Friccion UP..."); break;
            case 3: Serial.print("Buscando Friccion DOWN..."); break;
            case 4: Serial.print("Ejecutando Rele Astrom-Hagglund..."); break;
            case 5: Serial.print("Calculando Ganancias y Guardando..."); break;
            case 6: Serial.print("Descanso post-prueba..."); break;
            case 7: Serial.print("Transicion de motor..."); break;
        }
        last_state = state;
    }

    // =========================================================
    // MÁQUINA DE ESTADOS
    // =========================================================
    switch(state) {
        case 0: 
            if (motor == 0 && timer_tune == 0.0f) {
                test_pwm = 0.0f; fric_up = 0.0f; fric_down = 0.0f;
                Serial.println("\n>> [AUTO-TUNE] Iniciando evaluacion In-Situ...");
            }
            if(_sys) _sys->applyMotor(motor, 0, 'S'); 
            state = 1; 
            break;

        case 1: 
            if(_sys) _sys->applyMotor(motor, 0, 'S');
            timer_tune += dt;
            if (timer_tune > 0.5f) { timer_tune = 0.0f; test_pwm = 0.0f; state = 2; }
            break;

        case 2: 
            if (limite_peligroso) { fric_up = test_pwm; state = 3; test_pwm = 0.0f; break; }
            test_pwm += ramp_rate * dt;
            if(_sys) _sys->applyMotor(motor, (int)test_pwm, 'H');

            if (std::abs(sensor_q_dot[motor]) > vel_threshold || test_pwm >= 60.0f) {
                fric_up = test_pwm;
                if(_sys) _sys->applyMotor(motor, 0, 'S');
                Serial.printf(" LISTO (%.1f PWM)", fric_up); // Se imprime en la misma línea
                timer_tune = 0.0f; test_pwm = 0.0f; state = 3;
            }
            break;

        case 3: 
            timer_tune += dt;
            if (timer_tune < 0.5f) return; 
            if (limite_peligroso) { fric_down = test_pwm; state = 4; timer_tune = 0.0f; break; }
            test_pwm += ramp_rate * dt;
            if(_sys) _sys->applyMotor(motor, (int)test_pwm, 'A');

            if (std::abs(sensor_q_dot[motor]) > vel_threshold || test_pwm >= 60.0f) {
                fric_down = test_pwm;
                if(_sys) _sys->applyMotor(motor, 0, 'S');
                Serial.printf(" LISTO (%.1f PWM)", fric_down);
                
                // --- INICIO SETUP STEP RESPONSE (ESCALÓN) ---
                sum_amp = 0.0f; // Reutilizamos esta variable para guardar la velocidad máxima
                timer_tune = 0.0f; 
                state = 4;
            }
            break;

        case 4: // PRUEBA DE ESCALÓN (Step Response)
            {
                timer_tune += dt; 
                float step_amp = 20.0f; // Inyectamos 20 PWM estables sobre la fricción
                float pwm_prueba = std::min(fric_up + step_amp, 95.0f); // Protección de límite

                if(_sys) _sys->applyMotor(motor, (int)pwm_prueba, 'H');

                // Filtramos la velocidad máxima alcanzada en estado estacionario
                float vel = std::abs(sensor_q_dot[motor]);
                if (vel > sum_amp) sum_amp = vel; // Guardamos V_max en sum_amp

                // Terminamos la lectura tras 1 segundo (suficiente para estabilizar un worm gear) 
                // o inmediatamente si toca la pared virtual
                if (timer_tune > 1.0f || limite_peligroso) {
                    state = 5;
                }
            }
            break; 

        case 5: // CÁLCULO LAMBDA MODIFICADO PARA REDUCTORAS LENTAS
            if(_sys) _sys->applyMotor(motor, 0, 'S');
            
            if (sum_amp > 0.01f) { 
                float step_amp = 20.0f;
                float Kv = sum_amp / step_amp; 
                
                // 1. Relajamos los tiempos físicos
                float tau_mec = 0.15f; 
                float tau_c = 0.80f; // Exigimos que se estabilice en 0.8s, no en 0.2s. Mucho más natural.
                
                // 2. Cálculo Proporcional (Kp)
                float kp_raw = tau_mec / (Kv * tau_c);
                
                // 3. Regla Skogestad Modificada para Ki (Evita oscilaciones en motores duros)
                // En lugar de (kp/tau_mec), forzamos un tiempo de integración mucho más largo.
                float Ti = tau_mec + (4.0f * tau_c); 
                float ki_raw = kp_raw / Ti; 
                
                joints[motor].Kp_vel = constrain(kp_raw, 0.1f, 50.0f);
                joints[motor].Ki_vel = constrain(ki_raw, 0.1f, 80.0f);
                joints[motor].fric_up_pwm = fric_up; 
                joints[motor].fric_down_pwm = fric_down;

                Serial.printf("\n    -> EXITOSO! (Metodo Lambda Relajado)\n");
                Serial.printf("    -> Kv: %.4f | Kp: %.2f | Ki: %.2f | Fric: %.1f/%.1f\n", Kv, joints[motor].Kp_vel, joints[motor].Ki_vel, fric_up, fric_down);
                
                if (_sys) _sys->saveGains(motor, joints[motor].Kp_vel, joints[motor].Ki_vel, fric_up, fric_down);
            } else {
                Serial.printf("\n    -> FALLO! Motor atascado, el escalon de PWM no rompio la friccion estatica.\n");
            }

            timer_tune = 0.0f; state = 6;
            break;
        
        case 6: 
            if(_sys) _sys->applyMotor(motor, 0, 'S');
            timer_tune += dt;
            if (timer_tune > 1.0f) { timer_tune = 0.0f; state = 7; }
            break;
            
        case 7: 
            if(_sys) _sys->applyMotor(motor, 0, 'S');
            timer_tune += dt;
            if(timer_tune > 0.5f) { 
                motor++; timer_tune = 0.0f;
                if (motor > 3) {
                    is_tuning = false; state = 0; motor = 0; last_state = -1; stopRobot(); 
                    Serial.println("\n\n[=== AUTO-TUNE COMPLETADO ===]");
                } else {
                    state = 1; 
                }
            }
            break;
    }
}

void ControlManager::setGains(int id, float kp, float ki, float fup, float fdown) {
    if (id >= 0 && id < 4) {
        joints[id].Kp_vel = kp;
        joints[id].Ki_vel = ki;
        joints[id].fric_up_pwm = fup;
        joints[id].fric_down_pwm = fdown;
        if (_sys) _sys->saveGains(id, kp, ki, fup, fdown); // Guarda en NVS automáticamente
    }
}

void ControlManager::loadAllGains() {
    if (!_sys) return;
    for (int i = 0; i < 4; i++) {
        _sys->loadGains(i, joints[i].Kp_vel, joints[i].Ki_vel, joints[i].fric_up_pwm, joints[i].fric_down_pwm);
    }
    Serial.println(F("[+] Ganancias de motores cargadas desde memoria."));
}
// =================================================================
// Comandos Movimiento (Punteros de entrada en Radianes)
// =================================================================
// =================================================================
// Comandos Movimiento (Punteros de entrada en Radianes)
// =================================================================
bool ControlManager::moveA(float q1, float q2, float q3, float q4, float speed_deg_s) {
    traj_space = 'Q'; 
    float max_diff = 0.0f;
    for(int i = 0; i < 4; i++) { start_Q[i] = sensor_q[i]; }
    
    final_target_Q[0] = q1; final_target_Q[1] = q2;
    final_target_Q[2] = q3; final_target_Q[3] = q4;
    
    // Busca cuál articulación debe viajar más lejos (en radianes)
    for(int i = 0; i < 4; i++) { 
        float diff = std::abs(final_target_Q[i] - start_Q[i]);
        if (diff > max_diff) max_diff = diff;
    }
    
    // Convertimos la velocidad solicitada a Radianes/Segundo
    float speed_rad_s = speed_deg_s * (float)M_PI / 180.0f;
    if (speed_rad_s < 0.05f) speed_rad_s = 0.05f; // Seguridad min
    
    // El tiempo será la distancia de la articulación más exigida sobre la velocidad
    traj_duration = max_diff / speed_rad_s;
    if (traj_duration < 0.1f) traj_duration = 0.1f; 
    
    traj_time = 0.0f; 
    enable_interpolation = true;
    return true; 
}

// =================================================================
// SOBRECARGAS DE MOVEL (Línea Recta Cartesiana)
// =================================================================
bool ControlManager::moveL(float x, float y, float z, float speed_mm_s) {
    traj_space = 'C'; 
    control_mode = 0; 
    
    Kinematic::Matrix4f T_current;
    // [BUG ARREGLADO] ¡Se deben pasar grados, no radianes!
    _kinematic->angle2Pos(sensor_q[0]*180.0f/M_PI, sensor_q[1]*180.0f/M_PI, sensor_q[2]*180.0f/M_PI, sensor_q[3]*180.0f/M_PI, T_current);
    start_XYZ << T_current(0,3), T_current(1,3), T_current(2,3);
    final_target_XYZ << x, y, z;
    
    // Cálculo de Distancia Euclidiana en 3D
    float dist = (final_target_XYZ - start_XYZ).norm();
    if (speed_mm_s < 1.0f) speed_mm_s = 1.0f; // Evitar división por cero
    
    traj_duration = dist / speed_mm_s;
    if (traj_duration < 0.1f) traj_duration = 0.1f;

    traj_time = 0.0f;
    enable_interpolation = true;
    return true; 
}

bool ControlManager::moveL(float x, float y, float z, float speed_mm_s, float phi_val) {
    traj_space = 'C'; 
    control_mode = 1; 
    
    Kinematic::Matrix4f T_current;
    _kinematic->angle2Pos(sensor_q[0]*180.0f/M_PI, sensor_q[1]*180.0f/M_PI, sensor_q[2]*180.0f/M_PI, sensor_q[3]*180.0f/M_PI, T_current);
    start_XYZ << T_current(0,3), T_current(1,3), T_current(2,3);
    final_target_XYZ << x, y, z;
    
    start_Phi = sensor_q[1] + sensor_q[2] + sensor_q[3]; 
    final_target_Phi = phi_val; 
    
    float dist = (final_target_XYZ - start_XYZ).norm();
    if (speed_mm_s < 1.0f) speed_mm_s = 1.0f;
    
    traj_duration = dist / speed_mm_s;
    if (traj_duration < 0.1f) traj_duration = 0.1f;
    
    traj_time = 0.0f;
    enable_interpolation = true;
    return true; 
}

// =================================================================
// SOBRECARGAS DE MOVEJ (Cinemática Inversa)
// =================================================================
bool ControlManager::moveJ(float x, float y, float z, float speed_mm_s, bool elbowUp) {
    float th1_deg, th2_deg, th3_deg;
    bool alcanzable = _kinematic->pos2Angle(x, y, z, th1_deg, th2_deg, th3_deg, 0.0f, elbowUp); 
    if (!alcanzable) return false; 
    
    float target_rad[4] = {
        th1_deg * (float)M_PI / 180.0f, th2_deg * (float)M_PI / 180.0f,
        th3_deg * (float)M_PI / 180.0f, 0.0f
    };
    
    for(int i=0; i<4; i++) {
        if(target_rad[i] < _min_angles[i] || target_rad[i] > _max_angles[i]) {
            Serial.printf("\n[-] Error: MoveJ abortado. Fuera de limites.\n"); return false;
        }
    }

    // Calculamos el tiempo basado en la distancia cartesiana
    Kinematic::Matrix4f T_current;
    _kinematic->angle2Pos(sensor_q[0]*180.0f/M_PI, sensor_q[1]*180.0f/M_PI, sensor_q[2]*180.0f/M_PI, sensor_q[3]*180.0f/M_PI, T_current);
    Eigen::Vector3f s_XYZ(T_current(0,3), T_current(1,3), T_current(2,3));
    Eigen::Vector3f f_XYZ(x, y, z);
    
    float dist = (f_XYZ - s_XYZ).norm();
    if (speed_mm_s < 1.0f) speed_mm_s = 1.0f;
    
    // Si la distancia cartesiana es casi cero (solo rotó la muñeca), aseguramos un tiempo angular mínimo 
    float max_diff = 0.0f;
    for(int i=0; i<4; i++) { max_diff = std::max(max_diff, std::abs(target_rad[i] - sensor_q[i])); }
    float time_ang = max_diff / (30.0f * (float)M_PI / 180.0f); // Fallback: 30 grados/seg 
    
    traj_duration = std::max(dist / speed_mm_s, time_ang);
    if (traj_duration < 0.1f) traj_duration = 0.1f;

    traj_space = 'Q'; 
    for(int i = 0; i < 4; i++) { start_Q[i] = sensor_q[i]; final_target_Q[i] = target_rad[i]; }
    traj_time = 0.0f; enable_interpolation = true;
    return true; 
}

bool ControlManager::moveJ(float x, float y, float z, float speed_mm_s, float phi_val, bool elbowUp) {
    float th1_deg, th2_deg, th3_deg, th4_deg;
    float phi_deg = phi_val * 180.0f / M_PI; 
    
    bool alcanzable = _kinematic->pos2Angle(x, y, z, th1_deg, th2_deg, th3_deg, th4_deg, phi_deg, elbowUp);
    if (!alcanzable) return false; 
    
    float target_rad[4] = {
        th1_deg * (float)M_PI / 180.0f, th2_deg * (float)M_PI / 180.0f,
        th3_deg * (float)M_PI / 180.0f, th4_deg * (float)M_PI / 180.0f
    };

    for(int i=0; i<4; i++) {
        if(target_rad[i] < _min_angles[i] || target_rad[i] > _max_angles[i]) {
            Serial.printf("\n[-] Error: MoveJ abortado. Fuera de limites.\n"); return false;
        }
    }
    
    Kinematic::Matrix4f T_current;
    _kinematic->angle2Pos(sensor_q[0]*180.0f/M_PI, sensor_q[1]*180.0f/M_PI, sensor_q[2]*180.0f/M_PI, sensor_q[3]*180.0f/M_PI, T_current);
    Eigen::Vector3f s_XYZ(T_current(0,3), T_current(1,3), T_current(2,3));
    Eigen::Vector3f f_XYZ(x, y, z);
    
    float dist = (f_XYZ - s_XYZ).norm();
    if (speed_mm_s < 1.0f) speed_mm_s = 1.0f;
    
    float max_diff = 0.0f;
    for(int i=0; i<4; i++) { max_diff = std::max(max_diff, std::abs(target_rad[i] - sensor_q[i])); }
    float time_ang = max_diff / (30.0f * (float)M_PI / 180.0f);
    
    traj_duration = std::max(dist / speed_mm_s, time_ang);
    if (traj_duration < 0.1f) traj_duration = 0.1f;
    
    traj_space = 'Q'; 
    for(int i = 0; i < 4; i++) { start_Q[i] = sensor_q[i]; final_target_Q[i] = target_rad[i]; }
    traj_time = 0.0f; enable_interpolation = true;
    return true; 
}

//////////////////////////////////////////

void ControlManager::printGains() {
    Serial.println(F("\n================ GANANCIAS NVS Y FRICCIÓN ================"));
    for (int i = 0; i < 4; i++) {
        Serial.printf("Motor %d -> Kp: %6.2f | Ki: %6.2f | F_Up: %5.1f | F_Dn: %5.1f\n", 
                      i + 1, joints[i].Kp_vel, joints[i].Ki_vel, 
                      joints[i].fric_up_pwm, joints[i].fric_down_pwm);
    }
    Serial.println(F("==========================================================\n"));
}

///////////////////////////////////////