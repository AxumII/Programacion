import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Kinetic:
    # P0: Base (Servo 1)
    # P1: Codo (Servo 2)
    # P2: Punta (TCP)
    
    #es 2d , sera tratado como 2d
    def __init__(self, L, m_L, m_P, omega_max, alpha_max, t_stall ,m_load=0, theta = [0,0]):
        # --- Entradas en unidades estándar (SI) ---
        self.L = np.array(L)          # [L1, L2] en metros
        self.m_L = np.array(m_L)      # [mL1, mL2] en Kg
        self.m_P = np.array(m_P)      # [m_codo, m_punta] en Kg
        self.m_load = m_load          # Carga extra en punta en Kg
        
        # --- Conversión de Ángulos (Deg -> Rad) ---
        self.theta = np.radians(np.atleast_2d(theta))
        self.theta_cum = np.cumsum(self.theta, axis=1) # th1 (absoluto), th1+th2 (absoluto)
        
        # Datos del motor
        self.omega_max =  (np.pi / 3) / np.array(omega_max) # V angular maxima sin carga
        self.alpha_max = alpha_max # Aceleración angular [rad/s^2]        
        self.t_stall = np.array(t_stall) * 0.0980665            # Torque maximo estatico del fabricante en N m
        
# --- Lambdas Vectorizados ---
        # R devuelve un array de distancias para cada par de ángulos
        self.R = lambda: np.hypot(
            np.sum(self.L * np.cos(self.theta_cum), axis=1), 
            np.sum(self.L * np.sin(self.theta_cum), axis=1)
        )
        
        # Proyecciones horizontales (X) de los centroides
        self.centroid_arm_0_1 = lambda: (self.L[0] / 2) * np.cos(self.theta_cum[:, 0])
        self.centroid_arm_1_2 = lambda: (self.L[1] / 2) * np.cos(self.theta_cum[:, 1])
        
        # Centroide del brazo 2 visto desde la base
        self.centroid_arm_0_2 = lambda: (self.L[0] * np.cos(self.theta_cum[:, 0])) + \
                                        ((self.L[1] / 2) * np.cos(self.theta_cum[:, 1]))
        #Constantes
        self.g = 9.81
    
    
    def inertia(self):  
        r_vals = self.R()
             
        J_codo_point = (self.m_P[1] + self.m_load) * (self.L[1]**2)
        J_codo_arm = (1/3) * self.m_L[1] * (self.L[1]**2)
        J_codo = J_codo_point + J_codo_arm
        
        J_base_p1 = self.m_P[0]*(self.L[0]**2)
        J_base_arm1 = (1/3) * self.m_L[0] * (self.L[0]**2)
        J_base_p2 = (self.m_P[1] + self.m_load)*(self.R()**2)
        J_base_arm2 = self.m_L[1] * ((0.5 * self.R()**2) + (0.5 * self.L[0]**2) - (1/6 * self.L[1]**2))
        J_base = J_base_p1 + J_base_arm1 + J_base_p2 +  J_base_arm2  
        
              
        J_codo = np.full_like(J_base, J_codo)
        return J_base, J_codo
    
    def static_torque(self):
        cos_abs = np.cos(self.theta_cum)
        # Brazos de palanca horizontales (x) para masas puntuales
        x_p1 = self.L[0] * cos_abs[:, 0] 
        x_p2 = x_p1 + (self.L[1] * cos_abs[:, 1])
        
        #Torques seccion extrema
        t_s_codo_point = (self.m_P[1] + self.m_load)*self.g* (self.L[1] * np.cos(self.theta_cum[:, 1])) 
        t_s_codo_arm = self.m_L[1]*self.g*self.centroid_arm_1_2()
        t_s_codo =   t_s_codo_arm + t_s_codo_point
        #Torque ambas secciones 
        t_s_base_p1 = self.m_P[0] * self.g * x_p1
        t_s_base_arm1 = self.m_L[0] * self.g * self.centroid_arm_0_1()
        t_s_base_p2 = (self.m_P[1] + self.m_load) * self.g * x_p2
        t_s_base_arm2 = self.m_L[1] * self.g * self.centroid_arm_0_2() 
               
        t_s_base =   t_s_base_p1 + t_s_base_arm1 + t_s_base_p2 + t_s_base_arm2
        
         
        return np.column_stack((t_s_base,t_s_codo))
    
    def dynamic_torque(self):
        # Torque dinámico = J * alpha
        J_base, J_codo = self.inertia()        
        td_base = J_base * self.alpha_max
        td_codo = J_codo * self.alpha_max       
        return np.column_stack((td_base, td_codo))
        
    def total_torque(self):
        return self.static_torque() + self.dynamic_torque()
    
    
        
