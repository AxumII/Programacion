import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid as cum_trapz

class Analisis:

    def __init__(self,t,w1,w2,w_o,theta_init1,theta_init2,theta_init_o, L1,L2):
        self.t = t
        self.w1 = w1      # (N,3) (del punto C)
        self.w2 = w2      # (N,3) (Del punto B respecto a A)
        self.w_o = w_o    # (N,3) medición externa (comparación)
        self.theta_init1 = theta_init1  # (3,) 
        self.theta_init2 = theta_init2  # (3,) 
        self.theta_init_o     = theta_init_o      # (3,) 
        self.L1 = L1     # ||BC||
        self.L2 = L2     # ||AB||

        # resultados
        self.alpha1 = self.alpha2 = self.alpha_o = None
        self.theta1 = self.theta2 = self.theta_out = None
        self.r_BC = self.r_AB = None   # r1=BC, r2=AB #Son los vectores en cada instante
        

    def kinematic(self):    
        # ---------------- funciones primordiales ----------------
        
        # -------- lambdas primordiales --------
        F_take_z  = lambda W: W[:, 2]
        F_alpha   = lambda W, t: np.gradient(W, t, axis=0)  # -> (N,3)
        F_theta = lambda wz,t,th0: (lambda th0z,dt:np.concatenate((np.array([th0z]),np.array([th0z + (wz[0]*dt[0] if dt.size>0 else 0.0)]),
        (th0z + (wz[0]*dt[0] if dt.size>0 else 0.0) +(np.cumsum(0.5*(wz[2:]+wz[1:-1])*dt[1:]) if dt.size>1 else np.array([]))))))(float(np.asarray(th0).ravel()[-1]), np.diff(t))
        F_point_position   = lambda th, L: np.column_stack((L*np.cos(th), L*np.sin(th), np.zeros_like(th)))
        F_tip_position     = lambda r1, r2: r1 + r2
        vel       = lambda w, r: np.cross(w, r)
        acc       = lambda a, w, r: np.cross(a, r) + np.cross(w, np.cross(w, r))


        # ---------------- series escalares (z) ----------------
        w_BC_z = F_take_z(self.w1)   # ω_BC (absoluta, en C)
        w_AB_z = F_take_z(self.w2)   # ω_AB (absoluta, en B respecto a A)
        w_tip_z = F_take_z(self.w_o) if self.w_o is not None else None  # medición externa


        # ---------------- aceleraciones angulares (z) ----------------
        self.alpha1 = F_alpha(self.w1, self.t)  # (N,3)
        self.alpha2 = F_alpha(self.w2, self.t)  # (N,3)
        self.alpha_o = F_alpha(self.w_o, self.t) if self.w_o is not None else None

        # ---------------- ángulos ----------------
        theta_BC = F_theta(w_BC_z, self.t, self.theta_init1)  # θ_BC (absoluto)
        theta_AB = F_theta(w_AB_z, self.t, self.theta_init2)  # θ_AB (absoluto)
        theta_tip = F_theta(w_tip_z, self.t, self.theta_init_o) if w_tip_z is not None else None

        # ---------------- posiciones de los puntos clave ----------------
        self.r_AB  = F_point_position(theta_AB, self.L2)   # A->B
        self.r_BC  = F_point_position(theta_BC, self.L1)   # B->C
        self.r_tip = F_tip_position(self.r_AB, self.r_BC)  # A->C



        # ---------------- variables de cinematica y cinetica basica ----------------
        v_b = vel(self.w1,self.r_BC)
        a_b = acc(self.alpha1,self.w1,self.r_BC)

        v_a__b = vel(self.w2,self.r_AB)
        a_a__b = acc(self.alpha2,self.w2,self.r_AB)

        #velocidad en la punta 
        v_a = v_b + v_a__b
        a_a = a_b + a_a__b

        #velocidad en la punta alternativa
        v_a_with_output = vel(self.w_o, self.r_tip)
        a_a_with_output = acc(self.alpha_o, self.r_tip, self.w_o)

        # 7) guardar
        self.theta1, self.theta2, self.theta_out = theta_BC, theta_AB, theta_tip
        self.v_b, self.a_b = v_b, a_b
        self.v_a, self.a_a = v_a, a_a
        self.v_a_with_output, self.a_a_with_output = v_a_with_output, a_a_with_output
        return self
    
    def graf(self):
        t = self.t

        # ===== 1) ω por eje (w1, w2, w_o) =====
        fig1, ax = plt.subplots(3, 3, figsize=(14, 9), sharex=True)
        titles = [r'$\omega_{BC}$ (w1)', r'$\omega_{AB}$ (w2)', r'$\omega_{\mathrm{tip}}$ (w_o)']
        Ws = [self.w1, self.w2, self.w_o if self.w_o is not None else np.zeros_like(self.w1)]
        for i, W in enumerate(Ws):
            for j, lab in enumerate(['x','y','z']):
                ax[i, j].plot(t, W[:, j])
                ax[i, j].set_ylabel(f'{titles[i]} – {lab}')
                if i == 2 and self.w_o is None:
                    ax[i, j].text(0.5, 0.5, 'sin datos', ha='center', va='center',
                                transform=ax[i, j].transAxes)
        for j in range(3): ax[2, j].set_xlabel('t [s]')
        fig1.suptitle('Velocidades angulares por eje')
        fig1.tight_layout()

        # ===== 2) α por eje =====
        fig2, axa = plt.subplots(3, 3, figsize=(14, 9), sharex=True)
        atitles = [r'$\alpha_{BC}$', r'$\alpha_{AB}$', r'$\alpha_{\mathrm{tip}}$']
        As = [self.alpha1, self.alpha2, self.alpha_o if self.alpha_o is not None else np.zeros_like(self.alpha1)]
        for i, A in enumerate(As):
            for j, lab in enumerate(['x','y','z']):
                axa[i, j].plot(t, A[:, j])
                axa[i, j].set_ylabel(f'{atitles[i]} – {lab}')
                if i == 2 and self.alpha_o is None:
                    axa[i, j].text(0.5, 0.5, 'sin datos', ha='center', va='center',
                                transform=axa[i, j].transAxes)
        for j in range(3): axa[2, j].set_xlabel('t [s]')
        fig2.suptitle('Aceleraciones angulares por eje')
        fig2.tight_layout()

        # ===== 3) θ de los 3 puntos en los 3 ejes =====
        # En 2D solo z es distinto de 0; x,y se trazan como 0 por claridad
        N = t.size
        z = lambda th: np.asarray(th).ravel()
        zeros = lambda: np.zeros(N)
        THs = [
            np.column_stack((zeros(), zeros(), z(self.theta1))),   # θ_BC
            np.column_stack((zeros(), zeros(), z(self.theta2))),   # θ_AB
            np.column_stack((zeros(), zeros(), z(self.theta_out))) if self.theta_out is not None
                else np.zeros((N,3))
        ]
        ttitles = [r'$\theta_{BC}$', r'$\theta_{AB}$', r'$\theta_{\mathrm{tip}}$']

        fig3, axt = plt.subplots(3, 3, figsize=(14, 9), sharex=True)
        for i, TH in enumerate(THs):
            for j, lab in enumerate(['x','y','z']):
                axt[i, j].plot(t, TH[:, j])
                axt[i, j].set_ylabel(f'{ttitles[i]} – {lab}')
                if i == 2 and self.theta_out is None:
                    axt[i, j].text(0.5, 0.5, 'sin datos', ha='center', va='center',
                                transform=axt[i, j].transAxes)
        for j in range(3): axt[2, j].set_xlabel('t [s]')
        fig3.suptitle('Ángulos por eje')
        fig3.tight_layout()

        # ===== 4) v_a y a_a por eje =====
        fig4, axv = plt.subplots(2, 3, figsize=(14, 6), sharex=True)
        for j, lab in enumerate(['x','y','z']):
            axv[0, j].plot(t, self.v_a[:, j]); axv[0, j].set_ylabel(f'v_A – {lab} [m/s]')
            axv[1, j].plot(t, self.a_a[:, j]); axv[1, j].set_ylabel(f'a_A – {lab} [m/s²]')
        for j in range(3): axv[1, j].set_xlabel('t [s]')
        fig4.suptitle('Punta A: velocidad y aceleración por eje')
        fig4.tight_layout()

        # ===== 5) Comparación v_a (vectorial) vs v_a_with_output =====
        fig5, axc = plt.subplots(1, 3, figsize=(14, 3.5), sharex=True)
        if self.v_a_with_output is not None:
            for j, lab in enumerate(['x','y','z']):
                axc[j].plot(t, self.v_a[:, j], label='v_A (modelo)')
                axc[j].plot(t, self.v_a_with_output[:, j], '--', label='v_A (con ω_tip)')
                axc[j].set_ylabel(f'v – {lab} [m/s]'); axc[j].legend(); axc[j].grid(True)
            for j in range(3): axc[j].set_xlabel('t [s]')
            fig5.suptitle('Comparación de v_A')
            fig5.tight_layout()
        else:
            for j in range(3):
                axc[j].text(0.5,0.5,'sin ω_tip',ha='center',va='center',transform=axc[j].transAxes)
            for j in range(3): axc[j].set_xlabel('t [s]')
            fig5.suptitle('Comparación de v_A (no disponible)')
            fig5.tight_layout()

        # ===== 6) Trayectorias XY de B y A (origen en C) =====
        r_CB = -self.r_BC              # C→B
        r_CA = -self.r_BC - self.r_AB  # C→A
        
        fig6, ax = plt.subplots(1, 1, figsize=(6, 6))
        lineB, = ax.plot(r_CB[:,0], r_CB[:,1], label='Trayectoria B (C→B)')
        lineA, = ax.plot(r_CA[:,0], r_CA[:,1], label='Trayectoria A (C→A)')

        # --- flechas simples y grandes ---
        Nflechas = 12    # cuántas flechas por curva (sube/baja este número)
        K       = 4.0    # factor de tamaño (más grande = flechas más largas)

        # B
        iB  = np.linspace(0, len(r_CB)-2, Nflechas, dtype=int)
        dxB = r_CB[iB+1,0] - r_CB[iB,0]
        dyB = r_CB[iB+1,1] - r_CB[iB,1]
        ax.quiver(r_CB[iB,0], r_CB[iB,1], K*dxB, K*dyB,
                angles='xy', scale_units='xy', scale=1, width=0.010,
                color=lineB.get_color())

        # A
        iA  = np.linspace(0, len(r_CA)-2, Nflechas, dtype=int)
        dxA = r_CA[iA+1,0] - r_CA[iA,0]
        dyA = r_CA[iA+1,1] - r_CA[iA,1]
        ax.quiver(r_CA[iA,0], r_CA[iA,1], K*dxA, K*dyA,
                angles='xy', scale_units='xy', scale=1, width=0.010,
                color=lineA.get_color())

        # origen C
        ax.scatter(0, 0, s=60, c='k', label='C (origen)')

        ax.set_aspect('equal', 'box')
        ax.set_xlabel('X [m]'); ax.set_ylabel('Y [m]')
        ax.legend(); ax.grid(True)
        ax.set_title('Trayectorias con sentido de desplazamiento (origen en C)')

        plt.show()


