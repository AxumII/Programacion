import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sg


class Convolucion:
    def __init__(self, t, funcion1, funcion2):
        self.t = t
        self.funcion1 = funcion1
        self.funcion2 = funcion2   
           
        
    def conv(self):
        return sg.convolve(self.funcion1, self.funcion2, mode='same')

    
    
    def tipo(self):
        # Calcula la diferencia en tiempo entre las muestras
        diferencia_tiempo = self.t[1] - self.t[0]
        
        # Calcula la frecuencia de muestreo
        fm = 1.0 / diferencia_tiempo        
        return fm
    
    def graf(self):
        result = self.conv()
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8))
        
        v = self.tipo()
        
        
        if(v == 1):
            ax1.scatter(self.t, self.funcion1, color = 'green')
            ax1.set_title('Señal 1')
            ax1.set_xlabel('Tiempo')
            ax1.set_ylabel('Amplitud')
            ax1.grid(True)

            ax2.scatter(self.t, self.funcion2, color = 'red')
            ax2.set_title('Señal 2')
            ax2.set_xlabel('Tiempo')
            ax2.set_ylabel('Amplitud')
            ax2.grid(True)

            ax3.scatter(self.t, result, color = 'purple')
            ax3.set_title('Convolución')
            ax3.set_xlabel('Tiempo')
            ax3.set_ylabel('Amplitud')
            ax3.grid(True)
            
            
            plt.tight_layout()
            plt.show()
        
        else:       

            ax1.plot(self.t, self.funcion1, color = 'green')
            ax1.set_title('Señal 1')
            ax1.set_xlabel('Tiempo')
            ax1.set_ylabel('Amplitud')
            ax1.grid(True)

            ax2.plot(self.t, self.funcion2, color = 'red')
            ax2.set_title('Señal 2')
            ax2.set_xlabel('Tiempo')
            ax2.set_ylabel('Amplitud')
            ax2.grid(True)

            ax3.plot(self.t , result, color = 'purple')
            ax3.set_title('Convolución')
            ax3.set_xlabel('Tiempo')
            ax3.set_ylabel('Amplitud')
            ax3.grid(True)
            
            
            plt.tight_layout()
            plt.show()