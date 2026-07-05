import numpy as np
import matplotlib.pyplot as plt

class Accuracy:
    def __init__(self, W_custom, H_custom, E=1):
        self.E = E
        self.W_custom = np.array(W_custom)
        self.H_custom = np.array(H_custom)
    
    def calculate(self, W, H):
        # Si H > 500 usa H, de lo contrario usa H / 2
        H_transformado = np.where(H > 500, H, H / 2)
        
        return self.E * (0.15 * (200 / W) + 0.85 * H_transformado)
        
    
    def plot_contour_line(self, w_range, h_range, num_levels=20):
        """
        Calcula y grafica las curvas de nivel junto con la evolución de la torre (todo en mm).
        """
        W_grid, H_grid = np.meshgrid(w_range, h_range)
        Z = self.calculate(W_grid, H_grid)
        
        # Dibujar las curvas de nivel
        contour = plt.contour(W_grid, H_grid, Z, levels=num_levels, cmap='viridis')
        plt.clabel(contour, inline=True, fmt='%.1f', fontsize=8)
        plt.colorbar(contour, label='Valor de Accuracy')
        
        # Graficar la trayectoria de la torre (en mm)
        plt.plot(self.W_custom, self.H_custom, color='red', linestyle='-', alpha=0.6, label='Evolución de la Torre')
        plt.scatter(self.W_custom, self.H_custom, color='red', marker='o', s=80, zorder=5)
        
        # Etiquetar cada módulo
        for i in range(len(self.W_custom)):
            plt.text(self.W_custom[i] + 4, self.H_custom[i], f'Mód {i+1}', fontsize=9, verticalalignment='center')
        
        plt.title('Curvas de Nivel (mm) con Penalización < 500mm')
        plt.xlabel('Peso Total Acumulado (W) [g]')
        plt.ylabel('Altura Total Acumulada (H) [mm]')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()
        # Guardar resultado
        #plt.savefig('contour_tower_mm.png', bbox_inches='tight')
        plt.close()

# --- EJECUTABLE EN MILÍMETROS ---
if __name__ == "__main__":
    # 1. Definir los pesos (en gramos)
    modulos_base = np.array([25,30,45,50,65]) 
    peso_columnas_por_piso = 13 * 4
    pesos_individuales = modulos_base + peso_columnas_por_piso
    
    # 2. Definir la altura por módulo 
    altura_por_modulo_mm = 220 
    alturas_individuales = np.full(len(pesos_individuales), altura_por_modulo_mm)
    
    # 3. Calcular los vectores acumulados
    W_acumulado = np.cumsum(pesos_individuales)  + 20
    H_acumulado = np.cumsum(alturas_individuales)
    
    print("--- DATOS FÍSICOS DE LA TORRE (MÓDULOS EN mm) ---")
    print("Pesos acumulados totales (W) [g]:   ", W_acumulado)
    print("Alturas acumuladas totales (H) [mm]:", H_acumulado)
    
    # Evaluar el valor de Accuracy real en cada piso construido para control
    for i in range(len(W_acumulado)):
        val = Accuracy(W_acumulado, H_acumulado).calculate(W_acumulado[i], H_acumulado[i])
        print(f" -> Módulo {i+1}: H = {H_acumulado[i]}mm | Accuracy Final = {val:.2f}mm")
    
    # 4. Configurar los rangos de la gráfica en mm de forma dinámica
    w_intervalo = np.linspace(W_acumulado.min() - 20, W_acumulado.max() + 30, 100)
    h_intervalo = np.linspace(H_acumulado.min() - 50, H_acumulado.max() + 100, 100)
    
    # 5. Instanciar la clase y generar mapa de contornos
    torre = Accuracy(W_custom=W_acumulado, H_custom=H_acumulado, E=1)
    torre.plot_contour_line(w_intervalo, h_intervalo, num_levels=30)
    print("\nGráfica en mm guardada exitosamente como 'contour_tower_mm.png'")