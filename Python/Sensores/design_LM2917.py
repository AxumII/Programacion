import numpy as np

class DesignLm2917:
    def __init__(self, V_span, df, Vz, V_ref, V_ripple, f0):
        # Inputs
        self.V_span   = float(V_span)
        self.df       = float(df)
        self.Vz       = float(Vz)
        self.V_ref    = float(V_ref)
        self.V_ripple = float(V_ripple)
        self.f0       = float(f0)

        # Constantes
        self.u = 1e-6
        self.I_pump = 180*self.u       # ≈180 µA

        # Lambdas
        self.S_cp2  = lambda V_ref, f0: V_ref / f0                # V/Hz
        self.RpCp   = lambda S_cp2, Vz: S_cp2 / Vz                # = Vref/(Vz*f0)
        self.Rp_max = lambda V_ref, f0, df: (V_ref*((f0+df)/f0)) / self.I_pump
        self.Cp     = lambda tao, Rp: tao / Rp                    # aquí 'tao' = RpCp
        self.Cf_min = lambda Vz, f_max, Cp, V_ripple_pp: (Vz*f_max*Cp)/(2.0*V_ripple_pp)
        self.A_gain = lambda V_span, Vz, Cp, Rp, df: V_span/(Vz*Cp*Rp*df)
        self.S_out  = lambda V_span, df: V_span / df

    def calculate(self):
        Vz, Vref, f0, df, Vspan, Vrpp = self.Vz, self.V_ref, self.f0, self.df, self.V_span, self.V_ripple
        f_max = f0 + df

        # 1) Sensibilidad CP2 y producto Rp*Cp
        S_f  = self.S_cp2(V_ref=Vref, f0=f0)        
        RpCp = self.RpCp(S_cp2=S_f, Vz=Vz)          

        # 2) Rp max
        Rp = self.Rp_max(V_ref=Vref, f0=f0, df=df)

        # 3) Cp bruto
        Cp = self.Cp(tao=RpCp, Rp=Rp)

        # 4) Cf mínimo por rizado
        Cf = self.Cf_min(Vz=Vz, f_max=f_max, Cp=Cp, V_ripple_pp=Vrpp)

        # 5) Ganancia
        A_g = self.A_gain(V_span=Vspan, Vz=Vz, Cp=Cp, Rp=Rp, df=df)

        return Rp, Cp, Cf, A_g


#########################################################################
# Ejemplo de uso
def e():
    k = 1e3
    n = 1e-9
    u = 1e-6
    m = 1e-3

    # Inputs 
    V_span   = 3     # V
    df       = 100     # Hz 
    Vz       = 7.56    # V
    V_ref    = 2.5     # V
    V_ripple = 50*m     # Vpp
    f0       = 1*k     # Hz

    print("Frecuencia ω0 [rad/s]:", f0*2*np.pi)

    design = DesignLm2917(V_span, df, Vz, V_ref, V_ripple, f0)
    Rp, Cp, Cf, A = design.calculate()

    # Conversión correcta de unidades en el print
    print(f"Rp max = {Rp/ k:.3f} kΩ")
    print(f"Cp     = {Cp/ n:.3f} nF")
    print(f"Cf min = {Cf/ u:.3f} uF")
    print(f"A      = {A:.3f}")

e()
