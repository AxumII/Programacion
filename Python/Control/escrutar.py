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
   
    def plotComp(self, labels=None, min_imag_extent=5.0, other_responses = None, A = 1.0, w = 1.0):
        if labels is None:
            labels = [f"G{i+1}" for i in range(len(self.G))]
        
        # Decide la grilla según other_responses
        if other_responses:
            fig, axs = plt.subplots(3, 2, figsize=(12, 12))
            ax_imp   = axs[0, 0]
            ax_mag   = axs[0, 1]
            ax_pz    = axs[1, 0]
            ax_phase = axs[1, 1]
            ax_step  = axs[2, 0]
            ax_sin   = axs[2, 1]
        else:
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
            tout_imp, yimp = sg.impulse((num, den), T=self.t)
            ax_imp.plot(tout_imp, yimp, label=labels[i], color=self.col_G[i])

            # Bode (magnitud y fase)
            w, mag, phase = sg.bode((num, den))
            ax_mag.semilogx(w, mag, label=labels[i], color=self.col_G[i])
            ax_phase.semilogx(w, phase, label=labels[i], color=self.col_G[i])

            # Polos y ceros
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

            # Otras respuestas (opcional)
            if other_responses:
                # Escalón de amplitud A
                u_step = A * np.ones_like(self.t)
                tout, y_step, _ = sg.lsim((num, den), U=u_step, T=self.t, X0=self.x0)
                ax_step.plot(tout, y_step, label=labels[i], color=self.col_G[i])

                # Seno de amplitud A y frecuencia angular w (rad/s)
                u_sin = A * np.sin(w * self.t)
                tout, y_sin, _ = sg.lsim((num, den), U=u_sin, T=self.t, X0=self.x0)
                ax_sin.plot(tout, y_sin, label=labels[i], color=self.col_G[i])

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

        # Límites automáticos con mínimo deseado
        yext = max(min_imag_extent, max_imag_abs * 1.05)
        xext = max(min_imag_extent, max_real_abs * 1.05)
        ax_pz.set_ylim(-yext, yext)
        ax_pz.set_xlim(-xext, xext)

        if other_responses:
            ax_step.set_title(f"Respuesta al escalón (A = {A})")
            ax_step.set_xlabel("Tiempo [s]")
            ax_step.set_ylabel("Salida")
            ax_step.grid(True, which="both")
            ax_step.legend()

            ax_sin.set_title(f"Respuesta a seno (A = {A}, ω = {w} rad/s)")
            ax_sin.set_xlabel("Tiempo [s]")
            ax_sin.set_ylabel("Salida")
            ax_sin.grid(True, which="both")
            ax_sin.legend()

        fig.tight_layout()
        plt.show()
        return fig, axs
    
    def overshoot(self, A=1.0):
        results = []
        for Gi, typ in zip(self.G, self.types):
            num, den = self.ft_process(Gi, typ)

            # Entrada: escalón de amplitud A
            u = A * np.ones_like(self.t)

            # Simulación LTI con lsim (resp. al escalón A)
            tout, y, _ = sg.lsim((num, den), U=u, T=self.t, X0=self.x0)

            # Valor en régimen: promedio del 5% final
            k = max(1, int(len(y) // 20))  # 5%
            yss = float(np.mean(y[-k:]))

            # Pico
            i_peak = int(np.argmax(y))
            y_peak = float(y[i_peak])
            t_peak = float(tout[i_peak])

            # Overshoot relativo a |y_ss| (evita signo/0)
            if abs(yss) > 1e-12:
                OS = max(0.0, (y_peak - yss) / abs(yss)) * 100.0
            else:
                OS = 0.0

            results.append({"t_peak": t_peak, "y_peak": y_peak, "y_ss": yss, "%OS": OS})

        return results

# ----- Sistemas de ejemplo -----
# ----- Sistemas de ejemplo -----
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
esc.plotComp(labels=labels)
