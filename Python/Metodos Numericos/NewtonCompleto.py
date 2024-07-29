import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sympy as sp

class NewtonRaphson:
    


    def __init__(self, equation, initial, iterat=100, stoperror=1e-7, accelerate = False): 
        self.x = sp.symbols('x')

        self.equation = equation
        self.initial = initial 
        self.iterat = iterat
        self.stoperror = stoperror



    #sympyfy , convierte a expresion simbolica
    #lambdify, convierte a funcion numerica
    #diff, derivada simbolica
    def convert(self):
        func_expr = sp.sympify(self.equation)
        func_num = sp.lambdify(self.x, func_expr, "numpy")
        return func_num, func_expr

    def derivation(self):
        func_num, func_expr = self.convert() #expresion simbolica y numerica
        firstderiv_expr = sp.diff(func_expr, self.x) #primera derivada simbolica
        secderiv_expr = sp.diff(firstderiv_expr, self.x) #segunda derivada simbolica
        firstderiv_num = sp.lambdify(self.x,firstderiv_expr, "numpy" ) #primera derivada numerica, con lambdify se vuelve numerica modo np
        secderiv_num = sp.lambdify(self.x,secderiv_expr, "numpy" ) #segunda derivada numerica, con lambdify se vuelve numerica modo np
        return firstderiv_num, secderiv_num, firstderiv_expr, secderiv_expr

    def solve(self, report = False):
        xn = self.initial #es mas comodo trabajar con xn 
        func_num, func_expr = self.convert() #expresion simbolica y numerica
        firstderiv_num, secderiv_num, firstderiv_expr, secderiv_expr = self.derivation()

        #verificacion de la raiz para multiplicidad
        A = abs(secderiv_num)/( 2 * abs(func_num))

        for n in range(self.iterat): # por defecto esta el numero de iteraciones, en caso de que no llegue pa no petar XD
            fxn = func_num(xn)
            d1fxn = firstderiv_num(xn)
            d2fxn = secderiv_num(xn)

            #no puedo verificar el orden sin conocer la raiz, porque necesito la raiz y derivar hasta que la derivada reemplazada en la raiz deje de ser 0

            #verificaciones para la correcta ejecucion del metodo
            if d1fxn == 0:
                print("La derivada es 0, esta en un máximo o mínimo local, no puede proceder.")
                break

            if fxn*d2fxn > 0:
                print("la funcion por la segunda derivada no es 0, no puede proceder")
                break


            #Metodo en si
            xn_next = xn - (fxn/d1fxn)
            if abs(xn_next - xn) < self.stoperror:
                return xn_next
            
            xn = xn_next
            


        


    
    