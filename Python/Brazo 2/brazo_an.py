import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import itertools
import copy
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
try:
    from scipy.spatial import ConvexHull, QhullError
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

# ==========================================
# 1. CLASE MOTOR PASO A PASO
# ==========================================
class StepperMotor:
    def __init__(self, name, I_ph, R, L, T_H, J_m, m_motor, V=24, N_r=50, k_eddy=0.0005):
        self.name = name
        self.I_ph = I_ph
        self.R = R
        self.L = L
        self.T_H = T_H
        self.J_m = J_m
        self.m_motor = m_motor  # Masa física del motor (kg)
        self.V = V
        self.N_r = N_r
        self.k_eddy = k_eddy
        self.Kt = self.T_H / self.I_ph
        self.d_theta = np.pi / (2 * self.N_r)
        self.apply_transmission(ratio=1.0, eff=1.0, backlash_arcmin=0.0, J_trans=0.0)

    def apply_transmission(self, ratio, eff, backlash_arcmin=0.0, J_trans=0.0):
        self.ratio = ratio
        self.eff = eff
        self.backlash_rad = np.radians(backlash_arcmin / 60.0)
        self.J_trans = J_trans
        return self

    def get_Z(self, w_m):
        return np.sqrt(self.R**2 + (self.N_r * w_m * self.L)**2)
        
    def get_I_env(self, w_m):
        return np.maximum(0, (self.V - (self.Kt * w_m)) / self.get_Z(w_m))
        
    def get_I_act(self, w_m):
        return np.minimum(self.I_ph, self.get_I_env(w_m))
        
    def get_T_po(self, w_m):
        return np.maximum(0, (self.Kt * self.get_I_act(w_m)) - (self.k_eddy * w_m))
        
    def get_Tout_po(self, w_m):
        return self.get_T_po(w_m * self.ratio) * self.ratio * self.eff

# ==========================================
# 2. HELPER CINEMÁTICO: MATRIZ DH
# ==========================================
def dh_matrix(d, theta, a, alpha):
    c_t, s_t = np.cos(theta), np.sin(theta)
    c_a, s_a = np.cos(alpha), np.sin(alpha)
    return np.array([
        [c_t, -s_t*c_a,  s_t*s_a, a*c_t],
        [s_t,  c_t*c_a, -c_t*s_a, a*s_t],
        [0,    s_a,      c_a,     d],
        [0,    0,        0,       1]
    ])

# ==========================================
# 3. PROPIEDADES DE MATERIALES
# ==========================================
DENSITIES = {'PLA': 1250.0, 'PETG': 1270.0, 'ABS': 1040.0, 'Aluminio': 2700.0}

def get_material_mass(material, length_m):
    # Aluminio: Perfil estructural estándar 20x20 (~0.45 kg/m -> Área equivalente sólida 0.00017 m2)
    area_aluminio = 0.00017
    # Plásticos FDM: Perfil volumétrico robusto de 40x40mm con 40% de densidad de relleno (infill + perimetros)
    area_plastico = 0.0016
    factor_relleno = 0.40
    
    if material == 'Aluminio':
        return area_aluminio * length_m * DENSITIES['Aluminio']
    else:
        return area_plastico * length_m * (DENSITIES[material] * factor_relleno)

