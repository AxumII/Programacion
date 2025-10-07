import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sg

class LM2917:
    def __init__(self,Rp,Cp,Cf,Vz,Vspan,delta_f,w0):       


        self.Rp = float(Rp)
        self.Cp = float(Cp)
        self.Cf = float(Cf)
        self.Vz = float(Vz)
        self.Vspan = float(Vspan)
        self.delta_f = float(delta_f)


        self.A = np.array([[-1.0 / (self.Rp * self.Cf)]]) 
        self.B = np.array([[ (self.Vz * self.Cp) / (2.0 * np.pi * self.Cf) ]])  
        self.C = np.array([[ 1.0 ]])    
        self.D = np.array([[ 0.0 ]])                                       

        # Parámetros de salida (ganancia y offset de frecuencia)
        self.A_gain = self.Vspan / (self.Vz * self.Cp * self.Rp * self.delta_f)
        self.w0 = w0  
        # Offset para cero a w0
        self.Vref = (self.Vz * self.Cp * self.Rp / (2.0*np.pi)) * self.w0

    def _postproc(self, x):
        #Aplica offset y clamp.
        y_lin = self.A_gain * (x - self.Vref)
        y = np.maximum(0.0, y_lin)
        return y, y_lin

    def ss(self):
            return sg.StateSpace(self.A, self.B, self.C, self.D)
        
    def ss_out(self, t_sim=0.01, fs=1e5, u=None, x0=None):
        # condiciones iniciales
        if x0 is None:
            x0 = np.array([0.0])
        else:
            x0 = np.asarray(x0, dtype=float)
            if x0.shape != (1,):
                raise ValueError("x0 debe ser un vector de longitud 1.")
            
        npts = int(t_sim * fs)
        t = np.linspace(0.0, float(t_sim), npts, endpoint=False)
        if u is None:
            u = np.zeros_like(t)

        tout, y_raw, _ = sg.lsim(self.ss(), U=u, T=t, X0=x0)
        x = np.asarray(y_raw).reshape(-1)
        y, y_lin = self._postproc(x)  
        return tout, x, y, y_lin, u
    
    def ss2tf(self):    
        num, den = sg.ss2tf(self.A, self.B, self.C, self.D)
        num = np.squeeze(num)
        den = np.squeeze(den)
        return num, den


    def graf_ss(self, t_sim=0.5, fs=1e5, x0=None, mostrar=True, U=1.0, duty=0.5, w=1000.0):
        # ---------- Respuesta al IMPULSO (linearizada) ----------
        npts = int(t_sim*fs)
        t = np.linspace(0, t_sim, npts, endpoint=False)
        dt = 1.0/fs
        u_imp = np.zeros_like(t)
        u_imp[0] = 1.0/dt  # área ≈ 1 rad

        tout, x, y, y_lin, _ = self.ss_out(t_sim=t_sim, fs=fs, u=u_imp, x0=np.array([0.0]))

        # Linearizada (sin offset ni clamp): cae a 0
        y_imp_lin = self.A_gain * x
        plt.figure()
        plt.plot(tout, y_imp_lin)
        plt.xlabel("t [s]"); plt.ylabel("Vout lin [V]")
        plt.title("Respuesta a impulso (linearizada, sin offset ni clamp) — tiende a 0")
        plt.grid(True); plt.show()

        # ---------- Respuesta a UNA FRECUENCIA (constante) ----------
        # Interpretamos 'w' como ω absoluta (rad/s): ω(t) = w
        u_const = np.full_like(t, float(w))
        tout2, x2, y2, y2_lin, _ = self.ss_out(t_sim=t_sim, fs=fs, u=u_const, x0=x0)

        fin_hz = float(w)/(2*np.pi)  # solo para el título/etiquetas

        # Entrada (en Hz)
        plt.figure()
        plt.plot(tout2, u_const/(2*np.pi))
        plt.xlabel("t [s]"); plt.ylabel("f_in [Hz]")
        plt.title(f"Entrada constante: {fin_hz:.2f} Hz")
        plt.grid(True); plt.show()

        # Salida (con y sin clamp, con offset)
        plt.figure()
        plt.plot(tout2, y2_lin, label="y_lin (con offset, sin clamp)")
        plt.plot(tout2, y2,     label="y (con clamp)")
        plt.xlabel("t [s]"); plt.ylabel("Vout [V]")
        plt.title(f"Respuesta a frecuencia única: {fin_hz:.2f} Hz")
        plt.legend(); plt.grid(True); plt.show()


    #######################################
    # Parámetros de ejemplo 
def e():
    #Multiplicadores de unidades
    M = 1e6
    k = 1e3
    m = 1e-3
    u = 1e-6
    n = 1e-9
    p = 1e-12

    Rp = 14*k           #Ohm
    Cp = 22*n           #F
    Cf = 10*u         #F
    Vz = 7.56           #V
    Vspan = 5.0         #V
    delta_f = 400.0     # Hz

    f0   = 1_000.0
    w0   = 2*np.pi*f0
    lm   = LM2917(Rp, Cp, Cf, Vz, Vspan, delta_f, w0)
    lm.graf_ss(t_sim=0.5, fs=1e5, w=2*np.pi*1_000.0)  # ~0 V en régimen
    lm.graf_ss(t_sim=0.5, fs=1e5, w=2*np.pi*1_400.0)  # ~Vspan (si Δf=400 Hz y Vspan=5 V)


e()
