import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sg

class AnalisisLibre:
    def __init__(self, 
                 file="Libre 1.csv",
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
            decimal=",",
            skiprows=[1] 
        )

        for col in ["Tiempo", "Canal A", "Canal B"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=["Tiempo", "Canal A", "Canal B"])

        return (
            df["Tiempo"].to_numpy(),
            df["Canal A"].to_numpy(),
            df["Canal B"].to_numpy()
        )

    def fix(self):
        t, _, y = self.read()
        delta = y / 350.0
        theta = delta / self.d

        # 1. Corrección inicial: empezar la escala en 0
        t = t - t[0]

        # 2. Alineación automática: sincronizar para que el primer pico ocurra en t = 0
        rango = np.max(theta) - np.min(theta)
        prom_dinamica = rango * 0.15
        picos, _ = sg.find_peaks(np.abs(theta), prominence=prom_dinamica, distance=500)

        if len(picos) > 0:
            t_inicio = t[picos[0]]
            t = t - t_inicio

        # Mantener un margen pequeño antes del primer pico para la gráfica
        mascara = t >= -0.1
        return t[mascara], theta[mascara]

    def result(self):
        t, theta = self.fix()
        
        rango = np.max(theta) - np.min(theta)
        prom_dinamica = rango * 0.15
        picos, _ = sg.find_peaks(theta, prominence=prom_dinamica, distance=100)

        if len(picos) < 2:
            raise ValueError(
                f"No se encontraron suficientes picos en '{self.file}'."
            )

        t_peaks = t[picos]

        Tn = (t_peaks[-1] - t_peaks[0]) / (len(t_peaks) - 1)
        fn = 1.0 / Tn
        wn = 2 * np.pi * fn

        return Tn, fn, wn

    def graf(self, save=False, base=None, out_dir=None):
        t, theta = self.fix()

        plt.figure()
        plt.plot(t, theta, label="Ángulo θ (rad)")
        plt.xlabel("Tiempo [s]")
        plt.ylabel("Ángulo θ [rad]")
        plt.title(f"Oscilación Libre - {self.file} (Sincronizada)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        if save and base is not None:
            nombre_grafica = base + "_grafica.png"
            if out_dir:
                ruta_grafica = os.path.join(out_dir, nombre_grafica)
                os.makedirs(out_dir, exist_ok=True)
            else:
                ruta_grafica = nombre_grafica
            plt.savefig(ruta_grafica, dpi=300, bbox_inches="tight")
            print(f"Gráfica exportada en: {ruta_grafica}")
            plt.close()
        else:
            plt.show()


if __name__ == "__main__":
    OUTPUT_DIR = r"C:\GitHub\Programacion\Python\Dinamica\Lab 2026\Resultados"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    archivos = ["Libre 1.csv", "Libre 2.csv", "Libre 3.csv"]
    resultados_totales = []

    for archivo in archivos:
        base_name = os.path.splitext(archivo)[0]
        try:
            analisis = AnalisisLibre(file=archivo)
            Tn, fn, wn = analisis.result()
            resultados_totales.append({
                "Archivo": archivo,
                "Periodo Tn (s)": Tn,
                "Frecuencia fn (Hz)": fn,
                "Velocidad ωn (rad/s)": wn
            })
            print(f"✔ Éxito procesando '{archivo}'")
            analisis.graf(save=True, base=base_name, out_dir=OUTPUT_DIR)
        except Exception as e:
            print(f"❌ Error procesando '{archivo}': {e}")

    if resultados_totales:
        df_resultados = pd.DataFrame(resultados_totales)
        print("\n--- Tabla de Resultados Consolidados ---")
        print(df_resultados.to_string(index=False))
        ruta_csv_final = os.path.join(OUTPUT_DIR, "Resultados_Libres_Consolidados.csv")
        df_resultados.to_csv(ruta_csv_final, index=False, sep=";")
        print(f"Tabla consolidada exportada en: {ruta_csv_final}")