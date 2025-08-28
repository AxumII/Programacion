# Full executable demo with the Analisis class (no static methods) and synthetic data.
import numpy as np
import matplotlib.pyplot as plt

class Analisis:
    """
    t           : (N,) tiempos
    w1          : (N,3)  ω del motor en C, RELATIVA al marco de B (B-frame)
    w2          : (N,3)  ω del motor en B, ABSOLUTA en mundo (W-frame)
    w_o         : (N,3)  ω medida en la punta (solo para comparar)
    theta_init1 : (3,)   ángulo inicial RELATIVO de BC respecto a B
    theta_init2 : (3,)   ángulo inicial ABSOLUTO de AB respecto a A
    theta_o     : (3,)   ángulo inicial de la medición externa (opcional)
    L1, L2      : escalares, longitudes de BC y AB, respectivamente
    """
    def __init__(self,t,w1,w2,w_o,theta_init1,theta_init2,theta_o, L1,L2):
        self.t = t
        self.w1 = w1      # (N,3) RELATIVA (en marco B)
        self.w2 = w2      # (N,3) ABSOLUTA (en mundo)
        self.w_o = w_o    # (N,3) medición externa (comparación)
        self.theta_init1 = theta_init1  # (3,) relativo
        self.theta_init2 = theta_init2  # (3,) absoluto
        self.theta_o     = theta_o      # (3,) (opcional)
        self.L1 = L1     # |BC|
        self.L2 = L2     # |AB|

        # resultados
        self.alpha1 = self.alpha2 = self.alpha_o = None
        self.theta1_rel = self.theta2_abs = self.theta_out = None
        self.r_BC_W = self.r_AB_W = None   # r1=BC en mundo, r2=AB en mundo
        self.RB = None                      # ^W R_B (matrices)
        self.w1_abs = None                  # ω de BC ABSOLUTA en mundo

    # -------- utilidades internas (métodos de instancia) --------
    def _R_zyx(self, phi, th, psi):
        cφ, sφ = np.cos(phi), np.sin(phi)
        cθ, sθ = np.cos(th),  np.sin(th)
        cψ, sψ = np.cos(psi), np.sin(psi)
        Rz = np.array([[cψ,-sψ,0],[sψ,cψ,0],[0,0,1]])
        Ry = np.array([[cθ,0,sθ],[0,1,0],[-sθ,0,cθ]])
        Rx = np.array([[1,0,0],[0,cφ,-sφ],[0,sφ,cφ]])
        return Rz @ Ry @ Rx   # ^W R (para los ángulos dados)

    def _cumtrapz_vec(self, y, x):
        # integral acumulada por trapecios (solo NumPy)
        dt   = np.diff(x)                       # (N-1,)
        mid  = 0.5 * (y[1:] + y[:-1])           # (N-1,3)
        out  = np.zeros_like(y)
        out[1:] = np.cumsum(mid * dt[:,None], axis=0)
        return out

    # ---------------- derivar e integrar ----------------
    def variables_of_motion_operator(self, w, t, theta_init):
        alpha = np.gradient(w, t, axis=0)            # (N,3)
        theta = self._cumtrapz_vec(w, t) + np.asarray(theta_init, float).reshape(1,3)
        return alpha, theta

    # vector barra alineada a +Z rotada por Euler ZYX (devuelve (N,3))
    def radius_operator(self, L, angle):
        phi = angle[:,0]; th = angle[:,1]; psi = angle[:,2]
        cφ, sφ = np.cos(phi), np.sin(phi)
        cθ, sθ = np.cos(th),  np.sin(th)
        cψ, sψ = np.cos(psi), np.sin(psi)
        x = L * (cψ*sθ*cφ - sψ*sφ)
        y = L * (sψ*sθ*cφ + cψ*sφ)
        z = L * (cθ * cφ)
        return np.column_stack([x,y,z])

    # ---------- estado (orientaciones, radios y ω absolutas) ----------
    def state_of_motion(self):
        # Eslabón AB (motor en B): ω2 es ABSOLUTA -> θ2_abs directamente
        self.alpha2, self.theta2_abs = self.variables_of_motion_operator(self.w2, self.t, self.theta_init2)

        # Matrices de rotación de B a mundo en cada instante
        N = self.t.size
        self.RB = np.empty((N,3,3))
        for i in range(N):
            phi, th, psi = self.theta2_abs[i]
            self.RB[i] = self._R_zyx(phi, th, psi)  # ^W R_B(i)

        # Eslabón BC (motor en C): ω1 es RELATIVA en marco B -> θ1_rel
        self.alpha1, self.theta1_rel = self.variables_of_motion_operator(self.w1, self.t, self.theta_init1)

        # Radios:
        self.r_AB_W = self.radius_operator(self.L2, self.theta2_abs)         # (N,3) AB en mundo
        r_BC_local  = self.radius_operator(self.L1, self.theta1_rel)         # (N,3) BC en marco B
        self.r_BC_W = np.einsum('nij,nj->ni', self.RB, r_BC_local)           # (N,3) BC en mundo

        # ω absolutas del segundo eslabón:
        w1_rel_W = np.einsum('nij,nj->ni', self.RB, self.w1)                 # (N,3)
        self.w1_abs = self.w2 + w1_rel_W
        self.alpha1 = np.gradient(self.w1_abs, self.t, axis=0)

        # Señal externa para comparar (no interviene en cinemática)
        self.alpha_o, self.theta_out = self.variables_of_motion_operator(self.w_o, self.t, self.theta_o)

        return (self.alpha1, self.theta1_rel, self.r_BC_W), (self.alpha2, self.theta2_abs, self.r_AB_W), (self.alpha_o, self.theta_out)

    # ---------------- posiciones y cinemática ----------------
    def tip_position(self):
        if self.r_BC_W is None or self.r_AB_W is None:
            self.state_of_motion()
        return self.r_AB_W + self.r_BC_W  # (N,3) posición C respecto a A (en mundo)

    def kinematic_single(self, w, alpha, r):
        V = np.cross(w, r)
        A = np.cross(alpha, r) + np.cross(w, np.cross(w, r))
        return V, A

    # Velocidad y aceleración de la punta C
    def kinematic_general(self):
        if self.r_BC_W is None or self.r_AB_W is None:
            self.state_of_motion()
        V_B,  A_B  = self.kinematic_single(self.w2,     self.alpha2, self.r_AB_W)
        V_Cb, A_Cb = self.kinematic_single(self.w1_abs, self.alpha1, self.r_BC_W)
        Va = V_B + V_Cb
        Aa = A_B + A_Cb
        return Va, Aa

    # ---------- estimación geométrica de ω en la punta ----------
    def w_tip_from_Va(self, V, r):
        denom = np.sum(r*r, axis=1, keepdims=True) + 1e-12
        return np.cross(r, V) / denom

    # ---------------- gráficos ----------------
    def graf(self):
        self.state_of_motion()
        Va, Aa = self.kinematic_general()
        t = self.t
        ejes = ['x', 'y', 'z']

        # 1) ω entradas y medición
        fig, axs = plt.subplots(3,1,figsize=(10,9),sharex=True)
        for i, ax in enumerate(axs):
            ax.plot(t, self.w1[:,i], label='w1 (rel en B)')
            ax.plot(t, self.w2[:,i], label='w2 (abs en W)')
            ax.plot(t, self.w_o[:,i], label='w_o (medición)')
            ax.set_ylabel(f'w_{ejes[i]} [rad/s]'); ax.grid(True); ax.legend()
        axs[-1].set_xlabel('t [s]'); fig.suptitle('ω entradas y medición'); plt.tight_layout(); plt.show()

        # 2a) alphas
        fig, axs = plt.subplots(3,1,figsize=(10,9),sharex=True)
        for i, ax in enumerate(axs):
            ax.plot(t, self.alpha1[:,i], label='alpha BC (abs)')
            ax.plot(t, self.alpha2[:,i], label='alpha AB (abs)')
            ax.plot(t, self.alpha_o[:,i], label='alpha_o (medida)')
            ax.set_ylabel(f'α_{ejes[i]} [rad/s²]'); ax.grid(True); ax.legend()
        axs[-1].set_xlabel('t [s]'); fig.suptitle('Aceleraciones angulares'); plt.tight_layout(); plt.show()

        # 2b) thetas
        fig, axs = plt.subplots(3,1,figsize=(10,9),sharex=True)
        for i, ax in enumerate(axs):
            ax.plot(t, self.theta1_rel[:,i], label='theta1 (rel)')
            ax.plot(t, self.theta2_abs[:,i], label='theta2 (abs)')
            ax.plot(t, self.theta_out[:,i], label='theta_o (medida)')
            ax.set_ylabel(f'θ_{ejes[i]} [rad]'); ax.grid(True); ax.legend()
        axs[-1].set_xlabel('t [s]'); fig.suptitle('Ángulos (rel/abs)'); plt.tight_layout(); plt.show()

        # 3a) Va por eje
        fig, axs = plt.subplots(3,1,figsize=(10,9),sharex=True)
        for i, ax in enumerate(axs):
            ax.plot(t, Va[:,i], label='Va (punta)')
            ax.set_ylabel(f'V_{ejes[i]} [m/s]'); ax.grid(True); ax.legend()
        axs[-1].set_xlabel('t [s]'); fig.suptitle('Velocidad lineal de la punta'); plt.tight_layout(); plt.show()

        # 3b) Aa por eje
        fig, axs = plt.subplots(3,1,figsize=(10,9),sharex=True)
        for i, ax in enumerate(axs):
            ax.plot(t, Aa[:,i], label='Aa (punta)')
            ax.set_ylabel(f'A_{ejes[i]} [m/s²]'); ax.grid(True); ax.legend()
        axs[-1].set_xlabel('t [s]'); fig.suptitle('Aceleración lineal de la punta'); plt.tight_layout(); plt.show()

        # 4) Trayectoria de la punta en el plano YZ
        r_tip = self.tip_position()
        y, z = r_tip[:,1], r_tip[:,2]
        fig, ax = plt.subplots(1,1,figsize=(6,6))
        ax.plot(y, z, label='trayectoria YZ')
        ax.scatter(y[0],  z[0],  s=30, marker='o', label='inicio')
        ax.scatter(y[-1], z[-1], s=30, marker='x', label='fin')
        ax.set_xlabel('Y [m]'); ax.set_ylabel('Z [m]')
        ax.set_aspect('equal', 'box'); ax.grid(True); ax.legend()
        ax.set_title('Movimiento de la punta en el plano YZ')
        plt.tight_layout(); plt.show()

        # 5) Comparación: w_o (medida) vs ω_tip (geométrica desde Va y r_tip)
        w_tip = self.w_tip_from_Va(Va, r_tip)
        fig, axs = plt.subplots(3,1,figsize=(10,9),sharex=True)
        for i, ax in enumerate(axs):
            ax.plot(t, self.w_o[:,i], label='w_o (medición)')
            ax.plot(t, w_tip[:,i],   label='w_tip (de Va, r_tip)')
            ax.set_ylabel(f'ω_{ejes[i]} [rad/s]'); ax.grid(True); ax.legend()
        axs[-1].set_xlabel('t [s]'); fig.suptitle('Comparación ω_out vs ω_tip'); plt.tight_layout(); plt.show()


