import numpy as np


class Regresion:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.comprobador()
        pass
    
    def comprobador(self):
        if np.shape(self.x) != np.shape(self.y):
            print("No tienen misma longitud, se rellenara con 0")
            
        else:
            pass
    
    def ajuste_potencia(self, M = 2):
        nm = np.sum(self.x**2 *self.y)
        dm = np.sum(self.x**(2*M))
        return nm/dm
    
    def exponencial(self):
        pass
    
    def lineal(self, x=None, y=None):
        if x is None:
            x = self.x
        if y is None:
            y = self.y
            
        n = np.size(x,0)
        b1 = np.sum(x)
        c1 = np.sum(y)
        a2 = np.sum(x)
        b2 = np.sum(x**2)
        c2 = np.sum(x*y)
        A = np.array    ([[n, b1],
                          [a2, b2]])    
        B = np.array([c1, c2])
        return (np.linalg.solve(A,B))
    
    def exponencial(self):
        xln = np.log(self.x)
        yln = np.log(self.y)
        
        return self.lineal(x,y)
        
    
    def MSE(self,fx):
        return np.mean((fx - self.y)**2)
        
    def fx(self,type,param):
        if type == "pot":
            A,M = param
            return A*(self.x**M)
        if type == "lin":
            A,B = param
            return A*self.x + B
        