# -------- parámetros del escenario --------
T   = 2.0        # duración [s]
fs  = 50        # Hz
N   = int(T*fs)
t   = np.linspace(0.0, T, N)

L1, L2 = 1.35, 0.28   # longitudes BC y AB [m]


# Velocidades angulares (solo z)
w1z = 0.3*np.ones(N)                     # ω_BC: giro uniforme CCW
w2z = 0.3*np.ones(N)   #0.5*np.sin(2*np.pi*0.5*t)          # ω_AB: oscilación en B (servo)
w0z = 0.3*np.ones(N)
# Empaquetar a (N,3) con solo z ≠ 0
zeros = np.zeros(N)
w1 = np.column_stack([zeros, zeros, w1z])   # (N,3)
w2 = np.column_stack([zeros, zeros, w2z])   # (N,3)
w_o = np.column_stack([zeros, zeros, w2z])   # (N,3)                              # sensor en A: misma ω que AB

# Ángulos iniciales (solo se usa z)
theta_init1  = np.array([0.0, 0.0, np.deg2rad(-10)])   # θ_BC(0)
theta_init2  = np.array([0.0, 0.0, np.deg2rad(-80)])  # θ_AB(0)
theta_init_o = np.array([0.0, 0.0, theta_init2[2]])   # θ_tip(0) (opcional)



an = Analisis(t, w1, w2, w_o, theta_init1, theta_init2, theta_init_o, L1, L2)
an.kinematic()
an.graf()

