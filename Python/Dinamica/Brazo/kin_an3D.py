import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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
# 2. Módulo de Materiales (Masa y Flexión)
# ==========================================
DENSITIES = {
    'PLA': 1250.0,
    'ABS': 1040.0,
    'MDF': 750.0
}

# Módulo de Young (Elasticidad) en Pascales (N/m^2)
# Valores aproximados para material sólido
YOUNG_MODULUS = {
    'PLA': 3.5e9,  
    'ABS': 2.2e9,  
    'MDF': 4.0e9   
}

def get_material_properties(material, b, h):
    """
    Retorna la densidad efectiva y el Módulo de Young efectivo 
    dependiendo de si es impresión 3D (30% infill) o macizo (MDF).
    """
    area_m2 = b * h
    if material == 'MDF':
        densidad_ef = DENSITIES['MDF']
        E_ef = YOUNG_MODULUS['MDF']
    else:
        # Penalización por 30% de infill en masa y rigidez (aproximación analítica)
        densidad_ef = DENSITIES[material] * 0.30
        E_ef = YOUNG_MODULUS[material] * 0.30 
        
    return area_m2, densidad_ef, E_ef

def calc_link_mass(material, length_m):
    """
    Calcula la masa del eslabón basándose en la sección transversal y el método de fabricación.
    - PLA/ABS: 30x50mm (0.03 x 0.05 m) modelados como impresión 3D al 30% de infill.
    - MDF: 8x40mm (0.008 x 0.04 m) modelado como lámina maciza (100% densidad).
    """
    if material == 'MDF':
        area_m2 = 0.008 * 0.040
        densidad_efectiva = DENSITIES['MDF'] 
    else:
        area_m2 = 0.030 * 0.050
        densidad_efectiva = DENSITIES[material] * 0.30 
        
    return area_m2 * length_m * densidad_efectiva

