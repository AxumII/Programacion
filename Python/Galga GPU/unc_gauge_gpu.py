import cupy as cp
import numpy as np
import pandas as pd

from unc_model_gpu import UncGeneral as UncG
from unc_dist_gpu import UncDistance as UncD

class UncGauge(UncG):
    def __init__(self, num_values,
                 inputs_tipo_a_b, inputs_tipo_b,
                 inputs_tipo_a_b_dist, inputs_tipo_b_dist,
                 inputs_distance, sensitivity_dict=None):

        self.inputs_tipo_a_b = inputs_tipo_a_b
        self.inputs_tipo_b = inputs_tipo_b
        self.inputs_tipo_a_b_dist = inputs_tipo_a_b_dist
        self.inputs_tipo_b_dist = inputs_tipo_b_dist
        self.inputs_distance = inputs_distance
        self.num_values = num_values
        self.sensitivity_dict = sensitivity_dict

        super().__init__( num_values, sensitivity_dict)

    def calculate(self):
        for name, datos in self.inputs_tipo_a_b.items():
            if name not in self.inputs_distance:
                self.calc_a_and_b([datos])

        for name, datos in self.inputs_tipo_b.items():
            self.calc_b([datos])

        # Procesar submodelo UncDistance
        for var in self.inputs_distance:
            muestra, nombre, resol, calib, desvest = self.inputs_tipo_a_b[var]

            input_d_mean = (muestra, "d_mean", resol, calib, desvest)
            inputs_a_b_dist = {
                "d_mean": input_d_mean,
                "T": self.inputs_tipo_a_b_dist["T"],
                "theta": self.inputs_tipo_a_b_dist["theta"]
            }

            valor_medido = self.num_values[var]
            valores_modificados = {**self.num_values, "d_mean": valor_medido}

            unc = UncD(
            num_values=valores_modificados,
            inputs_tipo_a_b_dist=inputs_a_b_dist,
            inputs_tipo_b_dist=self.inputs_tipo_b_dist,
            sensitivity_dict=self.sensitivity_dict  
        )

            unc.calculate()

            """u_exp = unc.unc_expanded(k=3)
            print(f"Incertidumbre para {var}:")
            print(unc.df_gen)

            self.calc_b([(var, None, float(u_exp))])"""


