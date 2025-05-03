import numpy as np
import inspect

class Type_A:
    def __init__(self, muestra, bool_norm):
        self.muestra = muestra
        if bool_norm in ("Y", "Si"):
            self.Sn_m = self.des_est()

    def des_est(self):
        return np.sqrt(np.var(self.muestra, ddof=1))

class Type_B:
    def __init__(self, res, calib, f_c_calib=3):
        self.res = res
        self.calib = calib
        self.f_c_calib = f_c_calib
        self.vector_unc = []  
        self.call()
        self.vector_unc = np.array(self.vector_unc)

    def unc_res(self):
        return (self.res / np.sqrt(12)), 1 , 1
    
    def unc_calib(self):
        return (self.calib / self.f_c_calib), 1 , 1
    
    def call(self):
        resultados = {}
        
        # Obtenemos todos los métodos de instancia
        for nombre, metodo in inspect.getmembers(self, predicate=inspect.ismethod):
            if nombre not in ("call", "__init__"):  # Evitar call y __init__
                resultado = metodo()  # Ejecutar el método
                self.vector_unc.append(resultado)  # Agregar al vector de incertidumbres
                resultados[nombre] = resultado

        return resultados
