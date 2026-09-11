import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import copy

class StepperMotor:
    def __init__(self, name, I_ph, R, L, T_H, J_m, V=24, N_r=50, k_eddy=0.0005):
        self.name = name
        self.I_ph = I_ph        # Corriente nominal (A)
        self.R = R              # Resistencia por fase (Ohms)
        self.L = L              # Inductancia por fase (H)
        self.T_H = T_H          # Holding Torque (Nm)
        self.J_m = J_m          # Inercia del motor (kg*m^2)
        self.V = V              # Voltaje de alimentación (V)
        self.N_r = N_r          # Número de dientes del rotor (50 para 1.8 grados)
        self.k_eddy = k_eddy    # Pérdidas por Foucault y viscosidad (Nm*s/rad)
        
        # Ecuación (1): Constante de Torque
        self.Kt = self.T_H / self.I_ph
        # Salto angular por paso (rad)
        self.d_theta = np.pi / (2 * self.N_r)
        
        # Estado por defecto (Sin transmisión)
        self.apply_transmission(ratio=1.0, eff=1.0, J_load=0.0)

    def apply_transmission(self, ratio, eff, J_load=0.0):
        """ Aplica una caja reductora y actualiza inercias reflejadas """
        self.ratio = ratio
        self.eff = eff
        self.J_load = J_load
        self.J_tot = self.J_m + (self.J_load / (self.ratio**2))
        return self

    def get_Z(self, w_m):
        """ Impedancia sincrónica - Ecuación (3) """
        w_e = self.N_r * w_m
        return np.sqrt(self.R**2 + (w_e * self.L)**2)
        
    def get_I_env(self, w_m):
        """ Envolvente de corriente física - Ecuación (4) """
        E_b = self.Kt * w_m # Ecuación (2): FCEM
        Z = self.get_Z(w_m)
        return np.maximum(0, (self.V - E_b) / Z)
        
    def get_I_act(self, w_m):
        """ Corriente inyectada por el Chopper - Ecuación (5) """
        return np.minimum(self.I_ph, self.get_I_env(w_m))
        
    def get_T_po(self, w_m):
        """ Pull-out Torque (Eje Motor) - Ecuación (7) """
        T_ideal = self.Kt * self.get_I_act(w_m)
        T_loss = self.k_eddy * w_m
        return np.maximum(0, T_ideal - T_loss)
        
    def get_T_pi(self, w_m):
        """ Pull-in Torque (Eje Motor) - Ecuación (8) """
        T_po = self.get_T_po(w_m)
        T_accel = self.J_tot * (w_m**2) / (2 * self.d_theta)
        return np.maximum(0, T_po - T_accel)

    def get_Tout_po(self, w_m):
        """ Pull-out Torque (Efector / Salida de caja) - Ecuación (9) """
        return self.get_T_po(w_m) * self.ratio * self.eff
        
    def get_Tout_pi(self, w_m):
        """ Pull-in Torque (Efector / Salida de caja) """
        return self.get_T_pi(w_m) * self.ratio * self.eff
        
    def get_corner_speed_rpm(self):
        """ Calcula la Frecuencia de Corte w_c resolviendo I_env = I_ph """
        # Coeficientes de la ecuación cuadrática A*w_c^2 + B*w_c + C = 0
        A = self.Kt**2 - (self.I_ph * self.N_r * self.L)**2
        B = -2 * self.V * self.Kt
        C = self.V**2 - (self.I_ph * self.R)**2
        
        disc = B**2 - 4*A*C
        if disc >= 0 and A != 0:
            w_c1 = (-B + np.sqrt(disc)) / (2*A)
            w_c2 = (-B - np.sqrt(disc)) / (2*A)
            w_c = max(w_c1, w_c2)
            if w_c > 0: return w_c * (30 / np.pi) # rad/s a RPM
        return 0.0

