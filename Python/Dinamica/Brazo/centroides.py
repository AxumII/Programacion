import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class ArmStability:
    def __init__(self, df_componentes, df_ejes, origin=[0.0, 0.0, 0.0]):
        """
        df_componentes: DataFrame con los componentes, masas (g) y distancias (mm)
        df_ejes: DataFrame con las distancias entre los ejes (mm)
        """
        self.df_comp = df_componentes
        self.df_ejes = df_ejes
        
        # Origen del sistema (Base de rotación Z)
        self.origin = np.array(origin, dtype=float)
        
        self.joint_positions = []
        self.mass_centers_global = [] # Coordenadas globales de cada componente
        
        self.cm_total = np.zeros(3)
        self.torque_base = 0.0
        self.fuerza_z_base = 0.0

    def ang2distance(self, angles_rad):
        """
        angles_rad: lista o array con los 3 ángulos en radianes para los ejes 1, 2 y 3.
        """
        # Extraer longitudes entre ejes convirtiéndolas a metros
        L_0_1 = self.df_ejes.iloc[0]['Distancia'] / 1000.0
        L_1_2 = self.df_ejes.iloc[1]['Distancia'] / 1000.0
        L_2_3 = self.df_ejes.iloc[2]['Distancia'] / 1000.0

        # Calcular posiciones globales de los EJES
        # Eje 0 (Origen)
        pos_eje_0 = self.origin.copy()
        
        # Eje 1 (Fijo respecto a Eje 0, asumiendo orientación en X a 0 grados)
        pos_eje_1 = pos_eje_0 + np.array([L_0_1, 0.0, 0.0])
        
        # Eje 2 (Depende del ángulo del Eje 1)
        ang_acum_1 = angles_rad[0]
        pos_eje_2 = pos_eje_1 + np.array([
            L_1_2 * np.cos(ang_acum_1),
            0.0, # Asumimos plano X-Z
            L_1_2 * np.sin(ang_acum_1)
        ])
        
        # Eje 3 (Depende del ángulo acumulado de Eje 1 + Eje 2)
        ang_acum_2 = ang_acum_1 + angles_rad[1]
        pos_eje_3 = pos_eje_2 + np.array([
            L_2_3 * np.cos(ang_acum_2),
            0.0,
            L_2_3 * np.sin(ang_acum_2)
        ])
        
        self.joint_positions = [pos_eje_0, pos_eje_1, pos_eje_2, pos_eje_3]
        
        # Ángulo acumulado que afecta a los componentes de cada eje
        angulos_acumulados = {
            0: 0.0,
            1: ang_acum_1,
            2: ang_acum_2,
            3: ang_acum_2 + angles_rad[2]
        }
        
        # Calcular centroides GLOBALES de cada componente
        self.mass_centers_global = []
        
        for idx, row in self.df_comp.iterrows():
            eje_id = int(row['Eje'])
            # Convertir distancias a metros
            d_cx = row['Centroide_X'] / 1000.0
            d_cy = row['Centroide_Y'] / 1000.0
            
            origen_local = self.joint_positions[eje_id]
            ang_actual = angulos_acumulados[eje_id]
            
            # Transformación al marco global (plano X-Z + offset en Y)
            x_cm = origen_local[0] + d_cx * np.cos(ang_actual)
            z_cm = origen_local[2] + d_cx * np.sin(ang_actual)
            y_cm = origen_local[1] + d_cy 
            
            self.mass_centers_global.append(np.array([x_cm, y_cm, z_cm]))
            
        self.mass_centers_global = np.array(self.mass_centers_global)
        self.joint_positions = np.array(self.joint_positions)

    def mass_center(self):
        # Convertir masa a kg
        masas_kg = self.df_comp['Masa'].values / 1000.0
        masa_total = np.sum(masas_kg)
        
        suma_momentos = np.zeros(3)
        for i in range(len(masas_kg)):
            suma_momentos += masas_kg[i] * self.mass_centers_global[i]
            
        self.cm_total = suma_momentos / masa_total if masa_total > 0 else self.origin.copy()
        return self.cm_total, masa_total

    def torque_mass_center(self):
        g = 9.81
        masa_total = np.sum(self.df_comp['Masa'].values / 1000.0)
        
        self.fuerza_z_base = masa_total * g
        distancia_x = self.cm_total[0] - self.origin[0]
        self.torque_base = self.fuerza_z_base * distancia_x
        
        return self.torque_base, self.fuerza_z_base

    def graf(self):
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 1. Graficar los eslabones principales (líneas negras)
        xs = self.joint_positions[:, 0]
        ys = self.joint_positions[:, 1]
        zs = self.joint_positions[:, 2]
        ax.plot(xs, ys, zs, '-o', color='black', linewidth=4, markersize=6, label='Estructura (Distancia entre ejes)')
        
        # 2. Marcar el ORIGEN explícitamente
        ax.scatter(self.origin[0], self.origin[1], self.origin[2], 
                   color='green', s=150, marker='s', label='ORIGEN (0,0,0)')

        # 3. Dibujar los EJES DE GIRO (Vectores/Flechas)
        longitud_flecha = 0.15 # 15 cm para que las flechas sean visibles
        
        # Eje de giro de la Base (Motor 0 rota en Z)
        ax.quiver(self.origin[0], self.origin[1], self.origin[2], 
                  0, 0, longitud_flecha, 
                  color='green', linewidth=3, arrow_length_ratio=0.2, label='Eje de Rotación Z (Base)')
        
        # Ejes de giro de las articulaciones (Motores 1, 2 y 3 rotan en Y)
        colores_ejes = ['purple', 'cyan', 'magenta']
        nombres_ejes = ['Eje de Rotación 1 (Y)', 'Eje de Rotación 2 (Y)', 'Eje de Rotación 3 (Y)']
        
        for i in range(1, 4):
            pos_eje = self.joint_positions[i]
            ax.quiver(pos_eje[0], pos_eje[1], pos_eje[2], 
                      0, longitud_flecha, 0, # El vector apunta en la dirección Y positiva
                      color=colores_ejes[i-1], linewidth=3, arrow_length_ratio=0.2, label=nombres_ejes[i-1])

        # 4. Graficar las masas individuales (puntos azules)
        cm_xs = self.mass_centers_global[:, 0]
        cm_ys = self.mass_centers_global[:, 1]
        cm_zs = self.mass_centers_global[:, 2]
        ax.scatter(cm_xs, cm_ys, cm_zs, color='blue', s=30, alpha=0.6, label='Centroides de Componentes')
        
        # 5. Graficar Centro de Masa Total (Estrella roja)
        ax.scatter(self.cm_total[0], self.cm_total[1], self.cm_total[2], 
                   color='red', s=250, marker='*', label='Centro de Masa Total')
        
        # Línea de proyección del CM al piso
        ax.plot([self.cm_total[0], self.cm_total[0]], 
                [self.cm_total[1], self.cm_total[1]], 
                [0, self.cm_total[2]], 'r--', alpha=0.5)

        # Configuración visual
        ax.set_xlabel('Eje X (m) [Frente]')
        ax.set_ylabel('Eje Y (m) [Ancho]')
        ax.set_zlabel('Eje Z (m) [Alto]')
        ax.set_title('Modelo Estático 3D: Ejes de Giro y Origen')
        
        # Mover la leyenda afuera para que no tape el dibujo
        ax.legend(loc='center left', bbox_to_anchor=(1.05, 0.5))
        
        # Ajuste isométrico visual
        max_range = np.array([cm_xs.max()-cm_xs.min(), cm_ys.max()-cm_ys.min(), cm_zs.max()-cm_zs.min()]).max() / 2.0
        mid_x = (cm_xs.max()+cm_xs.min()) * 0.5
        mid_y = (cm_ys.max()+cm_ys.min()) * 0.5
        mid_z = (cm_zs.max()+cm_zs.min()) * 0.5
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(0, mid_z + max_range)
        
        plt.tight_layout()
        plt.show()
