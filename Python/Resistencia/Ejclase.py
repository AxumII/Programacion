import numpy as np


def ej():
    #Valores
    P = 15000
    Cy = 1.429
    Iz = 4.81
    L = 4
    width = 1/4
    #Calculos
    A = 2*(L*width) + (L - 2*width)*(width)
    ey = -L/2 + Cy
    puntoA = -2 + ey
    puntoB = 2 + ey
    Mz_A = P*ey*puntoA
    Mz_B = P*ey*puntoB 
    #Operaciones
    
    Esf_c = P/A
    Esf_exc_A = Mz_A/Iz
    Esf_exc_B = Mz_B/Iz

    Esf_A = Esf_c + Esf_exc_A
    Esf_B = Esf_c + Esf_exc_B

    print(Esf_c)
    print(Esf_exc_A)
    print(Esf_exc_B)
    return Esf_A,Esf_B

print(ej())
    
    
    