import sympy as sp


def Ej2():
    #Valores
    E = 200*(10**9)
    h = 90/1000
    w = 25/1000
    Ix = (1/12)*w*(h**3)
    An = w*h
    defor_A = 350*(10**-6)
    defor_B = -70**(10**-6)
    dist_A = 15*(10**-3)
    dist_B = 30*(10**-3)
    
    #Variables
    #d es la distancia de excentricidad
    #P es la carga    
    d , P = sp.symbols('d P')
    print(An,Ix)
    #Ecuaciones
    Ec_A = sp.Eq(((P/An) + ((P*d*dist_A)/Ix)), E*defor_A)
    Ec_B = sp.Eq(((P/An) - ((P*d*dist_B)/Ix)), E*defor_B)
    sol = sp.solve((Ec_A,Ec_B),(P,d))
    return sol



print(Ej2())
#TOca corregir



