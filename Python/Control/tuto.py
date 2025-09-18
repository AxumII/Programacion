import numpy as np
import control as ctrl
import matplotlib.pyplot as plt

class Example:
    def __init__(self):
        s = ctrl.tf('s')
        self.T = np.linspace(0, 2, 2000)
        plt.rcParams["figure.figsize"] = (6, 4)

        #Planta 2 orden
        self.wn = 10.0
        self.zeta = 0.3
        self.G = ctrl.TransferFunction([self.wn**2], [1, 2*self.zeta*self.wn, self.wn**2])

        #SS
        A = np.array([[0, 1],
        [-(self.wn**2), -2*self.zeta*self.wn]])
        B = np.array([[0],
        [self.wn**2]])
        C = np.array([[1, 0]])
        D = np.array([[0]])

        self.sys_ss = ctrl.ss(A, B, C, D)

        # Bloques para operaciones
        self.G1 = 10/(self.s + 10)
        self.G2 = (self.s + 3)/(self.s + 1)
        self.H = 1/(self.s + 5)



#------------------Tiempo y Frecuencia basico 

#   SS to TF
    def SStoTF(self):        
        G_from_ss = ctrl.tf(self.sys_ss)
        print("TF desde SS:\n", G_from_ss)
        return G_from_ss

#   TF to SS
    def TFtoSS(self):
        SS_from_tf = ctrl.ss(self.G)
        print("SS desde TF:\n", SS_from_tf)
        return SS_from_tf

#   SS y impulso
    def SS_impulso(self):

        T_imp, y_imp = ctrl.impulse_response(self.sys_ss, T=self.T)

        #Ploteo
        plt.plot(T_imp, y_imp.T)
        plt.title("Impulso (SS)")
        plt.xlabel("t [s]"); plt.ylabel("y(t)"); plt.grid(True); plt.show()
        return T_imp, y_imp

#   SS y señal

    def SS_senal(self):

        # Señal arbitraria: pulso + seno 5 Hz
        U = ((self.T >= 0.2) & (self.T <= 0.6)).astype(float) + 0.5*np.sin(2*np.pi*5*self.T)

        T_for, y_for, x_for = ctrl.forced_response(self.sys_ss, self.T, U, X0=[0, 0])
        
        #Ploteo
        plt.plot(self.T, U, label="u(t)")
        plt.plot(T_for, y_for.T, label="y(t)")
        plt.title("SS + señal arbitraria")
        plt.xlabel("t [s]"); plt.grid(True); plt.legend(); plt.show()
        return T_for, y_for, x_for

#   TF y impulso
    def TF_impulso(self):

        T_imp, y_imp = ctrl.impulse_response(self.G, T=self.T)

        #Ploteo
        plt.plot(T_imp, y_imp)
        plt.title("Impulso (TF)")
        plt.xlabel("t [s]"); plt.ylabel("y(t)"); plt.grid(True); plt.show()
        return T_imp, y_imp

#   TF y señal

    def TF_senal(self):

        U = np.sin(2*np.pi*3*self.T) + (self.T > 1.0).astype(float) # seno + escalón en 1 s

        T_for, y_for, _ = ctrl.forced_response(self.G, self.T, U)

        #Ploteo
        plt.plot(self.T, U, label="u(t)")
        plt.plot(T_for, y_for, label="y(t)")
        plt.title("TF + señal arbitraria")
        plt.xlabel("t [s]"); plt.grid(True); plt.legend(); plt.show()
        return T_for, y_for

#-----------------Operaciones Transferencia

#   Serie
    def Serie(self):
        """Serie: Gs = G1 * G2"""
        Gs = ctrl.series(self.G1, self.G2)
        print("Serie (G1*G2):\n", Gs)
        return Gs

#   Paralelo
    def Paralelo(self):
        """Paralelo: Gp = G1 + G2"""
        Gp = ctrl.parallel(self.G1, self.G2)
        print("Paralelo (G1+G2):\n", Gp)
        return Gp

#   Retro
    def Retro(self):
        """Retroalimentación negativa: T = feedback(G1*G2, H)"""
        Gs = ctrl.series(self.G1, self.G2)
        T_cl = ctrl.feedback(Gs, self.H) # T = Gs/(1+Gs*H)
        print("Retro (feedback):\n", T_cl)
        return T_cl

#   Integrador
    def Integrador(self):
        """Devuelve un integrador 1/s y grafica su Bode (advertencia práctica: amplifica bajas f)."""
        ctrl.bode_plot(self.Gi, dB=True, deg=True)
        plt.suptitle("Bode Integrador (1/s)"); plt.show()
        return self.Gi

#   Derivador
    def Derivador(self):
        """Devuelve un derivador s y grafica su Bode (advertencia práctica: amplifica ruido)."""
        ctrl.bode_plot(self.Gd, dB=True, deg=True)
        plt.suptitle("Bode Derivador (s)"); plt.show()
        return self.Gd


#-----------------Analisis numerico

#   TF Zeros y Polos
    def TF_zeros_polos(self):
        """Imprime y devuelve ceros y polos de la TF base. Grafica pzmap."""
        p = ctrl.pole(self.G)
        z = ctrl.zero(self.G)
        print("Polos:", p)
        print("Ceros:", z if len(z) else "ninguno")
        ctrl.pzmap(self.G, Plot=True)
        plt.title("Mapa Polos-Ceros (G)"); plt.grid(True); plt.show()
        return z, p

#   Bode
    def Bode(self, omega_limits=(1e-1, 1e3)):
        """Bode de la TF base en rad/s."""
        ctrl.bode_plot(self.G, dB=True, deg=True, Hz=False, omega_limits=omega_limits)
        plt.suptitle("Bode de G"); plt.show()

#   Error estado estacionario

    


    # ----------------- Análisis de Propiedades (SS) ----------------- #


    def Controlabilidad(self):
        """Rango de la matriz de controlabilidad y veredicto."""

        Ctrb = ctrl.ctrb(self.sys_ss.A, self.sys_ss.B)
        rank_ctrb = np.linalg.matrix_rank(Ctrb)
        n = self.sys_ss.A.shape[0]
        print(f"rank(ctrb) = {rank_ctrb} de {n} -> {'Controlable' if rank_ctrb==n else 'No controlable'}")
        return rank_ctrb, Ctrb


    def Observabilidad(self):
        """Rango de la matriz de observabilidad y veredicto."""

        Obsv = ctrl.obsv(self.sys_ss.A, self.sys_ss.C)
        rank_obsv = np.linalg.matrix_rank(Obsv)
        n = self.sys_ss.A.shape[0]
        print(f"rank(obsv) = {rank_obsv} de {n} -> {'Observable' if rank_obsv==n else 'No observable'}")
        return rank_obsv, Obsv


    def Sensitividad(self):
        """Calcula y grafica S=1/(1+L) y T=L/(1+L)."""
        S = ctrl.feedback(1, self.L)
        T = ctrl.feedback(self.L, 1)
        w = np.logspace(-2, 3, 400)
        
        ctrl.bode_plot(S, dB=True, Hz=False, omega=w)
        plt.suptitle("Bode de S (Sensitividad)"); plt.show()
        ctrl.bode_plot(T, dB=True, Hz=False, omega=w)
        plt.suptitle("Bode de T (Complementaria)"); plt.show()
        return S, T