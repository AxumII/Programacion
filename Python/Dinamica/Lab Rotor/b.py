import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sg

class AnalisisLibre:
    def __init__(self, file, folder = "archivo",  d = 0.119):
        #Constantes del sistema
        self.d = 0.119  #m
        
        #Archivo
        self.file = file
        self.folder = folder
        
        
    def read(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.join(base_dir, folder, file)
        
        df = pd.read_csv(
            ruta,
            sep=";",
            decimal=",",
            skiprows=[1, 2]
        )
        tiempo = df["Tiempo"].to_numpy()   # en ms
        canal_a = df["Canal A"].to_numpy()
        canal_b = df["Canal B"].to_numpy() # en mV
        return tiempo, canal_a, canal_b
        
    def fix(self):
        #Permite escalar y trasducir a las unidades deseadas
        t,x,y = self.read()
        
        #Tiempo en s
        t = t  * 1e-3
        
        #Voltaje a Angulo
        delta = (y / 1000.0) / 350.0
        theta = delta/ self.d
        
        return t,theta
        
    def result(self):
        
        t,theta = self.fix()
        picos, _ = sg.find_peaks(theta)
        
        T_n = picos[0] - picos[1]  # [s]
        f_n = 1.0 / T_n                   # [Hz]
        w_n = 2 * np.pi * f_n   # [rad/s]

        return T_n,f_n,w_n
    
    def tabulate(self):
        T_n,f_n,w_n = self.result()
        df = pd.DataFrame(
            resultados,
            columns=[ "Periodo Tn (s)", "Frecuencia fn (Hz)", "Velocidad ωn (rad/s)"]
        )
        return df
    
    def graf(self):
        t,theta = self.fix()
        plt.plot(t, theta, label="Ángulo")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Ángulo (rad)")
        plt.title(f"Señal: {file}")
        plt.grid(True)
        plt.legend()
        plt.show()