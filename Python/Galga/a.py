import numpy as np
import pandas as pd
import sympy as sp

from unc import Type_A as T_A
from unc import Type_B as T_B

class T_B_Total(T_B):
    def __init__(self, resol=None, calib=None, name=None, f_c_calib=3):
        super().__init__(resol, calib, name, f_c_calib)

    def unc_gen_function(self, num_values_gen):
        delta_V, Vi, GF, RL, RG = sp.symbols('delta_V Vi GF RL RG')    
        epsilon = (-4 * (delta_V / Vi)) / (GF * (1 + 2 * (delta_V / Vi))) * (1 + RL / RG)

        for var, label in zip(
            [Vi, GF, RL, RG, delta_V],
            ["Voltaje Input", "Gauge Factor", "Wire Resistance", "Gauge Resistance", "Delta Voltage"]
        ):
            tb = T_B(calib=1, name=label)
            sens = tb.coef_sens(i_var=var, equation=epsilon, num_values=num_values_gen)
            tb.unc_calib(sensitivity=sens)
            tb.add()
            self.df_unc = pd.concat([self.df_unc, tb.df_unc], ignore_index=True)

    def unc_misagnl(self, num_values_misagnl):
        v, phi = sp.symbols('v phi')
        error = ((1 - v + (1 + v) * sp.cos(2 * phi)) / 2) - 1

        tb = T_B(calib=1, name="Misalignment Angle")
        sens = tb.coef_sens(i_var=phi, equation=error, num_values=num_values_misagnl)
        tb.unc_calib(sensitivity=sens)
        tb.add()
        self.df_unc = pd.concat([self.df_unc, tb.df_unc], ignore_index=True)

    def unc_curvature(self, num_values_curv):
        h, E, b, F, L, x = sp.symbols('h E b F L x')
        error = h / ((E * (b * (h**3)) / 12) / (F * (L - x)))

        for var, label in zip(
            [h, b, L, x],
            ["High_Support", "Base_Support", "Long_Support", "Gauge_Distance"]
        ):
            tb = T_B(calib=1, name=label)
            sens = tb.coef_sens(i_var=var, equation=error, num_values=num_values_curv)
            tb.unc_calib(sensitivity=sens)
            tb.add()
            self.df_unc = pd.concat([self.df_unc, tb.df_unc], ignore_index=True)

    def unc_grid_mean(self, num_values_grid_mean): 
        lg, L = sp.symbols('lg L')
        error = lg / L

        for var, label in zip(
            [L, lg],
            ["Long_Support", "Gauge Length"]
        ):
            tb = T_B(calib=1, name=label)
            sens = tb.coef_sens(i_var=var, equation=error, num_values=num_values_grid_mean)
            tb.unc_calib(sensitivity=sens)
            tb.add()
            self.df_unc = pd.concat([self.df_unc, tb.df_unc], ignore_index=True)

########################################################

# Instancia
tb_total = T_B_Total(name="Total_Uncertainty")

# Símbolos
delta_V, Vi, GF, RL, RG = sp.symbols('delta_V Vi GF RL RG')
v, phi = sp.symbols('v phi')
h, E, b, F, L, x = sp.symbols('h E b F L x')
lg = sp.Symbol('lg')

# Valores numéricos
num_values_gen = {
    delta_V: 0.002,
    Vi: 5.0,
    GF: 2.1,
    RL: 120,
    RG: 120
}
num_values_misagnl = {
    v: 0.3,
    phi: sp.rad(5.0)
}
num_values_curv = {
    h: 0.01,
    E: 210e9,
    b: 0.02,
    F: 10,
    L: 0.3,
    x: 0.05
}
num_values_grid_mean = {
    lg: 0.005,
    L: 0.3
}

# Ejecutar métodos
tb_total.unc_gen_function(num_values_gen)
tb_total.unc_misagnl(num_values_misagnl)
tb_total.unc_curvature(num_values_curv)
tb_total.unc_grid_mean(num_values_grid_mean)

# Mostrar resultados
print(tb_total.df_unc)
