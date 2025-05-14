import cupy as cp
import sympy as sp

class Model:
    def __init__(self, Vlect,K, R1, R2, R3, RG, RL, Vi, GF, v, phi,L, E, lg):
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
        self.L = L
        self.E = E
        self.lg = lg
        self.K = K

    def _is_symbolic(self, x):
        return isinstance(x, sp.Basic)

    def _cos(self, x):
        return sp.cos(x) if self._is_symbolic(x) else cp.cos(x)

    def calculate(self):
        delta_V = (self.Vlect / self.K) - ((self.R3 / (self.R3 + self.RG + self.RL)) - (self.R2 / (self.R1 + self.R2)))
        epsilon = (-4 * (delta_V / self.Vi)) / (self.GF * (1 + 2 * (delta_V / self.Vi)))
        error_misalignment = ((1 - self.v + (1 + self.v) * self._cos(2 * self.phi)) / 2) - 1
        error_mid = (self.lg / self.L) - 1
        error_bridge = (1 + self.RL / self.RG)
        return epsilon * error_bridge * error_misalignment*error_mid 