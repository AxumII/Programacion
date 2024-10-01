import sympy as sp

# Definición de la función del amplificador
def AB():
    # Definición de la función de potencia
    def potencia(Vcc=None, Rl=None, Total_solve=False):
        # Definición de los símbolos necesarios
        Vcc_sym, Rl_sym = sp.symbols('Vcc Rl')
        
        # Usar valores numéricos si se proporcionan, de lo contrario usar símbolos
        Vcc = Vcc if Vcc is not None else Vcc_sym
        Rl = Rl if Rl is not None else Rl_sym
        
        # Potencia de la fuente DC
        Pvcc = (Vcc**2) / (2 * sp.pi * Rl)

        # Cálculo de Ic_prom
        Ic_prom = (Vcc / 2) / Rl

        # Potencia de salida de señal AC
        Pac = (Ic_prom**2 * Rl) / 2

        # Potencia disipada en el transistor Q1
        PQ1 = Pvcc - Pac

        # Eficiencia del amplificador
        ef = Pac / Pvcc

        # Corriente máxima
        Ic_max = Vcc / (sp.pi * Rl)

        # Potencia máxima disipada en el transistor Q1
        Pmax = (Vcc**2) / (4 * sp.pi**2 * Rl)
        
        # Diccionario con resultados
        resultados = {
            "Pvcc": Pvcc,
            "Ic_prom": Ic_prom,
            "Pac": Pac,
            "PQ1": PQ1,
            "ef": ef,
            "Ic_max": Ic_max,
            "Pmax": Pmax
        }
        
        # Evaluar numéricamente si Vcc y Rl no son simbólicos
        if not isinstance(Vcc, sp.Basic) and not isinstance(Rl, sp.Basic):
            resultados = {clave: float(expr) for clave, expr in resultados.items()}
        
        # Retornar resultados completos si Total_solve es True
        if Total_solve:
            return resultados
        else:
            # Retornar solo Ic_max si Total_solve es False
            return resultados["Ic_max"]

    # Definición de la función para cálculos DC
    def dc(Ic=None, B=None, Vcc=None, Is=None, Total_solve=False):
        # Parámetros constantes
        VT = 0.026  # Voltaje térmico en Voltios
        n = 1  # Factor de idealidad del diodo
        
        # Definir símbolos si no se proporcionan valores
        Vcc_sym, Vb_sym, R2_sym, Id_sym, Vd_sym = sp.symbols('Vcc Vb R2 Id Vd')
        
        # Asignar valores de entrada o usar símbolos
        Ic = Ic if Ic is not None else sp.symbols('Ic')
        B = B if B is not None else sp.symbols('B')
        Vcc = Vcc if Vcc is not None else Vcc_sym
        Is = Is if Is is not None else sp.symbols('Is')
        
        # Corriente base
        Ib = Ic / B
        
        # Definir resistencia del emisor
        Re = VT / Ic
        
        # Ecuación del diodo real
        VD = Vd_sym
        Id = Is * (sp.exp(VD / (n * VT)) - 1)
        
        # Resistencia del diodo
        Rd = VD / Id

        # Ecuaciones basadas en la imagen proporcionada
        Vcc_expr = 2 * Ib * R2_sym + 2 * VD
        Id_expr = (Vcc - Vb_sym) / R2_sym + Ib
        R2_expr = (Vcc / 2 - VD - Vb_sym) / Ib
        Vb_expr = Ib * (Re + R2_sym) * B
        
        # Crear diccionario de resultados
        resultados = {
            "Vcc": Vcc_expr,
            "Id": Id_expr,
            "R2": R2_expr,
            "Vb": Vb_expr,
            "Rd": Rd
        }
        
        # Sustituir valores numéricos si se proporcionan
        if all([valor is not None for valor in [Ic, B, Vcc, Is]]):
            resultados_num = {clave: expr.subs({sp.symbols('Ic'): Ic, sp.symbols('B'): B, 
                                                sp.symbols('Vcc'): Vcc, sp.symbols('Is'): Is}).evalf() 
                              for clave, expr in resultados.items()}
            
            if Total_solve:
                return resultados_num
            else:
                return resultados_num["Rd"]
        else:
            if Total_solve:
                return resultados
            else:
                return resultados["Rd"]

    return potencia, dc

# Ejemplo de uso
potencia, dc = AB()

resultados_dc = dc(Ic=0.02, B=100, Vcc=12, Is=1e-12, Total_solve=True)

# Imprimir resultados
for key, value in resultados_dc.items():
    print(f"{key}: {value}")
