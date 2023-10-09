import numpy as np
import matplotlib.pyplot as plt

class Integral_Fourier:
    def __init__(self, t, funcion, numArm = 0 , threshold = 0):
        self.t = t
        self.funcion = funcion
        self.numArm = numArm
        self.threshold = threshold

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

    def fresult(self):
        coef = self.fft()
        frecuencias = coef[0][:self.numArm]  # Tomar los primeros n elementos de frecuencias
        transformada = coef[1][:self.numArm]  # Tomar los primeros n elementos de la transformada
        N = len(self.t)
        integral2 = np.fft.ifft(transformada, n=N) * (frecuencias[1] - frecuencias[0])
        return frecuencias, transformada, integral2
    
    def mresult(self):
        coef = self.fft()
        frecuencias = coef[0]
        transformada = coef[1]
        magnitud = np.abs(transformada)
        
        # Encuentra los índices de los armónicos principales
        indices_de_armónicos_principales = np.where(magnitud > self.threshold * max(magnitud))
        
        # Tomar los armónicos principales
        armónicos_principales = transformada[indices_de_armónicos_principales]
        
        return frecuencias[indices_de_armónicos_principales], armónicos_principales

    def graf(self):
        frecuencias, transformada, integral = self.result()
        

        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(12, 8))
        
        # Graficar la señal original, la transformada y la integral
        ax1.plot(self.t, self.funcion)
        ax1.set_title('Señal Original')
        ax1.set_xlabel('Tiempo')
        ax1.set_ylabel('Amplitud')
        ax1.grid(True)

        ax2.scatter(frecuencias, np.abs(transformada))
        ax2.set_title('Transformada de Fourier')
        ax2.set_xlabel('Frecuencia')
        ax2.set_ylabel('Amplitud')
        ax2.grid(True)

        ax3.plot(self.t, np.real(integral))  
        ax3.set_title('Integral de Fourier')
        ax3.set_xlabel('Tiempo')
        ax3.set_ylabel('Amplitud')
        ax3.grid(True)

        if self.numArm != 0:
            frecuencias_f, transformada_f, integral_f = self.fresult()
            
            ax4.plot(self.t, np.real(integral_f), label='Armonicos usados = {:.6f}'.format(self.numArm))
            ax4.set_title('Integral de Fourier con Armonicos Limitados')
            ax4.set_xlabel('Tiempo')
            ax4.set_ylabel('Amplitud')
            ax4.legend()
            ax4.grid(True)
        else:
            pass
        
        if self.threshold != 0:
            frecuencias_m, transformada_m = self.mresult()  
            
            ax5.scatter(frecuencias_m, np.abs(transformada_m))
            ax5.set_title('Armonicos principales')
            ax5.set_xlabel('Frecuencia')
            ax5.set_ylabel('Amplitud')
            ax5.grid(True)
        else:
            pass
        
        
        
        plt.tight_layout()
        plt.show()
