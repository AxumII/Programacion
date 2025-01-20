import sympy as sp
import numpy as np

def p1():
    # Simbolos
    t, Vba = sp.symbols('t Vba')

    # Constantes
    Time = 1.5 
    
    # Ecuaciones
    Va = 3 * (t**2)  # Velocidad a
    Vb = (5 * (t**2)) - 1  # Velocidad b

    # Derivadas (aceleraciones)
    Aa = sp.diff(Va, t)  # Aceleración a
    Ab = sp.diff(Vb, t)  # Aceleración b
    
    # Ecuaciones de velocidad relativa
    # Componentes X
    eq_x = sp.Eq(-Vb * sp.cos(sp.pi / 3), Va - Vba * sp.cos(sp.pi / 6))  # 60° = pi/3 y 30° = pi/6
    
    # Componentes Y
    eq_y = sp.Eq(Vb * sp.sin(sp.pi / 3), Vba * sp.sin(sp.pi / 6))
    
    # Resolver el sistema de ecuaciones de la función p1
    sol_p1 = sp.solve([eq_x, eq_y], (Vba, t))
    
    return sol_p1


def p3():
    # Simbolos
    Np, Aa, Aba, Ab, Nba, P = sp.symbols('Np Aa Aba Ab Nba P') 

    # Constantes
    ma = 8
    mb = 15

    # Ecuaciones de fuerzas
    FBx = sp.Eq(Nba * sp.cos(75 * sp.pi / 180) - Np, 0)  # 75° en radianes
    FBy = sp.Eq(Nba * sp.sin(75 * sp.pi / 180) - mb, mb * Ab)
    FAx = sp.Eq(P - Nba * sp.cos(75 * sp.pi / 180), ma * Aa)
    
    # Ecuaciones de ligadura
    eq_ligadura_1 = sp.Eq(Ab, -Aba * sp.sin(15 * sp.pi / 180))  # 15° en radianes
    eq_ligadura_2 = sp.Eq(Aa, -Aba * sp.cos(15 * sp.pi / 180))

    # Resolver el sistema de ecuaciones de la función p3
    sol_p3 = sp.solve([FBx, FBy, FAx, eq_ligadura_1, eq_ligadura_2], (Np, P, Aa, Aba, Nba))
    
    return sol_p3


# Ejecución y obtención de soluciones
sol_p1 = p1()
sol_p3 = p3()

# Mostrar resultados
print("Solución del sistema de p1:")
print(sol_p1)

print("\nSolución del sistema de p3:")
print(sol_p3)
