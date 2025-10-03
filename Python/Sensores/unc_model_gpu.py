# unc_model_gpu.py

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
            sens = float(self.sensitivity_dict.get(name, 1.0))
            if not t_a.df_unc.empty:
                t_a.df_unc["Sensitivity"] = sens
                self.df_gen = pd.concat(
                    [self.df_gen, t_a.df_unc.dropna(how="all")],
                    ignore_index=True,
                )

            # === Tipo B ===
            t_b = TB(resol=resol, calib=calib, name=name)
            t_b.add()
            if not t_b.df_unc.empty:
                t_b.df_unc["Sensitivity"] = sens
                self.df_gen = pd.concat(
                    [self.df_gen, t_b.df_unc.dropna(how="all")],
                    ignore_index=True,
                )

    def calc_b(self, input_data):
        for name, resol, calib in input_data:
            t_b = TB(resol=resol, calib=calib, name=name)
            t_b.add()
            sens = float(self.sensitivity_dict.get(name, 1.0))
            if not t_b.df_unc.empty:
                t_b.df_unc["Sensitivity"] = sens
                self.df_gen = pd.concat(
                    [self.df_gen, t_b.df_unc.dropna(how="all")],
                    ignore_index=True,
                )

    def unc_expanded(self, k=2):
        # Convierte a float para evitar objetos SymPy
        u = pd.to_numeric(self.df_gen["Uncertainty"], errors="coerce").astype(float).to_numpy()
        c = pd.to_numeric(self.df_gen["Sensitivity"], errors="coerce").astype(float).to_numpy()
        uc2 = np.sum((u * c) ** 2)
        self.u_exp = float(np.sqrt(uc2) * k)
        return self.u_exp