class MotorAnalysis:
    def __init__(self):
        # Base de datos de motores (Datos de placa, sin reductores)
        self.base_motors = [
            StepperMotor("17HD60001", I_ph=1.6, R=2.4, L=0.0036, T_H=0.70, J_m=102e-7),
            StepperMotor("17HS4401",  I_ph=1.5, R=1.5, L=0.0028, T_H=0.42, J_m=54e-7),
            StepperMotor("17HS08-1004S", I_ph=0.4, R=3.5, L=0.0046, T_H=0.2, J_m=22e-7),
            StepperMotor("TS4215M2D", I_ph=1.0, R=2.3, L=0.0031, T_H=0.12, J_m=54e-7),
            StepperMotor("TS4215M5D", I_ph=2.0, R=1.65, L=0.0036, T_H=0.52, J_m=54e-7),
        ]
        # Expandida la paleta para soportar más de 4 motores
        self.colors = ['#d62728', '#1f77b4', '#2ca02c', '#9467bd', '#ff7f0e', '#8c564b', '#e377c2']

    def run_electrical_analysis(self, case_name, transmission_dict=None):
        print(f"\n{'='*60}\nEJECUTANDO ANÁLISIS: {case_name.upper()}\n{'='*60}")
        
        # 1. Configurar motores para este caso específico
        motors = copy.deepcopy(self.base_motors)
        for i, motor in enumerate(motors):
            if transmission_dict and motor.name in transmission_dict:
                conf = transmission_dict[motor.name]
                motor.apply_transmission(ratio=conf.get('ratio', 1.0), eff=conf.get('eff', 1.0))
                motor.name += f" (Caja {conf['ratio']}:1)"
            else:
                motor.name += " (Directo)"

        # 2. Configuración de Gráficas (Grid 2x2)
        fig, axs = plt.subplots(2, 2, figsize=(16, 11))
        fig.suptitle(f"Análisis Electromecánico: {case_name}", fontsize=16, fontweight='bold')
        
        w_motor_rpm = np.linspace(0, 1500, 400)
        w_m_rads = w_motor_rpm * (np.pi / 30)

        # Variables para calcular el límite máximo del eje X automáticamente
        max_w_out_rpm = 0

        # --- Subplot 1: Pull-in y Pull-out vs Velocidad de SALIDA ---
        ax = axs[0, 0]
        for i, motor in enumerate(motors):
            w_out_rpm = w_motor_rpm / motor.ratio
            max_w_out_rpm = max(max_w_out_rpm, max(w_out_rpm))
            
            T_out_po = motor.get_Tout_po(w_m_rads)
            T_out_pi = motor.get_Tout_pi(w_m_rads)
            
            ax.plot(w_out_rpm, T_out_po, '-', color=self.colors[i], linewidth=2, label=f'{motor.name} (P-out)')
            ax.plot(w_out_rpm, T_out_pi, '--', color=self.colors[i], linewidth=1.5, alpha=0.8)
            
        ax.set_title("Curvas Dinámicas (Eje de Salida)")
        ax.set_xlabel("Velocidad de Salida Efectiva (RPM)")
        ax.set_ylabel("Torque Dinámico de Salida (Nm)")
        ax.set_xlim(0, max_w_out_rpm) # Ajuste dinámico del eje X
        ax.grid(True, linestyle=':'); ax.legend(fontsize=8)

        # --- Subplot 2: Torque vs Voltaje (Motor Representativo) ---
        ax = axs[0, 1]
        test_motor = motors[1] # Usar el 17HS4401 como prueba
        V_array = np.linspace(12, 48, 200)
        rpm_tests = [300, 600, 900, 1200]
        
        for rpm in rpm_tests:
            w = rpm * (np.pi / 30)
            T_out_V = []
            for v in V_array:
                test_motor.V = v
                T_out_V.append(test_motor.get_Tout_po(w))
            ax.plot(V_array, T_out_V, linewidth=2, label=f'ω mot = {rpm} RPM')
            
        test_motor.V = 24 # Restaurar
        ax.set_title(f"T. Salida vs Voltaje ({test_motor.name})")
        ax.set_xlabel("Voltaje de Alimentación (V)")
        ax.set_ylabel("Pull-out Torque Disponible (Nm)")
        ax.axvline(x=24, color='k', linestyle='--', label='24V (Nominal)')
        ax.set_xlim(12, 48)
        ax.grid(True); ax.legend(fontsize=9)

        # --- Subplot 3: Torque vs Corriente (Estática) ---
        ax = axs[1, 0]
        for i, motor in enumerate(motors):
            I_range = np.linspace(0, motor.I_ph * 1.5, 100)
            T_static = motor.Kt * np.minimum(I_range, motor.I_ph) * motor.ratio * motor.eff
            ax.plot(I_range, T_static, color=self.colors[i], linewidth=2, label=motor.name)
            ax.plot(motor.I_ph, motor.T_H * motor.ratio * motor.eff, 'o', color=self.colors[i])
            
        ax.set_title("Torque de Salida vs Corriente de Fase")
        ax.set_xlabel("Corriente (A)")
        ax.set_ylabel("Holding Torque Efectivo (Nm)")
        ax.set_xlim(left=0)
        ax.grid(True, linestyle='--'); ax.legend(fontsize=8)

        # --- Subplot 4: Balance de Potencias (Todos los Motores) ---
        ax = axs[1, 1]
        for i, motor in enumerate(motors):
            # Potencia útil mecánica = Torque de salida * Velocidad angular de salida
            P_mech = motor.get_Tout_po(w_m_rads) * (w_m_rads / motor.ratio)
            
            # Pérdidas totales (I²R Cobre + Pérdidas Núcleo/Fricción)
            I_act_arr = motor.get_I_act(w_m_rads)
            P_cu = 2 * (I_act_arr**2) * motor.R
            P_core = motor.k_eddy * (w_m_rads**2)
            P_losses = P_cu + P_core
            
            # Línea continua para P. Útil, Línea punteada para Pérdidas
            ax.plot(w_motor_rpm, P_mech, '-', color=self.colors[i], linewidth=2.5, label=motor.name)
            ax.plot(w_motor_rpm, P_losses, '--', color=self.colors[i], linewidth=1.5, alpha=0.8)
            
        ax.set_title("Potencia Mecánica Útil vs Pérdidas Totales")
        ax.set_xlabel("Velocidad Motor (RPM)")
        ax.set_ylabel("Potencia (W)")
        ax.set_xlim(0, 1500)
        ax.grid(True, linestyle=':')
        ax.legend(fontsize=8, loc='center right')
        
        # Cuadro de texto explicativo para las líneas
        ax.text(0.03, 0.96, "Línea Continua: Potencia Útil\nLínea Punteada: Pérdidas (Cu + Fe)", 
                transform=ax.transAxes, fontsize=9, verticalalignment='top', 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

        plt.tight_layout()
        plt.show()

        # 3. Generar Tabla Resumen con Pandas
        data = []
        for m in motors:
            data.append({
                "Motor": m.name,
                "I_ph (A)": m.I_ph,
                "L (mH)": m.L * 1000,
                "Transmisión": f"{m.ratio}:1",
                "Torque Eje (Nm)": m.T_H,
                "Torque Salida Max (Nm)": round(m.T_H * m.ratio * m.eff, 2),
                "Frec. Corte Motor (RPM)": round(m.get_corner_speed_rpm(), 0)
            })
            
        df = pd.DataFrame(data).set_index("Motor")
        print("\nRESUMEN DE PROPIEDADES ELECTROMECÁNICAS:")
        print("-" * 80)
        print(df.to_string())
        print("-" * 80 + "\n")


if __name__ == "__main__":
    analisis = MotorAnalysis()
    
    # ==========================================
    # CASO 1.1: Tracción Directa (Sin Cajas)
    # ==========================================
    analisis.run_electrical_analysis(case_name="Caso 1.1 - Motores Directos", transmission_dict=None)
    
    # ==========================================
    # CASO 1.2: Con Transmisión Cicloidal 15:1 
    # ==========================================
    tr15 = {
        "17HD60001": {"ratio": 15.0, "eff": 0.96},
        "17HS4401": {"ratio": 15.0, "eff": 0.96},
        "17HS08-1004S":  {"ratio": 15.0,  "eff": 0.96}, 
        "TS4215M2D":    {"ratio": 15.0,  "eff": 0.96},  
        "TS4215M5D":    {"ratio": 15.0,  "eff": 0.96},  
    }
    
    analisis.run_electrical_analysis(case_name="Caso 1.2 - Motores con Reducción", transmission_dict=tr15)
    
    # ==========================================
    # CASO 1.3: Con Transmisión Cicloidal 30:1 
    # ==========================================
    tr30 = {
        "17HD60001": {"ratio": 30.0, "eff": 0.96},
        "17HS4401": {"ratio": 30.0, "eff": 0.96},
        "17HS08-1004S":  {"ratio": 30.0,  "eff": 0.96}, 
        "TS4215M2D":    {"ratio": 30.0,  "eff": 0.96},  
        "TS4215M5D":    {"ratio": 30.0,  "eff": 0.96},  
    }
    
    analisis.run_electrical_analysis(case_name="Caso 1.2 - Motores con Reducción", transmission_dict=tr30)