# ==========================================
# CARGA DE DATOS DE LA IMAGEN
# ==========================================
if __name__ == "__main__":
    # Tabla 1: Componentes (valores numéricos directos)
    datos_componentes = {
        'Nombre': [
            'Soporte Motor 1', 'Motor 1y', 'Articulacion 1 parte 1', 'Articulacion 1 parte 2', 
            'Motor 2Y', 'Articulacion 2', 'Motor 3Y', 'Articulacion 3', 'Gripper', 'Carga'
        ],
        'Masa': [150, 400, 200, 50, 160, 150, 160, 50, 120, 100],
        'Centroide_Y': [27, 24.5, 72, 63, 76, 39, 32, 47, 47, 47], # Sumas resueltas
        'Centroide_X': [67, 51, 97, 250, 279, 96, 85, 50, 140, 210], # Sumas/restas resueltas
        'Eje': [0, 0, 1, 1, 1, 2, 2, 3, 3, 3]
    }
    df_comp = pd.DataFrame(datos_componentes)

    # Tabla 2: Distancias de los ejes
    datos_ejes = {
        'Eje_Str': ['origen a 1', '1 a 2', '2 a 3'],
        'Distancia': [110, 304, 218]
    }
    df_ejes = pd.DataFrame(datos_ejes)

    # Inicializar analizador
    analizador = ArmStability(df_componentes=df_comp, df_ejes=df_ejes)
    
    # Pruebas con ángulos: El Eje 0 no varía en el plano XZ.
    # Ángulos para Eje 1, Eje 2, Eje 3 en radianes. 
    # Ejemplo: Brazo semi-extendido (30 grados, -15 grados, 0 grados)
    angulos_prueba = np.array([np.pi/6, -np.pi/12, 0.0])
    
    # Ejecutar cálculos
    analizador.ang2distance(angulos_prueba)
    cm_total, masa_total = analizador.mass_center()
    torque, fuerza = analizador.torque_mass_center()
    
    print("=== RESULTADOS DEL ANÁLISIS ===")
    print(f"Masa Total: {masa_total:.3f} kg")
    print(f"Centroide Total (X, Y, Z): ({cm_total[0]:.3f} m, {cm_total[1]:.3f} m, {cm_total[2]:.3f} m)")
    print(f"Torque en el punto de apoyo de la base (Eje Z): {torque:.2f} N*m")
    
    # Generar la gráfica 3D
    analizador.graf()