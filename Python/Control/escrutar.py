import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sg
import pandas as pd



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
        """
        Permite que pasando una lista de sistemas, actue en modos por defaullt
        Si no hay tipos, todos seran num/den
        Si no hay color, sera por defecto de matplotlib
        Si no hay x0, sera None
        Crea el vector de tiempo       
        
        """
        
    def normalize(self,num,den):
            num = np.asarray(num, dtype=float)
            den = np.asarray(den, dtype=float)
            if den.ndim != 1:
                den = np.squeeze(den)
            if np.isclose(den[0], 0.0):
                nz = np.flatnonzero(~np.isclose(den, 0.0))
                if nz.size == 0:
                    raise ValueError("Denominador nulo.")
                den = den[nz[0]:]
            num = num / den[0]
            den = den / den[0]
            return num, den
    """
            Quita valores del polinomio de orden mayor que son 0
            Divide todos sobre el de orden mayor para que sea 1       
        """
        
    def ft_process(self, G, type):
        """
        Convierte cualquier tipo de representación en (num, den) normalizados.
        Soporta: "nd", "zpk", "ss", "fopdt"
        """
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
            num = np.squeeze(num)
            den = np.squeeze(den)
            return self.normalize(num, den)

        elif type == "fopdt":
            # G = (alpha, tau, L)
            alpha, tau, L = G

            # Primer orden
            num_proc = [alpha]
            den_proc = [tau, 1]

            # Aproximación de Padé del retardo puro e^{-Ls} (orden 1)
            num_delay, den_delay = sg.pade(L, 1)

            # Combinar proceso y retardo
            num_total = np.polymul(num_proc, num_delay)
            den_total = np.polymul(den_proc, den_delay)

            return self.normalize(num_total, den_total)

        else:
            raise ValueError(f"Tipo desconocido: {type}")
    """
            Modifica para que de acuerdo al tipo, la salida siempre sea num/den
            normalizado      
        """
        
    def plotComp(self, labels=None, min_imag_extent=5.0, other_responses = None, A = 1.0, w_sin = 100.0):
        if labels is None:
            labels = [f"G{i+1}" for i in range(len(self.G))]
        
        # Decide la grilla según la cantidad de respuestas
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

                # Seno de amplitud A y frecuencia angular w_sin (rad/s)
                u_sin = A * np.sin(w_sin * self.t)
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

            ax_sin.set_title(f"Respuesta a seno (A = {A}, ω = {w_sin:.2f} rad/s ≈ {w_sin/(2*np.pi):.2f} Hz)")
            ax_sin.set_xlabel("Tiempo [s]")
            ax_sin.set_ylabel("Salida")
            ax_sin.grid(True, which="both")
            ax_sin.legend()

        fig.tight_layout()
        plt.show()
        return fig, axs

    def data(self, A=1.0, tol=0.02):
        """
        Calcula métricas dinámicas para cada sistema y muestra una tabla en Matplotlib.
        Incluye:
        - %OS: sobrepico
        - y_ss: valor en régimen
        - t_pico: tiempo hasta el pico máximo
        - t_asentamiento: tiempo de asentamiento (±tol)
        - e_ss: error estacionario
        - wn: frecuencia natural (modo dominante)
        - zeta: coeficiente de amortiguamiento (modo dominante)
        - tau: constante de tiempo dominante
        - alpha: coeficiente de decaimiento
        - L: tiempo muerto aproximado
        Devuelve un pandas.DataFrame.
        """
        resultados = []

        for i, (Gi, typ) in enumerate(zip(self.G, self.types)):
            num, den = self.ft_process(Gi, typ)

            # --- Simulación de respuesta al escalón ---
            u = A * np.ones_like(self.t)
            tout, y, _ = sg.lsim((num, den), U=u, T=self.t, X0=self.x0)

            # --- Valor en régimen (promedio del último 5%) ---
            k = max(1, int(len(y) // 20))
            y_ss = float(np.mean(y[-k:]))

            # --- Error estacionario ---
            e_ss = A - y_ss

            # --- Sobrepico ---
            i_pico = int(np.argmax(y))
            y_pico = float(y[i_pico])
            t_pico = float(tout[i_pico])
            OS = max(0.0, (y_pico - y_ss) / abs(y_ss)) * 100.0 if abs(y_ss) > 1e-12 else 0.0

            # --- Tiempo de asentamiento (banda ±tol del valor final) ---
            b1 = y_ss * (1 + tol)
            b2 = y_ss * (1 - tol)
            b_low, b_high = (b1, b2) if b1 <= b2 else (b2, b1)  # Corrige caso y_ss negativo

            inside = (y >= b_low) & (y <= b_high)
            idx_dentro = np.where(inside)[0]

            if len(idx_dentro) == 0:
                t_asentamiento = np.nan
            else:
                idx_final = None
                for j in range(len(idx_dentro)):
                    if np.all(inside[idx_dentro[j]:]):
                        idx_final = idx_dentro[j]
                        break
                if idx_final is not None:
                    t_asentamiento = float(tout[idx_final])
                else:
                    t_asentamiento = np.nan

            # --- Frecuencia natural y zeta (versión original tuya) ---
            try:
                polos = np.roots(den)
                n = len(polos)

                if n == 1:
                    wn, zeta = np.nan, np.nan

                elif n == 2:
                    p1, p2 = polos
                    wn = np.sqrt(p1 * p2)
                    wn = abs(wn.real)
                    zeta = - (p1 + p2).real / (2 * wn)

                else:
                    polos_ordenados = sorted(polos, key=lambda p: p.real, reverse=True)
                    p1, p2 = polos_ordenados[:2]
                    wn = np.sqrt(p1 * p2)
                    wn = abs(wn.real)
                    zeta = - (p1 + p2).real / (2 * wn)
            except Exception:
                wn, zeta = np.nan, np.nan

            # --- Cálculo de tau, alpha y L ---
            try:
                polos = np.roots(den)
                if len(polos) > 0:
                    p_dom = polos[np.argmin(np.abs(np.real(polos)))]
                    alpha = abs(np.real(p_dom))
                    tau = 1.0 / alpha if alpha != 0 else np.nan
                else:
                    alpha, tau = np.nan, np.nan
            except Exception:
                alpha, tau = np.nan, np.nan

            # --- Tiempo muerto L (basado en 5% de |y_ss|) ---
            try:
                umbral = 0.05 * abs(y_ss)
                idx_L = np.where(np.abs(y) >= umbral)[0]
                L = tout[idx_L[0]] if len(idx_L) > 0 else np.nan
            except Exception:
                L = np.nan

            resultados.append({
                "Sistema": f"G{i+1}",
                "%OS": OS,
                "y_ss": y_ss,
                "t_pico": t_pico,
                "t_asentamiento": t_asentamiento,
                "e_ss": e_ss,
                "wn": wn,
                "zeta": zeta,
                "tau": tau,
                "alpha": alpha,
                "L": L
            })

        # --- Convertir a DataFrame ---
        df = pd.DataFrame(resultados)

        # === Mostrar tabla en Matplotlib ===
        fig, ax = plt.subplots(figsize=(12, 2 + 0.4 * len(df)))
        ax.axis('off')
        tabla = ax.table(
            cellText=df.round(3).values,
            colLabels=df.columns,
            loc='center',
            cellLoc='center'
        )
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(9)
        tabla.scale(1.2, 1.3)
        ax.set_title("Resultados dinámicos de los sistemas", fontsize=14, fontweight="bold", pad=20)
        plt.show()

        return df


"""

# ----- Sistemas de ejemplo ampliados -----

# 1️⃣ Sistema subamortiguado (zpk)
z1 = [3.0]
p1 = [-1.0, -5.0]
k1 = 5.0
G1 = (z1, p1, k1)   # zpk

# 2️⃣ Sistema subamortiguado (nd): ζ < 1
num2 = [1.0]
den2 = [1.0, 2.0, 2.0]  # ζ = 0.707, wn = √2
G2 = (num2, den2)

# 3️⃣ Sistema críticamente amortiguado (nd): ζ = 1
num3 = [1.0]
den3 = [1.0, 2.0, 1.0]  # (s+1)^2
G3 = (num3, den3)

# 4️⃣ Sistema sobreamortiguado (nd): ζ > 1
num4 = [1.0]
den4 = [1.0, 4.0, 8.0]  # polos reales negativos distintos
G4 = (num4, den4)

# 5️⃣ Sistema integrador puro (nd)
num5 = [1.0]
den5 = [1.0, 0.0]  # G(s) = 1/s
G5 = (num5, den5)

# 6️⃣ Sistema de espacio de estados (segundo orden)
A = [[0.0, 1.0],
     [-4.0, -3.0]]
B = [[0.0],
     [1.0]]
C = [[1.0, 0.0]]
D = [[0.0]]
G6 = (A, B, C, D)

# 7️⃣ Sistema con ceros complejos (zpk)
z7 = [-1 + 2j, -1 - 2j]
p7 = [-0.5, -4.0, -8.0]
k7 = 10.0
G7 = (z7, p7, k7)

# Lista completa de sistemas
G = [G1, G2, G3, G4, G5, G6, G7]
types = ["zpk", "nd", "nd", "nd", "nd", "ss", "zpk"]

labels = [
    "G1 zpk (subamort.)",
    "G2 nd (subamort.)",
    "G3 nd (crítico)",
    "G4 nd (sobreamort.)",
    "G5 nd (integrador)",
    "G6 ss (espacio-estado)",
    "G7 zpk (ceros complejos)"
]

colores = [
    "#7e22ce", "#fb923c", "#16a34a",
    "#dc2626", "#0ea5e9", "#9333ea", "#facc15"
]

# Crear objeto de análisis
esc = Escrutinio(G=G, types=types, col_G=colores, t_end=10.0, fs=2000)

# 🔹 Comparación general
esc.plotComp(labels=labels, other_responses=True)

# 🔹 Análisis cuantitativo + gráfico de métricas
df = esc.data(A=1.0)
print("\n===== RESULTADOS =====")
print(df.to_string(index=False))

"""