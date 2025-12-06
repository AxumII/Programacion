import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sg


class AnalisisLibre:
<<<<<<< Updated upstream
    def __init__(self, filename):
        """
        filename: ruta relativa del archivo CSV dentro de la carpeta del script.
        Ejemplo:
            'Archivos/Libre - sin amortiguamiento_unido.csv'
        """
        self.d = 0.119  # distancia sensor–eje (m)
        self.file = filename

    def read(self):
        """
        Lee el archivo CSV indicado en self.file y devuelve:
        - tiempo
        - canal A
        - canal B
        como numpy arrays.
        """
        # Carpeta donde se encuentra este script
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Ruta completa del archivo CSV
        ruta = os.path.join(base_dir, self.file)

        # Verificación
        if not os.path.exists(ruta):
            raise FileNotFoundError(
                f"No se encontró el archivo:\n  {ruta}\n"
                f"Verifica el nombre del archivo dentro de /Archivos."
            )

        # Leer CSV
=======
    def __init__(self, file, folder = "archivo",  d = 0.119):
        #Constantes del sistema
        self.d = 0.119  #m
        
        #Archivo
        self.file = file
        self.folder = folder
        
        
    def read(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.join(base_dir, folder, file)
        
>>>>>>> Stashed changes
        df = pd.read_csv(
            ruta,
            sep=";",
            decimal=","
        )

        # Forzar conversión numérica y eliminar filas inválidas
        for col in ["Tiempo", "Canal A", "Canal B"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=["Tiempo", "Canal A", "Canal B"])

        t = df["Tiempo"].to_numpy()
        canal_a = df["Canal A"].to_numpy()
<<<<<<< Updated upstream
        canal_b = df["Canal B"].to_numpy()

        return t, canal_a, canal_b

    def result(self):
        """
        Calcula Tn, fn y omega_n para el archivo.
        """
        t_raw, x, y = self.read()

        # Si el tiempo está en ms (muy grande), convertir a segundos
        if t_raw.max() > 10:
            t = t_raw * 1e-3
        else:
            t = t_raw

        # Convertir señal y (mV → rad)
        delta = (y / 1000.0) / 350.0      # m
        theta = delta / self.d            # rad

        # Señal centrada para detección de picos
        th = theta - np.mean(theta)

        # Detección de picos simples
        idx_peaks = np.where((th[1:-1] > th[:-2]) & (th[1:-1] > th[2:]))[0] + 1

        if len(idx_peaks) < 2:
            raise ValueError(f"Pocos picos detectados en archivo {self.file}")

        t_peaks = t[idx_peaks]
        periodos = np.diff(t_peaks)

        Tn = np.mean(periodos)          # Periodo natural [s]
        fn = 1.0 / Tn                   # Frecuencia natural [Hz]
        omega_n = 2.0 * np.pi * fn      # Velocidad angular [rad/s]

        return Tn, fn, omega_n

    def tabla(self):
        """
        Devuelve un DataFrame con Tn, fn y ωn.
        """
        try:
            Tn, fn, omega_n = self.result()
            datos = [[self.file, Tn, fn, omega_n]]
        except Exception as e:
            print(f"Error en {self.file}: {e}")
            datos = [[self.file, None, None, None]]
=======
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
>>>>>>> Stashed changes

        return T_n,f_n,w_n
    
    def tabulate(self):
        T_n,f_n,w_n = self.result()
        df = pd.DataFrame(
<<<<<<< Updated upstream
            datos,
            columns=["Archivo", "Periodo Tn (s)", "Frecuencia fn (Hz)", "Velocidad ωn (rad/s)"]
        )
        return df

    def graf(self):
        """
        Grafica la señal del archivo CSV.
        """
        t_raw, _, y = self.read()

        # Convertir ms → s si hace falta
        if t_raw.max() > 10:
            t = t_raw * 1e-3
        else:
            t = t_raw

        delta = (y / 1000.0) / 350.0
        theta = delta / self.d

        plt.figure()
=======
            resultados,
            columns=[ "Periodo Tn (s)", "Frecuencia fn (Hz)", "Velocidad ωn (rad/s)"]
        )
        return df
    
    def graf(self):
        t,theta = self.fix()
>>>>>>> Stashed changes
        plt.plot(t, theta, label="Ángulo")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Ángulo (rad)")
        plt.title(f"Señal: {self.file}")
        plt.grid(True)
        plt.legend()
<<<<<<< Updated upstream
        plt.show()


# ===============================
# EJEMPLO DE USO


"""
analisis = AnalisisLibre("Archivos/Libre - sin amortiguamiento - unido.csv")

# Mostrar tabla con valores calculados
tabla_resultados = analisis.tabla()
print(tabla_resultados)

# Graficar el archivo
analisis.graf()"""
=======
        plt.show()
>>>>>>> Stashed changes
