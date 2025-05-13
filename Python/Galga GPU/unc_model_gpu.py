import numpy as np
import pandas as pd

from unc_base_gpu import TypeA as TA
from unc_base_gpu import TypeB as TB

class UncGeneral:
    def __init__(self, num_values, sensitivity_dict=None):
        self.df_gen = pd.DataFrame(columns=["Name", "Uncertainty", "Sensitivity"])
        self.num_values = num_values or {}
        self.sensitivity_dict = sensitivity_dict or {}
        self.u_exp = None

    def calc_a_and_b(self, input_data):
        for muestra, name, resol, calib, desvest in input_data:
            # === Tipo A ===
            t_a = TA(muestra=muestra, desvest=desvest, name=name)
            t_a.unc_est()
            sens = self.sensitivity_dict.get(name, 1)
            t_a.df_unc["Sensitivity"] = sens

            if not t_a.df_unc.empty and not t_a.df_unc.isna().all().all():
                self.df_gen = pd.concat([self.df_gen, t_a.df_unc], ignore_index=True)

            # === Tipo B ===
            t_b = TB(resol=resol, calib=calib, name=name)
            t_b.add()
            t_b.df_unc["Sensitivity"] = sens

            if not t_b.df_unc.empty and not t_b.df_unc.isna().all().all():
                self.df_gen = pd.concat([self.df_gen, t_b.df_unc], ignore_index=True)

    def calc_b(self, input_data):
        for name, resol, calib in input_data:
            t_b = TB(resol=resol, calib=calib, name=name)
            t_b.add()
            sens = self.sensitivity_dict.get(name, 1)
            t_b.df_unc["Sensitivity"] = sens

            if not t_b.df_unc.empty and not t_b.df_unc.isna().all().all():
                self.df_gen = pd.concat([self.df_gen, t_b.df_unc], ignore_index=True)

    def unc_expanded(self, k=2):
        u_cuad = (self.df_gen["Uncertainty"] * self.df_gen["Sensitivity"])**2
        self.u_exp =  np.sqrt(u_cuad.sum()) * k
        return self.u_exp
