import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

class StepperAnalysis:
    def __init__(self, I_ph, R, L, T_h_motor, ratio, J_motor=50e-7, V=24, 
                 l1=100.0, l2=120.0, m1=0.5, m2=0.3, J_gearbox=1.5e-5, backlash = 3/60):
        # Parámetros Eléctricos y del Motor
        self.I_ph = I_ph             
        self.R = R                   
        self.L = L                   
        self.V = V                   
        self.T_h_motor = T_h_motor   
        self.eff = 0.96              
        self.ratio = ratio           
        self.p = 50                
        
        # Parámetros Mecánicos y Geométricos (Brazo Planar 2R)
        self.l1_m = l1 / 1000.0  # Convertido a metros para dinámica
        self.l2_m = l2 / 1000.0
        self.l1_mm = l1          # En mm para graficación
        self.l2_mm = l2
        self.m1 = m1             # Masa eslabón 1 (kg)
        self.m2 = m2             # Masa eslabón 2 (kg)
        self.J_gb = J_gearbox    # Inercia de la caja referida al motor (kg*m^2)
        self.backlash = backlash  

    def electrical_analysis(self, rpm_motor_array):
        Kt = self.T_h_motor / self.I_ph
        f_elec = (rpm_motor_array / 60.0) * self.p
        omega_e = 2 * np.pi * f_elec
        omega_mech = rpm_motor_array * (2 * np.pi / 60.0)
        
        E_emf = Kt * omega_mech
        Z = np.sqrt(self.R**2 + (omega_e * self.L)**2)
        
        pasos_por_rev = self.p * 4
        t_step = 60.0 / (rpm_motor_array * pasos_por_rev)
        tau = self.L / self.R 
        
        I_transient = ((self.V - E_emf) / self.R) * (1 - np.exp(-t_step / tau))
        I_steady = (self.V - E_emf) / Z
        I_act = np.minimum(self.I_ph, np.maximum(np.minimum(I_transient, I_steady), 0))
        
        T_ideal = Kt * I_act
        k_eddy = 0.0008 
        T_loss = k_eddy * omega_mech
        
        T_dyn_motor = np.maximum(T_ideal - T_loss, 0)
        T_dyn_out = T_dyn_motor * self.ratio * self.eff
        rpm_out_array = rpm_motor_array / self.ratio
        P_cu = 2 * (I_act**2) * self.R
        
        return T_dyn_motor, T_dyn_out, rpm_out_array, E_emf, P_cu

    def _dh_matrix(self, theta, d, a, alpha):
        t = np.radians(theta)
        al = np.radians(alpha)
        return np.array([
            [np.cos(t), -np.sin(t)*np.cos(al),  np.sin(t)*np.sin(al), a*np.cos(t)],
            [np.sin(t),  np.cos(t)*np.cos(al), -np.cos(t)*np.sin(al), a*np.sin(t)],
            [0,          np.sin(al),            np.cos(al),           d],
            [0,          0,                     0,                    1]
        ])

    def kinematic_analysis(self, theta1, theta2):
        """Cinemática Directa usando parámetros DH"""
        A1 = self._dh_matrix(theta1, 0, self.l1_mm, 0)
        A2 = self._dh_matrix(theta2, 0, self.l2_mm, 0)
        T_final = A1 @ A2
        x = T_final[0, 3]
        y = T_final[1, 3]
        return x, y

    def plot_workspace(self, t1_min=0, t1_max=180, t2_min=-180, t2_max=0, step=3):
        theta1_vals = np.arange(t1_min, t1_max + step, step)
        theta2_vals = np.arange(t2_min, t2_max + step, step)
        
        X, Y = [], []
        for t1 in theta1_vals:
            for t2 in theta2_vals:
                x, y = self.kinematic_analysis(t1, t2)
                X.append(x)
                Y.append(y)
                
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.scatter(X, Y, s=2, color='blue', alpha=0.5)
        ax.set_title("Mapa de Posiciones Alcanzables (Cinemática DH)")
        ax.set_xlabel("X (mm)")
        ax.set_ylabel("Y (mm)")
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.axis('equal')
        plt.show()

    def plot_backlash_error(self, theta1_nom, theta2_nom):
        backlash_deg = self.backlash 
        x_nom, y_nom = self.kinematic_analysis(theta1_nom, theta2_nom)
        
        t1_errs = [theta1_nom - backlash_deg, theta1_nom, theta1_nom + backlash_deg]
        t2_errs = [theta2_nom - backlash_deg, theta2_nom, theta2_nom + backlash_deg]
        
        X_err, Y_err = [], []
        for t1 in t1_errs:
            for t2 in t2_errs:
                x, y = self.kinematic_analysis(t1, t2)
                X_err.append(x)
                Y_err.append(y)
                
        fig, ax = plt.subplots(figsize=(6, 6))
        points = np.column_stack((X_err, Y_err))
        hull = ConvexHull(points)
        
        for simplex in hull.simplices:
            ax.plot(points[simplex, 0], points[simplex, 1], 'r--', lw=2)
            
        ax.fill(points[hull.vertices,0], points[hull.vertices,1], 'red', alpha=0.2, 
                label=f"Zona de Error (Backlash ±{backlash_deg}°)")
        ax.plot(X_err, Y_err, 'ko', markersize=4)
        ax.plot(x_nom, y_nom, 'bo', markersize=8, label="Posición Nominal")
        
        ax.set_title(f"Desfase por Backlash en Efector Final\n(T1={theta1_nom}°, T2={theta2_nom}°)")
        ax.set_xlabel("X (mm)")
        ax.set_ylabel("Y (mm)")
        ax.legend()
        ax.grid(True, linestyle=':')
        ax.axis('equal')
        plt.show()

    def calculate_dynamic_torques(self, theta1, theta2, accel_1, accel_2):
        t2_rad = np.radians(theta2)
        r1, r2 = self.l1_m / 2, self.l2_m / 2
        
        I1 = (1/12) * self.m1 * self.l1_m**2
        I2 = (1/12) * self.m2 * self.l2_m**2
        
        M11 = self.m1*r1**2 + self.m2*(self.l1_m**2 + r2**2 + 2*self.l1_m*r2*np.cos(t2_rad)) + I1 + I2
        M12 = self.m2*(r2**2 + self.l1_m*r2*np.cos(t2_rad)) + I2
        M21 = M12
        M22 = self.m2*r2**2 + I2
        
        M = np.array([[M11, M12], [M21, M22]])
        accel_vec = np.array([accel_1, accel_2]) 
        
        T_link = M @ accel_vec
        
        T_gearbox_1 = (self.J_gb * self.ratio**2) * accel_1
        T_gearbox_2 = (self.J_gb * self.ratio**2) * accel_2
        
        T_total = T_link + np.array([T_gearbox_1, T_gearbox_2])
        T_motor_req = T_total / (self.ratio * self.eff)
        
        return T_total, T_motor_req
    
