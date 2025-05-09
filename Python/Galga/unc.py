import numpy as np
import pandas as pd
import sympy as sp
class Type_A:
    def __init__(self, muestra: np.ndarray, name=None):
        self.muestra = muestra
        self.name = name
        self.columns = ["Name", "Uncertainty", "Sensitivity"]
        self.df_unc =  pd.DataFrame(columns=self.columns, dtype=float)

    def des_est(self, sensitivity=1):
        label = "Statical" if not self.name else f"Statical of {self.name}"
        uncertainty = np.std(self.muestra, ddof=1)
        self.df_unc.loc[len(self.df_unc)] = [label, uncertainty, sensitivity]


    
class Type_B:
    def __init__(self, resol=None, calib=None, name=None, f_c_calib=3):
        self.resol = resol
        self.calib = calib
        self.name = name
        self.f_c_calib = f_c_calib
        self.columns = ["Name", "Uncertainty", "Sensitivity"]
        self.df_unc = pd.DataFrame(columns=self.columns)

    def coef_sens(self, i_var, equation, num_values):
        return float(sp.diff(equation, i_var).evalf(subs=num_values))

    def unc_resol(self, sensitivity=1):
        if self.resol is not None:
            label = "Resolution" if not self.name else f"Resolution of {self.name}"
            uncertainty = self.resol / np.sqrt(12)
            self.df_unc.loc[len(self.df_unc)] = [label, uncertainty, sensitivity]

    def unc_calib(self, sensitivity=1):
        if self.calib is not None:
            label = "Calibration" if not self.name else f"Calibration of {self.name}"
            uncertainty = self.calib / self.f_c_calib
            self.df_unc.loc[len(self.df_unc)] = [label, uncertainty, sensitivity]

    def add(self, sensitivity=1):
        self.unc_resol(sensitivity=sensitivity)
        self.unc_calib(sensitivity=sensitivity)
