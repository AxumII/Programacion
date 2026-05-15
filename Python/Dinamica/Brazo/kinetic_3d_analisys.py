import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Helpers para Matrices de Transformación Homogénea en 3D
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

class RobotDOF_3D:
    def __init__(self, joints, alpha_target, m_load=0.0):
        """
        joints: Lista de diccionarios describiendo el robot.
        alpha_target: Aceleración angular deseada por el usuario (rad/s^2).
        m_load: Carga extra en el efector final (kg).
        """
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
            T = T @ translation(joint['offset'])
            positions.append(T[:3, 3])
            
            if joint['axis'] == 'x':
                z_axes.append(T[:3, 0])
                T = T @ rot_x(thetas[i])
            elif joint['axis'] == 'y':
                z_axes.append(T[:3, 1])
                T = T @ rot_y(thetas[i])
            elif joint['axis'] == 'z':
                z_axes.append(T[:3, 2])
                T = T @ rot_z(thetas[i])
            
            T_com = T @ translation(joint['com_link'])
            com_positions.append(T_com[:3, 3])
            
        # Efector Final (TCP) en Z local (Ej: longitud del gripper es 3cm = 0.03m)
        T_tip = T @ translation([0, 0, 0.03]) 
        p_tip = T_tip[:3, 3]
        
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
            
            # Torque dinámico para la aceleración que pidió el usuario
            t_dynamic_target[i] = inertia_i * self.alpha_target
            
            # Cálculo del límite absoluto
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
            
            # Cálculo del Factor de Seguridad (FS)
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

        # Restaurar la llamada al graficador
        if show_plot:
            self._plot_3d(thetas, thetas_deg)

    def _plot_3d(self, thetas, thetas_deg):
        positions, z_axes, com_positions, p_tip = self.forward_kinematics(thetas)
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        xs, ys, zs = positions[:, 0], positions[:, 1], positions[:, 2]
        
        # Estructura principal
        ax.plot(np.append(xs, p_tip[0]), np.append(ys, p_tip[1]), np.append(zs, p_tip[2]), 
                'ko-', linewidth=4, markersize=6, label='Estructura')
        
        # Servos y Ejes de Rotación
        for i in range(self.N):
            ax.scatter(xs[i], ys[i], zs[i], color='red', s=80, zorder=5)
            ax.quiver(xs[i], ys[i], zs[i], z_axes[i,0]*0.05, z_axes[i,1]*0.05, z_axes[i,2]*0.05, 
                      color='green', linewidth=2)
            ax.text(xs[i], ys[i], zs[i] + 0.02, f'J{i}', fontweight='bold')
            
        # Centros de masa
        cx, cy, cz = com_positions[:, 0], com_positions[:, 1], com_positions[:, 2]
        ax.scatter(cx, cy, cz, color='orange', s=30)
        for i in range(self.N):
            if self.joints[i]['m_link'] > 0:
                ax.quiver(cx[i], cy[i], cz[i], 0, 0, -0.03, color='orange')

        # Carga en la punta
        if self.m_load > 0:
            ax.scatter(p_tip[0], p_tip[1], p_tip[2], color='blue', s=200, marker='s', label=f'Carga ({self.m_load*1000}g)')
            ax.quiver(p_tip[0], p_tip[1], p_tip[2], 0, 0, -0.08, color='blue', linewidth=3)
            ax.text(p_tip[0], p_tip[1], p_tip[2] - 0.09, f'{self.m_load*1000}g', color='blue', fontweight='bold')

        ax.set_xlabel('X [m]'); ax.set_ylabel('Y [m]'); ax.set_zlabel('Z [m]')
        ax.set_title(f"Brazo 3D - Carga: {self.m_load*1000}g\nÁngulos: {thetas_deg}")
        
        # Forzar proporciones iguales (Bounding Box workaround para 3D en Matplotlib)
        max_range = np.array([xs.max()-xs.min(), ys.max()-ys.min(), zs.max()-zs.min()]).max() / 2.0
        mid_x, mid_y, mid_z = (xs.max()+xs.min())*0.5, (ys.max()+ys.min())*0.5, (zs.max()+zs.min())*0.5
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)
        
        ax.legend()
        plt.show()

