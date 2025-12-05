import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from libre import AnalisisLibre     


class AnalisisForzadaLibre:
    def __init__(self, d=0.119, Mh=0.05616, r=0.045, k_theta=3):
        """
        d       : distancia sensor–eje [m]
        Mh      : masa faltante [kg]
        r       : radio [m]
        k_theta : rigidez rotacional [N·mm/rad] → se convierte a N·m/rad
        """

        self.d = d
        self.Mh = Mh
        self.r = r
        # N·mm/rad → N·m/rad
        self.k_theta = k_theta * 1e-3     

        # =====================================
        # OBTENER ωₙ AUTOMÁTICAMENTE DE AnalisisLibre
        # =====================================
        # OJO: nombre exacto según tu captura:
        # "Libre - sin amortiguamiento - unido.csv"
        archivo_libre = "Archivos/Libre - sin amortiguamiento - unido.csv"
        analisis_libre = AnalisisLibre(archivo_libre)

        tabla_libre = analisis_libre.tabla()
        # Como solo hay un archivo, tomamos la primera fila
        self.omega_n = tabla_libre["Velocidad ωn (rad/s)"].iloc[0]
        print("ωₙ obtenido del análisis libre =", self.omega_n)

        # FRECUENCIAS FORZADAS: usamos directamente los *_unido.csv
        self.config = {
            3.0: {
                "folder": "Archivos",
                "file": "Forzada sin amortiguamiento 3Hz_unido.csv",
            },
            3.5: {
                "folder": "Archivos",
                "file": "Forzada sin amortiguamiento 3.5Hz_unido.csv",
            },
            4.0: {
                "folder": "Archivos",
                "file": "Forzada sin amortiguamiento 4Hz_unido.csv",
            },
        }

    # ---------------- LEER ARCHIVO ----------------

    def _read_file(self, folder, filename):
        """
        Lee un archivo forzado (tiempo y Canal B).
        Asume separador ';' y coma decimal ','.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))

        if folder:
            ruta = os.path.join(base_dir, folder, filename)
        else:
            ruta = os.path.join(base_dir, filename)

        if not os.path.exists(ruta):
            raise FileNotFoundError(
                f"No se encontró el archivo:\n  {ruta}"
            )

        df = pd.read_csv(
            ruta,
            sep=";",
            decimal=","
        )

        # Convertir columnas a numéricas y eliminar filas no válidas
        for col in ["Tiempo", "Canal B"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=["Tiempo", "Canal B"])

        # En los archivos *_unido.csv el tiempo ya está en segundos (0–6)
        t = df["Tiempo"].to_numpy()
        y_mV = df["Canal B"].to_numpy()
        return t, y_mV

    # ---------------- VOLTAJE → ÁNGULO ----------------

    def _voltaje_a_angulo(self, t, y_mV):
        # t ya viene en segundos
        delta = (y_mV / 1000.0) / 350.0
        theta = delta / self.d
        return t, theta

    # ---------------- AMPLITUD ----------------

    def amplitud(self, theta, frac=0.1):
        """
        Calcula la amplitud a partir de la parte final de la señal
        (para evitar transitorios). frac=0.1 → últimos 90%.
        """
        n0 = int(len(theta) * frac)
        th = theta[n0:]
        return (np.max(th) - np.min(th)) / 2

    # ---------------- ANÁLISIS DE UNA FRECUENCIA ----------------

    def analizar_frecuencia(self, f):

        cfg = self.config[f]
        folder = cfg["folder"]
        filename = cfg["file"]

        t, y_mV = self._read_file(folder, filename)
        t, theta = self._voltaje_a_angulo(t, y_mV)

        # Como el archivo ya está unido, tomamos la amplitud sobre el tramo “estable”
        amp_rad = self.amplitud(theta)
        theta_exp_deg = np.degrees(amp_rad)

        # Fuerza excitadora
        w_f = 2 * np.pi * f
        Pm = self.Mh * self.r * w_f**2

        # Relación de frecuencias
        w_ratio = w_f / self.omega_n

        # Respuesta estática y factor de magnificación (sin amortiguamiento)
        theta_static = Pm / self.k_theta
        M = 1 / abs(1 - w_ratio**2)
        theta_teo_deg = np.degrees(theta_static * M)

        FA = theta_exp_deg / theta_teo_deg

        return Pm, theta_exp_deg, theta_teo_deg, FA, w_ratio

    # ---------------- TABLA FINAL ----------------

    def tabla_resultados(self):
        filas = []

        for f in self.config.keys():
            filas.append([f] + list(self.analizar_frecuencia(f)))

        tabla = pd.DataFrame(
            filas,
            columns=[
                "Frecuencia (Hz)",
                "Pm (N)",
                "θ_exp (°)",
                "θ_teo (°)",
                "FA",
                "ωf/ωn",
            ],
        )
        return tabla


    # ---------------- GRÁFICA COMPLETA ωf/ωn ----------------

    def graficar_wf_wn(self):
        """
        Grafica:
        - Curva teórica del factor de amplificación 1 / |1 - r^2|
        - Puntos experimentales FA vs ωf/ωn
        """

        # ---------- Datos experimentales ----------
        tabla = self.tabla_resultados()
        r_exp = tabla["ωf/ωn"].to_numpy()
        FA_exp = tabla["FA"].to_numpy()

        # ---------- Curva teórica ----------
        r = np.linspace(0, 2.0, 500)
        M_teo = 1 / np.abs(1 - r**2)

        # ---------- Graficar ----------
        plt.figure(figsize=(8,5))

        # Curva teórica
        plt.plot(r, M_teo, label="Curva teórica (sin amortiguamiento)", color="blue")

        # Puntos experimentales
        plt.plot(r_exp, FA_exp, "ro", markersize=8, label="Datos experimentales")

        # Líneas verticales desde los puntos experimentales a la curva
        for xi, yi in zip(r_exp, FA_exp):
            plt.plot([xi, xi], [0, yi], "r--", linewidth=0.7)

        plt.xlabel("ωf / ωn")
        plt.ylabel("FA = θ_exp / θ_teo")
        plt.title("Factor de amplificación vs razón de frecuencias")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

# =============================
# EJECUCIÓN
# =============================


analisis = AnalisisForzadaLibre()
tabla = analisis.tabla_resultados()
print(tabla)
analisis.graficar_wf_wn()
