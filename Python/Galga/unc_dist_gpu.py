import cupy as cp
import numpy as np
import pandas as pd

from unc_model_gpu import UncGeneral as UncG

class UncDistance(UncG):
    def __init__(self, derivadas, num_values,input_d_mean,
                 input_delta_0,
                 input_delta_paral,
                 input_delta_F,
                 input_delta_desg,
                 input_delta_h,
                 input_theta,
                 input_T):
        
        self.input_d_mean = input_d_mean
        self.input_delta_0 = input_delta_0
        self.input_delta_paral = input_delta_paral
        self.input_delta_F = input_delta_F
        self.input_delta_desg = input_delta_desg
        self.input_delta_h = input_delta_h
        self.input_theta = input_theta
        self.input_T = input_T
    

        
        super().__init__(derivadas, num_values)
        
    def calculate(self):
        self.calc_a_and_b(self.input_d_mean)
        self.calc_b(self.input_delta_0)
        self.calc_b(self.input_delta_paral)
        self.calc_b(self.input_delta_F)
        self.calc_b(self.input_delta_desg)
        self.calc_b(self.input_delta_h)
        self.calc_b(self.input_theta)
        self.calc_a_and_b(self.input_T)

"""
if __name__ == "__main__":
    def generar_input_tipo_a_y_b(nombre, sensibilidad):
        muestra = cp.random.normal(loc=0.1, scale=0.01, size=10)
        resol = 0.001
        calib = 0.002
        return (muestra, nombre, resol, calib)

    def generar_input_tipo_b(nombre, sensibilidad):
        resol = 0.001
        calib = 0.002
        return (nombre, resol, calib)

    input_d_mean = [generar_input_tipo_a_y_b("d_mean", 1)]
    input_delta_0 = [generar_input_tipo_b("delta_0", 1)]
    input_delta_paral = [generar_input_tipo_b("delta_paral", 1)]
    input_delta_F = [generar_input_tipo_b("delta_F", 1)]
    input_delta_desg = [generar_input_tipo_b("delta_desg", 1)]
    input_delta_h = [generar_input_tipo_b("delta_h", 1)]
    input_theta = [generar_input_tipo_b("theta", 1)]
    input_T = [generar_input_tipo_a_y_b("T", 1)]

    derivadas = {
    "d_mean":     "(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    "delta_0":    "-(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    "delta_paral":"(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    "delta_F":    "(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    "delta_desg": "(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    "delta_h":    "(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    "theta":      "((alpha_instr*(T - T0) + 1)*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral)*sin(theta))/((alpha_obj*(T - T0) + 1)*cos(theta)**2)",
    "T":          "(alpha_instr*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral))/((alpha_obj*(T - T0) + 1)*cos(theta)) - (alpha_obj*(alpha_instr*(T - T0) + 1)*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral))/((alpha_obj*(T - T0) + 1)**2*cos(theta))",
    "T0":         "(-alpha_instr*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral))/((alpha_obj*(T - T0) + 1)*cos(theta)) + (alpha_obj*(alpha_instr*(T - T0) + 1)*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral))/((alpha_obj*(T - T0) + 1)**2*cos(theta))",
    "alpha_instr":"(T - T0)*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    "alpha_obj":  "(-T + T0)*(alpha_instr*(T - T0) + 1)*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral)/((alpha_obj*(T - T0) + 1)**2*cos(theta))"
}
    num_values = {
    "T": 25,
    "T0": 20,
    "theta": 0.1,
    "alpha_instr": 0.00001,
    "alpha_obj": 0.000012,
    "d_mean": 10,
    "delta_0": 0.1,
    "delta_paral": 0.05,
    "delta_F": 0.02,
    "delta_desg": 0.01,
    "delta_h": 0.03,
}


    unc = UncDistance(
    input_d_mean=input_d_mean,
    input_delta_0=input_delta_0,
    input_delta_paral=input_delta_paral,
    input_delta_F=input_delta_F,
    input_delta_desg=input_delta_desg,
    input_delta_h=input_delta_h,
    input_theta=input_theta,
    input_T=input_T,
    derivadas=derivadas,
    num_values=num_values  # ← Agrega esto
    )


    # Mostrar resultados
    print("=== Tabla de Incertidumbres ===")
    print(unc.df_gen)
    print("\n=== Incertidumbre Expandida (k=3) ===")
    print(f"{unc.unc_expanded(k=3):.6f}")"""