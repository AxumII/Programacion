import cupy as cp
import numpy as np
import pandas as pd

from unc_model_gpu import UncGeneral as UncG

class UncC2V(UncG):
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
    