# =================== DEMO / EJECUCIÓN ===================
# Datos sintéticos
N = 1200
t = np.linspace(0, 6, N)

# w2: ω del eslabón AB (absoluta en mundo). Predominantemente plano (z), con leves x,y.
w2 = np.zeros((N,3))
#w2[:,2] = 0.6 + 0.3*np.sin(0.7*t)         # z
w2[:,0] = 0.2     # x
#w2[:,1] = 0.05*np.cos(0.4*t - 0.2)        # y

# w1: ω del eslabón BC (RELATIVA a B). Principalmente z en el marco de B.
w1 = np.zeros((N,3))
#w1[:,2] = 1.2 + 0.2*np.sin(1.3*t + 0.3)   # z
w1[:,0] = 0.2              # x
#w1[:,1] = 0.02*np.cos(0.9*t)              # y

# Señal externa w_o: colocamos una versión "medida" basada en la ω estimada de la punta + ruido
# Inicialmente cero; luego la reemplazamos tras construir el objeto.
w_o = np.zeros_like(w1)

# Longitudes y ángulos iniciales
L2 = 0.6   # |AB|
L1 = 0.6   # |BC|
theta_init2 = np.array([0.0, 0.0, 0.0])   # AB
theta_init1 = np.array([0.0, 0.0, 0.0])   # BC (relativo)
theta_o     = np.array([0.0, 0.0, 0.0])   # medición

# Crear analizador
an = Analisis(t, w1, w2, w_o, theta_init1, theta_init2, theta_o, L1, L2)

# Primera pasada: calcular estados y w_tip para generar una "medición" sintética realista
an.state_of_motion()
Va, Aa = an.kinematic_general()
r_tip = an.tip_position()
w_tip = an.w_tip_from_Va(Va, r_tip)


# Actualizar señales derivadas de la medición
an.alpha_o, an.theta_out = an.variables_of_motion_operator(an.w_o, t, theta_o)

# Gráficas completas
an.graf()
