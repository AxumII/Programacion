import cupy as cp
import numpy as np
import pandas as pd

from unc_model_gpu import UncGeneral as UncG

class UncDistance(UncG):
    def __init__(self, num_values, inputs_tipo_a_b_dist, inputs_tipo_b_dist, sensitivity_dict=None):
        self.inputs_tipo_a_b = inputs_tipo_a_b_dist
        self.inputs_tipo_b = inputs_tipo_b_dist
        self.num_values = num_values
        self.sensitivity_dict = sensitivity_dict
        super().__init__(num_values, sensitivity_dict)

    def calculate(self):
        for name, datos in self.inputs_tipo_a_b.items():
            self.calc_a_and_b([datos])
        for name, datos in self.inputs_tipo_b.items():
            self.calc_b([datos])


##########################################################
"""
if __name__ == "__main__":

    inputs_tipo_a_b = {
        "d_mean": (None, "d_mean", 0.001, 0.002, 0.01),
        "T": (None, "T", 0.1, 0.2, 0.5)
    }

    inputs_tipo_b = {
        "delta_0": ("delta_0", 0.001, 0.002),
        "delta_paral": ("delta_paral", 0.001, 0.002),
        "delta_F": ("delta_F", 0.001, 0.002),
        "delta_desg": ("delta_desg", 0.001, 0.002),
        "delta_h": ("delta_h", 0.001, 0.002),
        "theta": ("theta", 0.001, 0.002)
    }

    num_values = {
        "T": 25,
        "T0": 20,
        "theta": 0.1,
        "alpha_instr": 0.00001,
        "alpha_obj": 0.000012,
        "d_mean": 10,
        "delta_0": 0.1,
        "delta_paral": 0.05,
        "delta_F": 0.02,
        "delta_desg": 0.01,
        "delta_h": 0.03,
    }

    # Diccionario de coeficientes de sensibilidad ya calculados
    sensitivity_dict = {
        "d_mean": 1.5,
        "T": 0.8,
        "delta_0": 0.9,
        "delta_paral": 0.95,
        "delta_F": 0.92,
        "delta_desg": 0.93,
        "delta_h": 0.88,
        "theta": 1.2
    }

    # Crear objeto y calcular
    unc = UncDistance(
        num_values=num_values,
        inputs_tipo_a_b_dist=inputs_tipo_a_b,
        inputs_tipo_b_dist=inputs_tipo_b,
        sensitivity_dict=sensitivity_dict
    )
    unc.calculate()

    # Resultados
    print("=== Tabla de Incertidumbres ===")
    print(unc.df_gen)
    print("\n=== Incertidumbre Expandida (k=3) ===")
    print(f"{unc.unc_expanded(k=3):.6f}")
"""