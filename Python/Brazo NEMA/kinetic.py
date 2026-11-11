import numpy as np

class Kinetic:
    def __init__(self, joints, alpha_target, m_load=0.0, m_tool=0.0):
        """
        :param joints: Lista de diccionarios de las articulaciones
        :param alpha_target: Lista con la aceleración angular deseada para cada articulación (rad/s^2)
        :param m_load: Masa de la carga (kg)
        :param m_tool: Masa de la herramienta (kg)
        """
        self.joints = joints
        self.N = len(joints)
        self.alpha_target = np.array(alpha_target)
        
        # Pesos en la punta
        self.m_tcp = m_load + m_tool 
        self.g = 9.81  
        self.F_g = np.array([0, 0, -self.g])  # Vector aceleración gravedad
        
    def calculate_kinetic(self, kinematic_data):
        """
        Calcula fuerzas, momentos de reacción y torques del motor.
        :param kinematic_data: Diccionario retornado por Kinematic.calculate_kinematic()
        """
        positions = kinematic_data['positions']
        rot_axes = kinematic_data['rot_axes']
        com_positions = kinematic_data['com_positions']
        p_tcp = kinematic_data['p_tcp'] # Posición en [x,y,z] del TCP

        # Inicialización de arreglos (N filas x 3 columnas para vectores)
        reaction_forces = np.zeros((self.N, 3))   # [Fx, Fy, Fz] soportadas por el eje
        reaction_moments = np.zeros((self.N, 3))  # [Mx, My, Mz] soportados por la estructura/motor
        
        t_static = np.zeros(self.N)
        t_dynamic_target = np.zeros(self.N)
        t_total = np.zeros(self.N)
        inertia_array = np.zeros(self.N)
        alpha_max_permitida = np.zeros(self.N)
        
        for i in range(self.N):
            z_i = rot_axes[i]   # Vector (3,) de dirección del eje de rotación
            p_i = positions[i]  # Posición (3,) de la articulación
            
            F_total_i = np.zeros(3) # Sumatoria de Fuerzas sobre la articulación i
            M_total_i = np.zeros(3) # Sumatoria de Momentos (Torques 3D) respecto a i
            I_i = 0.0               # Inercia respecto a su propio eje de rotación
            
            # Barrido desde el eslabón actual hasta el último
            for j in range(i, self.N):
                # 1. Efecto del ESLABÓN j
                m_link = self.joints[j].get('m_link', 0.0)
                W_link = m_link * self.F_g
                r_link = com_positions[j] - p_i
                
                F_total_i += W_link
                M_total_i += np.cross(r_link, W_link)
                
                # Inercia del eslabón j respecto al eje z de i
                r_link_perp = r_link - np.dot(r_link, z_i) * z_i
                I_i += m_link * np.dot(r_link_perp, r_link_perp)
                
                # 2. Efecto del MOTOR j
                m_motor = self.joints[j].get('m_motor', 0.0)
                W_motor = m_motor * self.F_g
                r_motor = positions[j] - p_i
                
                F_total_i += W_motor
                M_total_i += np.cross(r_motor, W_motor)
                
                r_motor_perp = r_motor - np.dot(r_motor, z_i) * z_i
                I_i += m_motor * np.dot(r_motor_perp, r_motor_perp)

            # 3. Efecto del TCP (Carga + Herramienta)
            r_tcp = p_tcp - p_i
            F_total_i += self.m_tcp * self.F_g
            M_total_i += np.cross(r_tcp, self.m_tcp * self.F_g)
            
            r_tcp_perp = r_tcp - np.dot(r_tcp, z_i) * z_i
            I_i += self.m_tcp * np.dot(r_tcp_perp, r_tcp_perp)

            # --- ALMACENAR RESULTADOS 3D PARA RESISTENCIA DE MATERIALES ---
            
            # La fuerza de reacción que debe ejercer la articulación es igual y opuesta a F_total_i
            reaction_forces[i] = -F_total_i 
            
            # El momento de reacción 3D (para rodamientos/estructura)
            reaction_moments[i] = -M_total_i
            
            # --- CÁLCULOS 1D PARA EL MOTOR ---
            
            # Torque estático del motor: Proyección del momento total en el eje de rotación (producto punto)
            # El signo negativo se aplica para indicar el esfuerzo que debe hacer el motor para oponerse a la caída
            t_static[i] = -np.dot(M_total_i, z_i)
            
            # Inercia total
            I_i += self.joints[i].get('I_rotor', 0.0) 
            inertia_array[i] = I_i
            
            # Torque dinámico
            t_dynamic_target[i] = I_i * self.alpha_target[i]
            
            # Torque total que debe proveer el motor
            t_total[i] = t_static[i] + t_dynamic_target[i]
            
            # Aceleración máxima permitida por el hardware
            t_max = self.joints[i].get('torque_max', None)
            if t_max is not None:
                t_disponible = t_max - abs(t_static[i])
                if t_disponible > 0 and I_i > 0:
                    alpha_max_permitida[i] = t_disponible / I_i
                else:
                    alpha_max_permitida[i] = 0.0
            else:
                alpha_max_permitida[i] = np.inf
                
        return {
            # Vectores 3D (Matrices N x 3) - Usados para diseño mecánico y rodamientos
            'reaction_forces': reaction_forces,   # Fuerzas [Fx, Fy, Fz] en cada articulación
            'reaction_moments': reaction_moments, # Momentos [Mx, My, Mz] en cada articulación
            # Valores 1D (Vectores de tamaño N) - Usados para selección de motores y control
            't_static': t_static,                 # Torque necesario en el eje de giro para mantener posición
            't_dynamic_target': t_dynamic_target, # Torque extra necesario para acelerar
            't_total': t_total,                   # Suma de estático + dinámico
            'inertia_array': inertia_array,       # Inercia percibida por cada motor
            'alpha_max_permitida': alpha_max_permitida 
        }