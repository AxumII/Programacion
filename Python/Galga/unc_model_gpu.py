import cupy as cp
import numpy as np
import pandas as pd

from unc_base_gpu import TypeA as TA
from unc_base_gpu import TypeB as TB

class UncGeneral:
    def __init__(self, derivadas, num_values):
        self.columns = ["Name", "Uncertainty", "Sensitivity"]
        self.df_gen = pd.DataFrame(columns=self.columns, dtype=float)
        self.derivadas = derivadas
        self.num_values = num_values
        self.eval_derivates = {var: self.coef_sens(expr, self.num_values) for var, expr in derivadas.items()}

        self.calculate()

    def calculate(self):
        pass

    def calc_a_and_b(self, input_data):
        for muestra, name, resol, calib in input_data:
            t_a = TA(muestra=muestra, name=name)
            t_a.unc_est()
            t_a.df_unc["Sensitivity"] = self.eval_derivates[name]
            self.df_gen = pd.concat([self.df_gen, t_a.df_unc], ignore_index=True)

            t_b = TB(resol=resol, calib=calib, name=name)
            t_b.add()
            t_b.df_unc["Sensitivity"] = self.eval_derivates[name]
            self.df_gen = pd.concat([self.df_gen, t_b.df_unc], ignore_index=True)

    def calc_b(self, input_data):
        for name, resol, calib in input_data:
            t_b = TB(resol=resol, calib=calib, name=name)
            t_b.add()
            t_b.df_unc["Sensitivity"] = self.eval_derivates[name]
            self.df_gen = pd.concat([self.df_gen, t_b.df_unc], ignore_index=True)

    def unc_expanded(self, k=3):
        self.df_gen["WeightedSquared"] = (self.df_gen["Uncertainty"] * self.df_gen["Sensitivity"])**2
        combined_std = np.sqrt(self.df_gen["WeightedSquared"].sum())
        expanded_uncertainty = k * combined_std
        return expanded_uncertainty

    def coef_sens(self, expr_str, valores_dict):
        contexto = {**{f: getattr(cp, f) for f in ['cos', 'sin', 'tan', 'log', 'exp', 'sqrt']}, **valores_dict}
        resultado = eval(expr_str, contexto)
        return float(resultado)  