# ==========================================
# 3. Clase Principal de Simulación Dinámica
# ==========================================
class RobotDOF_3D:
    def __init__(self, joints, alpha_target, m_load=0.0):
        self.joints = joints
        self.N = len(joints)
        self.alpha_target = alpha_target
        self.m_load = m_load
        self.g = 9.81
        self.kgcm2Nm = 0.0980665 
        self.Nm2kgcm = 10.197    
        self.F_g = np.array([0, 0, -self.g])

    def forward_kinematics(self, thetas):
        T = np.eye(4)
        positions, z_axes, com_positions = [], [], []
        
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
            T_com = T @ translation(joint['com_link'])
            com_positions.append(T_com[:3, 3])
            T = T @ translation(joint['offset'])
            
        p_tip = T[:3, 3]
        return np.array(positions), np.array(z_axes), np.array(com_positions), p_tip
    
    def calculate_torques_and_limits(self, thetas):
        positions, z_axes, com_positions, p_tip = self.forward_kinematics(thetas)
        
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
                if j > i: 
                    r_vec = positions[j] - P_axis
                    tau_3d_static += np.cross(r_vec, self.joints[j]['m_servo'] * self.F_g)
                    r_parallel = np.dot(r_vec, u_axis) * u_axis
                    r_perp = np.linalg.norm(r_vec - r_parallel)
                    inertia_i += self.joints[j]['m_servo'] * (r_perp**2)
                
                r_vec_com = com_positions[j] - P_axis
                tau_3d_static += np.cross(r_vec_com, self.joints[j]['m_link'] * self.F_g)
                r_parallel_com = np.dot(r_vec_com, u_axis) * u_axis
                r_perp_com = np.linalg.norm(r_vec_com - r_parallel_com)
                inertia_i += self.joints[j]['m_link'] * (r_perp_com**2)
            
            if self.m_load > 0:
                r_vec_load = p_tip - P_axis
                tau_3d_static += np.cross(r_vec_load, self.m_load * self.F_g)
                r_parallel_load = np.dot(r_vec_load, u_axis) * u_axis
                r_perp_load = np.linalg.norm(r_vec_load - r_parallel_load)
                inertia_i += self.m_load * (r_perp_load**2)
            
            t_static[i] = abs(np.dot(tau_3d_static, u_axis))
            inertia_array[i] = inertia_i
            t_dynamic_target[i] = inertia_i * self.alpha_target
            
            t_rated_Nm = self.joints[i]['t_rated'] * self.kgcm2Nm
            t_margin_static = t_rated_Nm - t_static[i]
            
            if t_margin_static > 0 and inertia_i > 0:
                alpha_max_permitida[i] = t_margin_static / inertia_i
            else:
                alpha_max_permitida[i] = 0.0
                
        return t_static, t_dynamic_target, inertia_array, alpha_max_permitida

    def analyze_pose(self, thetas_deg, show_plot=True):
        thetas = np.radians(thetas_deg)
        t_static, t_dyn_target, inertias, alphas = self.calculate_torques_and_limits(thetas)
        
        metrics = []
        for i in range(self.N):
            t_rated_kgcm = self.joints[i]['t_rated']
            t_stat_kgcm = t_static[i] * self.Nm2kgcm
            t_dyn_kgcm = t_dyn_target[i] * self.Nm2kgcm
            t_total_kgcm = t_stat_kgcm + t_dyn_kgcm
            
            fs = t_rated_kgcm / t_total_kgcm if t_total_kgcm > 0 else float('inf')
            
            metrics.append({
                "Articulación": f"J{i} ({self.joints[i]['axis'].upper()})",
                "Límite [kgcm]": round(t_rated_kgcm, 1),
                "T. Estático [kgcm]": round(t_stat_kgcm, 2),
                "T. Dinámico [kgcm]": round(t_dyn_kgcm, 2),
                "T. Total [kgcm]": round(t_total_kgcm, 2),
                "Acel. MAX [rad/s²]": round(alphas[i], 2),
                "FS": round(fs, 2)
            })
            
        df = pd.DataFrame(metrics).set_index("Articulación")
        print(f"\n" + "="*85)
        print(f"ANÁLISIS DE POSTURA: {thetas_deg} | Carga: {self.m_load*1000}g | Acel. Deseada: {self.alpha_target} rad/s²")
        print("="*85)
        print(df.to_string())
        
        alpha_global = min([a for a in alphas if a > 0] or [0])
        if self.alpha_target > alpha_global:
            print(f"\n>> ADVERTENCIA: La aceleración deseada ({self.alpha_target}) SUPERA el cuello de botella ({alpha_global:.2f} rad/s²). Los motores pueden fallar. <<\n")
        else:
            print(f"\n>> ÉXITO: Aceleración deseada soportada. (Cuello de botella en todo el brazo: {alpha_global:.2f} rad/s²) <<\n")

        if show_plot:
            self._plot_3d(thetas, thetas_deg)

    def _plot_3d(self, thetas, thetas_deg):
        positions, z_axes, com_positions, p_tip = self.forward_kinematics(thetas)
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        xs, ys, zs = positions[:, 0], positions[:, 1], positions[:, 2]
        
        ax.plot(np.append(xs, p_tip[0]), np.append(ys, p_tip[1]), np.append(zs, p_tip[2]), 
                'ko-', linewidth=4, markersize=6, label='Estructura')
        
        for i in range(self.N):
            ax.scatter(xs[i], ys[i], zs[i], color='red', s=80, zorder=5)
            ax.quiver(xs[i], ys[i], zs[i], z_axes[i,0]*0.05, z_axes[i,1]*0.05, z_axes[i,2]*0.05, 
                      color='green', linewidth=2)
            ax.text(xs[i], ys[i], zs[i] + 0.02, f'J{i}', fontweight='bold')
            
        cx, cy, cz = com_positions[:, 0], com_positions[:, 1], com_positions[:, 2]
        ax.scatter(cx, cy, cz, color='orange', s=30)
        for i in range(self.N):
            if self.joints[i]['m_link'] > 0:
                ax.quiver(cx[i], cy[i], cz[i], 0, 0, -0.03, color='orange')

        if self.m_load > 0:
            ax.scatter(p_tip[0], p_tip[1], p_tip[2], color='blue', s=200, marker='s', label=f'Carga ({self.m_load*1000}g)')
            ax.quiver(p_tip[0], p_tip[1], p_tip[2], 0, 0, -0.08, color='blue', linewidth=3)
            ax.text(p_tip[0], p_tip[1], p_tip[2] - 0.09, f'{self.m_load*1000}g', color='blue', fontweight='bold')

        ax.set_xlabel('X [m]'); ax.set_ylabel('Y [m]'); ax.set_zlabel('Z [m]')
        ax.set_title(f"Brazo Analizado - Carga: {self.m_load*1000}g\nÁngulos: {thetas_deg}")
        
        ax.set_xlim([-0.7, 0.7])
        ax.set_ylim([-0.7, 0.7])
        ax.set_zlim([-0.05, 0.85])
        
        ax.legend()
        plt.show()

