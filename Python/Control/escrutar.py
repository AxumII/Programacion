import numpy as np
import control as ctrl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Estilo/figuras
plt.rcParams["figure.figsize"] = (7, 4)
plt.rcParams["axes.grid"] = True


class Escrutinio:
    """
    Analiza una función de transferencia SISO.
    - t_end: duración de la simulación temporal (s)
    - n_time: número de muestras del vector de tiempo
    """

    def __init__(self, G, t_end=2.0, n_time=2000):
        self.G = G
        self.t_end = float(t_end)
        self.n_time = int(n_time)
        self.t = np.linspace(0.0, self.t_end, self.n_time)  # vector de tiempo
        self.SS_G = ctrl.ss(G)  # por si luego quieres espacio de estados

    # ---- Cálculos base ----
    def impulso(self):
        t, y = ctrl.impulse_response(self.G, T=self.t)
        return t, np.squeeze(y)

    def zeros_polos(self):
        z = np.asarray(ctrl.zeros(self.G))
        p = np.asarray(ctrl.poles(self.G))
        return z, p

    def num_den_degrees(self):
        """Coeficientes num/den (1-D, sin ceros líderes) y grados."""
        ret = ctrl.tfdata(self.G)
        num, den = (ret[:2] if len(ret) >= 2 else ret)
        num = np.atleast_1d(np.squeeze(np.asarray(num, dtype=float)))
        den = np.atleast_1d(np.squeeze(np.asarray(den, dtype=float)))
        if num.size > 1:
            num = np.trim_zeros(num, 'f')
        if den.size > 1:
            den = np.trim_zeros(den, 'f')
        n_deg = max(num.size - 1, 0)
        d_deg = max(den.size - 1, 0)
        return num, den, n_deg, d_deg

    def bode_datos(self, omega_limits=(1e-1, 1e3), n=600, w=None, wrap_phase=False):
        """
        Devuelve (w, mag_db, phase_deg) sin usar ctrl.bode.
        Evalúa G(jw) con np.polyval. Robusto a tfdata que devuelve arreglos 0-D.

        wrap_phase=False -> fase "unwrapped" en grados (continua).
        wrap_phase=True  -> fase envuelta en [-180, 180] grados.
        """
        # Rejilla
        if w is None:
            w = np.logspace(np.log10(omega_limits[0]), np.log10(omega_limits[1]), int(n))
        else:
            w = np.asarray(w, dtype=float)

        # --- Coeficientes num/den robustamente ---
        num, den, _, _ = self.num_den_degrees()

        # --- Evaluar G(jw) ---
        jw = 1j * w
        H = np.polyval(num, jw) / np.polyval(den, jw)

        mag_db = 20.0 * np.log10(np.clip(np.abs(H), np.finfo(float).tiny, None))

        # Fase en grados
        phase_rad = np.unwrap(np.angle(H))
        phase_deg = np.degrees(phase_rad)
        if wrap_phase:
            # Mapear a [-180, 180]
            phase_deg = (phase_deg + 180.0) % 360.0 - 180.0

        mask = np.isfinite(mag_db) & np.isfinite(phase_deg)
        return w[mask], mag_db[mask], phase_deg[mask]

    # ---- Gráficos individuales (por si los quieres) ----
    def plot_impulso(self, label="G"):
        t, y = self.impulso()
        plt.figure()
        plt.plot(t, y, label=label)
        plt.title("Respuesta al impulso")
        plt.xlabel("t [s]"); plt.ylabel("y(t)")
        plt.legend(); plt.tight_layout(); plt.show()

    def plot_pzmap(self, label="G"):
        z, p = self.zeros_polos()
        _, _, n_deg, d_deg = self.num_den_degrees()
        ceros_inf = max(d_deg - n_deg, 0)

        fig, ax = plt.subplots()
        if z.size:
            ax.scatter(np.real(z), np.imag(z), marker='o', label=f"Ceros {label}")
        else:
            # añade entrada a la leyenda indicando ceros en ∞ si aplica
            if ceros_inf > 0:
                ax.plot([], [], marker='o', linestyle='None',
                        label=f"Ceros {label} ({ceros_inf} en ∞)")

        ax.scatter(np.real(p), np.imag(p), marker='x', label=f"Polos {label}")

        ax.axhline(0, linewidth=0.8); ax.axvline(0, linewidth=0.8)
        ax.set_title("Mapa Polos–Ceros")
        ax.set_xlabel("Re"); ax.set_ylabel("Im")
        ax.legend()
        # Asegurar al menos ±5 en Im y vista simétrica
        im_parts = np.concatenate([np.imag(a) for a in (z, p) if getattr(a, "size", 0)])
        max_im = float(np.max(np.abs(im_parts))) if im_parts.size else 0.0
        ymax = max(5.0, 1.1 * max_im)
        x0, x1 = ax.get_xlim()
        r = max(abs(x0), abs(x1), ymax)
        ax.set_xlim(-r, r)
        ax.set_ylim(-r, r)
        ax.set_aspect('equal', adjustable='box')
        fig.tight_layout(); plt.show()

    def plot_bode(self, omega_limits=(1e-1, 1e3), n=600, label="G", wrap_phase=True):
        w, mag_db, phase_deg = self.bode_datos(omega_limits, n, wrap_phase=wrap_phase)
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(7, 6))
        ax1.semilogx(w, mag_db, label=label)
        ax1.set_title("Bode - Magnitud")
        ax1.set_ylabel("|G(jω)| [dB]"); ax1.legend()

        ax2.semilogx(w, phase_deg, label=label)
        ax2.set_title("Bode - Fase" + (" (envuelta)" if wrap_phase else " (unwrapped)"))
        ax2.set_xlabel("ω [rad/s]"); ax2.set_ylabel("∠G(jω) [°]"); ax2.legend()
        # Guías en 0 y ±180°
        ax2.axhline(0, linewidth=0.8)
        ax2.axhline(180, linewidth=0.4, linestyle=':')
        ax2.axhline(-180, linewidth=0.4, linestyle=':')

        plt.tight_layout(); plt.show()

