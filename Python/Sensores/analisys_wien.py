import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.lines import Line2D
from cap_model import ModelCapacitor as mc
from ss_wien import Wien as wien
from escrutar import Escrutinio as ectr
from num_model_wien import NumModel as nwien


class Analisys: 
    def __init__(self, Ra, Rb, R1, R2, C1_base, C2, max_Cs,t_end):
        # Utilidades
        self.IIcap = lambda c1, c2: c1 + c2
        self.w0 = lambda r1, r2, c1, c2: 1 / np.sqrt(r1 * r2 * c1 * c2)

        # Parámetros del Wien
        self.Ra = Ra
        self.Rb = Rb
        self.R1 = R1
        self.R2 = R2
        self.C1_base = C1_base
        self.C2 = C2
        self.max_Cs = max_Cs
        self.t_end = t_end

        # Barrido de capacitancia del sensor
        self.C1_sensor = np.linspace(0.0, self.max_Cs, 3)  # 0 pF a 2000 pF (3 puntos)
        self.C1_total = self.IIcap(self.C1_base, self.C1_sensor)  # vector


    def c2tf(self):      
        # Lista de funciones de transferencia
        G = []  

        for c in self.C1_total:
            wm = wien(Ra = self.Ra, Rb = self.Rb, R1 = self.R1, R2 = self.R2, C1=c, C2 = self.C2)
            num, den = wm.ss2tf()
            G.append((num, den))   
        return G
        
    def c2tf_an(self):

        labels = ["G1 (h_low)", "G2 (h_mid)", "G3 (h_top)"]
        colores = ["#7e22ce", "#fb923c", "#f13cfb"]
        G = self.c2tf()
        # Crear objeto de escrutinio y graficar comparativa
        esc = ectr(G=G, types=["nd"] * len(G), col_G=colores, t_end=self.t_end, fs=5000)
        esc.plotComp(labels=labels)

    def wientf_an(self):
        filas = []
        G = self.c2tf()  # <- usar c2tf para obtener todas las FT

        for c, (num, den) in zip(self.C1_total, G):
            den = np.asarray(den, dtype=float).ravel()
            if den.size < 3:
                raise ValueError("Se esperaba un denominador al menos de orden 2.")

            # Si los coeficientes vinieran en orden descendente, invertir (heurística simple)
            if np.argmax(np.abs(den)) == 0:
                den = den[::-1]

            # Normalizar a0 = 1 (forma canónica 1 + (2ζ/ωn)s + (1/ωn²)s²)
            a2 = den[0]
            den_n = den / a2
            a1n = den_n[1]
            a0n = den_n[2]

            # Forma canónica: s^2 + 2*zeta*wn*s + wn^2
            wn_tf   = np.sqrt(a0n)
            zeta_tf = a1n / (2.0 * wn_tf)

            # Analítico (NumModel)
            nm = nwien(Ra=self.Ra, Rb=self.Rb, R1=self.R1, R2=self.R2, C1=c, C2=self.C2)
            wn_calc, zeta_calc = nm.calculate_tf_params()

            filas.append({
                "C1_total_F": float(c),
                "wn_tf": float(wn_tf),
                "wn_calc": float(wn_calc),
                "diff_wn": float(abs(wn_tf - wn_calc)),
                "zeta_tf": float(zeta_tf),
                "zeta_calc": float(zeta_calc),
                "diff_zeta": float(abs(zeta_tf - zeta_calc)),
            })

        return pd.DataFrame(filas)




    def rorc2w(self, w, R=None, C=None):
        if (R is not None) and (w is not None):
            return 1 / ((w) * R)

        elif (C is not None)  and (w is not None):
            return 1 / ((w) * (C))

        else:
            raise ValueError("Debes pasar R o bien C1 y C2")
        
    def randc1tow(self, Cs = None, R = None, plot = True):

        if (Cs is None) == (R is None):
            raise ValueError("Debes pasar únicamente C1 o únicamente R (no ambos).")

        if Cs is not None:
            x = np.asarray(Cs, dtype=float)
            if np.any(x <= 0) or self.C2 <= 0 or self.R1 <= 0 or self.R2 <= 0:
                raise ValueError("R1, R2, Cs y C2 deben ser positivos.")
            w = 1.0 / np.sqrt(self.R1 * self.R2 * ( x + self.C2) * self.C2)
            xlabel = "Cs [F]"
            title  = r"$\omega$ vs $C_s$"
        else:
            x = np.asarray(R, dtype=float)
            if np.any(x <= 0) or self.C1_base <= 0 or self.C2 <= 0:
                raise ValueError("R, C1_base y C2 deben ser positivos.")
            # usa C1_base fija y C2 fija del objeto
            Ceq = 2.0 * self.C1_base * self.C2
            w = np.sqrt(1.0 / (x * Ceq))
            xlabel = "R [Ω]"
            title  = r"$\omega$ vs $R$"

        if plot:

            fig, ax = plt.subplots()
            ax.plot(x, w)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(r"$\omega$  [rad/s]")
            ax.set_title(title)
            ax.grid(True, linestyle="--", alpha=0.5)
            plt.show()       

    def contour_candr2w(self, w_levels, R_range=(100, 50000), C_range=(1e-9, 1e-6), n=1000):
        levels = np.atleast_1d(np.array(w_levels, dtype=float))
        Rmin_ohm, Rmax_ohm = map(float, R_range)   # Ω
        Cmin_F,   Cmax_F   = map(float, C_range)   # F
        if (Rmin_ohm <= 0) or (Cmin_F <= 0) or (Rmax_ohm <= Rmin_ohm) or (Cmax_F <= Cmin_F):
            raise ValueError("Rangos inválidos para R (Ω) o C (F).")

        # Mallas en UNIDADES DE ENTRADA (Ω y F)
        R_ohm = np.linspace(Rmin_ohm, Rmax_ohm, n)     # Ω
        C_F   = np.linspace(Cmin_F,   Cmax_F,   n)     # F
        Rg_ohm, Cg_F = np.meshgrid(R_ohm, C_F)

        # ω = 1 / (R·C)
        W = 1.0 / (Rg_ohm * Cg_F)

        # Conversión 
        Rg_kohm = Rg_ohm / 1e3
        Cg_nF   = Cg_F   * 1e9

        colores = ["#7e22ce", "#fb923c", "#f13cfb"]
        if len(levels) > len(colores):
            raise ValueError(f"Hay {len(levels)} niveles pero solo {len(colores)} colores.")

        # Plot
        fig, ax = plt.subplots()
        CS = ax.contour(Rg_kohm, Cg_nF, W, levels=levels,
                        colors=colores[:len(levels)], linewidths=2)

        handles = [Line2D([0], [0], color=colores[i], lw=2) for i in range(len(levels))]
        labels  = [f"ω = {lvl:.0f} rad/s" for lvl in levels]
        ax.legend(handles, labels, loc="upper right", frameon=True, fontsize=9)

        ax.set_xlabel("R [kΩ]")   # mostrado en kΩ
        ax.set_ylabel("C [nF]")   # mostrado en nF
        ax.set_title("Curvas de nivel: ω = 1/(R·C)")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.set_xlim(Rmin_ohm / 1e3, Rmax_ohm / 1e3)
        ax.set_ylim(Cmin_F   * 1e9, Cmax_F   * 1e9)
        fig.tight_layout()
        plt.show()

        return {"R_kohm": Rg_kohm, "C_nF": Cg_nF, "w": W, "levels": levels, "CS": CS}


