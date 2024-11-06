import numpy as np
import sympy as sp

def poleas1():
    t = sp.symbols('t')
    l = sp.symbols('l')
    var_rb, var_vb, var_ab = sp.symbols('var_rb var_vb var_ab')
    
    ra = 8 + (3/2) * t**2 - (3/16) * t**3
    rc = 12 + (4/3) * t**2
    
    va = sp.diff(ra, t)
    vc = sp.diff(rc, t)
    
    aa = sp.diff(va, t)
    ac = sp.diff(vc, t)
    
    # Definir las ecuaciones de la distancia, velocidad y aceleración
    dist = sp.Eq(2 * ra + 2 * var_rb + rc, l)
    rb = sp.solve(dist, var_rb)[0]
    print("Distancia rb:", rb)
    
    vel = sp.Eq(2 * va + 2 * var_vb + vc, 0)
    vb = sp.solve(vel, var_vb)[0]
    print("Velocidad vb:", vb)
    
    acc = sp.Eq(2 * aa + 2 * var_ab + ac, 0)
    ab = sp.solve(acc, var_ab)[0]
    print("Aceleración ab:", ab)  
    
    # Evaluar para t = 0.6
    t_val = 0.6
    rb_eval = rb.subs(t, t_val)
    vb_eval = vb.subs(t, t_val)
    ab_eval = ab.subs(t, t_val)
    
    print(f"\nEvaluación para t = {t_val}:")
    print("rb =", rb_eval)
    print("vb =", vb_eval)
    print("ab =", ab_eval)
    
poleas1()
