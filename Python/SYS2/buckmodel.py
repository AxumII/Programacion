from scipy.signal import StateSpace, lsim
import numpy as np
import matplotlib.pyplot as plt


class BoostModel:
    def __init__(self, L, C, R, f_sw, duty):
        self.L = L
        self.C_val = C
        self.R = R
        self.f_sw = f_sw              # frecuencia de conmutación [Hz]
        self.T_sw = 1 / f_sw          # período total [s]
        self.duty = duty              # ciclo de trabajo (0 < D < 1)

        self.A = np.array([[0, -1 / self.L],
                           [1 / self.C_val, -1 / (self.R * self.C_val)]])
        self.C = np.array([[0, 1]])
        self.D = np.array([[0]])

    def stateon(self, X0, T, u_value):
        B = np.array([[1 / self.L], [0]])
        sys_on = StateSpace(self.A, B, self.C, self.D)
        U = np.ones_like(T) * u_value
        T, yout, xout = lsim(sys_on, U=U, T=T, X0=X0)
        return yout, xout

    def stateoff(self, X0, T):
        B = np.array([[0], [0]])
        sys_off = StateSpace(self.A, B, self.C, self.D)
        U = np.zeros_like(T)*0.7
        T, yout, xout = lsim(sys_off, U=U, T=T, X0=X0)
        return yout, xout

    def completesystem(self, T_total=5e-3, u=5, steps_per_half=20):
        n_cycles = int(self.f_sw * T_total)

        Ton = self.duty * self.T_sw
        Toff = (1 - self.duty) * self.T_sw

        t_on = np.linspace(0, Ton, steps_per_half)
        t_off = np.linspace(0, Toff, steps_per_half)

        y_total = []
        t_total = []
        x_total = []

        X0 = np.array([0, 0])  # iL=0, vC=0
        t_current = 0

        for _ in range(n_cycles):
            # ON
            y_on, x_on = self.stateon(X0, t_on, u_value=u)
            t_on_global = t_current + t_on
            y_total.append(y_on)
            t_total.append(t_on_global)
            x_total.append(x_on)
            X0 = x_on[-1]
            t_current = t_on_global[-1]

            # OFF
            y_off, x_off = self.stateoff(X0, t_off)
            t_off_global = t_current + t_off
            y_total.append(y_off)
            t_total.append(t_off_global)
            x_total.append(x_off)
            X0 = x_off[-1]
            t_current = t_off_global[-1]

        # Concatenar todo
        T = np.concatenate(t_total)
        Y = np.concatenate(y_total)
        X = np.vstack(x_total)

        return T, Y, X


# === PRUEBA Y GRÁFICAS ===
if __name__ == "__main__":
    boost = BoostModel(L=33e-6, C=22e-6, R=10, f_sw=100e3, duty=0.1)
    T, Y, X = boost.completesystem(T_total=0.05, u=5)

    plt.figure(figsize=(10, 5))

    plt.subplot(2, 1, 1)
    plt.plot(T, X[:, 0], label='$i_L(t)$', color='blue')
    plt.ylabel('Corriente [A]')
    plt.title('Corriente del inductor $i_L(t)$')
    plt.grid(True)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(T, X[:, 1], label='$v_C(t)$', color='green')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Voltaje [V]')
    plt.title('Voltaje del capacitor $v_C(t)$')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()