class MaxKinetic(Kinetic):
    def __init__(self, L, m_L, m_P, omega_max, alpha_max, t_stall, m_load=0, theta=[0, 0]):
        super().__init__(L, m_L, m_P, omega_max, alpha_max, t_stall, m_load, theta)
        self.Nm2kgcm = 10.197  # Factor de conversión

    def _get_comparison_table(self, idx):
        """Método privado para generar la tabla vertical comparativa de un índice específico."""
        ts = self.static_torque()
        td = self.dynamic_torque()
        tt = self.total_torque()
        
        # Cálculos de uso y FS
        use_static = (ts / self.t_stall) * 100
        use_total = (tt / self.t_stall) * 100
        fs_total = self.t_stall / tt

        # --- Cálculo de Carga Máxima (Headroom) ---
        cos_abs = np.cos(self.theta_cum)
        x_lever = self.L[0] * cos_abs[idx, 0] + self.L[1] * cos_abs[idx, 1]
        r_val = self.R()[idx]

        # Denominador: Esfuerzo por cada kg de carga en la punta
        # Incluye gravedad (estático) + inercia (dinámico)
        esfuerzo_por_kg = (self.g * x_lever) + (self.alpha_max * r_val**2)

        # Torque ya ocupado por el brazo y la carga actual
        torque_actual_base = tt[idx, 0]
        
        # Carga TOTAL permitida en la punta (en kg)
        # T_stall = T_brazo_vacio + m_total * esfuerzo_por_kg
        m_total_permitida = (self.t_stall[0] - (torque_actual_base - self.m_load * esfuerzo_por_kg)) / esfuerzo_por_kg
        m_max_g = (m_total_permitida - self.m_load) * 1000

        data = {
            "Métrica": [
                "Capacidad Nominal [Nm]",
                "Capacidad Nominal [kgcm]",
                "Torque Estático [Nm]", "Torque Estático [kgcm]",
                "Torque Dinámico [Nm]", "Torque Dinámico [kgcm]",
                "Torque Total [Nm]", "Torque Total [kgcm]",
                "Uso Estático [%]", "Uso Total [%]",
                "Factor de Seguridad (FS)", "Carga Máxima Punta [g]"
            ],
            "Servo 1 (Base)": [
                self.t_stall[0],
                self.t_stall[0] * self.Nm2kgcm,
                ts[idx, 0], ts[idx, 0] * self.Nm2kgcm,
                td[idx, 0], td[idx, 0] * self.Nm2kgcm,
                tt[idx, 0], tt[idx, 0] * self.Nm2kgcm,
                use_static[idx, 0], use_total[idx, 0], fs_total[idx, 0], m_max_g
            ],
            "Servo 2 (Codo)": [
                self.t_stall[0],
                self.t_stall[0] * self.Nm2kgcm,
                ts[idx, 1], ts[idx, 1] * self.Nm2kgcm,
                td[idx, 1], td[idx, 1] * self.Nm2kgcm,
                tt[idx, 1], tt[idx, 1] * self.Nm2kgcm,
                use_static[idx, 1], use_total[idx, 1], fs_total[idx, 1], m_max_g
            ]
        }
        
       
        return pd.DataFrame(data).set_index("Métrica").round(3)

    def worst_case(self):
        """Evalúa únicamente el caso de máxima extensión horizontal [0, 0]."""
        # Guardamos los ángulos originales
        original_theta = self.theta
        # Forzamos el caso [0, 0]
        self.theta = np.radians(np.atleast_2d([0, 0]))
        self.theta_cum = np.cumsum(self.theta, axis=1)
        
        print("\n" + "!"*50)
        print("ANÁLISIS DE PEOR CASO (EXTENSIÓN MÁXIMA [0, 0])")
        print("!"*50)
        
        tabla = self._get_comparison_table(0)
        self._show_table_window(tabla, "ANÁLISIS DE PEOR CASO (Extensión Máxima [0, 0])")
        
        # Restauramos ángulos originales
        self.theta = original_theta
        self.theta_cum = np.cumsum(self.theta, axis=1)
        return tabla
        
        

    def custom_case(self):
        for i in range(len(self.theta)):
            ang_deg = np.degrees(self.theta[i])
            tabla = self._get_comparison_table(i)
            self._show_table_window(tabla, f"RESULTADOS POSICIÓN {i+1}: [Th1:{ang_deg[0]}°, Th2:{ang_deg[1]}°]")
        
        for i in range(len(self.theta)):
            angulos_deg = np.degrees(self.theta[i])
            print(f"\n>>> Configuración {i+1}: [Th1: {angulos_deg[0]}°, Th2: {angulos_deg[1]}°]")
            tabla = self._get_comparison_table(i)
            print(tabla)
            print("-" * 30)
    
    def _show_table_window(self, df, title):
        """Renderiza un DataFrame como una tabla de Matplotlib en una ventana nueva."""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis('off')
        
        # Crear la tabla
        the_table = ax.table(cellText=df.values,
                            rowLabels=df.index,
                            colLabels=df.columns,
                            loc='center',
                            cellLoc='center')
        
        # Estilo de la tabla
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(10)
        the_table.scale(1.2, 2.2) # Estirar filas para que no se amontonen
        
        plt.title(title, fontweight='bold', pad=20, fontsize=12)
        plt.tight_layout()
        plt.show()
    
    
    def FBD(self, index=0):
        # 1. Datos de la postura (Lógica original del usuario)
        th1 = self.theta[index, 0]
        th2 = self.theta[index, 1]
        
        # 2. Cinemática
        x1, y1 = self.L[0] * np.cos(th1), self.L[0] * np.sin(th1)
        x2, y2 = x1 + self.L[1] * np.cos(th2), y1 + self.L[1] * np.sin(th2)
        
        # --- Función para dibujar Arcos ---
        def draw_arc(center, radius, start_angle, end_angle, label):
            angles = np.linspace(start_angle, end_angle, 50)
            plt.plot(center[0] + radius * np.cos(angles), 
                     center[1] + radius * np.sin(angles), 
                     color="blue", linestyle='--', linewidth=1.5)
            mid = (start_angle + end_angle) / 2
            plt.text(center[0] + radius * 1.8 * np.cos(mid), 
                     center[1] + radius * 1.8 * np.sin(mid), 
                     label, color="blue", fontweight='bold', ha='center', va='center', fontsize=9) 

        plt.figure(figsize=(9, 9))
        radius = np.min(self.L) / 7 
        
        # --- Arcos y Estructura ---
        draw_arc((0,0), radius, 0, th1, f'{np.degrees(th1):.0f}°')      
        draw_arc((x1, y1), radius, th1 - np.pi, th2, f'{np.degrees(th2):.0f}°')
        plt.plot([0, x1, x2], [0, y1, y2], 'ko-', linewidth=5, markersize=10, zorder=3, label="Estructura")
        
        # Etiquetas de Articulaciones
        plt.text(x1, y1 + 0.02, 'P1', fontweight='bold', ha='center')
        plt.text(x2, y2 + 0.02, 'P2', fontweight='bold', ha='center')

        # --- VECTORES DE PESO (Longitud Fija para Claridad) ---
        # Definimos una longitud visual estándar para todas las flechas (ej. 4cm)
        arrow_len = np.min(self.L) / 5
        text_offset = np.min(self.L) / 6
        
        # Puntos de aplicación
        xc1, yc1 = x1/2, y1/2
        xc2, yc2 = x1 + (self.L[1]/2)*np.cos(th2), y1 + (self.L[1]/2)*np.sin(th2)
        
        # 1. Pesos de los Brazos (NARANJA)
        # Brazo 1
        plt.arrow(xc1, yc1, 0, -arrow_len, color='orange', width=0.003, head_width=0.008, zorder=4)
        plt.text(xc1, yc1 - arrow_len - text_offset, f"{self.m_L[0]*1000:.1f}g", color='orange', ha='center', fontsize=8, fontweight='bold')
        # Brazo 2
        plt.arrow(xc2, yc2, 0, -arrow_len, color='orange', width=0.003, head_width=0.008, zorder=4, label="Peso Brazo")
        plt.text(xc2, yc2 - arrow_len - text_offset, f"{self.m_L[1]*1000:.1f}g", color='orange', ha='center', fontsize=8, fontweight='bold')

        # 2. Cargas Puntuales (ROJO)
        # Servo P1 (Codo)
        plt.arrow(x1, y1, 0, -arrow_len, color='red', width=0.003, head_width=0.008, zorder=4)
        plt.text(x1, y1 - arrow_len - text_offset, f"{self.m_P[0]*1000:.1f}g", color='red', ha='center', fontsize=8, fontweight='bold')
        # Carga en P2 (Punta + Carga Extra)
        m_total_punta = (self.m_P[1] + self.m_load) * 1000
        plt.arrow(x2, y2, 0, -arrow_len, color='red', width=0.003, head_width=0.008, zorder=4, label="Carga Puntual")
        plt.text(x2, y2 - arrow_len - text_offset, f"{m_total_punta:.1f}g", color='red', ha='center', fontsize=8, fontweight='bold')

        # --- Límites Enfocados ---
        puntos_x, puntos_y = [0, x1, x2], [0, y1, y2]
        margin = np.min(self.L) / 5
        plt.xlim(min(puntos_x) - margin, max(puntos_x) + margin)
        plt.ylim(min(puntos_y) - margin - arrow_len, max(puntos_y) + margin)
        
        plt.axhline(0, color='black', lw=1, alpha=0.3)
        plt.axvline(0, color='black', lw=1, alpha=0.3)
        plt.gca().set_aspect('equal')
        plt.grid(True, alpha=0.1)
        plt.title(f"FBD: Configuración {index+1}")
        plt.legend(loc='upper right', fontsize='small')
        plt.show()       
    

    

angulos_muestreo = [[0, 0], [45, -45], [0, -90]]

m_P = [0,0]
m_servo = 68/1000   #Servos metalicos
m_sensor = 1/1000  #Sensores Punta
m_conex = 1/1000 + 18/1000 #Cable + tornillos
m_grippen = 40/1000
m_P[0] = m_servo + m_sensor + m_conex
m_P[1] = m_servo + m_sensor + m_conex + m_grippen 
#print(m_P[1])


robot = MaxKinetic(
    L=[0.105, 0.19-0.03], 
    m_L=[0.038, 0.023], 
    m_P=m_P, 
    omega_max=[0.2, 0.2], 
    alpha_max = 50, 
    t_stall=[36, 36], 
    m_load=0.00, 
    theta=angulos_muestreo
    
)

robot.worst_case()
robot.custom_case()

robot.FBD(index=0)
robot.FBD(index=1)
robot.FBD(index=2)
robot.FBD(index=3)



