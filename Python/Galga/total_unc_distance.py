import numpy as np
import pandas as pd
import sympy as sp

from unc import Type_A as T_A
from unc import Type_B as T_B

class Total_unc_dist:
    def __init__(self,
                 num_values,
                 d_mean_data, d_mean_resol, d_mean_calib,
                 delta_params_calib,
                 theta_data, theta_resol, theta_calib,
                 T_data, T_resol, T_calib):
        
        self.columns = ["Name", "Uncertainty", "Sensitivity"]
        self.df_gen = pd.DataFrame(columns=self.columns, dtype=float)

        self.num_values = num_values

        self.datos_d_mean = d_mean_data
        self.resol_d_mean = d_mean_resol
        self.calib_d_mean = d_mean_calib

        self.calib_delta_0 = delta_params_calib.get("delta_0")
        self.calib_delta_paral = delta_params_calib.get("delta_paral")
        self.calib_delta_F = delta_params_calib.get("delta_F")
        self.calib_delta_desg = delta_params_calib.get("delta_desg")
        self.calib_delta_h = delta_params_calib.get("delta_h")

        self.datos_theta = theta_data
        self.resol_theta = theta_resol
        self.calib_theta = theta_calib

        self.datos_T = T_data
        self.resol_T = T_resol
        self.calib_T = T_calib

        self.calculate()
        self.u_e = self.unc_expanded(k=3)

    def calculate(self):
        d_mean, delta_0 = sp.symbols('d_mean delta_0')
        delta_paral, delta_desg, delta_h, delta_F = sp.symbols('delta_paral delta_desg delta_h delta_F')
        theta = sp.symbols('theta')
        T = sp.symbols('T')
        alpha_instr, alpha_obj = sp.symbols('alpha_instr alpha_obj')

        T0 = 20
        distance = (d_mean - delta_0 + delta_paral + delta_F + delta_desg + delta_h)/sp.cos(theta)
        temp_error = (1 + alpha_instr * (T - T0)) / (1 + alpha_obj * (T - T0))
        model = distance * temp_error

        # --- d_mean ---
        t_a_d_mean = T_A(muestra=self.datos_d_mean, name="Distance Measure")
        sens_d_mean = float(sp.diff(model, d_mean).evalf(subs=self.num_values))
        t_a_d_mean.des_est(sensitivity=sens_d_mean)
        self.df_gen = pd.concat([self.df_gen, t_a_d_mean.df_unc], ignore_index=True)

        t_b_d_mean = T_B(resol=self.resol_d_mean, calib=self.calib_d_mean, name="Distance Measure")
        sens_d_mean_b = t_b_d_mean.coef_sens(i_var=d_mean, equation=model, num_values=self.num_values)
        t_b_d_mean.add(sensitivity=sens_d_mean_b)
        self.df_gen = pd.concat([self.df_gen, t_b_d_mean.df_unc], ignore_index=True)

        # --- delta_0 ---
        t_b_delta_0 = T_B(calib=self.calib_delta_0, name="Error Delta 0")
        sens_delta_0 = t_b_delta_0.coef_sens(i_var=delta_0, equation=model, num_values=self.num_values)
        t_b_delta_0.add(sensitivity=sens_delta_0)
        self.df_gen = pd.concat([self.df_gen, t_b_delta_0.df_unc], ignore_index=True)

        # --- delta_paral ---
        t_b_delta_paral = T_B(calib=self.calib_delta_paral, name="Delta Paralelismo")
        sens_delta_paral = t_b_delta_paral.coef_sens(i_var=delta_paral, equation=model, num_values=self.num_values)
        t_b_delta_paral.add(sensitivity=sens_delta_paral)
        self.df_gen = pd.concat([self.df_gen, t_b_delta_paral.df_unc], ignore_index=True)

        # --- delta_F ---
        t_b_delta_F = T_B(calib=self.calib_delta_F, name="Delta Fuerza")
        sens_delta_F = t_b_delta_F.coef_sens(i_var=delta_F, equation=model, num_values=self.num_values)
        t_b_delta_F.add(sensitivity=sens_delta_F)
        self.df_gen = pd.concat([self.df_gen, t_b_delta_F.df_unc], ignore_index=True)

        # --- delta_desg ---
        t_b_delta_desg = T_B(calib=self.calib_delta_desg, name="Delta Desgaste")
        sens_delta_desg = t_b_delta_desg.coef_sens(i_var=delta_desg, equation=model, num_values=self.num_values)
        t_b_delta_desg.add(sensitivity=sens_delta_desg)
        self.df_gen = pd.concat([self.df_gen, t_b_delta_desg.df_unc], ignore_index=True)

        # --- delta_h ---
        t_b_delta_h = T_B(calib=self.calib_delta_h, name="Delta Altura")
        sens_delta_h = t_b_delta_h.coef_sens(i_var=delta_h, equation=model, num_values=self.num_values)
        t_b_delta_h.add(sensitivity=sens_delta_h)
        self.df_gen = pd.concat([self.df_gen, t_b_delta_h.df_unc], ignore_index=True)

        # --- theta ---
        t_a_theta = T_A(muestra=self.datos_theta, name="Theta")
        sens_theta = float(sp.diff(model, theta).evalf(subs=self.num_values))
        t_a_theta.des_est(sensitivity=sens_theta)
        self.df_gen = pd.concat([self.df_gen, t_a_theta.df_unc], ignore_index=True)

        t_b_theta = T_B(resol=self.resol_theta, calib=self.calib_theta, name="Theta")
        sens_theta_b = t_b_theta.coef_sens(i_var=theta, equation=model, num_values=self.num_values)
        t_b_theta.add(sensitivity=sens_theta_b)
        self.df_gen = pd.concat([self.df_gen, t_b_theta.df_unc], ignore_index=True)

        # --- T ---
        t_a_T = T_A(muestra=self.datos_T, name="Temperature Ambient")
        sens_T = float(sp.diff(model, T).evalf(subs=self.num_values))
        t_a_T.des_est(sensitivity=sens_T)
        self.df_gen = pd.concat([self.df_gen, t_a_T.df_unc], ignore_index=True)

        t_b_T = T_B(resol=self.resol_T, calib=self.calib_T, name="Temperature Ambient")
        sens_T_b = t_b_T.coef_sens(i_var=T, equation=model, num_values=self.num_values)
        t_b_T.add(sensitivity=sens_T_b)
        self.df_gen = pd.concat([self.df_gen, t_b_T.df_unc], ignore_index=True)

    def unc_expanded(self, k):
        self.df_gen["WeightedSquared"] = (self.df_gen["Uncertainty"] * self.df_gen["Sensitivity"])**2
        combined_std = np.sqrt(self.df_gen["WeightedSquared"].sum())
        expanded_uncertainty = k * combined_std
        return expanded_uncertainty