# ==========================================
# 4. CLASE ROBOT (Cinemática y Dinámica)
# ==========================================
class RobotDOF_3D:
    def __init__(self, dh_params, alpha_target, m_load=0.0, m_tool=0.0):
        self.dh_params = dh_params
        self.N = len(dh_params)
        self.alpha_target = alpha_target
        self.m_load = m_load
        self.m_tool = m_tool
        self.m_tip_total = m_load + m_tool 
        self.g = 9.81
        self.F_g = np.array([0, 0, -self.g])

    def forward_kinematics(self, thetas):
        T = np.eye(4)
        positions = [T[:3, 3]]
        z_axes = [T[:3, 2]]
        com_positions = []
        
        for i, p in enumerate(self.dh_params):
            A_i = dh_matrix(p['d'], thetas[i] + p.get('offset_theta', 0), p['a'], p['alpha'])
            T = T @ A_i
            # Aproximación del centro de masa del eslabón (mitad geométrica en X o Z)
            offset_x = -p['a']/2 if p['a'] != 0 else 0
            offset_z = -p['d']/2 if p['d'] != 0 and p['a'] == 0 else 0
            T_com = T @ np.array([[1,0,0, offset_x], [0,1,0,0], [0,0,1, offset_z], [0,0,0,1]])
            
            com_positions.append(T_com[:3, 3])
            positions.append(T[:3, 3])
            z_axes.append(T[:3, 2])
            
        p_tip = positions[-1]
        return np.array(positions[:-1]), np.array(z_axes[:-1]), np.array(com_positions), p_tip

    def jacobian(self, thetas):
        positions, z_axes, _, p_tip = self.forward_kinematics(thetas)
        J_v = np.zeros((3, self.N))
        J_w = np.zeros((3, self.N))
        for i in range(self.N):
            r_vec = p_tip - positions[i]
            J_v[:, i] = np.cross(z_axes[i], r_vec)
            J_w[:, i] = z_axes[i]
        return np.vstack((J_v, J_w))

    def compute_dynamics(self, thetas):
        positions, z_axes, com_positions, p_tip = self.forward_kinematics(thetas)
        t_static_joint = np.zeros(self.N)
        t_total_joint = np.zeros(self.N)
        t_req_motor = np.zeros(self.N)
        
        for i in range(self.N):
            tau_3d_grav = np.zeros(3)
            I_L = 0.0
            u_axis = z_axes[i]
            P_axis = positions[i]
            
            for j in range(i, self.N):
                m_link = self.dh_params[j]['m_link']
                L_link = self.dh_params[j]['L_link']
                mot = self.dh_params[j]['motor']
                
                # Efecto Gravitacional y Masa del Eslabón
                r_vec_link = com_positions[j] - P_axis
                tau_3d_grav += np.cross(r_vec_link, m_link * self.F_g)
                
                # Efecto Gravitacional del Motor físico ubicado en la articulación J
                r_vec_mot = positions[j] - P_axis
                tau_3d_grav += np.cross(r_vec_mot, mot.m_motor * self.F_g)
                
                # Inercias utilizando el Teorema de Ejes Paralelos (Steiner)
                r_perp_link = np.linalg.norm(r_vec_link - (np.dot(r_vec_link, u_axis) * u_axis))
                r_perp_mot  = np.linalg.norm(r_vec_mot - (np.dot(r_vec_mot, u_axis) * u_axis))
                I_local = (1/12) * m_link * (L_link**2)
                I_L += I_local + (m_link * (r_perp_link**2)) + (mot.m_motor * (r_perp_mot**2))
            
            # Efecto del Payload Final
            if self.m_tip_total > 0:
                r_tip = p_tip - P_axis
                tau_3d_grav += np.cross(r_tip, self.m_tip_total * self.F_g)
                r_perp_tip = np.linalg.norm(r_tip - (np.dot(r_tip, u_axis) * u_axis))
                I_L += self.m_tip_total * (r_perp_tip**2)
            
            # Torque Estático y Dinámico en la ARTICULACIÓN
            t_static_joint[i] = abs(np.dot(tau_3d_grav, u_axis))
            t_total_joint[i] = t_static_joint[i] + (I_L * self.alpha_target)
            
            # Reflexión del requerimiento hacia el EJE DEL MOTOR (Antes de la caja)
            motor = self.dh_params[i]['motor']
            alpha_m = self.alpha_target * motor.ratio
            inercia_propia_motor = (motor.J_m + motor.J_trans) * alpha_m
            carga_reflejada = t_total_joint[i] / (motor.ratio * motor.eff)
            
            t_req_motor[i] = inercia_propia_motor + carga_reflejada
            
        return t_static_joint, t_total_joint, t_req_motor

    def analyze_pose(self, thetas_deg, title_prefix="", nominal_rpm_out=5.0):
        thetas = np.radians(thetas_deg)
        t_static_joint, t_total_joint, t_req_motor = self.compute_dynamics(thetas)
        w_eval_motor = nominal_rpm_out * (np.pi / 30) * self.dh_params[0]['motor'].ratio
        
        # Propagación del Jacobiano para nubes de Backlash
        J = self.jacobian(thetas)[:3, :] 
        backlash_limits = [[-p['motor'].backlash_rad, p['motor'].backlash_rad] for p in self.dh_params]
        combinations = np.array(list(itertools.product(*backlash_limits)))
        _, _, _, p_tip = self.forward_kinematics(thetas)
        error_points = (J @ combinations.T).T + p_tip 
        max_err_mm = np.max(np.linalg.norm(error_points - p_tip, axis=1)) * 1000
        
        print(f"\n{'='*115}")
        print(f"{title_prefix} | TABLA DINÁMICA DE TORQUES (Vel. Efector: {nominal_rpm_out} RPM) | Error Max Posición: {max_err_mm:.2f} mm")
        print(f"Tool (Herramienta): {self.m_tool*1000}g | Payload (Carga Útil): {self.m_load*1000}g")
        print(f"{'='*115}")
        
        metrics = []
        for i in range(self.N):
            motor = self.dh_params[i]['motor']
            # Capacidad pura del motor a la velocidad requerida (antes de la caja)
            t_cap_motor = motor.get_T_po(w_eval_motor)
            fs = t_cap_motor / t_req_motor[i] if t_req_motor[i] > 0 else float('inf')
            
            metrics.append({
                "Eje": f"J{i} ({self.dh_params[i].get('axis_label', '?')})",
                "Motor Usado": motor.name,
                "T. Estático Articulación (Nm)": round(t_static_joint[i], 2),
                "T. Total Articulación (Nm)": round(t_total_joint[i], 2),
                "T. Req Eje Motor (Nm)": round(t_req_motor[i], 3),
                "T. Max Eje Motor (Nm)": round(t_cap_motor, 3),
                "Factor Seg.": round(fs, 2)
            })
        
        df = pd.DataFrame(metrics).set_index("Eje")
        print(df.to_string())
        self._plot_robot_and_error(thetas, title_prefix, error_points, max_err_mm)

    def _plot_robot_and_error(self, thetas, title_prefix, error_points, max_err_mm):
        positions, z_axes, _, p_tip = self.forward_kinematics(thetas)
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        xs = np.append(positions[:, 0], p_tip[0])
        ys = np.append(positions[:, 1], p_tip[1])
        zs = np.append(positions[:, 2], p_tip[2])
        ax.plot(xs, ys, zs, 'ko-', linewidth=4, markersize=6, label='Eslabones')
        
        for i in range(self.N):
            ax.quiver(positions[i,0], positions[i,1], positions[i,2], 
                      z_axes[i,0]*0.08, z_axes[i,1]*0.08, z_axes[i,2]*0.08, color='g', linewidth=2)
            ax.text(positions[i,0], positions[i,1], positions[i,2]+0.05, f'J{i}', fontweight='bold')
            
        ax.scatter(error_points[:,0], error_points[:,1], error_points[:,2], color='red', s=10, label='Nube de Error')
        
        if HAS_SCIPY and len(error_points) > 3:
            try:
                # Ruido imperceptible para forzar un volumen 3D en poses planas (Evita el QhullError)
                jitter = error_points + np.random.normal(0, 1e-9, error_points.shape)
                hull = ConvexHull(jitter)
                for s in hull.simplices:
                    tri = Poly3DCollection([jitter[s]])
                    tri.set_color('red'); tri.set_alpha(0.2)
                    ax.add_collection3d(tri)
                ax.set_title(f'{title_prefix}\nError Máx Cartesiano: ±{max_err_mm:.2f} mm', fontsize=12)
            except QhullError:
                pass
        
        ax.set_xlim([-0.6, 0.6]); ax.set_ylim([-0.6, 0.6]); ax.set_zlim([0, 0.8])
        ax.set_xlabel('X [m]'); ax.set_ylabel('Y [m]'); ax.set_zlabel('Z [m]')
        ax.legend()
        plt.show()

