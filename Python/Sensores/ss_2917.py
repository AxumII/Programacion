import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sg

class LM2917:
    def __init__(self,Rl,Cl,Cf,Vz,Vspan,delta_f):
        self.Rl = float(Rl)
        self.Cl = float(Cl)
        self.Cf = float(Cf)
        self.Vz = float(Vz)
        self.Vspan = float(Vspan)
        self.delta_f = float(delta_f)

        # Dinámica del nodo CP2 (1 polo)
        self.A = np.array([[-1.0 / (self.Rl * self.Cf)]])                        
        self.B = np.array([[ (self.Vz * self.Cl) / (2.0 * np.pi * self.Cf) ]])       
        # C=1 para que lsim nos devuelva el estado x (= v_CP2); salida real la calculamos fuera
        self.C = np.array([[ 1.0 ]])    
        self.D = np.array([[ 0.0 ]])                                       

        # Parámetros de salida (ganancia y offset de frecuencia)
        # A_gain = Vspan / (Vz * Cl * Rl * delta_f)
        self.A_gain = self.Vspan / (self.Vz * self.Cl * self.Rl * self.delta_f)
        self.w0 = 0.0  # <- asigna 2*pi*f0 desde tu script para fijar el cero en f0

    # ---- Helpers para salida con offset y clamp ----
    def _vref(self):
        # Vref = (Vz * Cl * Rl / (2π)) * w0
        return (self.Vz * self.Cl * self.Rl / (2.0*np.pi)) * self.w0

    def _y_from_x(self, x):
        y_lin = self.A_gain * (x - self._vref())
        y = np.maximum(0.0, y_lin)  # clamp a 0 V
        return y, y_lin

    # ---- API original (sin cambios de firma) ----
    def ss(self):
        return sg.StateSpace(self.A, self.B, self.C, self.D)
    
    def ss_out(self, t_sim=0.01, fs=1e5, x0=None):
        # condiciones iniciales
        if x0 is None:
            x0 = np.array([0.0])
        else:
            x0 = np.asarray(x0, dtype=float)
            if x0.shape != (1,):
                raise ValueError("x0 debe ser un vector de longitud 1.")

        npts = int(t_sim * fs)
        t = np.linspace(0.0, float(t_sim), npts, endpoint=False)
        u = np.zeros_like(t)  # entrada cero
        tout, y_raw, _x = sg.lsim(self.ss(), U=u, T=t, X0=x0)

        # Como C=1 y D=0, y_raw = x (estado). Construimos salida real con offset y clamp:
        x = np.asarray(y_raw).reshape(-1)        # estado 1-D
        y, _ = self._y_from_x(x)                 # salida con offset y clamp
        return tout, y.squeeze(), x
    
    def ss2tf(self):    
        num, den = sg.ss2tf(self.A, self.B, self.C, self.D)
        num = np.squeeze(num)
        den = np.squeeze(den)
        return num, den
    
    def graf_ss(self, t_sim=0.5, fs=1e5, x0=None, mostrar=True):
        tout, y, x = self.ss_out(t_sim=t_sim, fs=fs, x0=x0)

        plt.figure(); plt.plot(tout, x)          # <- x es 1-D, no x[:,0]
        plt.xlabel("t [s]"); plt.ylabel("x1(t) = v_CP2 [V]")
        plt.title("Estado x1(t) — entrada nula")
        if mostrar: plt.show()

        plt.figure(); plt.plot(tout, y)
        plt.xlabel("t [s]"); plt.ylabel("Vout [V]")
        plt.title("Salida y(t) — (con offset y clamp) entrada nula")
        if mostrar: plt.show()

        return tout, y, x
    
    def ss_out_square(self, w, t_sim=0.5, fs=1e5, U=1.0, duty=0.5, x0=None):
        if w <= 0:
            raise ValueError("w debe ser > 0 (rad/s).")
        if not (0.0 < duty < 1.0):
            raise ValueError("duty debe estar en (0, 1).")
        
        npts = int(t_sim * fs)
        t = np.linspace(0.0, float(t_sim), npts, endpoint=False)
        u = U * sg.square(w * t, duty=duty)

        tout, y_raw, _x = sg.lsim(self.ss(), U=u, T=t, X0=x0)
        x = np.asarray(y_raw).reshape(-1)
        y, y_lin = self._y_from_x(x)
        
        # --- Gráfica 1: entrada cuadrada ---
        plt.figure()
        plt.plot(t, u)
        plt.xlabel("t [s]"); plt.ylabel("ω_in(t) [rad/s]")
        plt.title(f"Entrada cuadrada — ω={w:.3g} rad/s, U={U}, duty={duty:.2f}")
        plt.grid(True); plt.show()

        # --- Gráfica 2: salida ---
        plt.figure()
        plt.plot(t, y_lin, label="y_lin (sin clamp)")
        plt.plot(t, y, label="y (con clamp)")
        plt.xlabel("t [s]"); plt.ylabel("Vout [V]")
        plt.title(f"Salida y(t) ante entrada cuadrada")
        plt.legend(); plt.grid(True); plt.show()

        return t, u, y, x


##########################################################
def exe():
    Rl = 10e3        # 10 kΩ
    Cl = 100e-9      # 100 nF
    Cf = 1e-6        # 1 uF
    Vz = 7.56        # zéner/ref
    Vspan = 5.0      # salto de salida deseado
    delta_f = 200.0  # Δf en Hz

    lm = LM2917(Rl, Cl, Cf, Vz, Vspan, delta_f)

    # >>> CERO A f0:
    f0 = 9_800.0        # Hz
    lm.w0 = 2*np.pi*f0  # rad/s

    # 1) Respuesta libre (entrada nula)
    t, y, x = lm.graf_ss(t_sim=0.2, fs=200_000, x0=np.array([0.5]))

    # 2) Respuesta a ω(t) cuadrada (opcional)
    w = 2*np.pi*1000    # cuadrada a 1 kHz
    t, u, y, x = lm.ss_out_square(w=w, t_sim=0.1, fs=200_000, U=1.0, duty=0.5)

exe()