# ==========================================
# 4. Función Continua de Análisis Comparativo
# ==========================================
def evaluar_barrido_multi_material(materiales=['PLA', 'ABS', 'MDF'], m_load=0.02, alpha_target=5.0):
    """
    Evalúa el requerimiento estático variando el hombro desde 180mm hasta 450mm.
    AHORA INCLUYE TODAS LAS ARTICULACIONES (J0 a J3).
    """
    print("\nGenerando gráficas de Torque para TODAS las articulaciones...")
    
    m_5840_31zy = 0.400
    m_jgy370 = 0.180
    L1 = 0.132  
    
    longitudes_hombro = np.linspace(0.180, 0.450, 100)
    
    fig, axes = plt.subplots(1, len(materiales), figsize=(18, 6), sharey=True)
    if len(materiales) == 1: axes = [axes]
        
    for idx, material in enumerate(materiales):
        t_j0, t_j1, t_j2, t_j3 = [], [], [], []
        
        # Dimensiones base de sección transversal
        b = 0.008 if material == 'MDF' else 0.030
        h = 0.040 if material == 'MDF' else 0.050
        
        area, den_ef, _ = get_material_properties(material, b, h)
        m_link1 = area * L1 * den_ef
        
        for L_hombro in longitudes_hombro:
            L2 = L_hombro
            L3 = 0.7 * L_hombro
            L4 = 0.3 * L_hombro
            
            m_link2 = area * L2 * den_ef
            m_link3 = area * L3 * den_ef
            m_link4 = area * L4 * den_ef
            
            robot_def = [
                {'axis': 'z', 'offset': [0.00475, 0.0, L1], 'm_servo': m_jgy370, 'm_link': m_link1, 'com_link': [0, 0, L1/2], 't_rated': 21.0}, # J0 (Base)
                {'axis': 'y', 'offset': [L2, -0.027, 0.0], 'm_servo': m_5840_31zy,'m_link': m_link2, 'com_link': [L2/2, 0, 0], 't_rated': 70.0}, # J1 (Hombro)
                {'axis': 'y', 'offset': [L3, -0.030, 0.0], 'm_servo': m_jgy370,   'm_link': m_link3, 'com_link': [L3/2, 0, 0], 't_rated': 21.0}, # J2 (Codo)
                {'axis': 'y', 'offset': [L4, -0.003, 0.0], 'm_servo': m_jgy370,   'm_link': m_link4, 'com_link': [L4/2, 0, 0], 't_rated': 21.0}  # J3 (Muñeca)
            ]
            
            arm = RobotDOF_3D(joints=robot_def, alpha_target=alpha_target, m_load=m_load)
            thetas_max = np.radians([0, 0, 0, 0])
            t_static, _, _, _ = arm.calculate_torques_and_limits(thetas_max)
            
            t_j0.append(t_static[0] * arm.Nm2kgcm)
            t_j1.append(t_static[1] * arm.Nm2kgcm)
            t_j2.append(t_static[2] * arm.Nm2kgcm)
            t_j3.append(t_static[3] * arm.Nm2kgcm)

        ax = axes[idx]
        ax.plot(longitudes_hombro * 1000, t_j0, 'k:', linewidth=2, label='J0 (Base - Eje Z)')
        ax.plot(longitudes_hombro * 1000, t_j1, 'b-', linewidth=2, label='J1 (Hombro)')
        ax.plot(longitudes_hombro * 1000, t_j2, 'r-', linewidth=2, label='J2 (Codo)')
        ax.plot(longitudes_hombro * 1000, t_j3, 'g-', linewidth=2, label='J3 (Muñeca)')
        
        ax.axhline(y=70, color='blue', linestyle='--', alpha=0.5, label='Límite J1 (70 kgcm)')
        ax.axhline(y=21, color='red', linestyle='--', alpha=0.5, label='Límite J0/J2/J3 (21 kgcm)')
        
        ax.set_title(f'Material: {material}')
        ax.set_xlabel('Longitud Hombro ($L$) [mm]')
        if idx == 0: ax.set_ylabel('Torque Estático Requerido [kgcm]')
            
        ax.grid(True, linestyle=':')
        ax.legend(fontsize=8)

    plt.suptitle(f'Torque en las Articulaciones vs Envergadura (Carga: {m_load*1000}g)', fontsize=14)
    plt.tight_layout()
    plt.show()

