import sympy as sp

# Definir símbolos
t, s = sp.symbols('t s')
R1, R2, C, L = sp.symbols('R1 R2 C L')
I1_s, I2_s = sp.symbols('I1_s I2_s')  # Corrientes de malla en el dominio de Laplace
Vi_s = sp.Function('Vi')(s)  # Entrada de voltaje en el dominio de Laplace

# Ecuación de malla 1 (contiene R1, capacitor y parte del generador Vi)
# -Vi(s) + I1_s * R1 + (I1_s - I2_s) / (s * C) = 0
eq_malla1 = sp.Eq(-Vi_s + I1_s * R1 + (I1_s - I2_s) / (s * C), 0)

# Ecuación de malla 2 (contiene resistencia R2 y el inductor L)
# (I2_s - I1_s) / (s * C) + I2_s * R2 + s * L * I2_s = 0
eq_malla2 = sp.Eq((I2_s - I1_s) / (s * C) + I2_s * R2 + s * L * I2_s, 0)

# Resolver el sistema de ecuaciones de mallas
sol_mallas = sp.solve([eq_malla1, eq_malla2], (I1_s, I2_s))
I1_sol, I2_sol = sol_mallas[I1_s], sol_mallas[I2_s]

# Mostrar las soluciones simbólicas de las corrientes de malla
print("Corriente de malla I1(s):")
sp.pprint(I1_sol)
print("\nCorriente de malla I2(s):")
sp.pprint(I2_sol)

# Voltaje en el inductor Vo(s) = L * s * I2(s)
Vo_s_inductor = L * s * I2_sol
print("\nVoltaje en el inductor Vo(s) por mallas:")
sp.pprint(Vo_s_inductor)

# Sustituir valores específicos en las soluciones
# R1 = 1 Ω, R2 = 5 Ω, C = 1/3 F, L = 1 H, Vi(s) = 1/s (entrada escalón)
valores = {R1: 1, R2: 5, C: 1/3, L: 1, Vi_s: 1/s}

Vo_s_inductor_val = Vo_s_inductor.subs(valores)

# Mostrar solución numérica de Vo(s)
print("\nVoltaje en el inductor Vo(s) con valores específicos:")
sp.pprint(Vo_s_inductor_val)

# Transformada inversa de Laplace para obtener Vo(t)
Vo_t_inductor = sp.inverse_laplace_transform(Vo_s_inductor_val, s, t)

print("\nVoltaje en el inductor Vo(t):")
sp.pprint(Vo_t_inductor)
