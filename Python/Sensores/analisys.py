import numpy as np
import matplotlib.pyplot as plt

from cap_model import ModelCapacitor as mc
from ss_wien import Wien as wien
from escrutar import Escrutinio as ectr


class Analisys: 
    def __init__(self):
        self.IIcap = lambda c1,c2: c1 + c2
        self.w0 = lambda r1, r2, c1, c2: 1 / np.sqrt(r1 * r2 * c1 * c2)


    def hl2c(self, h_l_arr, show = True):
        C = []  # usar lista

        for hl in h_l_arr:
            model = mc(
                e_d=[2.8, 1.0006, 40.0],  # [PLA, aire, agua] 
                d_s=1.4e-3,                 
                h_right_copper=41.2/1000,
                h_left_copper=39.5/1000,
                w_up_copper=99.1/1000,
                w_down_copper=99.1/1000,
                h_in=34.8/1000,
                w_in=16.6/1000,
                h_level=hl,             
            )
            C.append(model.calculate_c())

        C = np.array(C)

        if h_l_arr.size > 3 and show == True:
            # Conversión de unidades
            h_plot = h_l_arr * 1000      # m → mm
            C_plot = C * 1e12            # F → pF

            # Graficar
            plt.plot(h_plot, C_plot)
            plt.xlabel("Nivel de líquido (mm)")
            plt.ylabel("Capacitancia (pF)")
            plt.title("Relación h-level vs Capacitancia")
            plt.grid(True)
            plt.show()

        return C
        

    def c2tf_an(self, Ra, Rb, R1, R2, C1_base, C2, h_1_arr):
        # Calcular capacitancias del sensor
        C1_sensor = self.hl2c(h_l_arr=h_1_arr, show=False)
        C1_total = self.IIcap(c1=C1_base, c2=C1_sensor)

        # Lista de funciones de transferencia
        G = []
        labels = ["G1 (h_low)", "G2 (h_mid)", "G3 (h_top)"]
        colores = ["#7e22ce", "#fb923c", "#f13cfb"]

        for c in C1_total:
            wm = wien(Ra, Rb, R1, R2, C1=c, C2=C2)
            num, den = wm.ss2tf()
            G.append((num, den))   

        # Crear objeto de escrutinio y graficar comparativa
        esc = ectr(G=G, types=["nd"] * len(G), col_G=colores, t_end=0.2, fs=2000)
        esc.plotComp(labels=labels)

    def r2tf_an(self):
        pass

    def rorc2w(self, w, R=None, C1=None, C2=None):
        if (R is not None) and (w is not None):
            return 1 / ((w**2) * R)

        elif (C1 is not None) and (C2 is not None)  and (w is not None):
            return 1 / ((w**2) * (C1 * C2 * 2))

        else:
            raise ValueError("Debes pasar R o bien C1 y C2")
        


    def randc2w(self, R1, R2, C1_range, C2, levels=20, show=True,traj1=None, traj2=None):
    

        # Rango de C1
        C1_vals = np.linspace(C1_range[0], C1_range[1], C1_range[2])
        # Rango de R1 (ejemplo: 1kΩ a 100kΩ)
        R_vals = np.linspace(1e3, 100e3, 200)

        # Malla
        C1_grid, R_grid = np.meshgrid(C1_vals, R_vals)

        # Calcular ω0 en cada punto
        W0 = self.w0(R_grid, R2, C1_grid, C2)

        # Gráfico
        fig, ax = plt.subplots(figsize=(8,6))
        cs = ax.contourf(C1_grid*1e12, R_grid/1e3, W0, levels=levels, cmap="viridis")
        cbar = fig.colorbar(cs)
        cbar.set_label("ω₀ [rad/s]")

        ax.set_xlabel("C1 [pF]")
        ax.set_ylabel("R1 [kΩ]")
        ax.set_title("Curvas de nivel de ω₀ en función de C1 y R1")

        # Dibujar trayectorias si existen
        if traj1 is not None:
            c1_vals = [p[0]*1e12 for p in traj1]   # convertir a pF
            r1_vals = [p[1]/1e3 for p in traj1]   # convertir a kΩ
            ax.plot(c1_vals, r1_vals, 'o-r', label="Trayectoria 1")

        if traj2 is not None:
            c1_vals = [p[0]*1e12 for p in traj2]
            r1_vals = [p[1]/1e3 for p in traj2]
            ax.plot(c1_vals, r1_vals, 's-b', label="Trayectoria 2")

        if traj1 is not None or traj2 is not None:
            ax.legend()

        if show:
            plt.show()

        return C1_grid, R_grid, W0

an = Analisys()

"""
# Definir niveles de líquido (en metros, por ejemplo)
h_levels = np.linspace(0,(34.8/1000), 100)  

# Calcular capacitancias
C_values = an.hl2c(h_levels)


# Tres niveles de líquido (en metros)
h_levels = np.array([0.000, 0.016, 0.04])  

# Parámetros del oscilador Wien
Ra = 20e3
Rb = 10e3
R1 = R2 = 10e3
C1_base = 10e-9 - 44.51*1e-12
C2 = 10e-9

# Ejecutar análisis
an.c2tf_an(Ra,Rb,R1,R2,C1_base,C2,h_levels)

# Usando resistencia
print(an.rorc2w(w = 10000, R=100))

# Usando capacitores
print(an.rorc2w(w =10000, C1=10e-9, C2=11e-9))

"""
R2 = 10e3
C2 = 10e-12

# Dos trayectorias de puntos (ejemplo)
trayectoria1 = [(10e-12, 5e3), (30e-12, 20e3), (80e-12, 60e3)]
trayectoria2 = [(20e-12, 10e3), (50e-12, 30e3), (90e-12, 80e3)]

# Llamada al método
an.randc2w(R1=10e3, R2=R2, C1_range=(1e-12, 100e-12, 200),
           C2=C2, levels=30,
           traj1=trayectoria1, traj2=trayectoria2)