#########################################

"""
#EJEMPLO
if __name__ == "__main__":
    d_mean, delta_0 = sp.symbols('d_mean delta_0')
    delta_paral, delta_desg, delta_h, delta_F = sp.symbols('delta_paral delta_desg delta_h delta_F')
    theta = sp.symbols('theta')
    T = sp.symbols('T')
    alpha_instr = sp.symbols('alpha_instr')
    alpha_obj = sp.symbols('alpha_obj')

    num_values = {
        d_mean: 10.2, 
        delta_0: 0.005, 
        delta_paral: 0.002, 
        delta_F: 0.001, 
        delta_desg: 0.003, 
        delta_h: 0.004, 
        theta: 0.025,
        T: 22,
        alpha_instr: 1e-5,
        alpha_obj: 1e-5
    }

    delta_params_calib = {
        "delta_0": 0.005,
        "delta_paral": 0.002,
        "delta_F": 0.001,
        "delta_desg": 0.003,
        "delta_h": 0.004
    }

    modelo = Total_unc_dist(
        num_values=num_values,
        d_mean_data=[10.2, 10.3, 10.1],
        d_mean_resol=0.01,
        d_mean_calib=0.005,
        delta_params_calib = delta_params_calib,
        theta_data=[0.02, 0.025, 0.03],
        theta_resol=0.001,
        theta_calib=0.0005,
        T_data=[22, 23, 21],
        T_resol=0.5,
        T_calib=0.2
    )

    print("\n--- Tabla de incertidumbres ---")
    print(modelo.df_gen)

    print(f"\nIncertidumbre expandida (k=3): {modelo.u_e:.6f}")
"""