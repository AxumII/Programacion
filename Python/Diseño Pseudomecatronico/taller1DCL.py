import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.lines import Line2D

class DCL:
    def __init__(self, d, h, r_pol):
        self.d = d
        self.h = h
        self.r_pol = r_pol
        
        # --- Magnitudes de Fuerza (Newtons) ---
        self.W_eje = -40      # Peso del eje 
        self.Rz_inf = 40      # Reacción normal (axial)
        self.T1 = 60          # Tensión lado tenso
        self.T2 = 15          # Tensión lado flojo

    def param_graf(self):
        # Alturas
        self.a = 0.3 * self.h
        self.b = 0.3 * self.h
        self.c = 0.4 * self.h
        self.e = 0.2 * self.h
        self.f = 0.3 * self.h
        self.g = 0.15 * self.h
        
        # Radios y dimensiones
        self.diam_pol_ax = 0.3 * self.d
        self.r_polea = self.diam_pol_ax / 2
        self.r_in_aspa = 0.25 * self.d
        self.r_ex_aspa = 0.45 * self.d
        self.h_aspa = 0.05 + 0.04 * self.h
        
        self.r_eje = 0.015 * self.d
        self.r_rod = 0.04 * self.d
        
        # Coordenadas Z
        self.z_aspa_inf = self.a
        self.z_aspa_sup = self.a + self.b
        self.z_rod_inf = self.h + self.e
        self.z_rod_sup = self.h + self.e + self.f
        self.z_polea = self.h + self.e + self.f + self.g

    def draw_cylinder(self, ax, z0, z1, R, color, alpha=0.8):
        """Genera la malla de un cilindro 3D"""
        z = np.linspace(z0, z1, 10)
        theta = np.linspace(0, 2*np.pi, 20)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_grid = R * np.cos(theta_grid)
        y_grid = R * np.sin(theta_grid)
        ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=alpha, shade=True)

    def draw_impeller(self, ax, z_center, sf):
        """Dibuja el agitador con aspas completamente verticales (90°)"""
        h_manzana = self.h_aspa * 0.8
        self.draw_cylinder(ax, z_center - h_manzana/2, z_center + h_manzana/2, self.r_eje*2.5, 'silver', 1.0)
        
        for angle in [0, np.pi/2, np.pi, 3*np.pi/2]:
            # Barras de unión
            x0, y0 = (self.r_eje*2.5) * np.cos(angle), (self.r_eje*2.5) * np.sin(angle)
            x1, y1 = self.r_in_aspa * np.cos(angle), self.r_in_aspa * np.sin(angle)
            ax.plot([x0, x1], [y0, y1], [z_center, z_center], color='black', lw=3)
            
            H = self.h_aspa
            # Geometría de aspa vertical (90 grados de inclinación)
            v1_l = [self.r_in_aspa, 0, z_center - H/2]
            v2_l = [self.r_ex_aspa, 0, z_center - H/2]
            v3_l = [self.r_ex_aspa, 0, z_center + H/2]
            v4_l = [self.r_in_aspa, 0, z_center + H/2]
            
            # Rotación de vértices según el cuadrante
            vertices = []
            for v in [v1_l, v2_l, v3_l, v4_l]:
                x_g = v[0] * np.cos(angle) - v[1] * np.sin(angle)
                y_g = v[0] * np.sin(angle) + v[1] * np.cos(angle)
                vertices.append([x_g, y_g, v[2]])
            
            blade = Poly3DCollection([vertices], color='gray', alpha=0.9, edgecolors='k')
            ax.add_collection3d(blade)
            
            # Fuerza de resistencia multiplicada por el factor de escala (sf)
            r_mid = (self.r_in_aspa + self.r_ex_aspa)/2
            Fx, Fy = 10 * np.sin(angle), -10 * np.cos(angle)
            ax.quiver(r_mid * np.cos(angle), r_mid * np.sin(angle), z_center, Fx*sf, Fy*sf, 0, color='orange', arrow_length_ratio=0.3)

    def graficar(self):
        self.param_graf()
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')

        # Factor de escala visual para restringir el tamaño de los vectores de fuerza
        sf = 0.015 

        # Sólidos: Eje, Rodamientos, Polea
        self.draw_cylinder(ax, 0, self.z_polea + 0.1, self.r_eje, 'dimgray', 1.0)
        h_rod = 0.05 * self.h
        self.draw_cylinder(ax, self.z_rod_inf - h_rod/2, self.z_rod_inf + h_rod/2, self.r_rod, 'blue', 0.6)
        self.draw_cylinder(ax, self.z_rod_sup - h_rod/2, self.z_rod_sup + h_rod/2, self.r_rod, 'blue', 0.6)
        self.draw_impeller(ax, self.z_aspa_inf, sf)
        self.draw_impeller(ax, self.z_aspa_sup, sf)
        self.draw_cylinder(ax, self.z_polea - 0.02, self.z_polea + 0.02, self.r_polea, 'maroon', 0.9)
        
        # Vectores escalados por 'sf'
        ax.quiver(self.r_polea, 0, self.z_polea, 0, -self.T1*sf, 0, color='red', lw=2.5, arrow_length_ratio=0.2)
        ax.quiver(-self.r_polea, 0, self.z_polea, 0, -self.T2*sf, 0, color='red', lw=2.5, arrow_length_ratio=0.3)
        ax.quiver(0, 0, self.z_rod_inf, 0, 0, self.Rz_inf*sf, color='green', lw=3, arrow_length_ratio=0.2)
        ax.quiver(0, 0, self.z_rod_inf, -15*sf, 0, 0, color='cyan', lw=2)
        ax.quiver(0, 0, self.z_rod_inf, 0, 15*sf, 0, color='cyan', lw=2)
        ax.quiver(0, 0, self.z_rod_sup, 20*sf, 0, 0, color='cyan', lw=2)
        ax.quiver(0, 0, self.z_rod_sup, 0, -10*sf, 0, color='cyan', lw=2)
        
        z_cg = self.z_polea * 0.45
        ax.quiver(0, 0, z_cg, 0, 0, self.W_eje*sf, color='purple', lw=3, arrow_length_ratio=0.2)

        # Configuración de límites fijos
        limite = max(self.h, self.d) * 0.8
        ax.set_xlim([-limite, limite])
        ax.set_ylim([-limite, limite])
        ax.set_zlim([0, self.z_polea + 0.5])
        
        ax.set_xlabel('Eje X (m)')
        ax.set_ylabel('Eje Y (m)')
        ax.set_zlabel('Eje Z - Altura (m)')
        ax.set_title('Diagrama de Cuerpo Libre (DCL 3D)')
        
        # Cuadro de Leyendas
        elementos_leyenda = [
            Line2D([0], [0], color='red', lw=3, label='Tensión Correa (T1, T2)'),
            Line2D([0], [0], color='cyan', lw=2, label='Reacciones Radiales (Rx, Ry)'),
            Line2D([0], [0], color='green', lw=3, label='Reacción Axial (Rz)'),
            Line2D([0], [0], color='purple', lw=3, label='Peso del Eje (W)'),
            Line2D([0], [0], color='orange', lw=2, label='Resistencia Tangencial Fluido'),
            Line2D([0], [0], color='blue', lw=6, alpha=0.6, label='Rodamientos (Soportes)'),
            Line2D([0], [0], color='gray', lw=6, alpha=0.9, label='Aspas Verticales (90°)')
        ]
        
        # Posicionamiento de la leyenda fuera del gráfico para que no tape vectores
        ax.legend(handles=elementos_leyenda, loc='center left', bbox_to_anchor=(1.05, 0.5), fontsize=10)

        ax.view_init(elev=20, azim=45)
        plt.tight_layout() # Ajusta los bordes para que la leyenda se vea completa
        plt.show()

if __name__ == '__main__':
    modelo_dcl = DCL(d=0.49, h=0.89, r_pol=4) 
    modelo_dcl.graficar()