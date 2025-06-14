from buckmodel import BuckModel
import matplotlib.pyplot as plt

class PlotAnalisys:
    def __init__(self, C_val, L_val, f_sw, R_val=[10, 500] , u=12, total_time=0.05):
        self.C_val = C_val               # Capacitancia [F]
        self.L_val = L_val               # Inductancia [H]
        self.R_val = R_val               # Resistencia de carga [Ohm]
        self.u = u                       # Voltaje de entrada [V]
        self.f_sw = f_sw                 # Frecuencia de conmutación [rad/s]
        self.total_time= total_time
        

    def frecuency_und_duty(self):
        duty_values = [0.05, 0.3, 0.6, 0.95]  # Evitar 0.0 y 1.0 por problemas con arrays vacíos
        colors = ['red', 'green', 'blue', 'purple']

        for idx, f in enumerate(self.f_sw):
            plt.figure(figsize=(12, 8))

            # Subplot corriente iL
            plt.subplot(2, 1, 1)
            for i, d in enumerate(duty_values):
                buck = BuckModel(L=self.L_val[2], C=self.C_val[0], R=self.R_val[0], f_sw=f, duty=d, total_time=self.total_time, u=self.u)
                T, Y, X = buck.completesystem()
                plt.plot(T, X[:, 0], label=f"D={d}", color=colors[i])
            plt.title(f"Corriente del inductor $i_L(t)$ para f_sw = {f/1e3:.0f} kHz")
            plt.xlabel("Tiempo [s]")
            plt.ylabel("Corriente [A]")
            plt.legend()
            plt.grid(True)

            # Subplot voltaje vC
            plt.subplot(2, 1, 2)
            for i, d in enumerate(duty_values):
                buck = BuckModel(L=self.L_val[1], C=self.C_val[1], R=self.R_val[0], f_sw=f, duty=d, total_time=self.total_time, u=self.u)
                T, Y, X = buck.completesystem()
                plt.plot(T, X[:, 1], label=f"D={d}", color=colors[i])
            plt.title(f"Voltaje del capacitor $v_C(t)$ para f_sw = {f/1e3:.0f} kHz")
            plt.xlabel("Tiempo [s]")
            plt.ylabel("Voltaje [V]")
            plt.legend()
            plt.grid(True)

            plt.tight_layout()
            plt.show()



    def time_L_C(self):
        freq = 50e3
        duty = 0.95

        for L in self.L_val:
            for C in self.C_val:
                fig, axs = plt.subplots(len(self.R_val), 2, figsize=(12, 6 * len(self.R_val)))

                for i_r, R in enumerate(self.R_val):
                    buck = BuckModel(L=L, C=C, R=R, f_sw=freq, duty=duty, total_time=self.total_time, u=self.u)
                    T, Y, X = buck.completesystem()
                    axs[i_r, 0].plot(T, X[:, 0], label=f"R={R} Ω")
                    axs[i_r, 1].plot(T, X[:, 1], label=f"R={R} Ω")

                    axs[i_r, 0].set_title(f"Corriente $i_L(t)$ para R = {R} Ω, L = {L*1e6:.0f}uH, C = {C*1e6:.0f}uF")
                    axs[i_r, 0].set_xlabel("Tiempo [s]")
                    axs[i_r, 0].set_ylabel("Corriente [A]")
                    axs[i_r, 0].grid(True)
                    axs[i_r, 0].legend()

                    axs[i_r, 1].set_title(f"Voltaje $v_C(t)$ para R = {R} Ω, L = {L*1e6:.0f}uH, C = {C*1e6:.0f}uF")
                    axs[i_r, 1].set_xlabel("Tiempo [s]")
                    axs[i_r, 1].set_ylabel("Voltaje [V]")
                    axs[i_r, 1].grid(True)
                    axs[i_r, 1].legend()

                plt.tight_layout()
                plt.show()



    
    def disp_I(self):
        pass

if __name__ == "__main__":
    C_val = [10e-6, 330e-6, 1000e-6]
    L_val = [10e-6, 100e-6, 470e-6]
    f_sw = [50e3,100e3,1000e3]

    analisis = PlotAnalisys(C_val=C_val, L_val=L_val, f_sw = f_sw)
    analisis.frecuency_und_duty()
    #analisis.time_L_C()





