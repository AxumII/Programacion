import numpy as np
import pandas as pd
import sympy as sp

from unc import Type_A as T_A
from unc import Type_B as T_B
from total_unc_distance import Total_unc_dist as TUD


class Total_unc_gauge:
    def __init__(self,
             num_values=1,
             datos_delta_V=1, resol_delta_V=1,
             datos_Vi=1, resol_Vi=1, calib_Vi=1,
             calib_GF=1,
             datos_RL=1, resol_RL=1, calib=1,
             calib_RG=1,
             datos_phi=1, resol_phi=1, calib_phi=1,
             datos_theta=1, resol_theta=1, calib_theta=1,
             datos_T=1, resol_T=1, calib_T=1,
             resol_pdr=1, calib_pdr=1,
             datos_m=1, resol_m=1, calib_m=1,
             calib_g=1,
             calib_lg=1,
             datos_hg=1, datos_L=1, datos_x=1, datos_B=1, datos_h=1):  # <-- NUEVOS

        self.columns = ["Name", "Uncertainty", "Sensitivity"]
        self.df_gen = pd.DataFrame(columns=self.columns)

        self.num_values = num_values

        self.datos_delta_V = datos_delta_V
        self.resol_delta_V = resol_delta_V

        self.datos_Vi = datos_Vi
        self.resol_Vi = resol_Vi
        self.calib_Vi = calib_Vi

        self.calib_GF = calib_GF

        self.datos_RL = datos_RL
        self.resol_RL = resol_RL
        self.calib = calib

        self.calib_RG = calib_RG

        self.datos_phi = datos_phi
        self.resol_phi = resol_phi
        self.calib_phi = calib_phi

        self.datos_m = datos_m
        self.resol_m = resol_m
        self.calib_m = calib_m

        self.calib_g = calib_g
        self.calib_lg = calib_lg

        self.datos_theta = datos_theta
        self.resol_theta = resol_theta
        self.calib_theta = calib_theta

        self.datos_T = datos_T
        self.resol_T = resol_T
        self.calib_T = calib_T

        self.resol_pdr = resol_pdr
        self.calib_pdr = calib_pdr

        self.datos_hg = datos_hg
        self.datos_L = datos_L
        self.datos_x = datos_x
        self.datos_B = datos_B
        self.datos_h = datos_h


    def calculate(self):
        #Modelo
        delta_V, Vi, GF = sp.symbols('delta_V Vi GF')
        RL, RG = sp.symbols('RL RG')
        v, phi = sp.symbols('v phi')
        hg, m , g, L, x = sp.symbols('hg m g L x')
        E, b, h = sp.symbols('E b h')
        lg = sp.symbols('lg')

        #Formulas
        #epsilon
        epsilon = (-4 * (delta_V / Vi)) / (GF * (1 + 2 * (delta_V / Vi))) 
        #misalignment
        error_misalignment = ((1 - v + (1 + v) * sp.cos(2 * phi)) / 2) - 1
        #curvature
        error_curvature = (12 * hg * m * g * (L - x)) / (E * b * h**3) 
        #gauge longitude
        error_gauge_long = (lg / L ) - 1  
        #puente / termico
        error_bridge = (1 + RL / RG)
                
        model = epsilon*error_bridge*error_misalignment*error_curvature*error_gauge_long
       
           
        

        # --- Delta_V ---
        # Tipo A
        t_a_delta_V = T_A(muestra=self.datos_delta_V, name="Voltage Difference")
        t_a_delta_V.des_est(sensitivity=float(sp.diff(model, delta_V).evalf(subs=self.num_values)))
        self.df_gen = pd.concat([self.df_gen, t_a_delta_V.df_unc], ignore_index=True)

        # Tipo B
        t_b_delta_V = T_B(resol=self.resol_delta_V, name="Voltage Difference")
        sens_delta_V = t_b_delta_V.coef_sens(i_var=delta_V, equation=model, num_values=self.num_values)
        t_b_delta_V.add(sensitivity=sens_delta_V)
        self.df_gen = pd.concat([self.df_gen, t_b_delta_V.df_unc], ignore_index=True)


        # --- Vi ---
        #Tipo A
        t_a_Vi = T_A(muestra=self.datos_Vi, name="Voltage Input")
        t_a_Vi.des_est(sensitivity=float(sp.diff(model, Vi).evalf(subs=self.num_values)))
        self.df_gen = pd.concat([self.df_gen, t_a_Vi.df_unc], ignore_index=True)

        
        #Tipo B
        #Resolucion y Calibracion
        t_b_Vi = T_B(resol=self.resol_Vi, calib=self.calib_Vi, name="Voltage Input")
        sens_Vi = t_b_Vi.coef_sens(i_var=Vi, equation=model, num_values=self.num_values)
        t_b_Vi.add(sensitivity=sens_Vi)
        self.df_gen = pd.concat([self.df_gen, t_b_Vi.df_unc], ignore_index=True)

        # --- GF ---
        #No tiene Tipo A, es un dato de datasheet
        #Tipo B
        t_b_GF = T_B(calib=self.calib_GF, name="Gauge Factor")
        sens_GF = t_b_GF.coef_sens(i_var=GF, equation=model, num_values=self.num_values)
        t_b_GF.add(sensitivity=sens_GF)
        self.df_gen = pd.concat([self.df_gen, t_b_GF.df_unc], ignore_index=True)

        # --- RL ---
        #Tipo A
        t_a_RL = T_A(muestra=self.datos_RL, name="Load Resistance")
        t_a_RL.des_est(sensitivity=float(sp.diff(model, RL).evalf(subs= self.num_values)))
        self.df_gen = pd.concat([self.df_gen, t_a_RL.df_unc], ignore_index=True)
        
        #Tipo B
        #Resolucion y Calibracion
        t_b_RL = T_B(resol=self.resol_RL, calib=self.calib, name="Load Resistance")
        sens_RL = t_b_RL.coef_sens(i_var=RL, equation=model, num_values=self.num_values)
        t_b_RL.add(sensitivity=sens_RL)
        self.df_gen = pd.concat([self.df_gen, t_b_RL.df_unc], ignore_index=True)

        # --- RG ---
        #No tiene Tipo A, es un dato de datasheet
        #Tipo B
        t_b_RG = T_B(calib=self.calib_RG, name="Gauge Resistance")
        sens_RG = t_b_RG.coef_sens(i_var=RG, equation=model, num_values=self.num_values)
        t_b_RG.add(sensitivity=sens_RG)
        self.df_gen = pd.concat([self.df_gen, t_b_RG.df_unc], ignore_index=True)

        # --- v ---
        #No tiene Tipo A, es un dato de datasheet
        #Tipo B
        t_b_v = T_B(calib=self.calib_RG, name="Poisson Coefficient")
        sens_v = t_b_v.coef_sens(i_var=v, equation=model, num_values=self.num_values)
        t_b_v.add(sensitivity=sens_v)
        self.df_gen = pd.concat([self.df_gen, t_b_v.df_unc], ignore_index=True)

        # --- E ---
        #No tiene Tipo A, es un dato de datasheet
        #Tipo B
        t_b_E = T_B(calib=self.calib_RG, name="Young Module")
        sens_E = t_b_E.coef_sens(i_var=E, equation=model, num_values=self.num_values)
        t_b_E.add(sensitivity=sens_E)
        self.df_gen = pd.concat([self.df_gen, t_b_E.df_unc], ignore_index=True)

        # --- phi ---
        #Tipo A
        t_a_phi = T_A(muestra=self.datos_phi, name="Misalignment Angle")
        t_a_phi.des_est(sensitivity=float(sp.diff(model, phi).evalf(subs=self.num_values)))
        self.df_gen = pd.concat([self.df_gen, t_a_phi.df_unc], ignore_index=True)

        #Tipo B
        #Resolucion y Calibracion
        t_b_phi = T_B(resol=self.resol_phi, calib=self.calib_phi, name="Misalignment Angle")
        sens_phi = t_b_phi.coef_sens(i_var=phi, equation=model, num_values=self.num_values)
        t_b_phi.add(sensitivity=sens_phi)
        self.df_gen = pd.concat([self.df_gen, t_b_phi.df_unc], ignore_index=True)
               
        # --- m ---
        # Tipo A
        t_a_m = T_A(muestra=self.datos_m, name="Mass")
        t_a_m.des_est(sensitivity=float(sp.diff(model, m).evalf(subs=self.num_values)))
        self.df_gen = pd.concat([self.df_gen, t_a_m.df_unc], ignore_index=True)
        #Tipo B
        #  Resolucion y Calibracion
        t_b_m = T_B(resol=self.resol_m, calib=self.calib_m, name="Mass")
        sens_m = t_b_m.coef_sens(i_var=m, equation=model, num_values=self.num_values)
        t_b_m.add(sensitivity=sens_m)
        self.df_gen = pd.concat([self.df_gen, t_b_m.df_unc], ignore_index=True)

        # --- g ---
        #No tiene Tipo A, es un dato de datasheet
        #Tipo B
        t_b_g = T_B(calib=self.calib_g, name="Gravitational Acceleration")
        sens_g = t_b_g.coef_sens(i_var=g, equation=model, num_values=self.num_values)
        t_b_g.add(sensitivity=sens_g)
        self.df_gen = pd.concat([self.df_gen, t_b_g.df_unc], ignore_index=True)


        # --- lg ---
        #No tiene Tipo A, es un dato de datasheet
        #Tipo B
        #  Resolucion y Calibracion
        t_b_lg = T_B(calib=self.calib_lg, name="Gauge Length")
        sens_lg = t_b_lg.coef_sens(i_var=lg, equation=model, num_values=self.num_values)
        t_b_lg.add(sensitivity=sens_lg)
        self.df_gen = pd.concat([self.df_gen, t_b_lg.df_unc], ignore_index=True)

        #Calculos de Distancias
        d_mean, delta_0, delta_paral, delta_desg, delta_h, delta_F, theta, T, alpha_instr, alpha_obj = sp.symbols(
        'd_mean delta_0 delta_paral delta_desg delta_h delta_F theta T alpha_instr alpha_obj')
        num_values_pdr = {
        delta_0: 0, 
        delta_paral: 0, 
        delta_F: 0, 
        delta_desg: 0, 
        delta_h: 0, 
        alpha_instr: 1e-5,
        T: np.mean(self.datos_T),
        theta: np.mean(self.datos_theta),
        }

        # --- hg ---
        #Las distancias ya procesaron la expandida, se evaluan como calibracion, usan la clase TUD
        #Tipo B
        #  Resolucion y Calibracion
        num_values_hg = num_values_pdr.copy()
        num_values_hg.update({
            d_mean: np.mean(self.datos_hg),
            alpha_obj: 1  # Este símbolo es necesario en el modelo
        })


        modelo_hg = TUD(
        num_values = num_values_hg,
        d_mean_data =self.datos_hg,
        d_mean_resol = self.resol_pdr,
        d_mean_calib = self.calib_pdr,
        delta_params_calib = {
        "delta_0": 0,
        "delta_paral": 0,
        "delta_F": 0,
        "delta_desg": 0,
        "delta_h": 0
    },
        theta_data = self.datos_theta,
        theta_resol = self.resol_theta,
        theta_calib = self.calib_theta,
        T_data = self.datos_T,
        T_resol = self.resol_T,
        T_calib = self.calib_T
    )
        

        t_b_hg = T_B(calib= modelo_hg.u_e, name="Gauge High")
        sens_hg = t_b_hg.coef_sens(i_var=hg, equation=model, num_values=self.num_values)
        t_b_hg.add(sensitivity=sens_hg)
        self.df_gen = pd.concat([self.df_gen, t_b_hg.df_unc], ignore_index=True)
        # --- L ---
        #Las distancias ya procesaron la expandida, se evaluan como calibracion
        #Tipo B
        #  Resolucion y Calibracion
        num_values_L = num_values_pdr.copy()
        num_values_L.update({
            d_mean: np.mean(self.datos_L),
            alpha_obj: 1
        })

        modelo_L = TUD(
        num_values = num_values_L,
        d_mean_data=self.datos_L,
        d_mean_resol = self.resol_pdr,
        d_mean_calib = self.calib_pdr,
        delta_params_calib = {
        "delta_0": 0,
        "delta_paral": 0,
        "delta_F": 0,
        "delta_desg": 0,
        "delta_h": 0
    },
        theta_data = self.datos_theta,
        theta_resol = self.resol_theta,
        theta_calib = self.calib_theta,
        T_data = self.datos_T,
        T_resol = self.resol_T,
        T_calib = self.calib_T
    )
        
        t_b_L = T_B(calib=modelo_L.u_e, name="Length Cell")
        sens_L = t_b_L.coef_sens(i_var=L, equation=model, num_values=self.num_values)
        t_b_L.add(sensitivity=sens_L)
        self.df_gen = pd.concat([self.df_gen, t_b_L.df_unc], ignore_index=True)
        # --- x ---
        #Las distancias ya procesaron la expandida, se evaluan como calibracion
        #Tipo B
        #  Resolucion y Calibracion
        num_values_x = num_values_pdr.copy()
        num_values_x.update({
            d_mean: np.mean(self.datos_x),
            alpha_obj: 1
        })

        modelo_x = TUD(
        num_values = num_values_x,
        d_mean_data=self.datos_x,
        d_mean_resol = self.resol_pdr,
        d_mean_calib = self.calib_pdr,
        delta_params_calib = {
        "delta_0": 0,
        "delta_paral": 0,
        "delta_F": 0,
        "delta_desg": 0,
        "delta_h": 0
    },
        theta_data = self.datos_theta,
        theta_resol = self.resol_theta,
        theta_calib = self.calib_theta,
        T_data = self.datos_T,
        T_resol = self.resol_T,
        T_calib = self.calib_T
    )
        t_b_x = T_B(calib=modelo_x.u_e, name="Gauge Distance Force")
        sens_x = t_b_x.coef_sens(i_var=x, equation=model, num_values=self.num_values)
        t_b_x.add(sensitivity=sens_x)
        self.df_gen = pd.concat([self.df_gen, t_b_x.df_unc], ignore_index=True)

        # --- B ---
        #Las distancias ya procesaron la expandida, se evaluan como calibracion
        #Tipo B
        #  Resolucion y Calibracion
        num_values_B = num_values_pdr.copy()
        num_values_B.update({
            d_mean: np.mean(self.datos_B),
            alpha_obj: 1
        })

        modelo_b = TUD(
        num_values = num_values_B,
        d_mean_data = self.datos_B,
        d_mean_resol = self.resol_pdr,
        d_mean_calib = self.calib_pdr,
        delta_params_calib = {
        "delta_0": 0,
        "delta_paral": 0,
        "delta_F": 0,
        "delta_desg": 0,
        "delta_h": 0
    },
        theta_data = self.datos_theta,
        theta_resol = self.resol_theta,
        theta_calib = self.calib_theta,
        T_data = self.datos_T,
        T_resol = self.resol_T,
        T_calib = self.calib_T
    )
        t_b_b = T_B(calib=modelo_b.u_e, name="Base Cell")
        sens_b = t_b_b.coef_sens(i_var= b, equation=model, num_values=self.num_values)
        t_b_b.add(sensitivity=sens_b)
        self.df_gen = pd.concat([self.df_gen, t_b_b.df_unc], ignore_index=True)
        # --- h ---
        #Las distancias ya procesaron la expandida, se evaluan como calibracion
        #Tipo B
        #  Resolucion y Calibracion
        num_values_h = num_values_pdr.copy()
        num_values_h.update({
            d_mean: np.mean(self.datos_h),
            alpha_obj: 1
        })

        modelo_h = TUD(
        num_values = num_values_h,
        d_mean_data =self.datos_h,
        d_mean_resol = self.resol_pdr,
        d_mean_calib = self.calib_pdr,
        delta_params_calib = {
        "delta_0": 0,
        "delta_paral": 0,
        "delta_F": 0,
        "delta_desg": 0,
        "delta_h": 0
    },
        theta_data = self.datos_theta,
        theta_resol = self.resol_theta,
        theta_calib = self.calib_theta,
        T_data = self.datos_T,
        T_resol = self.resol_T,
        T_calib = self.calib_T
    )
        t_b_h = T_B(calib=modelo_h.u_e, name="Height Cell")
        sens_h = t_b_h.coef_sens(i_var= h, equation=model, num_values=self.num_values)
        t_b_h.add(sensitivity=sens_h)
        self.df_gen = pd.concat([self.df_gen, t_b_h.df_unc], ignore_index=True)
        
    def unc_expanded(self, k):
        self.df_gen["WeightedSquared"] = (self.df_gen["Uncertainty"] * self.df_gen["Sensitivity"])**2
        combined_std = np.sqrt(self.df_gen["WeightedSquared"].sum())
        expanded_uncertainty = k * combined_std
        return expanded_uncertainty

