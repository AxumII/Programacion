import sympy as sp

def RAB(Rf, R, B, Rl):
    # Si se pasa una variable simbólica, sustituir por los valores numéricos.
    if isinstance(Rf, sp.Basic) or isinstance(R, sp.Basic) or isinstance(B, sp.Basic) or isinstance(Rl, sp.Basic):
        # Definir las variables simbólicas y sustituir con los valores numéricos
        Rf_sym, R_sym, B_sym, Rl_sym = sp.symbols('Rf R B Rl')
        expr = 1 / (1 / (Rf_sym + R_sym) + 1 / (Rf_sym + 1 / (1 / R_sym + 1 / (B_sym * Rl_sym))))
        return expr.subs({Rf_sym: Rf, R_sym: R, B_sym: B, Rl_sym: Rl})
    else:
        # Si todos son numéricos, calcular directamente
        parallel_inner = 1 / ((1 / R) + (1 / (B * Rl)))
        sum_inner = Rf + parallel_inner
        Z_i = 1 / (1 / (Rf + R) + 1 / sum_inner)
        return Z_i

def A():
    def analisis(Av=None, B=None, Rl=None, Rc=None, Icq=None, Rlp=None, Vcc=None):
        # Definir las variables simbólicas
        Av_sym, B_sym, Rl_sym, Rc_sym, Icq_sym, Vcc_sym, Re_sym, Ic_sym, Vce_sym, R1_sym, R2_sym, Vb_sym, Vbe_sym = sp.symbols('Av B Rl Rc Icq Vcc Re Ic Vce R1 R2 Vb Vbe')
        
        # Asignar valores por defecto a variables simbólicas
        Av = Av if Av is not None else Av_sym
        B = B if B is not None else B_sym
        Rl = Rl if Rl is not None else Rl_sym
        Rc = Rc if Rc is not None else Rc_sym
        Icq = Icq if Icq is not None else Icq_sym
        Vbe = 0.7  # Voltaje base-emisor típico para un transistor
        Vcc = Vcc if Vcc is not None else 12  # Voltaje de la fuente


        # Constantes
        VT = 0.026  # Voltaje Térmico en voltios

        ########### Análisis AC #############################
        # IEq (Corriente del emisor en DC)
        Ieq = Icq * (1 + (1 / B))

        # re, resistencia interna del transistor en el emisor
        re = VT / Ieq

        # Verificar que Rlp esté definido
        if Rlp is None:
            raise ValueError("Rlp no está definido. Debes proporcionarlo como argumento.")
        
        # Re, Resistencia del Emisor
        Re = ((1 / ((1 / Rc) + (1 / Rlp))) / Av) + re

        ########### Análisis DC #############################
        #Apendice actual para analizar resistencias 
        # a. Rac, resistencia AC equivalente
        Rac = (1 / (1 / Rc + 1 / Rlp)) + Re

        # b. Rdc, resistencia DC
        Rdc = Rc + Re



        #1 Criterio de Diseño de punto centrado VCE
        Vce = Vcc / 2

        #2 Hallar Ic en ese VCE
        # Ecuación General para hallar Ic en términos de Vcc
        Vcc_eq = sp.Eq(Vcc, Rc * Ic_sym + Vce + Re * Ic_sym * (1 + (1 / B))) 
        Ic_sol = sp.solve(Vcc_eq, Ic_sym)[0]

        #3 Criterio de Diseño de estabilidad Rth(Rb) y Re
        Rth = 0.1*B*Re

        #4 Determinar Ib
        Ib = Ic_sol/B

        #5 Hallar Vb
        Vb = Rth*Ib + 0.7 + Re*Ic_sol*(1 + (1 / B)) 

        #6 Hallar R1 y R2
        R1 = (Vcc * Rth) / Vb
        R2 = Rth / ((1 - (Vb / Vcc)))

        # Retornar los valores solicitados
        return {
            'R1': R1,
            'R2': R2,
            'Vcc': Vcc,
            'Re': Re,
            'Rac': Rac,
            'Rdc': Rdc,
            'Ic_eq': Ic_sol,  # Valor simbólico de Ic hallado
            'Vce': Vce,  # Voltaje Vce calculado
            'Rth': Rth,  # Resistencia de Thevenin calculada
            'Vb': Vb,  # Voltaje en el nodo base
            'Ib': Ib   # Corriente de base calculada
        }
    
    return analisis








# Ejemplo de uso de la función A
Rf = 20
R = 2200
B = 70
Rl = 8
Vcc = 12  # Voltaje de la fuente

# Calcular Rlp usando la función RAB
Rlp_valor = RAB(Rf=Rf, R=R, B=B, Rl=Rl)

# Evaluar la expresión si es simbólica, si no, no usar evalf
if isinstance(Rlp_valor, sp.Basic):
    Rlp_valor = Rlp_valor.evalf()
print(f"Rlp: {Rlp_valor}")

# Usar el valor calculado de Rlp en la función analisis
analisis = A()
resultados = analisis(Av=25, B=B, Rl=Rl, Rc=500, Icq=0.001, Rlp=Rlp_valor, Vcc=Vcc)

# Imprimir los resultados
for key, value in resultados.items():
    # Evaluar solo si el valor es simbólico
    if isinstance(value, sp.Basic):
        print(f"{key}: {value.evalf()}")
    else:
        print(f"{key}: {value}")
