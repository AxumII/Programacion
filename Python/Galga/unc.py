import numpy as np
import pandas as pd
import inspect
import sympy as sp
class Type_A:
    def __init__(self, muestra: np.ndarray, name=None):
        self.muestra = muestra
        self.name = name
        self.columns = ["Name", "Uncertainty", "Sensitivity", "Degrees_of_Freedom"]
        self.Sn_m = self.des_est()
        

    def des_est(self):
        label = "Calibration" if not self.name else f"Calibration of {self.name}"
        uncertainty = np.sqrt(np.var(self.muestra, ddof=1))
        sensitivity = 1
        gof= len(self.muestra)

        df_out = pd.DataFrame(columns=self.columns)
        df_out.loc[0] = [label, uncertainty, sensitivity, gof]

        return df_out


class Type_B:
    def __init__(self, resol, calib, name=None, f_c_calib=3):
        self.name = name
        self.resol = resol
        self.calib = calib
        self.f_c_calib = f_c_calib
        self.columns = ["Name", "Uncertainty", "Sensitivity", "Degrees_of_Freedom"]
        self.df_unc = pd.DataFrame(columns=self.columns)

    def unc_resol(self, name=None):
        if self.resol is not None:
            label = "Resolution" if not self.name else f"Resolution of {self.name}"
            return label, (self.resol / np.sqrt(12)), 1, 1

    def unc_calib(self, sensitivity=None):
        sensitivity = sensitivity if sensitivity is not None else 1
        if self.calib is not None:
            label = "Calibration" if not self.name else f"Calibration of {self.name}"
            uncertainty = self.calib / self.f_c_calib
            return label, uncertainty, sensitivity, 1

    
    def coef_sens(i_var, equation, num_values):
        diff_equation = sp.diff(equation, i_var)
        return diff_equation.evalf(subs = num_values)

    def add(self):
        for nombre, metodo in inspect.getmembers(self, predicate=inspect.ismethod):
            if nombre.startswith("unc_"):
                resultado = metodo()
                if resultado is None:
                    continue
                elif isinstance(resultado, tuple) and len(resultado) == 4:
                    self.df_unc.loc[len(self.df_unc)] = resultado
                elif isinstance(resultado, pd.DataFrame):
                    self.df_unc = pd.concat([self.df_unc, resultado], ignore_index=True)
