import sympy as sp

# Define the symbols
C, R1, R2, R3, R4, A, w = sp.symbols('C R1 R2 R3 R4 A w')

omega_n = 1 / (C * sp.sqrt(R3 * R4))
Amort = C * (R3 + R4) / (2 * sp.sqrt(C**2 * R3 * R4))

# Given values
w_val = 62831 # in rad/s
A_val = 1  # unit not specified
C_val = 0.1e-6  # in Farads
R2_val = 5100  # in Ohms
R1_val = 5100  # in Ohms

# Define the equations to solve
eqn1 = sp.Eq(w, omega_n)
eqn2 = sp.Eq(A, Amort)

# Substitute the values into the equations
eqn1_subs = eqn1.subs({w: w_val, C: C_val, R2: R2_val, R1: R1_val})
eqn2_subs = eqn2.subs({A: A_val, C: C_val, R2: R2_val, R1: R1_val})

# Solve for R3 and R4
solutions = sp.solve([eqn1_subs, eqn2_subs], (R3, R4))
print("R3 R4",solutions)