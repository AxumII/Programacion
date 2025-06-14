from scipy.signal import StateSpace, lsim
import numpy as np
import matplotlib.pyplot as plt


class BuckModel:
    def __init__(self, L, C, R, f_sw, duty,total_time, u, enable_graf = False):
        self.L = L
        self.C_val = C
        self.R = R
        self.total_time = total_time  # Tiempo total de simulacion
        self.u = u                    # voltaje
        self.f_sw = f_sw              # frecuencia de conmutación [Hz]
        self.T_sw = 1 / f_sw          # período total [s]
        self.cycles = int(f_sw * total_time) #ciclos que se ejecutan en total
        self.duty = duty              # ciclo de trabajo (0 < D < 1)

        self.A = np.array([[0, -1 / self.L],
                           [1 / self.C_val, -1 / (self.R * self.C_val)]])
        self.C = np.array([[0, 1]])
        self.D = np.array([[0]])
        self.B_on = np.array([[1 / self.L], [0]])
        self.B_off = np.array([[0], [0]])
        self.sys_on = StateSpace(self.A, self.B_on, self.C, self.D)
        self.sys_off = StateSpace(self.A, self.B_off, self.C, self.D)


        self.enable_graf = enable_graf

    def stateon(self, X0, T, u_value):
        U = np.ones_like(T) * u_value
        _, yout, xout = lsim(self.sys_on, U=U, T=T, X0=X0)
        return yout, xout

    def stateoff(self, X0, T):
        U = np.zeros_like(T) #*-0.7
        _, yout, xout = lsim(self.sys_off, U=U, T=T, X0=X0)
        return yout, xout


    def completesystem(self, steps_period=50):
        ton = self.duty * self.T_sw
        toff = (1 - self.duty) * self.T_sw

        steps_on = int(round(steps_period * self.duty))
        steps_off = int(round(steps_period * (1 - self.duty)))
        steps_total = (steps_on + steps_off) * self.cycles

        ton_array = np.linspace(0, ton, steps_on)
        toff_array = np.linspace(0, toff, steps_off)

        # Prealocar memoria
        Y = np.zeros((steps_total,))
        T = np.zeros((steps_total,))
        X = np.zeros((steps_total, 2))

        X0 = np.array([0, 0])
        t_current = 0
        index = 0

        for _ in range(self.cycles):
            # ON
            y_on, x_on = self.stateon(X0, ton_array, u_value=self.u)
            t_on_global = t_current + ton_array
            n_on = len(ton_array)

            Y[index:index+n_on] = y_on.flatten()
            T[index:index+n_on] = t_on_global
            X[index:index+n_on, :] = x_on
            X0 = x_on[-1]
            t_current = t_on_global[-1]
            index += n_on

            # OFF
            y_off, x_off = self.stateoff(X0, toff_array)
            t_off_global = t_current + toff_array
            n_off = len(toff_array)

            Y[index:index+n_off] = y_off.flatten()
            T[index:index+n_off] = t_off_global
            X[index:index+n_off, :] = x_off
            X0 = x_off[-1]
            t_current = t_off_global[-1]
            index += n_off

        return T, Y, X


    def graf_single(self):
        if self.enable_graf == True:
            T,Y,X = self.completesystem()
                    
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

        else:
            pass

"""
# === PRUEBA Y GRÁFICAS ===
if __name__ == "__main__":
    boost = BuckModel(L=10e-6, C=470e-6, R=10, f_sw=100e3, duty=0.4,total_time=1,u = 12 ,enable_graf= True)
    T, Y, X = boost.completesystem()

    #print(T[-1],X[-1],Y[-1])
    boost.graf_single()
"""