# ==========================================
# 5. GENERADORES DE CONFIGURACIÓN Y BARRIDO
# ==========================================
def get_4dof_config(L, mot_heavy, mot_light, material):
    return [
        {'d': 0.5*L, 'a': 0.0,   'alpha': np.pi/2, 'L_link': 0.5*L, 'm_link': get_material_mass(material, 0.5*L), 'motor': mot_heavy, 'axis_label': 'Yaw Z'},
        {'d': 0.0,   'a': L,     'alpha': 0.0,     'L_link': L,     'm_link': get_material_mass(material, L),     'motor': mot_heavy, 'axis_label': 'Pitch Y'},
        {'d': 0.0,   'a': 0.7*L, 'alpha': 0.0,     'L_link': 0.7*L, 'm_link': get_material_mass(material, 0.7*L), 'motor': mot_heavy, 'axis_label': 'Pitch Y'},
        {'d': 0.0,   'a': 0.3*L, 'alpha': 0.0,     'L_link': 0.3*L, 'm_link': get_material_mass(material, 0.3*L), 'motor': mot_light, 'axis_label': 'Pitch Y'}
    ]

def get_5dof_config(L, mot_heavy, mot_light, material):
    return [
        {'d': 0.5*L, 'a': 0.0,   'alpha': np.pi/2, 'L_link': 0.5*L, 'm_link': get_material_mass(material, 0.5*L), 'motor': mot_heavy, 'axis_label': 'Yaw Z'},
        {'d': 0.0,   'a': L,     'alpha': 0.0,     'L_link': L,     'm_link': get_material_mass(material, L),     'motor': mot_heavy, 'axis_label': 'Pitch Y'},
        {'d': 0.0,   'a': 0.7*L, 'alpha': 0.0,     'L_link': 0.7*L, 'm_link': get_material_mass(material, 0.7*L), 'motor': mot_heavy, 'axis_label': 'Pitch Y'},
        {'d': 0.0,   'a': 0.0,   'alpha': np.pi/2, 'L_link': 0.3*L, 'm_link': get_material_mass(material, 0.3*L), 'motor': mot_light, 'axis_label': 'Pitch Y'}, 
        {'d': 0.05,  'a': 0.0,   'alpha': 0.0,     'L_link': 0.05,  'm_link': get_material_mass(material, 0.05),  'motor': mot_light, 'axis_label': 'Roll X'} 
    ]