def evaluar_deformacion_seccion(materiales=['PLA', 'ABS', 'MDF'], m_load=0.02):
    """
    Evalúa la deflexión en la punta del brazo analizando el segmento más crítico (el Hombro, L=300mm),
    variando el ancho de la sección (b) desde 10mm hasta 50mm.
    """
    print("\nGenerando gráfica de Deformación vs Ancho de Sección Transversal...")
    
    L_hombro = 0.300 # Fijamos el hombro en 300mm para este análisis
    
    # Masas de los componentes que "cuelgan" del extremo del hombro (motores + eslabones siguientes)
    # L3 = 210mm, L4 = 90mm
    # m_5840_31zy = 0.400
    # m_jgy370 = 0.180
    m_Nema17_42BLS04 = 500/1000 #Sin caja lazo cerrado 0.4nM
    m_Nema17_HBT4240C = 500/1000 #Sin caja lazo cerrado 0.4nM
    m_Nema17_17HD60001 = 500/1000 #Sin caja lazo cerrado  0.7nM 
    m_Nema17_17HS4401S_PG139 = 580/1000 #Con Caja lazo abierto y 4Nm, algunas config pesan mas pero llegan a 6Nm
    m_GB_Harmonic = 200/1000 # Es solo la caja de 30:1 
    m_Nema17_TS4260M5_Cicloidal = 520/1000 # Con caja lazo abierto al menos 10Nm
    m_Nema17_TS4260M2_Cicloidal = 290/1000 # Con caja lazo abierto al menos 2Nm
    m_Nema17_17HS08 = 100/1000 # SIn caja y lazo abierto, tiny y 0.1Nm Holding
    m_Nema17_17HS3401S = 0/1000 # Sin caja y lazo abierto, mediano
    
    # Rango de anchos (b) a evaluar: de 10mm a 50mm
    anchos_b = np.linspace(0.010, 0.050, 50)
    
    plt.figure(figsize=(10, 6))
    colores = {'PLA': 'blue', 'ABS': 'orange', 'MDF': 'green'}
    
    for material in materiales:
        deflexiones_mm = []
        
        # Fijamos la altura (h) según el material estándar planeado
        h = 0.040 if material == 'MDF' else 0.050
        
        for b in anchos_b:
            # Propiedades ajustadas por infill
            area, den_ef, E_ef = get_material_properties(material, b, h)
            
            # Momento de inercia de área I = (b * h^3) / 12
            I_area = (b * h**3) / 12.0
            
            # Masa propia del hombro (carga distribuida W)
            peso_propio_L2 = area * L_hombro * den_ef * 9.81
            
            # Masa de la carga en la punta del hombro (J2, J3, J4, L3, L4, load)
            area_restante, _, _ = get_material_properties(material, 0.030, h) # asumiendo el resto es estandar
            masa_restante = (area_restante * 0.210 * den_ef) + (area_restante * 0.090 * den_ef)
            peso_punta = (m_Nema17_17HS4401S_PG139 * 2 + masa_restante + m_load) * 9.81
            
            # Cálculo de deflexión (Viga en voladizo)
            # delta = (F_punta * L^3)/(3*E*I) + (W_propio * L^3)/(8*E*I)
            delta_punta = ((peso_punta * L_hombro**3) / (3 * E_ef * I_area)) + \
                          ((peso_propio_L2 * L_hombro**3) / (8 * E_ef * I_area))
                          
            deflexiones_mm.append(delta_punta * 1000) # Convertir a mm
            
        plt.plot(anchos_b * 1000, deflexiones_mm, color=colores[material], linewidth=2, label=f'{material} (h={h*1000}mm)')

    plt.title('Deflexión Máxima vs Ancho de Sección ($b$)\n(Brazo extendido, Segmento Hombro = 300mm)')
    plt.xlabel('Ancho de la Sección Transversal $b$ [mm]')
    plt.ylabel('Deformación en la punta $\delta$ [mm]')
    plt.axhline(y=2.0, color='red', linestyle='--', alpha=0.5, label='Límite de precisión aceptable (2 mm)')
    
    plt.grid(True, linestyle=':')
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # 1. Gráfica de Torques (TODAS las articulaciones J0 a J3)
    evaluar_barrido_multi_material(['PLA', 'ABS', 'MDF'], m_load=0.2, alpha_target=5.0)
    
    # 2. Nueva Gráfica de Deformación / Flexión
    evaluar_deformacion_seccion(['PLA', 'ABS', 'MDF'], m_load=0.2)
    # 1. Ejemplo para evaluar UNA postura con su tabla y render 3D (Usando PLA y L_hombro = 300mm por ejemplo)
    print("\nEjecutando Análisis 3D de una postura específica...")
    L_ejemplo = 0.2500    
    
    
    robot_def_ejemplo = [
        {'axis': 'z', 'offset': [0.00475, 0.0, 0.132], 'm_servo': 0.500, 'm_link': calc_link_mass('PLA', 0.150), 'com_link': [0, 0, 0.150/2], 't_rated': 10.0},
        {'axis': 'y', 'offset': [L_ejemplo, -0.027, 0.0], 'm_servo': 0.500, 'm_link': calc_link_mass('PLA', L_ejemplo), 'com_link': [L_ejemplo/2, 0, 0], 't_rated': 50.0},
        {'axis': 'y', 'offset': [0.7*L_ejemplo, -0.030, 0.0], 'm_servo': 0.300, 'm_link': calc_link_mass('PLA', 0.7*L_ejemplo), 'com_link': [0.7*L_ejemplo/2, 0, 0], 't_rated': 15.0},
        {'axis': 'y', 'offset': [0.3*L_ejemplo, -0.003, 0.0], 'm_servo': 0.900, 'm_link': calc_link_mass('PLA', 0.3*L_ejemplo), 'com_link': [0.3*L_ejemplo/2, 0, 0], 't_rated': 15.0}
    ]
    arm_test = RobotDOF_3D(joints=robot_def_ejemplo, alpha_target=5.0, m_load=0.2)
    arm_test.analyze_pose([0.0, 0.0, 0.0, 0.0], show_plot=True)
    
    # 2. Ejecutar la evaluación de barrido continuo que grafica los subplots de materiales
    evaluar_barrido_multi_material(['PLA', 'ABS', 'MDF'], m_load=0.2, alpha_target=5.0)