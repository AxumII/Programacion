import numpy as np
import matplotlib.pyplot as plt

class Integral_Fourier:
    def __init__(self, t, funcion):
        self.t = t
        self.funcion = funcion

    def fft(self):
        N = len(self.funcion)
        transformada = np.fft.fft(self.funcion)
        frecuencias = np.fft.fftfreq(N, self.t[1] - self.t[0])
        return frecuencias, transformada

    def result(self):
        coef = self.fft()
        frecuencias = coef[0]
        transformada = coef[1]
        integral = np.fft.ifft(transformada) * (frecuencias[1] - frecuencias[0])
        return frecuencias, transformada, integral

    def generate_approximation(self, selected_harmonics):
        frecuencias, transformada, integral = self.result()
        approximation = np.zeros(len(self.t), dtype=np.complex128)

        for i in range(selected_harmonics):
            approximation += transformada[i] * np.exp(2j * np.pi * frecuencias[i] * self.t)

        return np.real(approximation)

    def graf(self, selected_harmonics=None):
        frecuencias, transformada, integral = self.result()

        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 8))
        
        # Graficar la señal original, la transformada y la integral
        ax1.plot(self.t, self.funcion)
        ax1.set_title('Señal Original')
        ax1.grid(True)

        ax2.scatter(frecuencias, np.abs(transformada))
        ax2.set_title('Transformada de Fourier')
        ax2.grid(True)

        ax3.plot(self.t, np.real(integral))  
        ax3.set_title('Integral de Fourier')
        ax3.grid(True)

        if selected_harmonics is not None:
            approximation = self.generate_approximation(selected_harmonics)
            ax4.plot(self.t, approximation)
            ax4.set_title('Aproximación con {} armónicos'.format(selected_harmonics))
            ax4.grid(True)

        plt.tight_layout()
        plt.show()
