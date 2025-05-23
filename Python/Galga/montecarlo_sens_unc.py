import cupy as cp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from model_gauge_gpu import Model
from pb import N_fit as N_fit
import time




class MontecarloUncTestGauge:
    def __init__(self, n=10000, distribuciones=None):
        self.n = n
        self.results = cp.zeros(n)
        self.df_resumen = None

        # Diccionario con la especificación de las distribuciones por variable
        self.distribuciones = distribuciones if distribuciones else {}

    def generar_valores(self, nombre):
        dist = self.distribuciones[nombre]
        tipo = dist["tipo"]
        params = dist["params"]

        if tipo == "normal":
            return cp.random.normal(params["media"], params["desv"], self.n)
        elif tipo == "uniform":
            return cp.random.uniform(params["min"], params["max"], self.n)
        elif tipo == "const":
            return cp.full(self.n, params["valor"])
        else:
            raise ValueError(f"Distribución '{tipo}' no soportada para '{nombre}'")

    def simulation(self):
        n = self.n

        # === Generación dinámica según distribuciones definidas ===
        Vlect = self.generar_valores("Vlect")
        R1 = self.generar_valores("R1")
        R2 = self.generar_valores("R2")
        R3 = self.generar_valores("R3")
        RG = self.generar_valores("RG")
        RL = self.generar_valores("RL")
        Vi = self.generar_valores("Vi")
        GF = self.generar_valores("GF")
        v = self.generar_valores("v")
        phi = self.generar_valores("phi")
        hg = self.generar_valores("hg")
        m = self.generar_valores("m")
        g = self.generar_valores("g")
        L = self.generar_valores("L")
        x = self.generar_valores("x")
        E = self.generar_valores("E")
        b = self.generar_valores("b")
        h = self.generar_valores("h")
        lg = self.generar_valores("lg")
        K = self.generar_valores("K")

        # === Simulación Monte Carlo ===
        for i in range(n):
            modelo = Model(
                Vlect=float(Vlect[i]),
                R1=float(R1[i]),
                R2=float(R2[i]),
                R3=float(R3[i]),
                RG=float(RG[i]),
                RL=float(RL[i]),
                Vi=float(Vi[i]),
                GF=float(GF[i]),
                v=float(v[i]),
                phi=float(phi[i]),
                hg=float(hg[i]),
                m=float(m[i]),
                g=float(g[i]),
                L=float(L[i]),
                x=float(x[i]),
                E=float(E[i]),
                b=float(b[i]),
                h=float(h[i]),
                lg=float(lg[i]),
                K=float(K[i])
            )
            self.results[i] = modelo.calculate()

        return self.results


    def resumen_estadistico(self):
        media = float(cp.mean(self.results))
        std = float(cp.std(self.results, ddof=1))
        k = 3
        low, high = media - k * std, media + k * std

        self.df_resumen = pd.DataFrame([{
            "Media": media,
            "Desviación estándar": std,
            "Límite inferior (95%)": low,
            "Límite superior (95%)": high
        }])

        print(self.df_resumen)
        return self.df_resumen

    def graficar_resultados(self):
        datos = cp.asnumpy(self.results)
        plt.figure(figsize=(8, 5))
        plt.hist(datos, bins=50, color='skyblue', edgecolor='black')
        plt.title("Histograma de Resultados Monte Carlo")
        plt.xlabel("Valor del modelo")
        plt.ylabel("Frecuencia")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    

# === Ejemplo de uso ===
if __name__ == "__main__":
    distribuciones = {
        "Vlect": {"tipo": "normal", "params": {"media": 0.003, "desv": 1e-1}},
        "R1":    {"tipo": "uniform", "params": {"min": 110, "max": 130}},
        "R2":    {"tipo": "uniform", "params": {"min": 110, "max": 130}},
        "R3":    {"tipo": "uniform", "params": {"min": 110, "max": 130}},
        "RG":    {"tipo": "uniform", "params": {"min": 110, "max": 130}},
        "RL":    {"tipo": "uniform", "params": {"min": 110, "max": 130}},
        "Vi":    {"tipo": "normal", "params": {"media": 5.0, "desv": 0.1}},
        "GF":    {"tipo": "uniform", "params": {"min": 2.0, "max": 2.2}},
        "v":     {"tipo": "uniform", "params": {"min": 0.30, "max": 0.36}},
        "phi":   {"tipo": "normal", "params": {"media": np.radians(1), "desv": np.radians(0.1)}},
        "hg":    {"tipo": "normal", "params": {"media": 0.01, "desv": 0.0005}},
        "m":     {"tipo": "normal", "params": {"media": 0.2, "desv": 0.18}},
        "g":     {"tipo": "uniform", "params": {"min": 9.79, "max": 9.83}},
        "L":     {"tipo": "normal", "params": {"media": 0.1, "desv": 0.002}},
        "x":     {"tipo": "normal", "params": {"media": 0.05, "desv": 0.001}},
        "E":     {"tipo": "uniform", "params": {"min": 1.8e11, "max": 2.2e11}},
        "b":     {"tipo": "normal", "params": {"media": 0.05, "desv": 0.001}},
        "h":     {"tipo": "normal", "params": {"media": 0.05, "desv": 0.001}},
        "lg":    {"tipo": "const", "params": {"valor": 0.05}},
        "K":     {"tipo": "uniform", "params": {"min": 101, "max": 105}}
    }

    simulador = MontecarloUncTestGauge(n=10**6, distribuciones=distribuciones)
    inicio = time.time()
    simulador.simulation()
    fin = time.time()
    
    print(f"Tiempo de simulación: {fin - inicio:.2f} segundos")
    simulador.resumen_estadistico()
    simulador.graficar_resultados()
