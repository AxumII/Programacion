from unc_c2v_gpu import UncC2V as UncC2V
from symb_model_c2v import SymbModel as sbm


class UncAnalisys:
    def __init__(
        self,
        num_values=None,
        inputs_tipo_a_b=None,   # dict: var -> (muestra, name, resol, calib, desvest)
        inputs_tipo_b=None,     # dict: var -> (name, resol, calib)
    ):
        # === Defaults 
        if inputs_tipo_a_b is None:
            inputs_tipo_a_b = {
                "Cs": (None, "Cs", 0.0001, 0.0002, 1.0),
                "R1": (None, "R1", 0.0001, 0.0002, 1.0),
                "R2": (None, "R2", 0.0001, 0.0002, 1.0),
                "C1": (None, "C1", 0.0001, 0.0002, 1.0),
                "C2": (None, "C2", 0.0001, 0.0002, 1.0),
                "Rl": (None, "Rl", 0.0001, 0.0002, 1.0),
                "Vz": (None, "Vz", 0.0001, 0.0002, 1.0),
                "Cl": (None, "Cl", 0.0001, 0.0002, 1.0),
            }
        if inputs_tipo_b is None:
            inputs_tipo_b = {}  

        if num_values is None:
            num_values = {"R1":1e3,
                          "R2":1e3,
                          "Rl":1e3,
                          "C1":1e-9,
                          "C2":1e-9,
                          "Cs":1e-9,
                          "Cl":1e-9,
                          "Vz":1e-9}


        self.inputs_tipo_a_b = inputs_tipo_a_b
        self.inputs_tipo_b   = inputs_tipo_b
        self.num_values      = num_values

    def unc_an(self):
        # 1) Modelo simbólico
        sm = sbm()
        vo_sym = sm.calculate()
        print("Vo =", vo_sym)

        # (opcional) mostrar derivadas simbólicas + evaluación numérica
        sm.print_derivatives(values=self.num_values)

        # 2) Sensibilidades NUMÉRICAS en el punto (dict de floats)
        sens_num = sm.eval_sens_coeffs(self.num_values)  # {'R1': float, ...}
        sensitivity_dict = sens_num                      # usar directamente

        # 3) Ejecutar motor de incertidumbre
        unc = UncC2V(
            num_values=self.num_values,
            inputs_tipo_a_b_dist=self.inputs_tipo_a_b,
            inputs_tipo_b_dist=self.inputs_tipo_b,
            sensitivity_dict=sensitivity_dict,
        )
        unc.calculate()
        unc.unc_expanded(k=2)

        return unc.df_gen, unc.u_exp


# Ejecución mínima


num_values =   {"R1":1e3,
                "R2":1e3,
                "Rl":1e3,
                "C1":1e-9,
                "C2":1e-9,
                "Cs":1e-9,
                "Cl":1e-9,
                "Vz":1e-9}
u = UncAnalisys(num_values=num_values)
df, U = u.unc_an()
print("\n--- Resumen ---")
print(df)
print("U(k=2) =", U)