##################################################################################
if __name__ == "__main__":
    import sympy as sp

    # Variables simbólicas necesarias para num_values
    delta_V, Vi, GF = sp.symbols('delta_V Vi GF')
    RL, RG = sp.symbols('RL RG')
    v, phi = sp.symbols('v phi')
    hg, m, g, L, x = sp.symbols('hg m g L x')
    E, b, h = sp.symbols('E b h')
    lg = sp.symbols('lg')

    # Diccionario de valores nominales para coef. sensibilidad
    num_values = {
        delta_V: 1.5,
        Vi: 5,
        GF: 2.1,
        RL: 120,
        RG: 120,
        v: 0.3,
        phi: 0.1,
        hg: 10,
        m: 0.5,
        g: 9.81,
        L: 15,
        x: 7,
        E: 2e11,
        b: 5,
        h: 1,
        lg: 10
    }

    modelo = Total_unc_gauge(
        num_values=num_values,
        datos_delta_V=[1.5, 1.6, 1.4],
        resol_delta_V=0.01,
        datos_Vi=[5.0, 4.9, 5.1],
        resol_Vi=0.01,
        calib_Vi=0.005,
        calib_GF=0.01,
        datos_RL=[120, 121, 119],
        resol_RL=1,
        calib=0.5,
        calib_RG=0.5,
        datos_phi=[0.1, 0.09, 0.11],
        resol_phi=0.01,
        calib_phi=0.005,
        datos_theta=[0.02, 0.025, 0.03],
        resol_theta=0.001,
        calib_theta=0.0005,
        datos_T=[22, 23, 21],
        resol_T=0.5,
        calib_T=0.2,
        resol_pdr=0.01,
        calib_pdr=0.01,
        datos_m=[0.5, 0.51, 0.49],
        resol_m=0.01,
        calib_m=0.005,
        calib_g=0.01,
        calib_lg=0.01,
        datos_hg=[10.0, 10.1, 10.2],
        datos_L=[15.0, 15.1, 15.2],
        datos_x=[7.0, 7.1, 6.9],
        datos_B=[5.0, 5.1, 4.9],
        datos_h=[1.0, 1.1, 0.9])

    modelo.calculate()

    print("--- Tabla de incertidumbres ---")
    print(modelo.df_gen)

    modelo.df_gen["WeightedSquared"] = (modelo.df_gen["Uncertainty"] * modelo.df_gen["Sensitivity"])**2
    inc_exp = 3 * np.sqrt(modelo.df_gen["WeightedSquared"].sum())
    print(f"Incertidumbre expandida (k=3): {inc_exp:.6f}")

