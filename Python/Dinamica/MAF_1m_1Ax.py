import numpy as np
import matplotlib.pyplot as plt

class MAF:
    def __init__(self, m_r, k, c_amort, d_exc, m_exc, w_circular, C1, C2):
        # Parámetros del sistema
        self.m_r = m_r      # Masa del sistema
        self.k = k          # Constante del resorte
        self.c_amort = c_amort  # Coeficiente de amortiguamiento
        self.d_exc = d_exc  # Distancia excéntrica
        self.m_exc = m_exc  # Masa excéntrica
        self.w_circular = w_circular  # Frecuencia de excitación
        self.C1 = C1        # Constante de integración 1
        self.C2 = C2        # Constante de integración 2

    def solve_x(self, t):
        # Frecuencia natural
        w_n = np.sqrt(self.k / self.m_r)
        
        # Coeficiente de amortiguamiento crítico
        Cc = 2 * self.m_r * w_n

        # Fuerza de excitación
        P = self.m_r * self.d_exc * (self.w_circular**2)

        # Cálculo de los valores lambda1 y lambda2
        lmb_1 = (-self.c_amort / (2*self.m_r)) + np.sqrt(((self.c_amort / (2*self.m_r))**2) - (self.k / self.m_r))
        lmb_2 = (-self.c_amort / (2*self.m_r)) - np.sqrt(((self.c_amort / (2*self.m_r))**2) - (self.k / self.m_r))

        # Solución homogénea según el tipo de amortiguamiento
        if self.c_amort > Cc:  # Sobreamortiguado
            x_hom = (self.C1 * np.exp(lmb_1 * t)) + (self.C2 * np.exp(lmb_2 * t))

        elif self.c_amort < Cc:  # Subamortiguado
            w_d = w_n * np.sqrt(1 - ((self.c_amort / Cc)**2))
            x_hom = np.exp((-self.c_amort * t) / (2*self.m_r)) * (
                self.C1 * np.sin(w_d * t) + self.C2 * np.cos(w_d * t)
            )

        else:  # Amortiguamiento crítico
            print("Es críticamente amortiguado, modifique algún valor.")
            return None

        # Solución particular (respuesta forzada)
        x_m = P / np.sqrt((self.k - self.m_r * (self.w_circular**2))**2 + (self.c_amort * self.w_circular)**2)
        rel_w = self.w_circular / w_n
        gamma = np.arctan2((2 * (self.c_amort / Cc) * rel_w), (1 - rel_w**2))

        x_part = x_m * np.sin(self.w_circular * t - gamma)

        # Solución general
        x_total = x_hom + x_part

        # Factor de amplificación
        Fc_amp = x_m / (P/self.k)
        return x_total  



    def graf_x(self, t_max=10, t_points=1000):
        """
        Método para graficar la solución x(t) respecto al tiempo.
        Parámetros:
        t_max: Tiempo máximo de la simulación (segundos).
        t_points: Cantidad de puntos en la simulación.
        """
        t = np.linspace(0, t_max, t_points)  # Generamos el rango de tiempo
        x_vals = self.solve_x(t)  # Calculamos los valores de x(t)

        if x_vals is None:
            print("No se puede graficar debido a valores incorrectos en la ecuación.")
            return
        
        # Graficamos la solución x(t)
        plt.figure(figsize=(8, 5))
        plt.plot(t, x_vals, label='$x(t)$ - Movimiento Amortiguado Forzado', color='b')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Desplazamiento x(t)')
        plt.title('Respuesta del Sistema Amortiguado Forzado')
        plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
        plt.legend()
        plt.grid()
        plt.show()

    def graf_resonancia(self, w_rel_min=0.05, w_rel_max=3.0, num_points=500):
        """
        Método para graficar el factor de amplificación respecto a la frecuencia relativa.

        Parámetros:
        w_rel_min: Frecuencia relativa mínima a considerar.
        w_rel_max: Frecuencia relativa máxima a considerar.
        num_points: Número de puntos en la simulación.
        """
        w_n = np.sqrt(self.k / self.m_r)  # Frecuencia natural
        w_f_range = np.linspace(w_rel_min * w_n, w_rel_max * w_n, num_points)  # Rango de frecuencias de excitación

        Fc_amp_values = []

        for w_f in w_f_range:
            P = self.m_r * self.d_exc * (w_f**2)  # Fuerza de excitación

            # Amplitud de la respuesta forzada
            x_m = P / np.sqrt((self.k - self.m_r * (w_f**2))**2 + (self.c_amort * w_f)**2)
            Fc_amp = x_m / (P / self.k)  # Factor de amplificación

            Fc_amp_values.append(Fc_amp)

        # Graficamos la curva de resonancia
        plt.figure(figsize=(8, 5))
        plt.plot(w_f_range / w_n, Fc_amp_values, label='Factor de Amplificación', color='r')
        plt.xlabel('Razon de frecuencias $\\omega_f / \\omega_n$')
        plt.ylabel('Factor de Amplificación $F_c$')
        plt.title('Curva de Resonancia')
        plt.axhline(1, color='black', linestyle='--', linewidth=0.8, label='$F_c = 1$')
        plt.legend()
        plt.grid()
        plt.show()

        

################################################
# Definir parámetros del sistema
m_r = 1.0       # Masa [kg]
k = 100.0       # Constante del resorte [N/m]
c_amort = 5 # Coeficiente de amortiguamiento [Ns/m]
d_exc = 5/1000  # Excéntrica [m]
m_exc = 20/1000 # Masa excéntrica [kg]
w_circular = 1  # Frecuencia de excitación [rad/s]
C1 = 0          # Constante de integración 1
C2 = 0          # Constante de integración 2

# Crear el objeto del oscilador
oscilador = MAF(m_r, k, c_amort, d_exc, m_exc, w_circular, C1, C2)

# Graficar la solución x(t)
oscilador.graf_x(t_max=50, t_points=1000)

# Graficar la curva de resonancia
oscilador.graf_resonancia()
