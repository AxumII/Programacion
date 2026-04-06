import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sg

from libre import AnalisisLibre


class AnalisisLibreAmortiguado:
    def __init__(
        self,
        d=0.119,   # m  distancia sensor–eje
        L=0.845,   # m
        n=3,       # n picos
        k=3,        #kN/m
        config=None,
    ):
        """
        d   : distancia sensor–eje [m]
        L   : longitud [m]
        n   : número de picos entre d0 y dn
        """

        if config is None:
            config = {
                "Abierta": {
                    "folder": "Archivos",
                    "file": "Libre - con amortiguamiento - abierto_unido.csv",
                },
                "Cerrada": {
                    "folder": "Archivos",
                    "file": "Libre - con amortiguamiento - cerrado_unido.csv",
                },
            }

        # Constantes del sistema
        self.d = d
        self.L = L
        self.k = k / 1e-3
        self.n = n
        self.m_amort = 0.275    #Kg
        self.config = config
        

        # wn tomada del caso libre
        self.w_n = self.extract_w_n()
        self.I = ((self.k* self.L**2)/self.w_n**2) + (self.m_amort* self.L**2)

    # ---------------------------------------------------------
    def read(self):
        """
        Lee TODOS los archivos de self.config.
        Devuelve un diccionario:
        {
            "Abierta": (tiempo, canal_a, canal_b),
            "Cerrada": (tiempo, canal_a, canal_b)
        }
        """

        base_dir = os.path.dirname(os.path.abspath(__file__))
        datos = {}

        for caso, info in self.config.items():
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

            datos[caso] = (tiempo, canal_a, canal_b)

        return datos

    # ---------------------------------------------------------
    def fix(self):
        """
        Convierte voltajes → ángulos (rad) para cada archivo.
        Devuelve:
        {
            "Abierta": (t, theta),
            "Cerrada": (t, theta)
        }
        """
        datos = self.read()
        resultados = {}

        for caso, (t_a, _, y) in datos.items():
            t = t_a  # ya está en segundos
            # y está en mV, sensor 350 mV/mm → dividir entre 1000 y 350
            delta = (y / 1000.0) / 350.0  # [m]
            theta = delta / self.d        # [rad]

            resultados[caso] = (t, theta)

        return resultados

    # ---------------------------------------------------------
    def p2p(self, theta, frac=0.1):
        """
        Calcula la amplitud pico a pico a partir de la fraccion de la señal
        """
        n0 = int(len(theta) * frac)
        th = theta[n0:]
        return (np.max(th) - np.min(th)) / 2

    # ---------------------------------------------------------
    def extract_w_n(self):
        analisis = AnalisisLibre()
        T_n, f_n, w_n = analisis.result()
        return w_n
       
        
    # ---------------------------------------------------------
    def result(self):
        """
        Calcula todos los parámetros para cada caso.
        Devuelve un diccionario:
        {
            'Abierta': {...},
            'Cerrada': {...}
        }
        """
        resultados = {}
        datos = self.fix()  # dict: caso -> (t, theta)

        for caso, (t, theta) in datos.items():
            

            # Buscar picos
            picos, _ = sg.find_peaks(theta, prominence=0.001, distance=80)

            if len(picos) <= self.n:
                raise ValueError(
                    f"No hay suficientes picos en el caso '{caso}' para n={self.n}"
                )

            t_peaks = t[picos]
            amps = np.abs(theta[picos])

            # Tomar los dos primeros picos para Td
            pico1 = picos[0]
            pico2 = picos[1]
            t1 = t[pico1]
            t2 = t[pico2]

            # Periodo amortiguado, frecuencia y velocidad angular amortiguada
            T_d = t2 - t1
            f_d = 1.0 / T_d
            w_d = 2 * np.pi * f_d

            # Amplitudes (en rad)
            d0_theta = amps[0]
            dn_theta = amps[self.n]

            # Pasar amplitudes de rad → V (invirtiendo la conversión)
            escala = 1000.0 * 350.0 * self.d
            d0_V = d0_theta * escala
            dn_V = dn_theta * escala

            # Coeficiente de amortiguamiento crítico
            Cc = (2 * self.I * self.w_n) / (self.L ** 2)

            # Zeta: factor de amortiguamiento
            # zeta = L / sqrt(L^2 + 4*pi^2*n^2), con L = ln(d0/dn)
            L_log = np.log(d0_V / dn_V)
            zeta = L_log / np.sqrt(L_log ** 2 + 4 * np.pi ** 2 * self.n ** 2)

            #Coeficiente de amortiguamento
            C = zeta*Cc

            resultados[caso] = dict(
                d0=d0_V,
                dn=dn_V,
                Td=T_d,
                wd=w_d,
                zeta=zeta,
                C=C,
            )

        return resultados

    # ---------------------------------------------------------
    def tabulate(self):

        res = self.result()

        filas = []
        index = []
        for caso, vals in res.items():
            filas.append([
                vals["d0"],
                vals["dn"],
                vals["Td"],
                vals["wd"],
                vals["zeta"],
                vals["C"],
            ])
            index.append(caso)

        columnas = ["d0 [mV]", "dn [mV]", "Td [s]", "ωd [rad/s]", "ζ", "C [Ns/m]"]

        df = pd.DataFrame(filas, index=index, columns=columnas)
        return df

    # ---------------------------------------------------------
    def graf(self, save=False, base=None):
        """
        Grafica el voltaje del Canal B vs tiempo para cada caso.
        """
        datos = self.read()

        plt.figure()
        for caso, (t, _, canal_b) in datos.items():
            # canal_b viene en mV → pasar a V para ser consistentes con la etiqueta
            plt.plot(t, canal_b / 1000.0, label=caso)

        plt.xlabel("Tiempo [s]")
        plt.ylabel("Voltaje Canal B [V]")
        plt.title("Respuesta libre amortiguada")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        if save and base is not None:
            png_name = base + "_grafica.png"
            plt.savefig(png_name, dpi=300, bbox_inches="tight")
            print(f"Gráfica exportada como: {png_name}")
            plt.close()
        else:
            plt.show()

    def export(self, base="Libre Amortiguada"):
        """
        Exporta:
        - la tabla procesada de vibración forzada (CSV)
        - la gráfica de FA vs r (PNG) usando graf_resonance()

        base : prefijo para los nombres de archivo exportados
        """

        # ===== EXPORTAR TABLA =====

        df = self.tabulate()
        csv_name = base + "_resultados.csv"
        df.to_csv(csv_name, index=False, sep=";")
        print(f"Tabla exportada como: {csv_name}")

        # Exportar gráfica usando graf
        self.graf(save=True, base=base)

    
# ----------------- Uso -----------------

"""
analisis = AnalisisLibreAmortiguado()

# Tabla pedida
tabla = analisis.tabulate()
print(tabla)

# Gráfica
analisis.graf()
#analisis.export()
"""