#############################################################
if __name__ == "__main__":
    #Multiplicadores de unidades
    M = 1e6
    k = 1e3
    m = 1e-3
    u = 1e-6
    n = 1e-9
    p = 1e-12


    # Parámetros del oscilador Wien
    Ra = 10*k           #Ohm
    Rb = 20*k           #Ohm
    R1 = 3.3*k           #Ohm
    R2 = 3.3*k           #Ohm
    C1_base = 100*n      #Faradios
    C2 = 100*n           #Faradios
    max_Cs = 50*p       #Faradios
    f = 0.1*k             #Hertz
    R_test = 3.3*k       #Ohm
    C_test = 1000*n       #Ohm
    t_end = 1

    w_levels=[3*k, 6*k, 60*k]
    R_range=(100,20*k)
    C_range=(1*n, 1*u)

    an = Analisys(Ra, Rb, R1, R2, C1_base, C2,max_Cs,t_end)

    def r():

        C_result = an.rorc2w(w=2*np.pi*f, R=R_test)/n
        R_result = an.rorc2w(w=2*np.pi*f, C=C_test)/k

        # Ejemplos de cálculo rápido
        print(f"Capacitancia nF: {C_result}")
        print(f"Resistencia kOhm: {R_result}")

    def tot():

        an.contour_candr2w(w_levels,R_range,C_range,n  = 1000)

        # ω vs Cs 
        Cs_vec = np.linspace(1*p, 1*n, 3000)
        an.randc1tow(Cs=Cs_vec)

        # ω vs R 
        R_vec = np.linspace(100,15*k , 3000)
        an.randc1tow(R=R_vec)

        # Ejecutar análisis y graficar comparativa
        an.c2tf_an()

        print(an.wientf_an())

    r()
    tot()
