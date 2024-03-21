from sympy import symbols, solve, I

# Defining the variable
s = symbols('s')

# Defining the transfer functions H3 and H4
H3 = -0.2 * s / (0.0002 * s**2 + 0.2 * s + 10100)
H4 = (5.508e-5 * s**2 - 0.0408000000000001 * s + 5100) / (5100 * (1.08e-8 * s**2 + 0.000208 * s + 1))

# Calculating the poles for H3 and H4
poles_H3 = solve(H3.as_numer_denom()[1], s)
poles_H4 = solve(H4.as_numer_denom()[1], s)

# Extracting the damping coefficients from the poles
# The damping coefficient for a complex pole is -Real(Pole)/|Pole|
damping_coefficients_H3 = [-pole.as_real_imag()[0]/abs(pole) for pole in poles_H3 if (pole) != 0]
damping_coefficients_H4 = [-pole.as_real_imag()[0]/abs(pole) for pole in poles_H4 if (pole) != 0]

print(damping_coefficients_H3, damping_coefficients_H4)

