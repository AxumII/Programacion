import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sg

from libre import AnalisisLibre

class AnalisisForzada:
    def __init__(
        self,
        d=0.119,
        L=0.845,    
        Mh=0.05616,
        r=0.045,
        k=1.5,        #  kN/m
        config=None
    ):
        if config is None:
            config = {
                2.9: {
                    "folder": "Archivos",
                    "file": "Forzado libre 2,9.csv",
                },
                3.1: {
                    "folder": "Archivos",
                    "file": "Forzado libre 3,1.csv",
                },
                3.5: {
                    "folder": "Archivos",
                    "file": "Forzado libre 3,5.csv",
                },
            }

        self.d = d
        self.L = L
        self.Mh = Mh
        self.r = r
        # Corrección: kN/m a N/m para mantener consistencia 
        self.k = k * 1000.0  

        self.config = config
        self.w_n = self.extract_w_n()

    def extract_w_n(self):
        analisis = AnalisisLibre()
        _, _, w_n = analisis.result()
        return w_n

    def p2p(self, theta, frac=0.1):
        n0 = int(len(theta) * frac)
        th = theta[n0:]
        return (np.max(th) - np.min(th)) / 2

    def read(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        datos = {}

        for freq, info in self.config.items():
            folder = info["folder"]
            file = info["file"]
            ruta = os.path.join(base_dir, folder, file)

            if not os.path.exists(ruta):
                raise FileNotFoundError(
                    f"No se encontró el archivo:\n{ruta}\n"
                )

            # Salta la fila de unidades
            df = pd.read_csv(
                ruta,
                sep=";",
                decimal=",",
                skiprows=[1]
            )

            for col in ["Tiempo", "Canal A", "Canal B"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            df = df.dropna(subset=["Tiempo", "Canal A", "Canal B"])
            datos[freq] = (
                df["Tiempo"].to_numpy(),
                df["Canal A"].to_numpy(),
                df["Canal B"].to_numpy()
            )

        return datos

    def fix(self):
        datos = self.read()
        resultados = {}

        for freq, (t, _, y) in datos.items():
            t = t - t[0]
            delta = y / 350.0
            theta = delta / self.d
            resultados[freq] = (t, theta)

        return resultados

    def phi_exp(self, t, x, y):
        n0 = len(t) // 2
        t_ss = t[n0:]
        x_ss = x[n0:]
        y_ss = y[n0:]

        idx_zc = np.where((y_ss[:-1] <= 0.0) & (y_ss[1:] > 0.0))[0]
        if len(idx_zc) < 2:
            return 0.0, 1.0, 0.0
        t_zc = t_ss[idx_zc]

        umbral = (np.max(x_ss) + np.min(x_ss)) / 2.0
        idx_edges = np.where((x_ss[:-1] <= umbral) & (x_ss[1:] > umbral))[0]
        if len(idx_edges) < 2:
            return 0.0, 1.0, 0.0
        t_edges = t_ss[idx_edges]

        T = np.mean(np.diff(t_edges))

        deltas = []
        for te in t_edges:
            posteriores = t_zc[t_zc >= te]
            if len(posteriores) == 0:
                continue
            tz = posteriores[0]
            deltas.append(tz - te)

        if len(deltas) == 0:
            return 0.0, T, 0.0

        delta_t = np.mean(deltas)
        phi = (-(delta_t / T)*(2.0 * np.pi)) - (np.pi/2)
        phi = np.arctan2(np.sin(phi), np.cos(phi))

        return phi, T, delta_t

    def result(self):
        resultados = {}
        datos_ang = self.fix()
        datos_raw = self.read()

        for f_forzada, (t, theta) in datos_ang.items():
            w_f = 2.0 * np.pi * f_forzada
            P_m = self.Mh * self.r * (w_f ** 2)

            r = w_f / self.w_n
            
            # CORRECCIÓN: Deflexión estática angular (Torque / K_rotacional)
            # Torque = P_m * L, K_rot = k * L^2  => theta_st = P_m / (k * L)
            theta_st = P_m / (self.k * self.L)
            
            theta_m_teorico = theta_st / np.abs(1.0 - r**2)
            theta_m_exp = self.p2p(theta)

            FA = theta_m_exp / theta_st

            phi_teorico = 0.0 if r < 1.0 else -np.pi

            t_raw, x_raw, y_raw = datos_raw[f_forzada]
            phi_exp, T_exp, delta_t = self.phi_exp(t_raw, x_raw, y_raw)

            resultados[f_forzada] = {
                "f": f_forzada,
                "w_f": w_f,
                "P_m": P_m,
                "theta_m_teorico": theta_m_teorico,
                "theta_m_exp": theta_m_exp,
                "FA": FA,
                "r": r,
                "phi_teorico": phi_teorico,
                "phi_exp": phi_exp,
                "T_exp": T_exp,
                "delta_t": delta_t
            }

        return resultados

    def tabulate(self):
        resultados = self.result()
        filas = []
        for f_motor, vals in resultados.items():
            filas.append({
                "Frecuencia (Hz)": f_motor,
                "Pm (N)": round(vals["P_m"], 4),
                "theta_m Exp (°)": round(np.degrees(vals["theta_m_exp"]), 4),
                "theta_m Teo (°)": round(np.degrees(vals["theta_m_teorico"]), 4),
                "FA": round(vals["FA"], 4),
                "wf/wn": round(vals["r"], 4)
            })

        df = pd.DataFrame(filas).sort_values("Frecuencia (Hz)")
        return df

    def graf_resonance(self, n_points=500, save=False, base="Forzada", out_dir=None):
        resultados = self.result()
        if not resultados:
            print("No hay datos para graficar.")
            return

        r_exp = []
        FA_exp = []

        for f_forzada, vals in resultados.items():
            r_exp.append(vals["r"])
            FA_exp.append(vals["FA"])

        r_exp = np.array(r_exp)
        FA_exp = np.array(FA_exp)

        # Se segmenta el dominio teórico para evitar el pico infinito matemático en r=1
        r_grid_left = np.linspace(0.4, 0.98, int(n_points/2))
        r_grid_right = np.linspace(1.02, 1.5, int(n_points/2))
        
        FA_teorico_left = 1.0 / np.abs(1.0 - r_grid_left**2)
        FA_teorico_right = 1.0 / np.abs(1.0 - r_grid_right**2)

        plt.figure(figsize=(8, 5))
        plt.plot(r_grid_left, FA_teorico_left, color="blue", label="Teórico (Amortiguamiento nulo)")
        plt.plot(r_grid_right, FA_teorico_right, color="blue")
        
        plt.scatter(r_exp, FA_exp, color="red", zorder=5, s=80, edgecolors="black", label="Datos experimentales")
        plt.axvline(1.0, color="gray", linestyle="--", label="Resonancia (r=1)")

        # Limitar Y dinámicamente según la amplitud experimental máxima para que la gráfica no se rompa
        plt.ylim(0, np.max(FA_exp) * 1.5)
        plt.xlim(0.4, max(1.5, np.max(r_exp) * 1.1))

        plt.xlabel(r"$\omega_f / \omega_n$")
        plt.ylabel("FA")
        plt.title("Factor de Amplificación Dinámica (Sin Amortiguamiento)")
        plt.grid(True, alpha=0.4)
        plt.legend()
        plt.tight_layout()

        if save:
            filename = base + "_resonancia_grafica.png"
            if out_dir:
                ruta_grafica = os.path.join(out_dir, filename)
                os.makedirs(out_dir, exist_ok=True)
            else:
                ruta_grafica = filename
            plt.savefig(ruta_grafica, dpi=300, bbox_inches="tight")
            print(f"Gráfica de resonancia guardada en: {ruta_grafica}")
            plt.close()
        else:
            plt.show()

    def export(self, base="Forzada", out_dir=None):
        df = self.tabulate()
        csv_name = base + "_resonancia_resultados.csv"
        
        if out_dir:
            ruta_csv = os.path.join(out_dir, csv_name)
            os.makedirs(out_dir, exist_ok=True)
        else:
            ruta_csv = csv_name
            
        df.to_csv(ruta_csv, index=False, sep=";")
        print(f"Tabla exportada en: {ruta_csv}")
        self.graf_resonance(save=True, base=base, out_dir=out_dir)

if __name__ == "__main__":
    try:
        OUTPUT_DIR = r"C:\GitHub\Programacion\Python\Dinamica\Lab 2026\Resultados"
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        print("Iniciando análisis forzado...\n")
        af = AnalisisForzada()

        tabla_forzada = af.tabulate()
        print("\n--- Tabla de Resultados Forzados Sin Amortiguamiento ---")
        print(tabla_forzada.to_string(index=False))
        
        af.export(out_dir=OUTPUT_DIR)
        
    except Exception as e:
        print(f"Ocurrió un error en la ejecución: {e}")