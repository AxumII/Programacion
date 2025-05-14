import numpy as np
import cupy as cp
from scipy.stats import norm
from SALib.sample import sobol as sobol_sampler
from SALib.analyze import sobol as sobol_analyzer
import matplotlib.pyplot as plt
from model_gauge_s import Model


class SobolAnalysis:
    def __init__(self, distribuciones, n=10000):
        self.distribuciones = distribuciones
        self.n = n
        self.problem = self._build_problem()
        self.samples = None
        self.transformed_samples = None
        self.s1 = None
        self.st = None

    def _build_problem(self):
        names = list(self.distribuciones.keys())
        bounds = [[0, 1]] * len(names)
        return {
            "num_vars": len(names),
            "names": names,
            "bounds": bounds
        }

    def _transform_inputs(self, samples):
        transformed = np.zeros_like(samples)
        for i, name in enumerate(self.distribuciones):
            tipo = self.distribuciones[name]["tipo"]
            params = self.distribuciones[name]["params"]

            if tipo == "uniform":
                a, b = params["min"], params["max"]
                transformed[:, i] = a + (b - a) * samples[:, i]
            elif tipo == "normal":
                mu, sigma = params["media"], params["desv"]
                transformed[:, i] = norm.ppf(samples[:, i], loc=mu, scale=sigma)
        return transformed

    def calculate(self):
        self.samples = sobol_sampler.sample(self.problem, self.n, calc_second_order=True)
        self.transformed_samples = self._transform_inputs(self.samples)
        return self.transformed_samples

    def run_model(self):
        data = self.transformed_samples
        n = data.shape[0]
        resultados = cp.zeros(n)

        for i in range(n):
            entrada = {name: data[i, j] for j, name in enumerate(self.problem["names"])}
            modelo = Model(
                Vlect=entrada["Vlect"],
                K=entrada["K"],
                R1=entrada["R1"],
                R2=entrada["R2"],
                R3=entrada["R3"],
                RG=entrada["RG"],
                RL=entrada["RL"],
                Vi=entrada["Vi"],
                GF=entrada["GF"],
                v=entrada["v"],
                phi=entrada["phi"],
                L=entrada["L"],
                E=entrada["E"],
                lg=entrada["lg"]
            )
            resultados[i] = modelo.calculate()

        return cp.asnumpy(resultados)

    def analyze(self, Y):
        resultados = sobol_analyzer.analyze(self.problem, Y, calc_second_order=True)
        self.s1 = resultados["S1"]
        self.st = resultados["ST"]
        return resultados

    def plot_sobol_indices(self, titulo="Índices de Sobol"):
        if self.s1 is None or self.st is None:
            raise ValueError("Primero debes ejecutar `analyze()` para obtener los índices de Sobol.")

        x = np.arange(len(self.problem["names"]))
        width = 0.35

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(x - width/2, self.s1, width, label='S1 (Primer orden)')
        #ax.bar(x + width/2, self.st, width, label='ST (Total)')

        ax.set_ylabel('Índice de Sobol')
        ax.set_title(titulo)
        ax.set_xticks(x)
        ax.set_xticklabels(self.problem["names"], rotation=45, ha='right')
        ax.legend()
        ax.grid(True, axis='y', linestyle='--', alpha=0.5)

        fig.tight_layout()
        plt.show()


"""
if __name__ == "__main__":
    distribuciones = {
        "Vlect": {"tipo": "normal", "params": {"media": 0.0003, "desv": 0.1}},
        "R1":    {"tipo": "uniform", "params": {"min": 119.88, "max": 120.12}},
        "R2":    {"tipo": "uniform", "params": {"min": 119.88, "max": 120.12}},
        "R3":    {"tipo": "uniform", "params": {"min": 119.88, "max": 120.12}},
        "RG":    {"tipo": "uniform", "params": {"min": 119.88, "max": 120.12}},
        "RL":    {"tipo": "uniform", "params": {"min": 119.88, "max": 120.12}},
        "Vi":    {"tipo": "normal", "params": {"media": 5.0, "desv": 0.01}},
        "GF":    {"tipo": "uniform", "params": {"min": 2.0, "max": 2.2}},
        "v":     {"tipo": "uniform", "params": {"min": 0.30, "max": 0.36}},
        "phi":   {"tipo": "normal", "params": {"media": np.radians(1), "desv": np.radians(0.01)}},
        "hg":    {"tipo": "normal", "params": {"media": 0.01, "desv": 0.0005}},
        "m":     {"tipo": "normal", "params": {"media": 0.205, "desv": 0.194}},
        "g":     {"tipo": "uniform", "params": {"min": 9.79, "max": 9.83}},
        "L":     {"tipo": "normal", "params": {"media": 0.05, "desv": 0.00001}},
        "x":     {"tipo": "normal", "params": {"media": 0.01, "desv": 0.01}},
        "E":     {"tipo": "uniform", "params": {"min": 1.8e11, "max": 2.2e11}},
        "b":     {"tipo": "normal", "params": {"media": 0.05, "desv": 0.01}},
        "h":     {"tipo": "normal", "params": {"media": 0.05, "desv": 0.01}},
        "lg":    {"tipo": "uniform", "params": {"min": 0.05, "max": 0.05}},
        "K":     {"tipo": "uniform", "params": {"min": 101, "max": 105}}
    }

    print("Generando muestras y ejecutando modelo...")
    sobol = SobolAnalysis(distribuciones, n=2**9)
    sobol.calculate()
    Y = sobol.run_model()
    resultados = sobol.analyze(Y)

    nombres = sobol.problem["names"]
    s1 = resultados["S1"]
    st = resultados["ST"]

    print("\nÍndices de Sobol (primer orden):")
    for name, val in zip(nombres, s1):
        print(f"{name}: {val:.5f}")

    print("\nÍndices de Sobol (total):")
    for name, val in zip(nombres, st):
        print(f"{name}: {val:.5f}")

    plot_sobol_indices(nombres, s1, st)"""
