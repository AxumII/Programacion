import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sg

from libre import AnalisisLibre

class AnalisisLibreAmortiguado:
    def __init__(
        self,
        d=0.119,   
        L=0.845,   
        n=3,       
        k=1.5,     # kN/m
        config=None,
    ):
        if config is None:
            config = {
                "Abierto 1": {"folder": "Archivos", "file": "Amortiguado Libre abierto 1.csv"},
                "Abierto 2": {"folder": "Archivos", "file": "Amortiguado Libre abierto 2.csv"},
                "Abierto 3": {"folder": "Archivos", "file": "Amortiguado Libre abierto 3.csv"},
                "Cerrado 1": {"folder": "Archivos", "file": "Amortiguado Libre cerrado 1.csv"},
                "Cerrado 2": {"folder": "Archivos", "file": "Amortiguado Libre cerrado 2.csv"},
                "Cerrado 3": {"folder": "Archivos", "file": "Amortiguado Libre cerrado 3.csv"},
            }

        self.d = d
        self.L = L
        self.k = k / 1e-3  
        self.n = n
        self.m_amort = 0.275  
        self.config = config
        
        self.w_n = self.extract_w_n()
        self.I = ((self.k * self.L**2) / self.w_n**2) + (self.m_amort * self.L**2)

    def read(self):
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

            df = pd.read_csv(ruta, sep=";", decimal=",", skiprows=[1])

            for col in ["Tiempo", "Canal A", "Canal B"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            df = df.dropna(subset=["Tiempo", "Canal A", "Canal B"])

            tiempo = df["Tiempo"].to_numpy()
            canal_a = df["Canal A"].to_numpy()
            canal_b = df["Canal B"].to_numpy()

            datos[caso] = (tiempo, canal_a, canal_b)

        return datos

    def fix(self):
        datos = self.read()
        resultados = {}

        for caso, (t, _, y) in datos.items():
            delta = y / 350.0       
            theta = delta / self.d  

            # 1. Ajuste de tiempo inicial
            t = t - t[0]

            # 2. Sincronización de picos
            rango_senal = np.max(theta) - np.min(theta)
            prom_dinamica = rango_senal * 0.15
            picos, _ = sg.find_peaks(np.abs(theta), prominence=prom_dinamica, distance=1000)

            if len(picos) > 0:
                t_inicio = t[picos[0]]
                t = t - t_inicio

            mascara = t >= -0.1
            resultados[caso] = (t[mascara], theta[mascara])

        return resultados

    def p2p(self, theta, frac=0.1):
        n0 = int(len(theta) * frac)
        th = theta[n0:]
        return (np.max(th) - np.min(th)) / 2

    def extract_w_n(self):
        analisis = AnalisisLibre()
        T_n, f_n, w_n = analisis.result()
        return w_n
        
    def result(self):
        resultados = {}
        datos = self.fix() 

        for caso, (t, theta) in datos.items():
            rango_senal = np.max(theta) - np.min(theta)
            prom_dinamica = rango_senal * 0.15
            picos, _ = sg.find_peaks(theta, prominence=prom_dinamica, distance=1000)

            if len(picos) <= self.n:
                raise ValueError(
                    f"No hay suficientes picos en el caso '{caso}' para n={self.n}"
                )

            t_peaks = t[picos]
            amps = np.abs(theta[picos])

            # Al estar sincronizados en t=0, t_peaks[0] es ~ 0
            T_d = t_peaks[1] - t_peaks[0]
            f_d = 1.0 / T_d
            w_d = 2 * np.pi * f_d

            d0_theta = amps[0]
            dn_theta = amps[self.n]

            escala_mV = self.d * 350.0 * 1000.0
            d0_mV = d0_theta * escala_mV
            dn_mV = dn_theta * escala_mV

            Cc = (2 * self.I * self.w_n) / (self.L ** 2)

            L_log = np.log(d0_mV / dn_mV)
            zeta = L_log / np.sqrt(L_log ** 2 + 4 * np.pi ** 2 * self.n ** 2)
            C = zeta * Cc

            resultados[caso] = dict(
                d0=d0_mV,
                dn=dn_mV,
                Td=T_d,
                wd=w_d,
                zeta=zeta,
                C=C,
            )

        return resultados

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

    def graf(self, save=False, base=None, out_dir=None):
        datos = self.fix()

        # 1. GRÁFICA COMBINADA (Sincronizada)
        plt.figure(figsize=(10, 6))
        for caso, (t, theta) in datos.items():
            plt.plot(t, theta, label=caso)
            
        plt.xlabel("Tiempo [s]")
        plt.ylabel("Ángulo $\\theta$ [rad]")
        plt.title("Respuesta Libre Amortiguada (Señales Sincronizadas)")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left') # Mueve la leyenda afuera para que no tape los datos
        plt.grid(True)
        plt.tight_layout()
        
        if save and base is not None:
            nombre_combinada = f"{base}_Sincronizada_grafica.png"
            if out_dir:
                ruta_combinada = os.path.join(out_dir, nombre_combinada)
                os.makedirs(out_dir, exist_ok=True)
            else:
                ruta_combinada = nombre_combinada
                
            plt.savefig(ruta_combinada, dpi=300, bbox_inches="tight")
            print(f"Gráfica combinada exportada en: {ruta_combinada}")
        else:
            plt.show()
            
        plt.close() # Cierra la combinada antes de crear las individuales

        # 2. GRÁFICAS SEPARADAS (Individuales)
        for caso, (t, theta) in datos.items():
            plt.figure()
            plt.plot(t, theta, label=caso)
            plt.xlabel("Tiempo [s]")
            plt.ylabel("Ángulo $\\theta$ [rad]")
            plt.title(f"Respuesta Libre Amortiguada - {caso}")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            
            if save and base is not None:
                nombre_grafica = f"{base}_{caso}_grafica.png"
                
                if out_dir:
                    ruta_grafica = os.path.join(out_dir, nombre_grafica)
                else:
                    ruta_grafica = nombre_grafica
                    
                plt.savefig(ruta_grafica, dpi=300, bbox_inches="tight")
                print(f"Gráfica individual exportada en: {ruta_grafica}")
            else:
                plt.show()
                
            plt.close() # Cierra la gráfica actual para no sobreescribir la siguiente
            
            
    def export(self, base="Libre Amortiguada", out_dir=None):
        df = self.tabulate()
        csv_name = base + "_resultados.csv"
        
        if out_dir:
            ruta_csv = os.path.join(out_dir, csv_name)
            os.makedirs(out_dir, exist_ok=True)
        else:
            ruta_csv = csv_name
            
        df.to_csv(ruta_csv, index=False, sep=";")
        print(f"Tabla exportada en: {ruta_csv}")
        
        self.graf(save=True, base=base, out_dir=out_dir)


if __name__ == "__main__":
    OUTPUT_DIR = r"C:\GitHub\Programacion\Python\Dinamica\Lab 2026\Resultados"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    analisis = AnalisisLibreAmortiguado()
    tabla = analisis.tabulate()
    print("\n--- Tabla de Resultados Amortiguados ---")
    print(tabla)
    analisis.export(out_dir=OUTPUT_DIR)