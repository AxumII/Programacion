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
# 2. Propiedades de Materiales
# ==========================================
DENSITIES = {'PLA': 1250.0, 'ABS': 1040.0, 'Aluminio': 2700.0}

def get_material_properties(material, b, h):
    area_m2 = b * h
    densidad_ef = DENSITIES['Aluminio'] if material == 'Aluminio' else DENSITIES[material] * 0.30
    return area_m2, densidad_ef

def calc_link_mass(material, length_m):
    area_m2 = (0.008 * 0.040) if material == 'Aluminio' else (0.030 * 0.050)
    densidad_efectiva = DENSITIES['Aluminio'] if material == 'Aluminio' else DENSITIES[material] * 0.30 
    return area_m2 * length_m * densidad_efectiva

# ==========================================
# 3. Clase Principal (Física y Cinemática)
# ==========================================
class RobotDOF_3D:
    def __init__(self, joints, alpha_target, m_load=0.0, m_tool=0.0):
        self.joints = joints
        self.N = len(joints)
        self.alpha_target = alpha_target
        self.m_load = m_load
        self.m_tool = m_tool
        self.m_tip_total = m_load + m_tool 
        self.g = 9.81
        self.kgcm2Nm = 0.0980665 
        self.Nm2kgcm = 10.197    
        self.F_g = np.array([0, 0, -self.g])

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
        
        motor_positions = []
        for k, joint in enumerate(self.joints):
            mount_idx = joint.get('motor_mount_joint', k) 
            mount_offset = joint.get('motor_mount_offset', [0, 0, 0])
            T_mount = T_matrices[mount_idx]
            pos = (T_mount @ translation(mount_offset))[:3, 3]
            motor_positions.append(pos)

        t_static = np.zeros(self.N)
        t_dynamic_target = np.zeros(self.N)
        inertia_array = np.zeros(self.N)
        alpha_max_permitida = np.zeros(self.N)
        
        for i in range(self.N):
            tau_3d_static = np.zeros(3)
            inertia_i = 0.0
            P_axis = positions[i]
            u_axis = z_axes[i]
            
            for j in range(i, self.N):
                r_vec_com = com_positions[j] - P_axis
                tau_3d_static += np.cross(r_vec_com, self.joints[j]['m_link'] * self.F_g)
                r_parallel_com = np.dot(r_vec_com, u_axis) * u_axis
                r_perp_com = np.linalg.norm(r_vec_com - r_parallel_com)
                inertia_i += self.joints[j]['m_link'] * (r_perp_com**2)
                
            for k, joint in enumerate(self.joints):
                mount_idx = joint.get('motor_mount_joint', k)
                if mount_idx >= i:
                    m_mot = joint.get('m_motor', joint.get('m_servo', 0.0))
                    r_vec_mot = motor_positions[k] - P_axis
                    tau_3d_static += np.cross(r_vec_mot, m_mot * self.F_g)
                    r_parallel_mot = np.dot(r_vec_mot, u_axis) * u_axis
                    r_perp_mot = np.linalg.norm(r_vec_mot - r_parallel_mot)
                    inertia_i += m_mot * (r_perp_mot**2)
            
            if self.m_tip_total > 0:
                r_vec_load = p_tip - P_axis
                tau_3d_static += np.cross(r_vec_load, self.m_tip_total * self.F_g)
                r_parallel_load = np.dot(r_vec_load, u_axis) * u_axis
                r_perp_load = np.linalg.norm(r_vec_load - r_parallel_load)
                inertia_i += self.m_tip_total * (r_perp_load**2)
            
            t_static[i] = abs(np.dot(tau_3d_static, u_axis))
            t_dynamic_target[i] = inertia_i * self.alpha_target
            
            ratio = self.joints[i].get('pulley_ratio', 1.0)
            eff = self.joints[i].get('pulley_eff', 1.0)
            t_mot_base = self.joints[i].get('t_motor', self.joints[i].get('t_rated', 0.0))
            t_rated_joint_Nm = t_mot_base * ratio * eff * self.kgcm2Nm
            
            t_margin_static = t_rated_joint_Nm - t_static[i]
            alpha_max_permitida[i] = (t_margin_static / inertia_i) if (t_margin_static > 0 and inertia_i > 0) else 0.0
                
        return t_static, t_dynamic_target, inertia_array, alpha_max_permitida, motor_positions

    def analyze_pose(self, thetas_deg, show_plot=True, title="Visualización"):
        thetas = np.radians(thetas_deg)
        t_static, t_dyn_target, inertias, alphas, motor_pos = self.calculate_torques_and_limits(thetas)
        
        metrics = []
        for i in range(self.N):
            ratio = self.joints[i].get('pulley_ratio', 1.0)
            eff = self.joints[i].get('pulley_eff', 1.0)
            t_mot_base = self.joints[i].get('t_motor', self.joints[i].get('t_rated', 0.0))
            t_joint_capacity = t_mot_base * ratio * eff
            
            t_total_kgcm = (t_static[i] + t_dyn_target[i]) * self.Nm2kgcm
            fs = t_joint_capacity / t_total_kgcm if t_total_kgcm > 0 else float('inf')
            ubicacion = self.joints[i].get('motor_mount_joint', i)
            
            metrics.append({
                "Joint (Eje)": f"J{i} ({self.joints[i]['axis'].upper()})",
                "Motor En": f"J{ubicacion}",
                "Polea": f"{ratio}:1",
                "Capacidad [kgcm]": round(t_joint_capacity, 1),
                "T. Requerido [kgcm]": round(t_total_kgcm, 2),
                "Acel MAX [rad/s²]": round(alphas[i], 2),
                "Factor Seg": round(fs, 2)
            })
            
        df = pd.DataFrame(metrics).set_index("Joint (Eje)")
        print(f"\n" + "="*85)
        print(f"{title.upper()} | Herramienta: {self.m_tool*1000}g | Carga: {self.m_load*1000}g")
        print("="*85)
        print(df.to_string())

        if show_plot:
            self._plot_3d(thetas, motor_pos, title)

    def _plot_3d(self, thetas, motor_positions, title):
        positions, z_axes, com_positions, p_tip, _ = self.forward_kinematics(thetas)
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        xs, ys, zs = positions[:, 0], positions[:, 1], positions[:, 2]
        
        ax.plot(np.append(xs, p_tip[0]), np.append(ys, p_tip[1]), np.append(zs, p_tip[2]), 
                'ko-', linewidth=5, markersize=8, label='Estructura')
        
        for i in range(self.N):
            ax.quiver(xs[i], ys[i], zs[i], z_axes[i,0]*0.06, z_axes[i,1]*0.06, z_axes[i,2]*0.06, color='green', linewidth=2)
            ax.text(xs[i], ys[i], zs[i] + 0.03, f'J{i}', fontweight='bold')
            
            mx, my, mz = motor_positions[i]
            ax.scatter(mx, my, mz, color='cyan', s=150, marker='s', zorder=6)
            
            if self.joints[i].get('motor_mount_joint', i) != i:
                ax.plot([mx, xs[i]], [my, ys[i]], [mz, zs[i]], color='cyan', linestyle='--', linewidth=2)
                ax.text(mx, my, mz-0.02, f'Mot J{i}', color='darkcyan')
            else:
                ax.text(mx+0.02, my, mz, f'Mot J{i}', color='darkcyan')

        if self.m_tip_total > 0:
            ax.scatter(p_tip[0], p_tip[1], p_tip[2], color='blue', s=200, marker='D', label='Punta (Carga+Herr)')

        ax.set_title(title)
        ax.set_xlim([-0.6, 0.6]); ax.set_ylim([-0.6, 0.6]); ax.set_zlim([-0.1, 0.7])
        ax.set_xlabel('X [m]'); ax.set_ylabel('Y [m]'); ax.set_zlabel('Z [m]')
        ax.legend()
        plt.show()

