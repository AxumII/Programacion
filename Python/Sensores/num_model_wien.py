import numpy as np

class NumModel:
    def __init__(self, R1=None, R2=None, C1=None, C2=None, Cs=None, Ra=None, Rb=None, K=None):
        self.R1 = R1; self.R2 = R2
        self.C1 = C1; self.C2 = C2; self.Cs = Cs
        self.Ra = Ra; self.Rb = Rb
        if K is not None:
            self.K = float(K)
        elif (Ra is not None) and (Rb is not None):
            self.K = 1.0 + (Rb / Ra)
        else:
            self.K = 1.0

    def _check_ready(self, params):
        faltantes = [p for p in params if getattr(self, p) is None]
        if faltantes:
            raise ValueError(f"Faltan parámetros: {', '.join(faltantes)}")

    def calculate_tf_params(self, c2w=False):
        # Para ωn y ζ sólo se requieren R1, R2, C1, C2
        self._check_ready(["R1", "R2", "C1", "C2"])
        R1, R2, C1, C2, K = self.R1, self.R2, self.C1, self.C2, self.K

        wn = 1.0 / np.sqrt(R1 * C1 * R2 * C2)
        z  = (R1*C1 + R1*C2*(1 - K) + R2*C2) / (2.0 * np.sqrt(R1*C1*R2*C2))

        return wn if c2w else (wn, z)
