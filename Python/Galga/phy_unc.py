import numpy as np
import pandas as pd
import sympy as sp

from unc import Type_B as T_B

class Type_B_Total(Type_B):
    def __init__(self, resol, calib, temp, name=None, f_c_calib=3):
        super().__init__(resol, calib, name, f_c_calib)  # Hereda el constructor de Type_B
        self.temp = temp  # Nueva fuente de incertidumbre

    def unc_temp(self, name=None):
        label = "Temperature" if not self.name else f"Temperature of {self.name}"
        uncertainty = self.temp / np.sqrt(3)  # Ejemplo de incertidumbre
        sensitivity = 1
        degrees_of_freedom = 1  # O el valor que corresponda
        return label, uncertainty, sensitivity, degrees_of_freedom