# ==========================================
# 4. Análisis de Barrido Continuo DINÁMICO
# ==========================================
def evaluar_barrido_multi_material(robot_template, materiales=['PLA', 'ABS', 'Aluminio'], m_load=0.0, m_tool=0.150, alpha_target=5.0, titulo="Análisis Paramétrico"):
    L1 = robot_template[0]['offset'][2] 
    longitudes_hombro = np.linspace(0.180, 0.450, 100)
    fig, axes = plt.subplots(1, len(materiales), figsize=(18, 6), sharey=True)
    if len(materiales) == 1: axes = [axes]
    
    max_torque_global = 0 
        
    for idx, material in enumerate(materiales):
        t_j0, t_j1, t_j2, t_j3 = [], [], [], []
        b, h = (0.008, 0.040) if material == 'Aluminio' else (0.030, 0.050)
        area, den_ef = get_material_properties(material, b, h)
        
        for L_hombro in longitudes_hombro:
            robot_def = copy.deepcopy(robot_template)
            
            L2 = L_hombro
            L3 = 0.7 * L_hombro
            L4 = 0.3 * L_hombro
            
            robot_def[1]['offset'][0] = L2
            robot_def[1]['m_link'] = area * L2 * den_ef
            robot_def[1]['com_link'][0] = L2/2
            
            robot_def[2]['offset'][0] = L3
            robot_def[2]['m_link'] = area * L3 * den_ef
            robot_def[2]['com_link'][0] = L3/2
            
            robot_def[3]['offset'][0] = L4
            robot_def[3]['m_link'] = area * L4 * den_ef
            robot_def[3]['com_link'][0] = L4/2
            
            arm = RobotDOF_3D(joints=robot_def, alpha_target=alpha_target, m_load=m_load, m_tool=m_tool)
            thetas_max = np.radians([0, 0, 0, 0])
            t_static, _, _, _, _ = arm.calculate_torques_and_limits(thetas_max)
            
            t_j0.append(t_static[0] * arm.Nm2kgcm)
            t_j1.append(t_static[1] * arm.Nm2kgcm)
            t_j2.append(t_static[2] * arm.Nm2kgcm)
            t_j3.append(t_static[3] * arm.Nm2kgcm)

        ax = axes[idx]
        ax.plot(longitudes_hombro * 1000, t_j0, 'k:', linewidth=2, label='Req. J0 (Base)')
        ax.plot(longitudes_hombro * 1000, t_j1, 'b-', linewidth=2, label='Req. J1 (Hombro)')
        ax.plot(longitudes_hombro * 1000, t_j2, 'r-', linewidth=2, label='Req. J2 (Codo)')
        ax.plot(longitudes_hombro * 1000, t_j3, 'g-', linewidth=2, label='Req. J3 (Muñeca)')
        
        nombres = ['J0', 'J1', 'J2', 'J3']
        colores = ['grey', 'cyan', 'orange', 'lightgreen']
        for i in range(4):
            t_base = robot_template[i].get('t_motor', robot_template[i].get('t_rated', 0.0))
            cap = t_base * robot_template[i].get('pulley_ratio', 1.0) * robot_template[i].get('pulley_eff', 1.0)
            ax.axhline(y=cap, color=colores[i], linestyle='--', alpha=0.5, label=f'Límite {nombres[i]} ({cap:.1f} kgcm)')

        max_torque_global = max(max_torque_global, max(t_j1))
        
        ax.set_title(f'Material: {material}')
        ax.set_xlabel('Longitud Hombro ($L$) [mm]')
        if idx == 0: ax.set_ylabel('Torque Estático  [kgcm]')
        ax.grid(True, linestyle=':')
        ax.legend(fontsize=7, loc='upper left')
        
    for ax in axes:
        ax.set_ylim(-2, max_torque_global * 1.25)

    plt.suptitle(titulo, fontsize=14)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    L_ejemplo = 0.250    
    
    # ==========================================
    # CASO 1: SIN POLEAS (Accionamiento Directo)
    # Todos los motores en sus respectivas articulaciones
    # ==========================================
    robot_def_sin_poleas = [
        {'axis': 'z', 'offset': [0.00475, 0.0, 0.132], 'm_servo': 0.500, 'm_link': calc_link_mass('PLA', 0.150), 'com_link': [0, 0, 0.150/2], 't_rated': 15.0, 'motor_mount_joint': 0, 'pulley_ratio': 1.0, 'pulley_eff': 1.0},
        {'axis': 'y', 'offset': [L_ejemplo, -0.027, 0.0], 'm_servo': 0.500, 'm_link': calc_link_mass('PLA', L_ejemplo), 'com_link': [L_ejemplo/2, 0, 0], 't_rated': 50.0, 'motor_mount_joint': 1, 'pulley_ratio': 1.0, 'pulley_eff': 1.0},
        {'axis': 'y', 'offset': [0.7*L_ejemplo, -0.030, 0.0], 'm_servo': 0.300, 'm_link': calc_link_mass('PLA', 0.7*L_ejemplo), 'com_link': [0.7*L_ejemplo/2, 0, 0], 't_rated': 25.0, 'motor_mount_joint': 2, 'pulley_ratio': 1.0, 'pulley_eff': 1.0}, 
        {'axis': 'y', 'offset': [0.3*L_ejemplo, -0.003, 0.0], 'm_servo': 0.300, 'm_link': calc_link_mass('PLA', 0.3*L_ejemplo), 'com_link': [0.3*L_ejemplo/2, 0, 0], 't_rated': 15.0, 'motor_mount_joint': 3, 'pulley_ratio': 1.0, 'pulley_eff': 1.0}  
    ]

    arm_sin_poleas = RobotDOF_3D(joints=robot_def_sin_poleas, alpha_target=5.0, m_load=0.2, m_tool=0.150)
    arm_sin_poleas.analyze_pose([0.0, 0.0, 0.0, 0.0], show_plot=True, title="Caso 1: Accionamiento Directo (Sin Poleas)")
    
    # ==========================================
    # CASO 2: CON POLEAS EN J2 y J3
    # El motor de J2 se reubica en J1, y el de J3 en J2
    # ==========================================
    robot_def_con_poleas = copy.deepcopy(robot_def_sin_poleas)
    robot_def_con_poleas[2]['motor_mount_joint'] = 1  # Motor de J2 ubicado en el hombro (J1)
    robot_def_con_poleas[2]['pulley_ratio'] = 2.0     # Ejemplo: Ganancia mecánica de la polea
    robot_def_con_poleas[3]['motor_mount_joint'] = 2  # Motor de J3 ubicado en el codo (J2)

    arm_con_poleas = RobotDOF_3D(joints=robot_def_con_poleas, alpha_target=5.0, m_load=0.2, m_tool=0.150)
    arm_con_poleas.analyze_pose([0.0, 0.0, 0.0, 0.0], show_plot=True, title="Caso 2: Sistema Optimizado (Con Poleas)")

    # Gráficas de barrido
    evaluar_barrido_multi_material(robot_template=robot_def_sin_poleas, m_load=0.2, m_tool=0.150, titulo="Barrido Paramétrico - CASO 1 (Sin Poleas)")
    evaluar_barrido_multi_material(robot_template=robot_def_con_poleas, m_load=0.2, m_tool=0.150, titulo="Barrido Paramétrico - CASO 2 (Con Poleas)")