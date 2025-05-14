import cupy as cp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from model_gauge_s import Model
import time


class MontecarloUncTestGauge:
    def __init__(self, n=10000, distribuciones=None):
        self.n = n
        self.results = cp.zeros(n)
        self.df_resumen = None
        self.distribuciones = distribuciones or {}
        self.muestras = {}

    def generar_muestras(self):
        for nombre, dist in self.distribuciones.items():
            tipo = dist["tipo"]
            params = dist["params"]
            if tipo == "normal":
                self.muestras[nombre] = cp.random.normal(params["media"], params["desv"], self.n)
            elif tipo == "uniform":
                self.muestras[nombre] = cp.random.uniform(params["min"], params["max"], self.n)
            elif tipo == "const":
                self.muestras[nombre] = cp.full(self.n, params["valor"])
            else:
                raise ValueError(f"Distribución '{tipo}' no soportada para '{nombre}'")

    def simulation(self):
        self.generar_muestras()
        nombres = list(self.muestras.keys())
        # Convertir todas las muestras a NumPy para operar con `Model` que espera float normales
        muestras_np = {k: cp.asnumpy(v) for k, v in self.muestras.items()}

        # Procesar cada muestra con el modelo
        for i in range(self.n):
            modelo = Model(**{k: float(muestras_np[k][i]) for k in nombres})
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

"""    
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

    # Crear instancia del simulador
    simulador = MontecarloUncTestGauge(n=10**2, distribuciones=distribuciones)

    # === Medición de tiempo por fases ===
    total_inicio = time.time()

    print("🔧 Generando muestras...")
    t0 = time.time()
    simulador.generar_muestras()
    print(f"✅ Muestras generadas en {time.time() - t0:.2f} s\n")

    print("⚙️ Ejecutando simulación...")
    t1 = time.time()
    simulador.simulation()
    print(f"✅ Simulación completada en {time.time() - t1:.2f} s\n")

    print("📊 Resumen estadístico:")
    simulador.resumen_estadistico()

    print("📈 Graficando resultados...")
    simulador.graficar_resultados()

    total_fin = time.time()
    print(f"\n⏱️ Tiempo total: {total_fin - total_inicio:.2f} segundos")
"""