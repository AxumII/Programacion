import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import copy

# ==========================================
# 1. Helpers de Cinemática (Transformaciones)
# ==========================================
def rot_x(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]])

def rot_y(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]])

def rot_z(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

def translation(v):
    return np.array([[1, 0, 0, v[0]], [0, 1, 0, v[1]], [0, 0, 1, v[2]], [0, 0, 0, 1]])

# ==========================================
# 2. Propiedades de Materiales y Geometría
# ==========================================
DENSITIES = {'PLA': 1250.0, 'PETG': 1270.0, 'Aluminio': 2700.0}
# Módulos de elasticidad (Pa) para cálculo de deflexión
E_MODULI = {'PLA': 2.0e9, 'PETG': 2.2e9, 'Aluminio': 69.0e9} 

def get_material_properties(material, b, h):
    area_m2 = b * h
    # Para plástico se asume un infill estructural (ej. 30% densidad efectiva)
    densidad_ef = DENSITIES['Aluminio'] if material == 'Aluminio' else DENSITIES[material] * 0.30
    return area_m2, densidad_ef

def calc_link_mass(material, length_m, b, h):
    area_m2, densidad_efectiva = get_material_properties(material, b, h)
    return area_m2 * length_m * densidad_efectiva

def get_inertia(material, b, h):
    if material == 'Aluminio':
        return (b * h**3) / 12
    else:
        # Para impresión 3D, el infill reduce la inercia efectiva (~50%)
        return (b * h**3) / 12 * 0.5 

# ==========================================
# 3. Clase Principal (Física 5 DOF Direct Drive)
# ==========================================
class RobotDOF_3D:
    def __init__(self, joints, alpha_target, m_load=0.0, m_tool=0.0, material='PLA'):
        self.joints = joints
        self.N = len(joints)
        self.alpha_target = alpha_target
        self.m_load = m_load
        self.m_tool = m_tool
        self.m_tip_total = m_load + m_tool 
        self.g = 9.81  
        self.F_g = np.array([0, 0, -self.g])
        
        self.material = material
        self.r_brida = 0.015 # 15 mm de radio para los tornillos M4
        self.n_tornillos = 6

    def forward_kinematics(self, thetas):
        T = np.eye(4)
        positions, z_axes, com_positions = [], [], []
        T_matrices = [] 
        
        for i, joint in enumerate(self.joints):
            if joint['axis'] == 'x':
                z_axes.append(T[:3, 0])
                T = T @ rot_x(thetas[i])
            elif joint['axis'] == 'y':
                z_axes.append(T[:3, 1])
                T = T @ rot_y(thetas[i])
            elif joint['axis'] == 'z':
                z_axes.append(T[:3, 2])
                T = T @ rot_z(thetas[i])
            
            positions.append(T[:3, 3])
            T_matrices.append(T.copy()) 
            
            T_com = T @ translation(joint['com_link'])
            com_positions.append(T_com[:3, 3])
            T = T @ translation(joint['offset'])
            
        p_tip = T[:3, 3]
        return np.array(positions), np.array(z_axes), np.array(com_positions), p_tip, T_matrices
    
    def calculate_torques_and_limits(self, thetas):
        positions, z_axes, com_positions, p_tip, T_matrices = self.forward_kinematics(thetas)

        t_static = np.zeros(self.N)
        t_dynamic_target = np.zeros(self.N)
        inertia_array = np.zeros(self.N)
        alpha_max_permitida = np.zeros(self.N)
        
        f_axial_tornillo = np.zeros(self.N)
        f_cortante_tornillo = np.zeros(self.N)
        deflexiones = np.zeros(self.N)
        
        for i in range(self.N):
            tau_3d_static = np.zeros(3)
            peso_acumulado_3d = np.zeros(3)
            inertia_i = 0.0
            P_axis = positions[i]
            u_axis = z_axes[i]
            
            for j in range(i, self.N):
                # Torque debido a los links
                r_vec_com = com_positions[j] - P_axis
                f_peso_j = self.joints[j]['m_link'] * self.F_g
                tau_3d_static += np.cross(r_vec_com, f_peso_j)
                peso_acumulado_3d += f_peso_j
                
                r_parallel_com = np.dot(r_vec_com, u_axis) * u_axis
                r_perp_com = np.linalg.norm(r_vec_com - r_parallel_com)
                inertia_i += self.joints[j]['m_link'] * (r_perp_com**2)
                
                # Torque debido a los motores en Direct Drive
                m_mot = self.joints[j].get('m_motor', self.joints[j].get('m_servo', 0.0))
                r_vec_mot = positions[j] - P_axis
                f_peso_mot = m_mot * self.F_g
                tau_3d_static += np.cross(r_vec_mot, f_peso_mot)
                peso_acumulado_3d += f_peso_mot
                
                r_parallel_mot = np.dot(r_vec_mot, u_axis) * u_axis
                r_perp_mot = np.linalg.norm(r_vec_mot - r_parallel_mot)
                inertia_i += m_mot * (r_perp_mot**2)
            
            if self.m_tip_total > 0:
                r_vec_load = p_tip - P_axis
                f_peso_load = self.m_tip_total * self.F_g
                tau_3d_static += np.cross(r_vec_load, f_peso_load)
                peso_acumulado_3d += f_peso_load
                r_parallel_load = np.dot(r_vec_load, u_axis) * u_axis
                r_perp_load = np.linalg.norm(r_vec_load - r_parallel_load)
                inertia_i += self.m_tip_total * (r_perp_load**2)
            
            torque_motor_nm = np.dot(tau_3d_static, u_axis)
            t_static[i] = abs(torque_motor_nm)
            t_dynamic_target[i] = inertia_i * self.alpha_target
            
            torque_flector_3d = tau_3d_static - (torque_motor_nm * u_axis)
            m_bend = np.linalg.norm(torque_flector_3d)
            
            f_axial_tornillo[i] = m_bend / (3 * self.r_brida) if self.r_brida > 0 else 0
            
            f_peso_magnitud = np.linalg.norm(peso_acumulado_3d)
            f_cortante_peso = f_peso_magnitud / self.n_tornillos
            f_cortante_torque = abs(torque_motor_nm) / (self.r_brida * self.n_tornillos)
            f_cortante_tornillo[i] = np.sqrt(f_cortante_peso**2 + f_cortante_torque**2)
            
            # Cálculo de deflexión leyendo los b y h parametrizados de la junta
            L_eff = np.linalg.norm(p_tip - P_axis)
            E = E_MODULI[self.material]
            b_link = self.joints[i].get('b', 0.030)
            h_link = self.joints[i].get('h', 0.050)
            I = get_inertia(self.material, b_link, h_link)
            deflexiones[i] = (f_peso_magnitud * (L_eff**3)) / (3 * E * I) if I > 0 else 0
            
            t_mot_base = self.joints[i].get('t_motor', self.joints[i].get('t_rated', 0.0))
            t_rated_joint_Nm = t_mot_base # Todo está en Nm
            
            t_margin_static = t_rated_joint_Nm - t_static[i]
            alpha_max_permitida[i] = (t_margin_static / inertia_i) if (t_margin_static > 0 and inertia_i > 0) else 0.0
                
        return t_static, t_dynamic_target, inertia_array, alpha_max_permitida, positions, f_axial_tornillo, f_cortante_tornillo, deflexiones

    def analyze_pose(self, thetas_deg, show_plot=True):
        thetas = np.radians(thetas_deg)
        t_static, t_dyn_target, inertias, alphas, motor_pos, f_axial, f_cortante, defls = self.calculate_torques_and_limits(thetas)
        
        metrics = []
        for i in range(self.N):
            t_mot_base = self.joints[i].get('t_motor', self.joints[i].get('t_rated', 0.0))
            t_joint_capacity = t_mot_base
            
            t_total_Nm = t_static[i] + t_dyn_target[i]
            fs = t_joint_capacity / t_total_Nm if t_total_Nm > 0 else float('inf')
            
            metrics.append({
                "Joint (Eje)": f"J{i} ({self.joints[i]['axis'].upper()})",
                "Capacidad [Nm]": round(t_joint_capacity, 2),
                "T. Req [Nm]": round(t_total_Nm, 2),
                "F. Axial M4 [N]": round(f_axial[i], 2),
                "F. Cortante M4 [N]": round(f_cortante[i], 2),
                "Deflexión Aprox [mm]": round(defls[i]*1000, 2),
                "Factor Seg": round(fs, 2)
            })
            
        df = pd.DataFrame(metrics).set_index("Joint (Eje)")
        print(f"\n" + "="*95)
        print(f"ANÁLISIS DE 5 DOF (Direct Drive) | Herramienta: {self.m_tool*1000}g | Carga: {self.m_load*1000}g")
        print("="*95)
        print(df.to_string())

        if show_plot:
            self._plot_3d(thetas, motor_pos)

    def _plot_3d(self, thetas, motor_positions):
        positions, z_axes, com_positions, p_tip, _ = self.forward_kinematics(thetas)
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        xs, ys, zs = positions[:, 0], positions[:, 1], positions[:, 2]
        
        ax.plot(np.append(xs, p_tip[0]), np.append(ys, p_tip[1]), np.append(zs, p_tip[2]), 
                'ko-', linewidth=5, markersize=8, label='Estructura')
        
        for i in range(self.N):
            ax.quiver(xs[i], ys[i], zs[i], z_axes[i,0]*0.06, z_axes[i,1]*0.06, z_axes[i,2]*0.06, color='green', linewidth=2)
            ax.text(xs[i], ys[i], zs[i] + 0.03, f'J{i}', fontweight='bold')
            
            mx, my, mz = motor_positions[i]
            ax.scatter(mx, my, mz, color='cyan', s=150, marker='s', zorder=6)
            ax.text(mx+0.02, my, mz, f'Mot J{i}', color='darkcyan')

        if self.m_tip_total > 0:
            ax.scatter(p_tip[0], p_tip[1], p_tip[2], color='blue', s=200, marker='D', label='Punta (Carga+Herr)')

        ax.set_title(f"Visualización Masas Direct Drive - Carga: {self.m_tip_total*1000}g")
        ax.set_xlim([-0.6, 0.6]); ax.set_ylim([-0.6, 0.6]); ax.set_zlim([-0.1, 0.7])
        ax.set_xlabel('X [m]'); ax.set_ylabel('Y [m]'); ax.set_zlabel('Z [m]')
        ax.legend()
        plt.show()

# ==========================================
# 4. Análisis de Barrido Continuo DINÁMICO
# ==========================================
def evaluar_barrido_multi_material(robot_template, materiales=['PLA', 'PETG', 'Aluminio'], m_load=0.0, m_tool=0.150, alpha_target=5.0):
    print("\nGenerando gráficas... Evaluando con secciones paramétricas (Valores en Nm).")
    
    longitudes_hombro = np.linspace(0.180, 0.450, 100)
    fig, axes = plt.subplots(1, len(materiales), figsize=(18, 6), sharey=True)
    if len(materiales) == 1: axes = [axes]
    
    fig2, axes2 = plt.subplots(2, len(materiales), figsize=(18, 10), sharex=True)
    if len(materiales) == 1: axes2 = np.array([axes2]).T
    
    max_torque_global = 0 
        
    for idx, material in enumerate(materiales):
        t_j0, t_j1, t_j2, t_j3, t_j4 = [], [], [], [], []
        f_axial_j1, f_cort_j1 = [], []
        deflexion_punta = []
        
        for L_hombro in longitudes_hombro:
            robot_def = copy.deepcopy(robot_template)
            
            L2 = L_hombro
            L3 = 0.7 * L_hombro
            L4 = 0.2 * L_hombro
            L5 = 0.1 * L_hombro
            
            longitudes = [0, L2, L3, L4, L5]
            
            for i in range(1, 5):
                b_link = robot_def[i].get('b', 0.030)
                h_link = robot_def[i].get('h', 0.050)
                area, den_ef = get_material_properties(material, b_link, h_link)
                
                robot_def[i]['offset'][0] = longitudes[i]
                robot_def[i]['m_link'] = area * longitudes[i] * den_ef
                robot_def[i]['com_link'][0] = longitudes[i] / 2
            
            arm = RobotDOF_3D(joints=robot_def, alpha_target=alpha_target, m_load=m_load, m_tool=m_tool, material=material)
            thetas_max = np.radians([0, 0, 0, 0, 0]) 
            t_static, _, _, _, _, f_ax, f_cort, defls = arm.calculate_torques_and_limits(thetas_max)
            
            t_j0.append(t_static[0])
            t_j1.append(t_static[1])
            t_j2.append(t_static[2])
            t_j3.append(t_static[3])
            t_j4.append(t_static[4])
            
            f_axial_j1.append(f_ax[1])
            f_cort_j1.append(f_cort[1])
            deflexion_punta.append(sum(defls) * 1000)

        # --- GRÁFICA 1: TORQUES ---
        ax = axes[idx]
        ax.plot(longitudes_hombro * 1000, t_j0, 'k:', linewidth=2, label='Req. J0 (Base)')
        ax.plot(longitudes_hombro * 1000, t_j1, 'b-', linewidth=2, label='Req. J1 (Hombro)')
        ax.plot(longitudes_hombro * 1000, t_j2, 'r-', linewidth=2, label='Req. J2 (Codo)')
        ax.plot(longitudes_hombro * 1000, t_j3, 'g-', linewidth=2, label='Req. J3 (Muñeca Pitch)')
        ax.plot(longitudes_hombro * 1000, t_j4, 'm-', linewidth=2, label='Req. J4 (Muñeca Roll)')
        
        nombres = ['J0', 'J1', 'J2', 'J3', 'J4']
        colores = ['grey', 'cyan', 'orange', 'lightgreen', 'purple']
        for i in range(5):
            t_base = robot_template[i].get('t_motor', robot_template[i].get('t_rated', 0.0))
            ax.axhline(y=t_base, color=colores[i], linestyle='--', alpha=0.5, label=f'Límite {nombres[i]} ({t_base:.1f} Nm)')

        max_torque_global = max(max_torque_global, max(t_j1))
        
        ax.set_title(f'Material: {material}')
        ax.set_xlabel('Longitud Hombro ($L$) [mm]')
        if idx == 0: ax.set_ylabel('Torque Estático REQUERIDO [Nm]')
        ax.grid(True, linestyle=':')
        ax.legend(fontsize=7, loc='upper left')
        
        # --- GRÁFICA 2: DEFLEXIÓN Y CARGAS M4 ---
        ax_defl = axes2[0, idx]
        ax_fuerza = axes2[1, idx]
        
        ax_defl.plot(longitudes_hombro * 1000, deflexion_punta, color='purple', linewidth=2)
        ax_defl.set_title(f'Material: {material}')
        ax_defl.grid(True, linestyle=':')
        if idx == 0: ax_defl.set_ylabel('Deflexión en la Punta [mm]')
        
        ax_fuerza.plot(longitudes_hombro * 1000, f_axial_j1, 'r-', label='Fuerza Axial M4 (Arrastre)')
        ax_fuerza.plot(longitudes_hombro * 1000, f_cort_j1, 'b--', label='Fuerza Cortante M4 (Cizalla)')
        
        if material != 'Aluminio':
            ax_fuerza.axhline(y=200, color='red', linestyle=':', alpha=0.7, label='Límite Aprox. PETG/PLA (200N)')
            
        ax_fuerza.grid(True, linestyle=':')
        ax_fuerza.set_xlabel('Longitud Hombro ($L$) [mm]')
        if idx == 0: ax_fuerza.set_ylabel('Fuerza por Tornillo J1 [N]')
        ax_fuerza.legend(fontsize=8, loc='upper left')

    for ax in axes:
        ax.set_ylim(-1, max_torque_global * 1.25)

    fig.suptitle(f'Efecto de Geometría en 5 DOF vs Envergadura\n(Herramienta: {m_tool*1000}g | Carga Útil: {m_load*1000}g)', fontsize=14)
    fig.tight_layout()
    
    fig2.suptitle(f'Análisis Mecánico: Deflexión del Brazo 5 DOF y Cargas en Tornillos (J1)', fontsize=14)
    fig2.tight_layout()
    
    plt.show()

if __name__ == "__main__":
    L_ejemplo = 0.3    
    
    # --- PARÁMETROS GEOMÉTRICOS MODIFICABLES A GUSTO ---
    b_val = 0.040  # 30 mm
    h_val = 0.050  # 50 mm
    
    # --- ESPECIFICACIONES DE MOTORES (Valores directos en Nm) ---
    # J0 (Base)   -> TS4230Y5D: 15.8 Nm | Masa: 520g
    # J1 (Hombro) -> TS4260Y5D: 31.6 Nm | Masa: 520g 
    # J2 (Codo)   -> TS4230Y5D: 15.8 Nm | Masa: 520g
    # J3 (Muñeca) -> TS4230Y4D: 11.2 Nm | Masa: 450g
    # J4 (Muñeca) -> TS4230Y4D: 11.2 Nm | Masa: 450g
    
    robot_def_ejemplo = [
        {'axis': 'z', 'offset': [0.00475, 0.0, 0.132], 'm_servo': 0.520, 'm_link': calc_link_mass('PLA', 0.150, b_val, h_val), 'com_link': [0, 0, 0.150/2], 't_rated': 15.8, 'b': b_val, 'h': h_val},
        {'axis': 'y', 'offset': [L_ejemplo, -0.027, 0.0], 'm_servo': 0.520, 'm_link': calc_link_mass('PLA', L_ejemplo, b_val, h_val), 'com_link': [L_ejemplo/2, 0, 0], 't_rated': 31.6, 'b': b_val, 'h': h_val},
        {'axis': 'y', 'offset': [0.5*L_ejemplo, -0.030, 0.0], 'm_servo': 0.520, 'm_link': calc_link_mass('PLA', 0.5*L_ejemplo, b_val, h_val), 'com_link': [0.5*L_ejemplo/2, 0, 0], 't_rated': 15.8, 'b': b_val, 'h': h_val},
        {'axis': 'y', 'offset': [0.3*L_ejemplo, -0.003, 0.0], 'm_servo': 0.450, 'm_link': calc_link_mass('PLA', 0.3*L_ejemplo, b_val, h_val), 'com_link': [0.3*L_ejemplo/2, 0, 0], 't_rated': 11.2, 'b': b_val, 'h': h_val},
        {'axis': 'x', 'offset': [0.2*L_ejemplo, 0.0, 0.0], 'm_servo': 0.450, 'm_link': calc_link_mass('PLA', 0.2*L_ejemplo, b_val, h_val), 'com_link': [0.2*L_ejemplo/2, 0, 0], 't_rated': 11.2, 'b': b_val, 'h': h_val}
    ]
    
    arm_test = RobotDOF_3D(joints=robot_def_ejemplo, alpha_target=5.0, m_load=0.350, m_tool=0.150, material='PLA')
    arm_test.analyze_pose([0.0, 0.0, 0.0, 0.0, 0.0], show_plot=True)
    
    evaluar_barrido_multi_material(robot_template=robot_def_ejemplo, materiales=['PLA', 'PETG', 'Aluminio'], m_load=0.2, m_tool=0.150, alpha_target=5.0)