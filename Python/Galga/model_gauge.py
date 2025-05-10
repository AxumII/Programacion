import numpy as np

class Model:
    def __init__(self, Vlect,K, R1, R2, R3, RG, RL, Vi, GF, v, phi, hg, m, g, L, x, E, b, h, lg):
        self.Vlect = Vlect
        self.R1 = R1
        self.R2 = R2
        self.R3 = R3
        self.RG = RG
        self.RL = RL
        self.Vi = Vi
        self.GF = GF
        self.v = v
        self.phi = phi
        self.hg = hg
        self.m = m
        self.g = g
        self.L = L
        self.x = x
        self.E = E
        self.b = b
        self.h = h
        self.lg = lg
        self.K = K

    def calculate(self):
        delta_V = (self.Vlect/self.K) - ((self.R3 / (self.R3 + self.RG + self.RL)) - (self.R2 / (self.R1 + self.R2)))
        epsilon = (-4 * (delta_V / self.Vi)) / (self.GF * (1 + 2 * (delta_V / self.Vi)))
        error_misalignment = ((1 - self.v + (1 + self.v) * np.cos(2 * self.phi)) / 2) - 1
        error_curvature = (12 * self.hg * self.m * self.g * (self.L - self.x)) / (self.E * self.b * self.h**3)
        error_gauge_long = (self.lg / self.L) - 1
        error_bridge = (1 + self.RL / self.RG)
        model = epsilon * error_bridge * error_misalignment * error_curvature * error_gauge_long
        return model
    


