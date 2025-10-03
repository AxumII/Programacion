import cupy as cp

class NumModel:
    
    def __init__(self, R1=None, R2=None, C1=None, Cs=None, C2=None,
                 Rl=None, Cl = None, Vz = None):
        self.R1 = R1; self.R2 = R2
        self.C1 = C1; self.Cs = Cs; self.C2 = C2
        self.Rl = Rl, self.Cl = Cl, self.Vz = Vz
        self.calculate()

    def _check_ready(self, params):
        faltantes = [p for p in params if getattr(self, p) is None]
        if faltantes:
            raise ValueError(f"Faltan parámetros: {', '.join(faltantes)}")

    def calculate(self):
        params = ["R1","R2","C1","Cs","C2","Rl","Rt","Ct","Rs"]
        self._check_ready(params)
        R1, R2 = self.R1, self.R2
        C1, Cs, C2 = self.C1, self.Cs, self.C2
        Rl, Vz, Cl = self.Rl, self.Vz, self.Cl


        wn = 1/ cp.sqrt(R1*R2*(C1+Cs)*C2)
        Vo = (wn/(2*cp.pi))*Vz*Cl*Rl
        return Vo
    
    