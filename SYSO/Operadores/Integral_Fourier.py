import numpy as np
import matplotlib.pyplot as plt

class Integral_Fourier:
    def __init__(self, t, funcion, numArm = None):
        self.t = t
        self.funcion = funcion
        self.numArm = numArm

    def fft(self):
        N = len(self.funcion)
        transformada = np.fft.fft(self.funcion)
        frecuencias = np.fft.fftfreq(N, self.t[1] - self.t[0])
        
        print(transformada)
        return frecuencias, transformada

    def result(self):
        coef = self.fft()
        frecuencias = coef[0]
        transformada = coef[1]
        integral = np.fft.ifft(transformada) * (frecuencias[1] - frecuencias[0])
        return frecuencias, transformada, integral

    def limitresult(self):
        coef = self.fft()
        frecuencias = coef[0][:self.numArm]  # Tomar los primeros n elementos de frecuencias
        transformada = coef[1][:self.numArm]  # Tomar los primeros n elementos de la transformada
        N = len(self.t)
        integral2 = np.fft.ifft(transformada, n=N) * (frecuencias[1] - frecuencias[0])
        return frecuencias, transformada, integral2
    
    def graf(self):
        frecuencias, transformada, integral = self.result()
        frecuencias, transformada, integral2 = self.limitresult()

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

        if self.numArm != None:
            ax4.plot(self.t, np.real(integral2), label='Armonicos usados = {:.6f}'.format(self.numArm))
            ax4.set_title('Integral de Fourier ')
            ax4.grid(True)
        else:
            pass
        
        plt.tight_layout()
        plt.show()
