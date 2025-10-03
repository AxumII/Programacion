import cupy as cp
import numpy as np
import pandas as pd

class TypeA:
    def __init__(self, muestra = None , name=None, sensitivity=1, desvest = None):
        self.muestra = muestra
        self.name = name
        self.sensitivity = sensitivity
        self.desvest = desvest
        self.columns = ["Name", "Uncertainty", "Sensitivity"]
        self.df_unc = pd.DataFrame(columns=self.columns)

    def unc_est(self):
        label = "Statical" if not self.name else f"Statical of {self.name}"
        uncertainty = 0.0

        if self.desvest is not None and self.muestra is None:
            uncertainty = float(self.desvest) 

        elif (self.desvest is None) and (self.muestra is not None):
            arr = self.muestra
            if isinstance(arr, cp.ndarray):
                uncertainty = float(cp.std(arr, ddof=1).get())
            else:
                arr = np.asarray(arr)
                uncertainty = float(np.std(arr, ddof=1))


        self.df_unc.loc[len(self.df_unc)] = [label, uncertainty, float(self.sensitivity)]



class TypeB:
    def __init__(self, resol = None, calib = None, sensitivity = 1, f_c_calib = 3, name = None):
        self.resol = resol
        self.calib = calib
        self.sensitivity = sensitivity
        self.name = name
        self.f_c_calib = f_c_calib
        self.columns = ["Name", "Uncertainty", "Sensitivity"]
        self.df_unc = pd.DataFrame(columns=self.columns)

    def unc_resol(self):
        if self.resol is not None:
            label = "Resolution" if not self.name else f"Resolution of {self.name}"
            uncertainty = float(self.resol) / float(np.sqrt(12.0))
            self.df_unc.loc[len(self.df_unc)] = [label, uncertainty, float(self.sensitivity)]



    def unc_calib(self):
        if self.calib is not None:
            label = "Calibration" if not self.name else f"Calibration of {self.name}"
            uncertainty = float(self.calib) / float(self.f_c_calib)
            self.df_unc.loc[len(self.df_unc)] = [label, uncertainty, float(self.sensitivity)]


    def add(self):
        self.unc_resol()
        self.unc_calib()