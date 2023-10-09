import numpy as np
import sympy as sp
import scipy.signal as signal


class Generator:
    
    def __init__(self,a,b,fs):
        self.a = a
        self.b = b
        self.fs = fs
        self.t_var = sp.symbols('t')
        
    def t(self):
        var = np.linspace(self.a,self.b,self.fs)
        return var
                
    def sq(self,amp,f):
        y = amp*signal.square( 2*np.pi * f * self.t())
        return y
    
    def sen(self,amp,f):
        y = amp * np.sin( 2*np.pi * f * self.t())
        return y
    
    def triang(self,amp,f):
        y = amp*signal.sawtooth(2*np.pi * f *self.t(), width=0.5)
        return y
    
    def saw(self,amp,f):
        y = amp*signal.sawtooth(2*np.pi * f * self.t())
        return y

    def new(self, formula):
        t_values = self.t()
        symbolic_expr = sp.sympify(formula)  # Convierte la fórmula en una expresión simbólica
        func = sp.lambdify(self.t_var, symbolic_expr, "numpy")  # Crea una función numpy
        y = np.zeros_like(t_values)
        y = func(t_values)  # Evalúa la función en los valores de t
        return y
    
    def new_piece(self,matriz):
        # Extraer los puntos de inicio y fin de la matriz y convertirlos a enteros
        puntos_de_inicio = np.array([int(float(valor)) for valor in matriz[:, 1]])
        puntos_de_fin = np.array([int(float(valor)) for valor in matriz[:, 2]])
        arrFormulas = matriz[:,0]        

        # Encontrar los índices de los valores más cercanos en el array
        indices_inicio = np.searchsorted(self.t()  , puntos_de_inicio, side='left')
        indices_fin = np.searchsorted(self.t(), puntos_de_fin, side='right')

        # Dividir el array en trozos usando los índices encontrados
        trozos = [self.t()[inicio:fin] for inicio, fin in zip(indices_inicio, indices_fin)]
        
        #Crear array de respuestas 
        resp = np.array([])
        
        for i in range(len(arrFormulas)):
            t_values = trozos[i]   
            symbolic_expr = sp.sympify(arrFormulas[i])  # Convierte la fórmula en una expresión simbólica
            func = sp.lambdify(self.t_var, symbolic_expr, "numpy")  # Crea una función numpy                              
            y = func(t_values)  # Evalúa la función en los valores de t
            resp = np.append(resp,y)
            
        unido = np.concatenate(trozos) #sirve para verificar si la concatenacion es igual al original, es verdadero
        
        
        
        return resp


        
            
        
        
