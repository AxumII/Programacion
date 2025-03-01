import numpy as np
import matplotlib.pyplot as plt

class MAFS:
    def __init__(self, m_s=1, k_h=100, k_v=100, Pa_dx=1, Pa_dy=1, Pb_dx = 1, Pb_dy = 1 , w_f=100):
        self.m_s =  m_s /1000 #esta en gramos, verificar que este en kg
        #print("masa de sistema",self.m_s)
        self.k_h = k_h
        self.k_v = k_v
        self.Pa_dx = Pa_dx
        self.Pa_dy = Pa_dy
        self.Pb_dx = Pb_dx
        self.Pb_dy = Pb_dy
        self.w_f = w_f

        # Cálculo de frecuencias naturales
        #El k tiene que ser la mitad, ya que no es un resorte, son dos resortes y la suma en serie de dos iguales es la mitad
        self.w_n_h = np.sqrt((self.k_h/2) / self.m_s)
        self.w_n_v = np.sqrt((self.k_v/2) / self.m_s)
        
        
        

    def reson_x(self, n=200):
        # Definir el rango de frecuencia forzada en RPM y convertir a rad/s
        w_f_Val_rpm = np.linspace(0, 2000, n)
        w_f_Val_rad = w_f_Val_rpm * np.pi / 30
        
        # Razón de frecuencias
        Rz_f = w_f_Val_rad / self.w_n_h
        
        # Evitar singularidad en la resonancia
        F_A = np.where(np.isclose(Rz_f, 1, atol=1e-3), np.nan, 1 / (1 - Rz_f**2))
        
        # Conversión de RPM para la razón de frecuencias y su factor de amplificación
        w_n_h_rpm = self.w_n_h * 30 / np.pi
        Rz_f_rpm = w_f_Val_rpm / w_n_h_rpm
        F_A_rpm = np.where(np.isclose(Rz_f_rpm, 1, atol=1e-3), np.nan, 1 / (1 - Rz_f_rpm**2))
        
        # Cálculo del punto específico de la frecuencia forzada
        w_f_ratio_actual = self.w_f / self.w_n_h
        F_A_actual = 1 / (1 - w_f_ratio_actual**2)
        
        # Cálculo del punto en RPM
        w_f_actual_rpm = self.w_f * 30 / np.pi
        w_f_ratio_actual_rpm = w_f_actual_rpm / w_n_h_rpm
        F_A_actual_rpm = 1 / (1 - w_f_ratio_actual_rpm**2)
        
        # Crear la gráfica con los puntos resaltados
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))
        
        # Gráfico en radianes por segundo
        axs[0].plot(Rz_f, F_A, label="Factor de Amplificación", linestyle="-", color="g")
        axs[0].axvline(x=1, color="r", linestyle="--", label=f"Resonancia: $w_n = {self.w_n_h:.2f}$ rad/s")
        axs[0].scatter([w_f_ratio_actual], [F_A_actual], color="b", label=f"$w_f = {self.w_f}$ rad/s", zorder=3)
        axs[0].set_xlabel("Razón de Frecuencias $w_f / w_n$")
        axs[0].set_ylabel("Factor de Amplificación")
        axs[0].set_title("Gráfico de Resonancia en Rad/s")
        axs[0].legend()
        axs[0].grid()
        axs[0].set_ylim(-5, 5)
        
        # Gráfico en RPM
        axs[1].plot(Rz_f_rpm, F_A_rpm, label="Factor de Amplificación", linestyle="-", color="g")
        axs[1].axvline(x=1, color="r", linestyle="--", label=f"Resonancia: $w_n = {w_n_h_rpm:.2f}$ rpm")
        axs[1].scatter([w_f_ratio_actual_rpm], [F_A_actual_rpm], color="b", label=f"$w_f = {w_f_actual_rpm:.2f}$ rpm", zorder=3)
        axs[1].set_xlabel("Razón de Frecuencias $w_f / w_n$")
        axs[1].set_ylabel("Factor de Amplificación")
        axs[1].set_title("Gráfico de Resonancia en RPM")
        axs[1].legend()
        axs[1].grid()
        axs[1].set_ylim(-5, 5)
        
        # Ajustar diseño
        plt.tight_layout()
        plt.show()

    def amplitud(self):
        #la masa tiene que estar en Kg
        #El k tiene que ser la mitad, ya que no es un resorte, son dos resortes y la suma en serie de dos iguales es la mitad
        print("masa de sistema",self.m_s)
        
        X_a = (self.Pa_dx / (self.k_h/2)) / (1 - (self.w_f / self.w_n_h)**2)
        X_b = (self.Pb_dx / (self.k_h/2)) / (1 - (self.w_f / self.w_n_h)**2)
        return  X_a , X_b

# Crear instancia y graficar
"""Ex = MAFS()
Ex.reson_x()"""
