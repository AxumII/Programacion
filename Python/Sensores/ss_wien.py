import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sg

class Wien:
    def __init__(self, Ra,Rb,R1,R2,C1,C2):
        self.Ra = float(Ra); self.Rb = float(Rb)
        self.R1 = float(R1); self.R2 = float(R2)
        self.C1 = float(C1); self.C2 = float(C2)

        # Ganancia lazo del opamp
        self.K = 1.0 + (self.Rb / self.Ra)

        # Matriz A
        A11 = -(1.0 - self.K)/(self.R2*self.C1) - 1.0/(self.R1*self.C1)
        A12 =  1.0/(self.R2*self.C1)
        A21 =  (1.0 - self.K)/(self.R2*self.C2)
        A22 = -1.0/(self.R2*self.C2)
        self.A = np.array([[A11, A12],
                           [A21, A22]], dtype=float)

        # Entrada ficticia (u=0)
        self.B = np.array([[1.0],
                   [0.0]], dtype=float)
        self.C = np.array([[self.K, 0.0]])
        self.D = np.zeros((1,1))

    def ss(self):
        return sg.StateSpace(self.A, self.B, self.C, self.D)
    
    def ss_out(self, t_sim=0.01, fs=1e5, x0=None):
        # condiciones iniciales
        if x0 is None:
            x0 = np.array([1.0, 0.0])
        else:
            x0 = np.asarray(x0, dtype=float)
            if x0.shape != (2,):
                raise ValueError("x0 debe ser un vector de longitud 2.")

        npts = int(t_sim * fs)
        t = np.linspace(0.0, float(t_sim), npts)
        u = np.zeros_like(t)  # entrada cero
        tout, y, x = sg.lsim(self.ss(), U=u, T=t, X0=x0)
        return tout, y.squeeze(), x
    
    def ss2tf(self):    
        num, den = sg.ss2tf(self.A, self.B, self.C, self.D)
        num = np.squeeze(num)
        den = np.squeeze(den)
        return num, den
    
    def graf_ss(self, t_sim=0.5, fs=1e5, x0=None, mostrar=True):
        tout, y, x = self.ss_out(t_sim=t_sim, fs=fs, x0=x0)

        plt.figure(); plt.plot(tout, x[:, 0])
        plt.xlabel("t [s]"); plt.ylabel("x1(t)")
        plt.title("Estado x1(t) — respuesta sin entrada")
        if mostrar: plt.show()

        plt.figure(); plt.plot(tout, x[:, 1])
        plt.xlabel("t [s]"); plt.ylabel("x2(t)")
        plt.title("Estado x2(t) — respuesta sin entrada")
        if mostrar: plt.show()

        plt.figure(); plt.plot(tout, y)
        plt.xlabel("t [s]"); plt.ylabel("y(t)")
        plt.title("Salida y(t) — respuesta sin entrada")
        if mostrar: plt.show()

        return tout, y, x
    
def exe():
# Valores de ejemplo (ajústalos a tu circuito)
    Ra = 20e3
    Rb = 10e3
    R1 = 10e3
    R2 = 10e3
    C1 = 10e-9
    C2 = 10e-9

    wien = Wien(Ra, Rb, R1, R2, C1, C2)

    # Espacio de estados y FT
    sys = wien.ss()
    num, den = wien.ss2tf()
    print("G(s) (coeficientes):")
    print("Numerador:", num)
    print("Denominador:", den)

    # Respuesta sin entrada (por condiciones iniciales)
    t, y, x = wien.graf_ss(t_sim=0.02, fs=1e5, x0=[1e-10, 0.0])


#exe()