import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sg


class Escrutinio:
    def __init__(self, G, types=None, col_G=None, t_end=2.0, fs=2000, x0=None):
        self.G = list(G) if not isinstance(G, list) else G
        if types is None:
            self.types = ["nd"] * len(self.G)
        else:
            self.types = list(types)
        if len(self.G) != len(self.types):
            raise ValueError("G y types deben tener la misma longitud.")

        self.col_G = col_G if col_G is not None else [None] * len(self.G)
        self.t_end = float(t_end)
        self.fs = int(fs)
        self.x0 = None if x0 is None else np.asarray(x0, dtype=float)

        npts = max(2, int(np.round(self.t_end * self.fs)))
        self.t = np.linspace(0.0, self.t_end, npts, endpoint=True)

    def normalize(self,num,den):
            num = np.asarray(num, dtype=float)
            den = np.asarray(den, dtype=float)
            if den.ndim != 1:
                den = np.squeeze(den)
            if num.ndim != 1:
                num = np.squeeze(num)
            if np.isclose(den[0], 0.0):
                nz = np.flatnonzero(~np.isclose(den, 0.0))
                if nz.size == 0:
                    raise ValueError("Denominador nulo.")
                den = den[nz[0]:]
            num = num / den[0]
            den = den / den[0]
            return num, den

    def ft_process(self, G, type):
        if type == "nd":
            num, den = G
            return self.normalize(num, den)
        elif type == "zpk":
            z, p, k = G
            num, den = sg.zpk2tf(z, p, k)
            return self.normalize(num, den)
        elif type == "ss":
            A, B, C, D = G
            num, den = sg.ss2tf(A, B, C, D)
            num = np.squeeze(num); den = np.squeeze(den)
            return self.normalize(num, den)
        else:
            raise ValueError(f"Tipo desconocido: {type}")
   

    def plotComp(self, labels=None, min_imag_extent=5.0):
        if labels is None:
            labels = [f"G{i+1}" for i in range(len(self.G))]
        fig, axs = plt.subplots(2, 2, figsize=(12, 9))
        ax_imp   = axs[0, 0]
        ax_mag   = axs[0, 1]
        ax_pz    = axs[1, 0]
        ax_phase = axs[1, 1]

        max_imag_abs = 0.0  # para tener cuadricula en caso de no tener valores imag
        max_real_abs = 0.0  # para tener cuadricula en caso de no tener valores real

        for i, (Gi, typ) in enumerate(zip(self.G, self.types)):
            num, den = self.ft_process(Gi, typ)
            # Impulso
            tout, yimp = sg.impulse((num, den), T=self.t)
            ax_imp.plot(tout, yimp, label=labels[i], color=self.col_G[i])

            # Bode (magnitud y fase)
            w, mag, phase = sg.bode((num, den))
            ax_mag.semilogx(w, mag, label=labels[i], color=self.col_G[i])
            ax_phase.semilogx(w, phase, label=labels[i], color=self.col_G[i])

            # Polos y ceros (abajo-izquierda)
            z, p, k = sg.tf2zpk(num, den)
            if z is not None and len(z) > 0:
                ax_pz.scatter(np.real(z), np.imag(z), marker='o', facecolors='none',
                            edgecolors=self.col_G[i], label=f"Ceros {labels[i]}")
                max_imag_abs = max(max_imag_abs, float(np.max(np.abs(np.imag(z)))))
                max_real_abs = max(max_real_abs, float(np.max(np.abs(np.real(z)))))
            if p is not None and len(p) > 0:
                ax_pz.scatter(np.real(p), np.imag(p), marker='x',
                            color=self.col_G[i], label=f"Polos {labels[i]}")
                max_imag_abs = max(max_imag_abs, float(np.max(np.abs(np.imag(p)))))
                max_real_abs = max(max_real_abs, float(np.max(np.abs(np.real(p)))))


        # Estética y etiquetas
        ax_imp.set_title("Respuesta al impulso")
        ax_imp.set_xlabel("Tiempo [s]")
        ax_imp.set_ylabel("Amplitud")
        ax_imp.grid(True, which="both")
        ax_imp.legend()

        ax_mag.set_title("Bode - Magnitud")
        ax_mag.set_ylabel("Magnitud [dB]")
        ax_mag.grid(True, which="both")
        ax_mag.legend()

        ax_phase.set_title("Bode - Fase")
        ax_phase.set_xlabel("Frecuencia angular [rad/s]")
        ax_phase.set_ylabel("Fase [°]")
        ax_phase.grid(True, which="both")
        ax_phase.legend()

        ax_pz.set_title("Diagrama de polos y ceros (plano s)")
        ax_pz.axhline(0, color='k', linewidth=0.8)
        ax_pz.axvline(0, color='k', linewidth=0.8)
        ax_pz.set_xlabel("Re{s}")
        ax_pz.set_ylabel("Im{s}")
        ax_pz.grid(True, which="both")
        ax_pz.legend()
        ax_pz.set_aspect('equal', adjustable='box')

        #y si hay polos mas grandes que 5i?

    

        min_imag_extent = 5.0 
        y = max(min_imag_extent, max_imag_abs * 1.05)  #retorna el maximo entre la max magnitud de ceros y polos y el min dado : 5
        ax_pz.set_ylim(-y, y)

        min_real_extent = 5.0 
        x = max(min_real_extent, max_real_abs * 1.05)  #retorna el maximo entre la max magnitud de ceros y polos y el min dado : 5
        ax_pz.set_xlim(-x, x)

        

        fig.tight_layout()
        plt.show()
        return fig, axs
    



# ----- Sistemas de ejemplo -----
"""# ----- Sistemas de ejemplo -----
z1 = [3.0]
p1 = [-1.0, -5.0]
k1 = 5.0

num2 = [1.0]
den2 = [1.0, 2.0, 2.0]

A = [[0.0, 1.0],
     [-4.0, -3.0]]
B = [[0.0],
     [1.0]]
C = [[1.0, 0.0]]
D = [[0.0]]

# G SOLO con tuplas de datos (sin etiquetas de texto)
G = [
    (z1, p1, k1),        # zpk
    (num2, den2),        # nd
    (A, B, C, D),        # ss
]
types = ["zpk", "nd", "ss"]

labels = ["G1 (zpk)", "G2 (nd)", "G3 (ss)"]
colores = ["#7e22ce", "#fb923c", "#f13cfb"]

esc = Escrutinio(G=G, types=types, col_G=colores, t_end=3.0, fs=2000)
esc.plotComp(labels=labels)"""
