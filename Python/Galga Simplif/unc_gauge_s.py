import cupy as cp
import numpy as np
import pandas as pd

from unc_model_s import UncGeneral as UncG


class UncGauge(UncG):
    def __init__(self, num_values, inputs_tipo_a_b, inputs_tipo_b, sensitivity_dict=None):
        self.inputs_tipo_a_b = inputs_tipo_a_b
        self.inputs_tipo_b = inputs_tipo_b
        self.num_values = num_values
        self.sensitivity_dict = sensitivity_dict
        super().__init__(num_values, sensitivity_dict)

    def calculate(self):

        for name, datos in self.inputs_tipo_a_b.items():
            self.calc_a_and_b([datos])
        for name, datos in self.inputs_tipo_b.items():
            self.calc_b([datos])



            """u_exp = unc.unc_expanded(k=3)
            print(f"Incertidumbre para {var}:")
            print(unc.df_gen)

            self.calc_b([(var, None, float(u_exp))])"""


