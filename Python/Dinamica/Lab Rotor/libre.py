import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sg


class AnalisisLibre:
    def __init__(self, 
                 file="Libre - sin amortiguamiento - unido.csv",
                 folder="Archivos",
                 d=0.119):


        self.d = d
        
        self.file = file
        self.folder = folder


    def read(self):

        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.join(base_dir, self.folder, self.file)

        if not os.path.exists(ruta):
            raise FileNotFoundError(
                f"No se encontró el archivo:\n{ruta}\n"
                f"Verifica el nombre de la carpeta y del archivo."
            )

        df = pd.read_csv(
            ruta,
            sep=";",
            decimal=","
        )

        # Limpieza
        for col in ["Tiempo", "Canal A", "Canal B"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=["Tiempo", "Canal A", "Canal B"])

        return (
            df["Tiempo"].to_numpy(),
            df["Canal A"].to_numpy(),
            df["Canal B"].to_numpy()
        )


    def fix(self):
        """Convierte voltaje → ángulo (rad)."""

        t_a, _, y = self.read()

        t = t_a 
        # No es necesario ms → s
        delta = (y / 1000.0) / 350.0
        theta = delta / self.d

        
        return t, theta


    def result(self):
        """Calcula Tn, fn, wn usando detección de picos."""

        t, theta = self.fix()
        picos, _ = sg.find_peaks(theta, prominence=0.001, distance=80)

        if len(picos) < 2:
            raise ValueError("No se detectaron suficientes picos.")

        
        # Tomar los dos primeros picos en el tiempo
        pico1 = picos[0]
        pico2 = picos[1]

        # Obtener tiempos
        t1 = t[pico1]
        t2 = t[pico2]

        # Periodo = diferencia entre esos tiempos
        T_n = t2 - t1

        # Frecuencia y velocidad angular
        f_n = 1.0 / T_n
        w_n = 2 * np.pi * f_n
        return T_n, f_n, w_n


    def tabulate(self):
        """Retorna tabla con los parámetros dinámicos."""

        T_n, f_n, w_n = self.result()
        df = pd.DataFrame([[T_n, f_n, w_n]],
                          columns=["Periodo Tn (s)", "Frecuencia fn (Hz)", "Velocidad ωn (rad/s)"])
        return df


    def graf(self, save=False, base=None):
        """Grafica la señal angular."""

        t, theta = self.fix()
        
        
            # --- Detección de picos ---
        picos, _ = sg.find_peaks(theta, prominence=0.001, distance=80)
        t_picos = t[picos]
        theta_picos = theta[picos]

        plt.figure()
        plt.plot(t, theta, label="Ángulo (rad)")
        
        #plt.plot(t_picos, theta_picos, "ro", label="Picos detectados")  # <<--- aquí se grafican
            
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Ángulo (rad)")
        plt.title(f"Señal: {self.file}")
        plt.grid(True)
        plt.legend()

        if save and base is not None:
            png_name = base + "_grafica.png"
            plt.savefig(png_name, dpi=300, bbox_inches="tight")
            print(f"Gráfica exportada como: {png_name}")
            plt.close()
        else:
            plt.show()

    def export(self):
        base, _ = os.path.splitext(self.file)

        # Exportar tabla
        df = self.tabulate()
        csv_name = base + "_resultados.csv"
        df.to_csv(csv_name, index=False, sep=";")
        print(f"Tabla exportada como: {csv_name}")

        # Exportar gráfica usando graf
        self.graf(save=True, base=base)


# ============================
# EJEMPLO DE USO
# ============================

"""
analisis = AnalisisLibre() 

tabla = analisis.tabulate()
print(tabla)

analisis.graf()
analisis.export()"""