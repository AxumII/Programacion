import sympy as sp

# Símbolos
h, V = sp.symbols("h V")
m , g, k, S, L = sp.symbols("m g k S L")

# Ecuaciones
# Ecuación básica de velocidad
Ec_Velocidad = sp.Eq((2*g*h + (k/m) * ((S - L)**2 - ((h**2 + S**2)**(1/2) - L)**2))**(1/2), V)

# Evaluaciones
# Hallar h limite
Hlim = sp.Eq((2*m*g*h)/k + (S-L)**2 , (((h**2 + S**2)**1/2 - L)**2))

# Evaluar el Vmax
# Hallar el h donde se da la Vmax
HVmax = sp.Eq((m*g) - (k * ((h**2 + S**2)**1/2 - L) * (h/((h**2 + S**2)**1/2))), 0)

# Valores constantes
m_val = 5
g_val = 9.81
k_val = 120
S_val = 1
L_val = 0.5

# Sustituyendo valores constantes en la ecuación de la velocidad
Ec_Velocidad_sub = Ec_Velocidad.subs({m: m_val, g: g_val, k: k_val, S: S_val, L: L_val})

# Resolviendo para V general en terminos de h
V_sol = sp.solve(Ec_Velocidad_sub, V)
print(f"Velocidad: {V_sol}")

# Resolviendo para el valor límite de h 
Hlim_sol = sp.solve(Hlim.subs({m: m_val, g: g_val, k: k_val, S: S_val, L: L_val}), h)
print(f"h límite: {Hlim_sol}")

# Resolviendo para h en el punto de Vmax
HVmax_sol = sp.solve(HVmax.subs({m: m_val, g: g_val, k: k_val, S: S_val, L: L_val}), h)
print(f"h para Vmax: {HVmax_sol}")

# Reemplazando h en la ecuación de velocidad para obtener Vmax
Vmax_sol = V_sol[0].subs(h, HVmax_sol[0])
print(f"Vmax: {Vmax_sol}")
