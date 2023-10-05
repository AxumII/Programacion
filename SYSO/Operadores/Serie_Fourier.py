import numpy as np
import matplotlib.pyplot as plt

class Serie_Fourier:
    def __init__(self,t,l,N,funcion):
        self.t = t
        self.l = l
        self.N = N
        self.funcion = funcion
    
    # Función para calcular los coeficientes de la serie de Fourier
    def coeficientes(self):
        a0 = (2 / self.l) * np.trapz(self.funcion, dx=self.l)
        a_coeffs = []
        b_coeffs = []
        for n in range(1, self.N + 1):
            a_n = (2 / self.l) * np.trapz(self.funcion * np.cos(2 * np.pi * n * self.t / self.l), dx=self.l)
            b_n = (2 / self.l) * np.trapz(self.funcion * np.sin(2 * np.pi * n * self.t / self.l), dx=self.l)
            a_coeffs.append(a_n)
            b_coeffs.append(b_n)
        return a0, a_coeffs, b_coeffs
    
    #Funcion que calcula la serie de Fourier dado los coeficientes
    def result(self):
        
        metCoef = self.coeficientes()
        a0 = metCoef[0]
        a_coeffs = metCoef[1]
        b_coeffs = metCoef[2]
        
        suma = a0 / 2
        for n in range(len(a_coeffs)):
            suma += a_coeffs[n] * np.cos(2 * np.pi * (n + 1) * self.t / self.l) + b_coeffs[n] * np.sin(2 * np.pi * (n + 1) * self.t / self.l)
        return suma
    
    #Funcion que grafica la serie y la funcion original
    def graf(self): 
        
        resultado = self.result()
        
        fig = plt.figure(figsize=(12, 6))
        
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.plot(self.t, self.funcion, label='Función Original', color="red")
        ax1.set_xlabel('Tiempo')
        ax1.set_ylabel('Amplitud')
        ax1.grid(True)
        ax1.legend(fontsize=10, loc="upper right")
        
        ax2 = fig.add_subplot(2, 1, 2)
        ax2.plot(self.t, resultado, label='Serie de Fourier', color="purple")
        ax2.plot(4, 0.5, marker="o", markersize=4, color="green", label='N = {:.6f}'.format(self.N))
        ax2.set_xlabel('Variable t')
        ax2.set_ylabel('Amplitud y')
        ax2.legend( fontsize=10, loc="upper right")
        ax2.grid(True)
        
        plt.tight_layout()
        plt.show()
