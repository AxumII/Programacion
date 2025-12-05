import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class AnalisisLibre:
    def __init__(self):
        self.d = 0.119  # distancia sensor–eje (en metros)
        self.files = [
            f"Libre - sin amortiguamiento_{i}.csv" for i in range(1, 7)
        ]

    def read(self, file):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        folder = "Libre - sin amortiguamiento"
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

    def result(self, file):
        t_ms, x, y = self.read(file)

        # Pasar tiempo a segundos
        t = t_ms * 1e-3

        # Convertir señal
        delta = (y / 1000.0) / 350.0
        theta = delta / self.d

        # Señal centrada para buscar picos
        th = theta - np.mean(theta)

        # Detección de picos (máximos locales)
        idx_peaks = np.where((th[1:-1] > th[:-2]) & (th[1:-1] > th[2:]))[0] + 1

        if len(idx_peaks) < 2:
            raise ValueError(f"Pocos picos detectados en archivo {file}")

        t_peaks = t[idx_peaks]
        periodos = np.diff(t_peaks)

        Tn = np.mean(periodos)          # [s]
        fn = 1.0 / Tn                   # [Hz]
        omega_n = 2.0 * np.pi * fn      # [rad/s]

        return Tn, fn, omega_n

    def tabla(self):
        """
        Calcula Tn, fn y omega_n para los 6 archivos y
        devuelve una tabla pandas.
        """
        resultados = []

        for f in self.files:
            try:
                Tn, fn, omega_n = self.result(f)
                resultados.append([f, Tn, fn, omega_n])
            except Exception as e:
                resultados.append([f, None, None, None])
                print(f"Error en {f}: {e}")

        df = pd.DataFrame(
            resultados,
            columns=["Archivo", "Periodo Tn (s)", "Frecuencia fn (Hz)", "Velocidad ωn (rad/s)"]
        )

        return df

    def graf(self, file):
        """
        Grafica el archivo especificado (picos + señal).
        """
        t_ms, _, y = self.read(file)
        t = t_ms * 1e-3
        delta = (y/1000)/350
        theta = delta / self.d

        plt.plot(t, theta, label="Ángulo")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Ángulo (rad)")
        plt.title(f"Señal: {file}")
        plt.grid(True)
        plt.legend()
        plt.show()


# ===============================
# USO
# ===============================

analisis = AnalisisLibre()

# Mostrar tabla con los valores calculados
tabla_resultados = analisis.tabla()
print(tabla_resultados)

# Graficar uno específico (opcional)
# analisis.graf("Libre - sin amortiguamiento_1.csv")
