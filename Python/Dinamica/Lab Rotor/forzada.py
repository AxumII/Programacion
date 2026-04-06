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
        Mh=0.05616,
        r=0.045,
        k=3,
        config=None
    ):
        """
        d   : distancia sensor–eje [m]
        Mh  : masa faltante [kg]
        r   : radio [m]
        k   : rigidez rotacional [N·mm/rad] → se convierte a N·m/rad
        config : diccionario con info de archivos (frecuencia → {folder, file})
        """

        # Si no se pasa config, usamos la que definiste:
        if config is None:
            config = {
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

        # Constantes del sistema
        self.d = d
        self.Mh = Mh
        self.r = r
        self.k = k / 1e-3   

        # Archivos forzados (3 Hz, 3.5 Hz, 4 Hz)
        self.config = config

        # wn tomada del caso libre
        self.w_n = self.extract_w_n()

    def extract_w_n(self):
        analisis = AnalisisLibre()
        T_n, f_n, w_n = analisis.result()
        return w_n
    
    def p2p(self, theta, frac=0.1):
        """
        Calcula la amplitud a partir de la fraccion de la respuesta
        """
        n0 = int(len(theta) * frac)
        th = theta[n0:]
        return (np.max(th) - np.min(th)) / 2

    def read(self):
        """
        Lee TODOS los archivos de self.config.
        Devuelve un diccionario:
        {
            3.0: (tiempo, canal_a, canal_b),
            3.5: (tiempo, canal_a, canal_b),
            4.0: (tiempo, canal_a, canal_b)
        }
        """

        base_dir = os.path.dirname(os.path.abspath(__file__))
        datos = {}

        for freq, info in self.config.items():
            folder = info["folder"]
            file = info["file"]

            ruta = os.path.join(base_dir, folder, file)

            if not os.path.exists(ruta):
                raise FileNotFoundError(
                    f"No se encontró el archivo:\n{ruta}\n"
                    f"Verifica el nombre de la carpeta y del archivo."
                )

            df = pd.read_csv(
                ruta,
                sep=";",
                decimal=",",
            )

            # Limpieza
            for col in ["Tiempo", "Canal A", "Canal B"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            df = df.dropna(subset=["Tiempo", "Canal A", "Canal B"])

            tiempo = df["Tiempo"].to_numpy()
            canal_a = df["Canal A"].to_numpy()
            canal_b = df["Canal B"].to_numpy()

            datos[freq] = (tiempo, canal_a, canal_b)

        return datos

    def fix(self):
        """
        Convierte voltajes → ángulos (rad) para cada archivo.
        Devuelve:
        {
            3.0: (t, theta),
            3.5: (t, theta),
            4.0: (t, theta)
        }
        """
        datos = self.read()
        resultados = {}

        for freq, (t_a, _, y) in datos.items():
            t = t_a  # ya está en segundos
            delta = (y / 1000.0) / 350.0
            theta = delta / self.d

            resultados[freq] = (t, theta)

        return resultados

    def result(self):
        """
        Calcula, para cada frecuencia forzada:
        - w_f : frecuencia angular forzada
        - P_m : carga dinámica equivalente
        - theta_m_teorico : amplitud teórica en régimen permanente
        - theta_m_exp : amplitud experimental (pico a pico/2)
        - FA : factor de amplificación
        - r : relación w_f / w_n

        Devuelve un diccionario:
        {
            3.0: {...},
            3.5: {...},
            4.0: {...}
        }
        """
        datos_theta = self.fix()   # {freq: (t, theta)}
        resultados = {}

        for f_forzada, (t, theta) in datos_theta.items():
            # Frecuencia angular de excitación
            w_f = 2 * np.pi * f_forzada

            # Carga dinámica
            P_m = self.Mh * self.r * w_f**2

            k = self.k  # rigidez en N·m/rad

            # Amplitud teórica (modelo)
            theta_m_teorico = (P_m / k) / (1 - (w_f / self.w_n)**2)

            # Amplitud experimental (pico a pico/2)
            theta_m_exp = self.p2p(theta)

            # Factor de amplificación
            FA = theta_m_exp / (P_m / k)

            # Relación de frecuencia
            r = w_f / self.w_n

            resultados[f_forzada] = {
                "w_f": w_f,
                "P_m": P_m,
                "theta_m_teorico": theta_m_teorico,
                "theta_m_exp": theta_m_exp,
                "FA": FA,
                "r": r,
            }

        return resultados

    def tabulate(self):
        """
        Devuelve un DataFrame con una fila por velocidad del motor.
        Columnas:
        - f_motor (Hz) = rev/s del motor
        - w_f (rad/s)
        - P_m (N·m)
        - theta_m_teorico (rad)
        - theta_m_exp (rad)
        - FA
        - r = w_f/w_n
        """
        resultados = self.result()

        filas = []
        for f_motor, vals in resultados.items():
            filas.append(
                {
                    "f_motor (Hz)": f_motor,                # Hz = rev/s
                    "w_f (rad/s)": vals["w_f"],
                    "P_m (N·m)": vals["P_m"],
                    "theta_m_teorico (rad)": vals["theta_m_teorico"],
                    "theta_m_exp (rad)": vals["theta_m_exp"],
                    "FA": vals["FA"],
                    "r = w_f/w_n": vals["r"],
                }
            )

        df = pd.DataFrame(filas).sort_values("f_motor (Hz)")
        return df

    def graf_resonance(self, n_points=500, save=False, base="Forzada"):
        """
        Grafica la curva teórica de amplificación FA vs r = wf/wn
        junto con los datos experimentales obtenidos en tabulate().
        """

        # ======= 1. Datos experimentales =======
        df = self.tabulate()
        r_exp = df["r = w_f/w_n"].to_numpy()
        FA_exp = df["FA"].to_numpy()

        # Si por alguna razón no hay datos:
        if len(r_exp) == 0:
            print("No hay datos experimentales para graficar.")
            return

        # ======= 2. Curva teórica =======
        # Rango de r: desde 0 hasta algo mayor que tus r_exp
        r_min = 0.4
        r_max = max(1.2, np.max(r_exp) * 1.5)   # evita quedarte demasiado cerca de 0
        r_teo = np.linspace(r_min, r_max, n_points)

        FA_teo = 1.0 / np.abs(1.0 - r_teo**2)   # modelo sin amortiguamiento

        # ======= 3. Crear figura =======
        plt.figure(figsize=(8, 5))

        # Curva teórica
        plt.plot(r_teo, FA_teo, label="Curva teórica")

        # Datos experimentales
        plt.scatter(
            r_exp,
            FA_exp,
            s=80,
            zorder=10,
            edgecolors="black",
            linewidth=2,
            label="Datos experimentales"
        )

        # Línea de resonancia r = 1
        plt.axvline(1.0, linestyle="--", label="Resonancia (r=1)")

        # Etiquetas, título, etc.
        plt.title("Curva de Amplificación vs Relación de Frecuencia")
        plt.xlabel(r"$\omega_f / \omega_n$")
        plt.ylabel("FA")
        plt.grid(True, alpha=0.4)
        plt.ylim(0, 50)

        plt.legend()

        # ======= 5. Guardar o mostrar =======
        if save:
            filename = base + "_resonancia_grafica.png"
            plt.savefig(filename, dpi=300, bbox_inches="tight")
            print(f"Gráfica exportada como: {filename}")
            plt.close()
        else:
            plt.show()

    def export(self, base="Forzada"):
        """
        Exporta:
        - la tabla procesada de vibración forzada (CSV)
        - la gráfica de FA vs r (PNG) usando graf_resonance()

        base : prefijo para los nombres de archivo exportados
        """

        # ===== EXPORTAR TABLA =====
        df = self.tabulate()
        csv_name = base + "_resonancia_resultados.csv"
        df.to_csv(csv_name, index=False, sep=";")
        print(f"Tabla exportada como: {csv_name}")

        # ===== EXPORTAR GRÁFICA =====
        self.graf_resonance(save=True, base=base)

    
    
 
  
af = AnalisisForzada()

# Obtener diccionario con resultados
res = af.result()
print(res[3.0]["theta_m_exp"])

# Obtener tabla
tabla_forzada = af.tabulate()
print(tabla_forzada)
af.graf_resonance()
#af.export()