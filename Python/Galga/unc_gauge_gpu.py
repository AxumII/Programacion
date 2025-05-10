import cupy as cp
import numpy as np
import pandas as pd

from unc_model_gpu import UncGeneral as UncG
from unc_dist_gpu import UncDistance as UncD

class UncGauge(UncG):
    def __init__(self, derivadas, num_values,
                 num_values_dist,
                 derivadas_dist,
                 input_d_mean,
                 input_delta_0,
                 input_delta_paral,
                 input_delta_F,
                 input_delta_desg,
                 input_delta_h,
                 input_theta,
                 input_T,
                 input_Vlect,
                 input_R1,
                 input_R2,
                 input_R3,
                 input_Vi,
                 input_GF,
                 input_RL,
                 input_RG,
                 input_v,
                 input_E,
                 input_phi,
                 input_m,
                 input_g,
                 input_lg,
                 
                 input_hg,
                 input_L,
                 input_x,
                 input_b,
                 input_h
                 ):
          
          
        
        self.input_d_mean = input_d_mean
        self.input_delta_0 = input_delta_0
        self.input_delta_paral = input_delta_paral
        self.input_delta_F = input_delta_F
        self.input_delta_desg = input_delta_desg
        self.input_delta_h = input_delta_h
        self.input_theta = input_theta
        self.input_T = input_T
        self.input_Vlect = input_Vlect
        self.input_R1 = input_R1
        self.input_R2 = input_R2
        self.input_R3 = input_R3
        self.input_Vi = input_Vi
        self.input_GF = input_GF
        self.input_RL = input_RL
        self.input_RG = input_RG
        self.input_v = input_v
        self.input_E = input_E
        self.input_phi = input_phi
        self.input_m = input_m
        self.input_g = input_g
        self.input_lg = input_lg

        self.input_hg = input_hg
        self.input_L = input_L
        self.input_x = input_x
        self.input_b = input_b
        self.input_h = input_h

        self.input_data_distance = [input_hg,input_L,input_x,input_b,input_h]
        self.num_values_dist = num_values_dist
        self.derivadas_dist = derivadas_dist
        
        super().__init__(derivadas, num_values)
        
    def calculate(self):
        self.calc_a_and_b(self.input_Vlect)
        self.calc_b(self.input_R1)
        self.calc_b(self.input_R2)
        self.calc_b(self.input_R3)
        self.calc_a_and_b(self.input_Vi)
        self.calc_b(self.input_GF)
        self.calc_b(self.input_RL)
        self.calc_b(self.input_RG)
        self.calc_b(self.input_v)
        self.calc_b(self.input_E)
        self.calc_a_and_b(self.input_phi)
        self.calc_a_and_b(self.input_m)
        self.calc_b(self.input_g)
        self.calc_b(self.input_lg)

        
        for input_data in self.input_data_distance:
            u_exp_data_n = self.unc_expanded_dist(input_data)
            name = input_data["name"]
            resol = None
            calib = float(u_exp_data_n)  
            self.calc_b([(name, resol, calib)])


                

    def unc_expanded_dist(self, input_data):
        input_d_mean = [(input_data["muestra"], input_data["name"], input_data["resol"], input_data["calib"])]
        
        unc = UncD(
            input_d_mean=input_d_mean,
            input_delta_0=self.input_delta_0,
            input_delta_paral=self.input_delta_paral,
            input_delta_F=self.input_delta_F,
            input_delta_desg=self.input_delta_desg,
            input_delta_h=self.input_delta_h,
            input_theta=self.input_theta,
            input_T=self.input_T,
            derivadas=self.derivadas_dist,
            num_values=self.num_values_dist
        )
        
        return unc.unc_expanded(k=3)


        