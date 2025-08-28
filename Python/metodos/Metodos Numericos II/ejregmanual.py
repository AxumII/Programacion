from regresionManual import Regresion
import numpy as np

def ej1():
    x = np.array([3,4,5,6,8])
    y = np.array([1.6,2.4,2.9,3.4,4.6])
    reg = Regresion(x,y)
    Apot = reg.ajuste_potencia(2)
    print(Apot)
    print(reg.MSE(   reg.fx("pot",[ Apot, 2]))   )
    A,B = reg.lineal()
    print(A,B)
    print(reg.MSE(   reg.fx("lin",[A,B ]))   )


   





ej1()
#ej2()