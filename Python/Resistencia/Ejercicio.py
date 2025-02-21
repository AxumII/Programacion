import sympy as sp

def Ejercicio():
    # Definir símbolos
    mb, md, l, r, theta_1, k, wb = sp.symbols('mb md l r theta_1 k wb')
    
    # Momento de inercia
    Ib = (1/12) * mb * (l**2)  # Momento de inercia de una barra delgada
    Id = (1/2) * md * (r**2)   # Momento de inercia de un disco

    # Altura de la barra en función del ángulo
    h1 = l * sp.sin(theta_1)  # Debe ser radianes

    # Constantes
    g = 9.81

    # Ecuación de energía mecánica
    Energia = sp.Eq((0.5*mb * g * h1) + (0.5 * k * (h1**2)), (1/6) * (mb * (l**2) * (wb**2)))

    # Resolver para wb
    Sol_sym = sp.solve(Energia, wb)
    
    print("\nSolución Simbólica:")
    sp.pprint(Sol_sym)
    
    # Sustituir valores numéricos
    valores = {mb: 4, md: 5, l: 0.32, r: 0.08, theta_1: sp.rad(50).evalf(), k: 400}
    
    # Evaluar soluciones numéricamente
    Sol_num = [sol.subs(valores).evalf() for sol in Sol_sym]

    print("\nSolución Numérica:")
    sp.pprint(Sol_num)

Ejercicio()
