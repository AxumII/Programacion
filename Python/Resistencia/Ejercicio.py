import sympy as sp

def Ejercicio():
    # Definir símbolos
    mb, md, l, r, theta_1, k, wb = sp.symbols('mb,md,l,r,theta_1,k, wb')
    
    # Términos dependientes
    Ib = (1/12) * mb * (l**2)
    Id = (0.5) * md * (r**2)
    h1 = l * sp.sin(theta_1)  # convertir a radianes, no olvidar
    
    # Constantes
    g = 9.81

    # Ecuaciones
    Energia = sp.Eq((mb * g * h1) + (0.5 * k * (h1**2 - r**2)), (1/6) * (mb * (l**2) * (wb**2)))
    
    Sol_sym = sp.solve(Energia, wb)
    sp.pprint(Sol_sym)
    
    # Sustituir valores
    valores = {mb: 4, md: 5, l: 0.32, r: 0.08, theta_1: sp.rad(50), k: 400}
    
    # Aplicar la sustitución a cada solución en la lista
    Sol_num = [sol.subs(valores) for sol in Sol_sym]
    
    sp.pprint(Sol_num)

Ejercicio()