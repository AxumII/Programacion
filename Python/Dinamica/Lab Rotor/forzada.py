import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class AnalisisForzadaLibre:
    def __init__(self, omega_n, d=0.119, Mh=0.05616, r=0.045, k_theta=None):
        """
        omega_n : velocidad angular natural [rad/s] (la pones tú)
        d       : distancia sensor–eje [m]
        Mh      : masa faltante [kg]  (56.16 g -> 0.05616 kg)
        r       : radio [m]           (45 mm -> 0.045 m)
        k_theta : rigidez rotacional [N·m/rad] (si la conoces; si no, dejar None)
        """
        self.omega_n = omega_n
        self.d = d
        self.Mh = Mh
        self.r = r
        self.k_theta = k_theta

        # Ajusta nombres si tus carpetas/archivos se llaman distinto
        self.config = {
            3.0: {
                "folder": "Forzada sin amortiguamiento 3Hz",
                "pattern": "Forzada sin amortiguamiento 3Hz_{}.csv",
                "runs": 6,
            },
            3.5: {
                "folder": "Forzada sin amortiguamiento 3.5Hz",
                "pattern": "Forzada sin amortiguamiento 3.5Hz_{}.csv",
                "runs": 6,
            },
            4.0: {
                "folder": "Forzada sin amortiguamiento 4Hz",
                "pattern": "Forzada sin amortiguamiento 4Hz_{}.csv",
                "runs": 6,
            },
        }

    # ---------- utilidades internas ----------

    def _read_file(self, folder, filename):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.join(base_dir, folder, filename)

        df = pd.read_csv(
            ruta,
            sep=";",
            decimal=",",
            skiprows=[1, 2],
        )

        t_ms = df["Tiempo"].to_numpy()   # [ms]
        y_mV = df["Canal B"].to_numpy()  # [mV]
        return t_ms, y_mV

    def _voltaje_a_angulo(self, t_ms, y_mV):
        t = t_ms * 1e-3                 # [s]
        delta = (y_mV / 1000.0) / 350.0 # -> distancia
        theta = delta / self.d          # [rad]
        return t, theta

    def _amplitud_steady_state(self, theta, frac_descartar=0.1):
        """
        Amplitud (max-min)/2 ignorando el primer 'frac_descartar' de datos
        para quitar el transitorio.
        """
        n0 = int(len(theta) * frac_descartar)
        th_ss = theta[n0:]
        amp = (np.max(th_ss) - np.min(th_ss)) / 2.0
        return amp

    # ---------- cálculo para una frecuencia f ----------

    def analizar_frecuencia(self, f):
        """
        Analiza todas las corridas de una frecuencia dada (3, 3.5, 4 Hz)
        y devuelve:
           Pm, θm_exp (deg), θm_teo (deg o NaN), FA (o NaN), ωf/ωn
        """
        cfg = self.config[f]
        folder = cfg["folder"]
        pattern = cfg["pattern"]
        runs = cfg["runs"]

        amplitudes_deg = []

        for i in range(1, runs + 1):
            filename = pattern.format(i)
            t_ms, y_mV = self._read_file(folder, filename)
            t, theta = self._voltaje_a_angulo(t_ms, y_mV)
            amp_rad = self._amplitud_steady_state(theta)
            amplitudes_deg.append(np.degrees(amp_rad))

        theta_exp_deg = float(np.mean(amplitudes_deg))

        # Fuerza de excitación
        omega_f = 2.0 * np.pi * f
        Pm = self.Mh * self.r * (omega_f ** 2)  # [N]

        w_ratio = omega_f / self.omega_n

        # Si conoces k_theta, calculamos θ_teo y FA
        if self.k_theta is not None:
            theta_static_rad = Pm / self.k_theta      # amplitud estática
            M = 1.0 / abs(1.0 - w_ratio ** 2)         # magnificación sin amortiguamiento
            theta_teo_rad = theta_static_rad * M
            theta_teo_deg = np.degrees(theta_teo_rad)
            FA = theta_exp_deg / theta_teo_deg
        else:
            theta_teo_deg = np.nan
            FA = np.nan

        return Pm, theta_exp_deg, theta_teo_deg, FA, w_ratio

    # ---------- tabla final ----------

    def tabla_resultados(self):
        filas = []

        for f in sorted(self.config.keys()):
            Pm, theta_exp_deg, theta_teo_deg, FA, w_ratio = self.analizar_frecuencia(f)

            filas.append([
                f,
                Pm,
                theta_exp_deg,
                theta_teo_deg,
                FA,
                w_ratio,
            ])

        tabla = pd.DataFrame(
            filas,
            columns=[
                "Frecuencia (Hz)",
                "Pm (N)",
                "θm Exp (°)",
                "θm Teo (°)",
                "FA",
                "ωf/ωn",
            ],
        )

        return tabla
# Ejemplo: si f_n teórica = 1.2 Hz
omega_n_teo = 2 * np.pi * 1.2   # cámbialo por tu valor real

analisis_f = AnalisisForzadaLibre(omega_n=omega_n_teo)

tabla = analisis_f.tabla_resultados()
print(tabla)