import sympy as sp

# Define the symbols
C, R1, R2, R3, A, w = sp.symbols('C R1 R2 R3 A w')

a = R1*R2*R3*C**2
b = 2*R2*R3*C
c = R2 + R3

eqn1 = sp.Eq(w, sp.sqrt((c) / (a)))
eqn2 = sp.Eq(A, (b/2)/sp.sqrt((a)*(c)) )


# Given values
w_val = 43982 # in R
A_val = 0.07036   # in ?
C_val = 0.1e-6  # in Farads
R2_val = 100 # in Ohms

# Substitute the values into the equations
eqn1_subs = eqn1.subs({w: w_val, C: C_val, R2: R2_val})
eqn2_subs = eqn2.subs({A: A_val, C: C_val, R2: R2_val})

# Solve for R1 and R3
solutions = sp.solve([eqn1_subs, eqn2_subs], (R1, R3))
print("R1 R3", solutions)

