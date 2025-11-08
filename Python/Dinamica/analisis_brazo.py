import numpy as np
import matplotlib.pyplot as plt

class Analisis:
    """
    Punto C: Punto de origen
    Punto B: Punto del codo
    Punto A: Punto de la pinza
    
    
    
    """

    def __init__(self,t,theta_1,theta_2,L1,L2):
        self.t = t
        self.theta_1 = theta_1
        self.theta_2 = theta_2
        self.L1 = float(L1)     # |BC|
        self.L2 = float(L2)     # |AB|
        
        self.omega_1,self.alpha_1 = self.variables_of_motion(theta=self.theta_1) #Angular en el brazo
        self.omega_2,self.alpha_2 = self.variables_of_motion(theta=self.theta_2) #Angular en el antebrazo relativa
        
        self.posx = lambda L,theta : L * np.cos(theta)
        self.posy = lambda L,theta : L * np.sin(theta)     
        
        self.graf()
        
    
    def variables_of_motion(self, theta):
        omega = np.gradient(theta, self.t, axis = 0)
        alpha = np.gradient(omega, self.t, axis = 0)
        return omega, alpha
        
    def kinematic_single(self, w, alpha, r):
        zeros = np.zeros_like(w)
        w_vec = np.stack([zeros, zeros, w], axis=1)           # (N,3)
        a_vec = np.stack([zeros, zeros, alpha], axis=1)       # (N,3)
        V = np.cross(w_vec, r)
        a = np.cross(a_vec, r) + np.cross(w_vec, np.cross(w_vec, r))
        return V[:, :2], a[:, :2]

    def kinematic_general(self):
        rB = np.stack([self.L1*np.cos(self.theta_1),
                    self.L1*np.sin(self.theta_1),
                    np.zeros_like(self.theta_1)], axis=1)
        rAB = np.stack([self.L2*np.cos(self.theta_1 + self.theta_2),
                        self.L2*np.sin(self.theta_1 + self.theta_2),
                        np.zeros_like(self.theta_1)], axis=1)

        V_B, a_B = self.kinematic_single(self.omega_1, self.alpha_1, rB)
        V_A_B, a_A_B = self.kinematic_single(self.omega_1 + self.omega_2,
                                            self.alpha_1 + self.alpha_2, rAB)
        V_A = V_B + V_A_B
        a_A = a_B + a_A_B
        return np.array(V_B), np.array(V_A_B), np.array(V_A), np.array(a_B), np.array(a_A_B), np.array(a_A)

            
    def position(self):
        X_B = self.posx(self.L1, self.theta_1)
        Y_B = self.posy(self.L1, self.theta_1)
        X_A = X_B + self.posx(self.L2, self.theta_1 + self.theta_2)
        Y_A = Y_B + self.posy(self.L2, self.theta_1 + self.theta_2)
        return (X_B, Y_B), (X_A, Y_A)
        
        
        
        
    def graf(self):
        V_B, V_A_B, V_A, a_B, a_A_B, a_A = self.kinematic_general()
        (X_B, Y_B), (X_A, Y_A) = self.position()
        
        
        # θ
        plt.figure()
        plt.plot(self.t, self.theta_1, label='θ1')
        plt.plot(self.t, self.theta_2, label='θ2')
        plt.title('Ángulos articulares'); plt.xlabel('t [s]'); plt.ylabel('θ [rad]')
        plt.legend(); plt.grid(True)
        
        # ω
        plt.figure()
        plt.plot(self.t, self.omega_1, label='ω1')
        plt.plot(self.t, self.omega_2, label='ω2')
        plt.title('Velocidades angulares'); plt.xlabel('t [s]'); plt.ylabel('ω [rad/s]')
        plt.legend(); plt.grid(True)
        
        # α
        plt.figure()
        plt.plot(self.t, self.alpha_1, label='α1')
        plt.plot(self.t, self.alpha_2, label='α2')
        plt.title('Aceleraciones angulares'); plt.xlabel('t [s]'); plt.ylabel('α [rad/s²]')
        plt.legend(); plt.grid(True)
        
        # Velocidad de la pinza
        plt.figure()
        VA_mod = np.linalg.norm(V_A, axis=1) 
        plt.plot(self.t, VA_mod, label='|V_A|')
        plt.title('Velocidad lineal de la pinza'); plt.xlabel('t [s]'); plt.ylabel('V [m/s]')
        plt.legend(); plt.grid(True)
        
        # Aceleración de la pinza
        plt.figure()
        aA_mod = np.linalg.norm(a_A, axis=1)
        plt.plot(self.t, aA_mod, label='|a_A|')
        plt.title('Aceleración lineal de la pinza'); plt.xlabel('t [s]'); plt.ylabel('a [m/s²]')
        plt.legend(); plt.grid(True)
        
        # Trayectorias

        plt.figure()
        plt.plot(X_B, Y_B, label='Trayectoria codo B', color='tab:orange')
        plt.plot(X_A, Y_A, label='Trayectoria pinza A', color='tab:blue')

        # Puntos de inicio (verde) y fin (rojo)
        plt.scatter(X_B[0], Y_B[0], color='green', s=60, label='Inicio B')
        plt.scatter(X_A[0], Y_A[0], color='green', s=60, label='Inicio A')
        plt.scatter(X_B[-1], Y_B[-1], color='red', s=60, label='Fin B')
        plt.scatter(X_A[-1], Y_A[-1], color='red', s=60, label='Fin A')
                # Segmentos del brazo en la posición inicial (sólido) y final (discontinuo)
        plt.plot([0, X_B[0],  X_A[0]],  [0, Y_B[0],  Y_A[0]],  linewidth=2, label='Brazo (inicio)', color='green')
        plt.plot([0, X_B[-1], X_A[-1]], [0, Y_B[-1], Y_A[-1]], linewidth=2, label='Brazo (fin)', color='red')

        plt.axis('equal')
        plt.title('Trayectorias en el plano (inicio y fin)')
        plt.xlabel('X [m]')
        plt.ylabel('Y [m]')
        plt.legend()
        plt.grid(True)
        plt.show()

       
"""
# === Demostración ===
t = np.linspace(0, 5, 400)
theta1 = np.deg2rad(np.linspace(0, 80, 400))
theta2 = np.deg2rad(np.linspace(20, 120, 400))
modelo = Analisis(t, theta1, theta2, L1=0.5, L2=0.35)
modelo.graf()"""