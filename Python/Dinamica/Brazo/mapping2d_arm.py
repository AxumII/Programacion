import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from xy2deg import XYtoDeg 
class Mapping2DArm:
    def __init__(self, l1, l2):
        self.l1 = l1
        self.l2 = l2
        self.max_reach = l1 + l2
        self.min_reach = abs(l1 - l2) 
        self.xy2ang = XYtoDeg(l1, l2)  
        
    def dk(self, theta1, theta2):
        t1_rad = np.radians(theta1)
        t2_rad = np.radians(theta2)
        
        x = self.l1 * np.cos(t1_rad) + self.l2 * np.cos(t1_rad + t2_rad)
        y = self.l1 * np.sin(t1_rad) + self.l2 * np.sin(t1_rad + t2_rad)
        
        return x, y 
        
        

    def plot_arm(self, theta1, theta2):
        if theta1 is None or theta2 is None:
            print("No se pueden graficar las posiciones debido a un error en el cálculo de los ángulos")
        else:
            t1_rad = np.radians(theta1)
            t2_rad = np.radians(theta2)
            
            # Calcular posiciones de las articulaciones
            x0, y0 = 0, 0
            x1 = self.l1 * np.cos(t1_rad)
            y1 = self.l1 * np.sin(t1_rad)
            x2 = x1 + self.l2 * np.cos(t1_rad + t2_rad)
            y2 = y1 + self.l2 * np.sin(t1_rad + t2_rad)
            
            # Graficar el brazo
            fig, ax = plt.subplots(figsize=(8, 8))
            #Segmentos
            ax.plot([x0, x1], [y0, y1], '-', color="black", linewidth=5)
            ax.plot([x1, x2], [y1, y2], '-', color="black", linewidth=5)
            #Puntos
            ax.plot([x0, x1, x2], [y0, y1, y2], 'ro', markersize=10, zorder=2)
            #Arcos de los ángulos   
            r_arc = (l1+l2/2)*0.2
            arc1 = patches.Arc((x0, y0), r_arc, r_arc, angle=0, 
                            theta1=min(0, theta1), theta2=max(0, theta1), 
                            color='blue', linewidth=2, 
                            label=f'θ1 = {theta1:.2f}°')
            arc2 = patches.Arc((x1, y1), r_arc, r_arc, angle=theta2, 
                            theta1=min(0, theta1), theta2=max(0, theta1), 
                            color='green', linewidth=2, 
                            label=f'θ2 = {theta2:.2f}°')      
            ax.add_patch(arc1)
            ax.add_patch(arc2)
            ax.text(x0, y0 , 'θ1', color='blue', 
        fontweight='bold', ha='center', va='center')
            ax.text(x1, y1 , 'θ2', color='green', 
        fontweight='bold', ha='center', va='center')
            
            #Limites de trabajo
            workspace_max = plt.Circle((0, 0), self.max_reach, color='gray', alpha=0.1, label='Alcance Máximo')
            ax.add_patch(workspace_max)
            
            if self.min_reach > 1:
                workspace_min = plt.Circle((0, 0), self.min_reach, color='purple', alpha=0.1, label='Límite Interno')
                ax.add_patch(workspace_min)
            
            #Limites de la gráfica
            lim = self.l1 + self.l2 + 10
            ax.set_xlim(-lim, lim)
            ax.set_ylim(-lim, lim)
            
            #Aspecto 
            ax.set_aspect('equal', adjustable='box')
            ax.set_title(f"Configuración del Brazo")
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend(loc='upper right', fontsize=12, frameon=True, shadow=True)
            plt.show()
      
            
    def position_mapping(self,theta1_min, theta1_max, theta2_min, theta2_max, step_deg = 1):
        #Discretiza, restringe a angulos posibles, restringe a alcance real y mapea a coordenadas XY
        theta1_values = np.arange(theta1_min, theta1_max + step_deg, step_deg)
        theta2_values = np.arange(theta2_min, theta2_max + step_deg, step_deg)
        theta1,theta2 = np.meshgrid(theta1_values, theta2_values)
        
        x,y = self.dk(theta1, theta2)            
        return x,y
        
    def plot_mapping(self, x, y, physical_restrictions = [[],[]]):
        x_res =physical_restrictions[0]
        y_res =physical_restrictions[1]

        fig, ax = plt.subplots(figsize=(7, 7))
        ax.scatter(x, y, s=1, color='blue', alpha=0.5)
        ax.fill(x_res, y_res, color='red', alpha=0.3, label='Zona Restringida')
        ax.plot(x_res, y_res, color='darkred', linestyle='--', linewidth=2)
        ax.set_title("Mapa de Posiciones Alcanzables del Brazo")
        ax.set_xlabel("X (mm)")
        ax.set_ylabel("Y (mm)")
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.axis('equal')
        plt.show()
        
        
        
if __name__ == "__main__":
    l1 = 106.0
    l2 = 97.0
    mapping = Mapping2DArm(l1, l2)
    
    x_target = 100.0
    y_target = 100.0
    
    x_res = 
    y_res = 
    physical_restrictions = [x_res, y_res]
    
    
    angles = mapping.xy2ang.ik(x_target, y_target)
    if angles:
        theta1, theta2 = angles        
        mapping.plot_arm(theta1, theta2)
    theta1_values, theta2_values = mapping.position_mapping(theta1_min=0, theta1_max=180, theta2_min=-180, theta2_max = 0)
    mapping.plot_mapping(theta1_values, theta2_values)
    