if __name__ == "__main__":    

    motor_database = {
        "TS4215Y3N": {"I_ph": 1.7, "R": 1.5, "L": 0.0028, "ratio": 15, "T_h_motor": 3.9 / (15 * 0.96)},
        "TS4230Y3N": {"I_ph": 1.7, "R": 1.5, "L": 0.0028, "ratio": 30, "T_h_motor": 7.8 / (30 * 0.96)},
        "TS4215Y4N": {"I_ph": 1.7, "R": 1.8, "L": 0.0032, "ratio": 15, "T_h_motor": 5.6 / (15 * 0.96)},
        "TS4230Y4N": {"I_ph": 1.7, "R": 1.8, "L": 0.0032, "ratio": 30, "T_h_motor": 11.2 / (30 * 0.96)},
        "TS4215Y5N": {"I_ph": 2.0, "R": 1.2, "L": 0.0025, "ratio": 15, "T_h_motor": 7.9 / (15 * 0.96)},
        "TS4230Y5N": {"I_ph": 2.0, "R": 1.2, "L": 0.0025, "ratio": 30, "T_h_motor": 15.8 / (30 * 0.96)},
    }

    # Instanciamos un motor para el análisis cinemático/dinámico
    specs = motor_database["TS4215Y3N"]
    analisis = StepperAnalysis(
        I_ph=specs["I_ph"], R=specs["R"], L=specs["L"], 
        T_h_motor=specs["T_h_motor"], ratio=specs["ratio"]
    )

    # --- 1. ANÁLISIS ELÉCTRICO ---
    rpm_range = np.linspace(10, 1500, 200)
    T_dyn_motor, T_dyn_out, rpm_out, E_emf, P_cu = analisis.electrical_analysis(rpm_range)
    
    plt.figure(figsize=(8, 4))
    plt.plot(rpm_range, T_dyn_out, 'b-', linewidth=2, label="Torque de Salida Disponible")
    plt.title("Curva de Torque Electromecánico (TS4215Y3N)")
    plt.xlabel("RPM Motor")
    plt.ylabel("Torque Salida (Nm)")
    plt.grid(True)
    plt.legend()
    plt.show()

    # --- 2. ANÁLISIS CINEMÁTICO ---
    analisis.plot_workspace(t1_min=0, t1_max=180, t2_min=-180, t2_max=0)
    # Se eliminó backlash_deg=1.2 de los argumentos porque ahora es un atributo de clase
    analisis.plot_backlash_error(theta1_nom=45, theta2_nom=-45)

    # --- 3. ANÁLISIS DINÁMICO ---
    T_out_req, T_motor_req = analisis.calculate_dynamic_torques(theta1=45, theta2=-45, accel_1=8.0, accel_2=8.0)
    print("--- REQUERIMIENTOS DINÁMICOS ---")
    print(f"Torque requerido en salida caja: Articulación 1 = {T_out_req[0]:.3f} Nm, Articulación 2 = {T_out_req[1]:.3f} Nm")
    print(f"Torque requerido desde motor:    Motor 1 = {T_motor_req[0]:.3f} Nm, Motor 2 = {T_motor_req[1]:.3f} Nm")