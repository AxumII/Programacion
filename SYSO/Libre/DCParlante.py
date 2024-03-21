import sympy as sp

# Variables Simbólicas
Ir5, Ir4, Ir8, Vb1, Vce2, Vce3, Vbc4, Vcb3, Vec4, Vec1 = sp.symbols('Ir5 Ir4 Ir8 Vb1 Vce2 Vce3 Vbc4 Vcb3 Vec4 Vec1')

# Constantes
r1 = 33000
r2 = 33000
r6 = 4700
r4 = 680
r5 = 100
r8 = 820
Vdiod = 0.8
Vi = 18
#Vbe1 = 0.8
Vbe2 = 0.8
Vbe3 = 0.8
#Vbe4 = 0.8

def Sistema():
    # Sistema 
    eq1 = sp.Eq(Vec4 - Ir4*r4 - Vec1 - Ir8*r8, 0) #Se desconoce Vec1
    eq2 = sp.Eq(Ir8*r8, Vbe2) #Ayuda en 1
    
    eq3 = sp.Eq(Vi - Ir5*r5 - Vdiod - Vce2, 0) #Se desconoce Vce2
    
    eq4 = sp.Eq(Vi - Vce3 - Vec4, 0)
    
    eq5 = sp.Eq(Ir5*r5, Vcb3)
    eq6 = sp.Eq(Vcb3 + Vbe3, Vce3)
   
    

    # Solución
    solution = sp.solve((eq1, eq2, eq3, eq4, eq5, eq6), (Ir5, Ir4, Ir8, Vec1,  Vce2, Vce3, Vec4, Vcb3))

    return solution

resultado = Sistema()
print(resultado)