def plot_parametric_sweep(mot_heavy, mot_light, alpha_target=5.0, m_load=0.2, m_tool=0.150, dof=4):
    materiales = ['PLA', 'PETG', 'ABS', 'Aluminio']
    longitudes = np.linspace(0.200, 0.400, 50)
    fig, axes = plt.subplots(2, 2, figsize=(16, 11), sharey=True)
    axes = axes.flatten()
    
    # Velocidad a nivel motor = 5 RPM * Ratio (30) = 150 RPM en la bobina.
    w_eval_motor = 5.0 * (np.pi / 30) * mot_heavy.ratio
    max_t_req = 0
    
    line_styles = ['k:', 'b-', 'r-', 'g-', 'm-']
    limit_colors = ['cyan', 'orange']
    joint_names = ['J0 (Base)', 'J1 (Hombro)', 'J2 (Codo)', 'J3 (Muñeca Pitch)', 'J4 (Muñeca Roll)']
    
    for idx, material in enumerate(materiales):
        t_req_all = [[] for _ in range(dof)]
        
        for L in longitudes:
            dh_test = get_4dof_config(L, mot_heavy, mot_light, material) if dof == 4 else get_5dof_config(L, mot_heavy, mot_light, material)
            brazo_test = RobotDOF_3D(dh_test, alpha_target, m_load, m_tool)
            # Evaluar en postura gravitacional más crítica (brazo totalmente horizontal)
            _, t_total_joint, _ = brazo_test.compute_dynamics(np.zeros(dof))
            
            for i in range(dof):
                t_req_all[i].append(t_total_joint[i])
                
        ax = axes[idx]
        for i in range(dof):
            ax.plot(longitudes * 1000, t_req_all[i], line_styles[i], linewidth=2.5, label=f'Req. {joint_names[i]}')
            max_t_req = max(max_t_req, max(t_req_all[i]))
            
        motores_unicos = []
        dh_test = get_4dof_config(L, mot_heavy, mot_light, material) if dof == 4 else get_5dof_config(L, mot_heavy, mot_light, material)
            
        for i, mot in enumerate([mot_heavy, mot_light]):
            # Trazar el torque MÁXIMO disponible en la articulación (T_motor * ratio * eff)
            limite_articulacion = mot.get_Tout_po(w_eval_motor / mot.ratio)
            ax.axhline(limite_articulacion, color=limit_colors[i], linestyle='--', linewidth=2, label=f'Capacidad {mot.name} ({limite_articulacion:.1f} Nm)')
        
        ax.set_title(f'Material: {material}', fontsize=12)
        ax.set_xlabel('Longitud Base $L$ (mm)')
        if idx in [0, 2]: ax.set_ylabel('Torque en Articulación (Nm)')
        ax.grid(True, linestyle=':')
        ax.legend(fontsize=8, loc='upper left')
        
    for ax in axes:
        ax.set_ylim(0, max_t_req * 1.5)

    plt.suptitle(f"Barrido Paramétrico {dof}-DOF: Torque en Articulaciones vs Escalamiento (0.2m - 0.4m)\nCarga Útil: {m_load*1000}g | Herramienta: {m_tool*1000}g", fontsize=15, fontweight='bold')
    plt.tight_layout()
    plt.show()