class PlotComp:
    """
    Comparaciones superpuestas entre dos funciones de transferencia.
    """
    def __init__(self, G1, G2, COL_G1 = "#7e22ce", COL_G2 = "#fb923c", t_end=2.0, n_time=2000):
        self.E1 = Escrutinio(G1, t_end=t_end, n_time=n_time)
        self.E2 = Escrutinio(G2, t_end=t_end, n_time=n_time)
        self.c1 = COL_G1
        self.c2 = COL_G2

    def impulsos(self, label1="G1", label2="G2"):
        t1, y1 = self.E1.impulso()
        t2, y2 = self.E2.impulso()
        t = t1 if t1.size <= t2.size else t2
        if y1.size != t.size: y1 = np.interp(t, t1, y1)
        if y2.size != t.size: y2 = np.interp(t, t2, y2)

        plt.figure()
        plt.plot(t, y1, label=label1, color=self.c1, linestyle='--',linewidth=2)
        plt.plot(t, y2, label=label2, color=self.c2, linestyle='--', linewidth=2)
        plt.title("Impulso")
        plt.xlabel("t [s]"); plt.ylabel("y(t)")
        plt.legend(); plt.tight_layout(); plt.show()

    def pzmap(self, label1="G1", label2="G2"):
        z1, p1 = self.E1.zeros_polos()
        z2, p2 = self.E2.zeros_polos()
        _, _, n1, d1 = self.E1.num_den_degrees()
        _, _, n2, d2 = self.E2.num_den_degrees()
        ceros_inf1 = max(d1 - n1, 0)
        ceros_inf2 = max(d2 - n2, 0)

        fig, ax = plt.subplots()

        # G1 (morado)
        if z1.size:
            ax.scatter(np.real(z1), np.imag(z1), marker='o',
                       facecolors='none', edgecolors=self.c1, label=f"Ceros {label1}")
        else:
            if ceros_inf1 > 0:
                ax.plot([], [], marker='o', linestyle='None',
                        markerfacecolor='none', markeredgecolor=self.c1,
                        label=f"Ceros {label1} ({ceros_inf1} en ∞)")
        ax.scatter(np.real(p1), np.imag(p1), marker='x',
                   c=self.c1, s=70, label=f"Polos {label1}")

        # G2 (naranja)
        if z2.size:
            ax.scatter(np.real(z2), np.imag(z2), marker='o',
                       facecolors='none', edgecolors=self.c2, label=f"Ceros {label2}")
        else:
            if ceros_inf2 > 0:
                ax.plot([], [], marker='o', linestyle='None',
                        markerfacecolor='none', markeredgecolor=self.c2,
                        label=f"Ceros {label2} ({ceros_inf2} en ∞)")
        ax.scatter(np.real(p2), np.imag(p2), marker='x',
                   c=self.c2, s=80, label=f"Polos {label2}")

        ax.axhline(0, linewidth=0.8); ax.axvline(0, linewidth=0.8)
        ax.set_title("Mapa Polos–Ceros")
        ax.set_xlabel("Re"); ax.set_ylabel("Im")
        ax.legend(loc="best")

        im_parts = np.concatenate([np.imag(a) for a in (z1, p1, z2, p2) if getattr(a, "size", 0)])
        max_im = float(np.max(np.abs(im_parts))) if im_parts.size else 0.0
        ymax = max(5.0, 1.1 * max_im)
        x0, x1 = ax.get_xlim(); r = max(abs(x0), abs(x1), ymax)
        ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_aspect('equal', adjustable='box')
        fig.tight_layout(); plt.show()

    def bodes(self, omega_limits=(1e-1, 1e3), n=800, label1="G1", label2="G2", wrap_phase=True):
        w = np.logspace(np.log10(omega_limits[0]), np.log10(omega_limits[1]), int(n))
        w1, mag1_db, ph1_deg = self.E1.bode_datos(w=w, wrap_phase=wrap_phase)
        w2, mag2_db, ph2_deg = self.E2.bode_datos(w=w, wrap_phase=wrap_phase)

        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(7, 6))
        ax1.semilogx(w1, mag1_db, label=label1, color=self.c1, linestyle='--',linewidth=2)
        ax1.semilogx(w2, mag2_db, label=label2, color=self.c2, linestyle='--', linewidth=2)
        ax1.set_title("Bode - Magnitud"); ax1.set_ylabel("[dB]"); ax1.legend()

        ax2.semilogx(w1, ph1_deg, label=label1, color=self.c1, linestyle='--',linewidth=2)
        ax2.semilogx(w2, ph2_deg, label=label2, color=self.c2, linestyle='--', linewidth=2)
        ax2.set_title("Bode - Fase" + (" (envuelta)" if wrap_phase else ""))
        ax2.set_xlabel("ω [rad/s]"); ax2.set_ylabel("[°]"); ax2.legend()

        ax2.axhline(0, linewidth=0.8)
        ax2.axhline(180, linewidth=0.4, linestyle=':')
        ax2.axhline(-180, linewidth=0.4, linestyle=':')

        plt.tight_layout(); plt.show()

# ------------------- Ejemplo de uso -------------------
if __name__ == "__main__":
    # Cierra figuras previas si corres varias veces
    plt.close('all')
    s = ctrl.tf('s')

    #G1 = (s-4)/(s**2+4*s+13 )
    #G2 = (s+4)/(s**2+4*s+13 )
    
    G1 = (1)/((s+2)**2*(1))
    G2 = (s)/((s+2)**2*(1))

    comp = PlotComp(G1, G2, t_end=3.0, n_time=3000)
    comp.impulsos("G1", "G2")
    comp.pzmap("G1", "G2")
    comp.bodes(omega_limits=(1e-1, 1e3), n=800, label1="G1", label2="G2", wrap_phase=False)

    pass
