import cupy as cp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from model_gauge_gpu import Model

from SALib.sample import saltelli
from SALib.analyze import sobol


class MontecarloUncTestGauge:
    def __init__(self, n=10000):
        self.n = n
        self.results = cp.zeros(n)
        self.df_resumen = None

    def simulation(self):
        n = self.n

        # === Distribuciones por variable ===
        Vlect = cp.random.normal(0.0003, 1e-5, n)
        R1 = cp.random.uniform(110, 130, n)
        R2 = cp.random.uniform(110, 130, n)
        R3 = cp.random.uniform(110, 130, n)
        RG = cp.random.uniform(110, 130, n)
        RL = cp.random.uniform(110, 130, n)
        Vi = cp.random.normal(5.0, 0.1, n)
        GF = cp.random.uniform(2.0, 2.2, n)
        v = cp.random.uniform(0.30, 0.36, n)
        phi = cp.random.normal(cp.radians(1), cp.radians(0.1), n)
        hg = cp.random.normal(0.01, 0.0005, n)
        m = cp.random.normal(0.2, 0.18, n)
        g = cp.random.uniform(9.79, 9.83, n)
        L = cp.random.normal(0.1, 0.002, n)
        x = cp.random.normal(0.05, 0.001, n)
        E = cp.random.uniform(1.8e11, 2.2e11, n)
        b = cp.random.normal(0.05, 0.001, n)
        h = cp.random.normal(0.05, 0.001, n)
        lg = cp.full(n, 0.05)
        K = cp.random.uniform(101, 105, n)

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

    def sobol_analysis(self):
        # Definición del problema
        problem = {
            'num_vars': 4,
            'names': ['m', 'L', 'E', 'h'],
            'bounds': [
                [0.01, 0.4],        # m
                [0.095, 0.105],     # L
                [1.8e11, 2.2e11],   # E
                [0.048, 0.052]      # h
            ]
        }

        # Muestras con Saltelli
        param_values = saltelli.sample(problem, 1024, calc_second_order=False)
        n = param_values.shape[0]
        resultados = np.zeros(n)

        for i in range(n):
            modelo = Model(
                Vlect=0.0003,
                R1=120, R2=120, R3=120, RG=120, RL=120,
                Vi=5.0, GF=2.1, v=0.33, phi=cp.radians(1),
                hg=0.01,
                m=param_values[i, 0],
                g=9.81,
                L=param_values[i, 1],
                x=0.05,
                E=param_values[i, 2],
                b=0.05,
                h=param_values[i, 3],
                lg=0.05,
                K=100.0
            )
            resultados[i] = modelo.calculate()

        # Análisis de Sobol
        sobol_indices = sobol.analyze(problem, resultados, print_to_console=True)
        df_sobol = pd.DataFrame({
            'Variable': problem['names'],
            'Sobol_1er_orden': sobol_indices['S1'],
            'Sobol_total': sobol_indices['ST']
        })
        print(df_sobol)
        return df_sobol


# === Ejemplo de uso ===
if __name__ == "__main__":
    simulador = MontecarloUncTestGauge(n=1000)
    simulador.simulation()
    simulador.resumen_estadistico()
    simulador.graficar_resultados()
    simulador.sobol_analysis()