# ==========================================
# EJECUCIÓN PRINCIPAL
# ==========================================
if __name__ == "__main__":
    
    # 1. Definición estricta de motores TS (Con masas físicas reales)
    mot_TS4230M5D = StepperMotor("TS4230M5D", I_ph=2.0, R=1.65, L=0.0036, T_H=0.52, J_m=54e-7, m_motor=0.50)
    mot_TS4230M5D.apply_transmission(ratio=30.0, eff=0.96, backlash_arcmin=3.0, J_trans=40e-7)

    mot_TS4230M2D = StepperMotor("TS4230M2D", I_ph=1.0, R=2.3, L=0.0031, T_H=0.12, J_m=54e-7, m_motor=0.29)
    mot_TS4230M2D.apply_transmission(ratio=30.0, eff=0.96, backlash_arcmin=3.0, J_trans=20e-7)

    # 2. Análisis Estático Cartesiano L = 0.25m
    L_eval = 0.30
    m_carga_util = 0.350 # 200g
    m_herramienta = 0.150 # 150g
    
    # Caso 4-DOF
    dh_4dof = get_4dof_config(L_eval, mot_TS4230M5D, mot_TS4230M2D, 'PLA')
    brazo_4 = RobotDOF_3D(dh_4dof, alpha_target=5.0, m_load=m_carga_util, m_tool=m_herramienta)
    brazo_4.analyze_pose(thetas_deg=[0, 0, 0, 0], title_prefix="ANÁLISIS 4-DOF (L=250mm)")

    # Caso 5-DOF
    dh_5dof = get_5dof_config(L_eval, mot_TS4230M5D, mot_TS4230M2D, 'PLA')
    brazo_5 = RobotDOF_3D(dh_5dof, alpha_target=5.0, m_load=m_carga_util, m_tool=m_herramienta)
    brazo_5.analyze_pose(thetas_deg=[0, 0, 0, 0, 0], title_prefix="ANÁLISIS 5-DOF (L=250mm)")

    # 3. Barrido Paramétrico Escalar - Todas las articulaciones graficadas
    plot_parametric_sweep(mot_TS4230M5D, mot_TS4230M2D, m_load=m_carga_util, m_tool=m_herramienta, dof=4)
    plot_parametric_sweep(mot_TS4230M5D, mot_TS4230M2D, m_load=m_carga_util, m_tool=m_herramienta, dof=5)