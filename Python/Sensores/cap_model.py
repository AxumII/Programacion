import numpy as np
from capacitor import Capacitor as Cap


class ModelCapacitor: #Modelo con aire, pla y agua
    def __init__(
        self,
        e_d=None,
        d_s: float = 10e-3,
        *,
        h_right_copper: float = 41.2/1000,
        h_left_copper: float  = 39.5/1000,
        w_up_copper: float    = 99.1/1000,
        w_down_copper: float  = 99.1/1000,
        h_in: float           = 34.8/1000,
        w_in: float           = 16.6/1000,
        h_level: float        = 1.0/1000,
    ):
        # Geometría global (cobre perimetral)
        self.h_right_copper = float(h_right_copper)
        self.h_left_copper  = float(h_left_copper)
        self.w_up_copper    = float(w_up_copper)
        self.w_down_copper  = float(w_down_copper)

        # Ventanas internas
        self.h_in = float(h_in)
        self.w_in = float(w_in)

        # Nivel de fluido dentro de la ventana
        self.h_level = float(h_level)

        # Separación entre placas
        self.d_s = float(d_s)

        # Validaciones básicas
        if self.h_level < 0:
            self.h_level = 0.0
        if self.h_level > self.h_in:
            self.h_level = self.h_in

        self.e_d = np.array(e_d, dtype=float) if e_d is not None else np.array([1.0, 1.0, 1.0], dtype=float)
        #   Verificador dimensión de e_d
        if self.e_d.ndim != 1 or self.e_d.size not in (1, 3):
            raise ValueError("e_d debe ser escalar o un array de tamaño 3: [e_PLA, e_aire, e_fluido]")


        # Permitividades relativas por región [PLA, aire, fluido]
        self.e_d = np.array(e_d, dtype=float) if e_d is not None else np.array([1.0, 1.0, 1.0], dtype=float)


        self.irregular = lambda h_right, h_left, w_up, w_down: (h_right*w_up)/2 + (h_left*w_down)/2
        self.rectangle = lambda h, b: h * b
        self.complement = lambda A_t, A_m: A_t - A_m 

        # Área del cobre 
        self.A_total = self.irregular(
            h_right=self.h_right_copper,
            h_left=self.h_left_copper,
            w_up=self.w_up_copper,
            w_down=self.w_down_copper,
        )

    def calculate_c(self):
        areas = [self.pla_area(), self.air_area(), self.fluid_area()]
        # Si e_d es escalar, replicarlo a 3 regiones
        e_d_vec = np.repeat(self.e_d, 3) if self.e_d.size == 1 else self.e_d
        c1 = Cap(d_s=self.d_s, A=areas, e_d=e_d_vec)
        return c1.c

    def pla_area(self):
        # Área de PLA = área total menos 4 ventanas rectangulares
        return self.A_total - 4.0 * self.rectangle(self.h_in, self.w_in)

    def air_area(self):
        # Aire en 4 ventanas por encima del nivel del fluido
        h_air = max(self.h_in - self.h_level, 0.0)
        return 4.0 * self.rectangle(h_air, self.w_in)

    def fluid_area(self):
        # Fluido en 4 ventanas hasta h_level
        h_fluid = min(self.h_level, self.h_in)
        return 4.0 * self.rectangle(h_fluid, self.w_in)

"""# -------------------------
# Ejemplo de uso (runnable)
# -------------------------
if __name__ == "__main__":
    model = ModelCapacitor(
        e_d=[2.8, 1.0006, 80.0],  # [PLA, aire, agua] 
        d_s=1.4e-3,                 
        h_right_copper=41.2/1000,
        h_left_copper=39.5/1000,
        w_up_copper=99.1/1000,
        w_down_copper=99.1/1000,
        h_in=34.8/1000,
        w_in=16.6/1000,
        h_level=0/1000,             
    )

    print("ÁREAS (m^2):")
    print("  PLA   :", model.pla_area())
    print("  Aire  :", model.air_area())
    print("  Fluido:", model.fluid_area())

    C = model.calculate_c()
    print("\nCapacitancia total (pF):", C* 1e12)"""