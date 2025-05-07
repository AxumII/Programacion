import numpy as np
import scipy.stats as st
import pandas as pd
import inspect
#######MODIFICAR LECTURA DE DATOS; LO MODIFIQUE PARA LA COMBINADA
class Uncertainty:  # Cambié a Uncertainty (tenías Uncertainly)
    def __init__(self, unc_array):
        self.unc_array = unc_array

    def U_comb(self):
        # Multiplicar incertidumbre por coeficiente de sensibilidad
        productos = self.unc_array[:, 0] * self.unc_array[:, 1]
        # Elevar al cuadrado y sumar
        Sn2_comb = np.sum(productos**2)
        # Retornar raíz cuadrada de la suma
        return np.sqrt(Sn2_comb)
    
    def U_exp(self, f_cob=3):
        # Sumar todos los grados de libertad
        n_freedom = np.sum(self.unc_array[:, 2])
        if n_freedom > 30:
            return self.U_comb() * f_cob
        else:
            # Aquí podrías agregar manejo para casos donde n_freedom <= 30
            return None
