import sympy as sp

def AB(Vcc_value=None, Rl_value=None):
    # Definición de la función de potencia
    def potencia(Vcc=None, Rl=None):
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
        
        return resultados

    return potencia(Vcc=Vcc_value, Rl=Rl_value)

# Ejemplo de uso con valores numéricos
resultados_numericos = AB(10, 4)
print("Resultados con valores numéricos:")
for key, value in resultados_numericos.items():
    print(f"{key}: {value}")

# Ejemplo de uso sin valores numéricos (simbólicos)
resultados_simbolicos = AB()
print("\nResultados simbólicos:")
for key, value in resultados_simbolicos.items():
    print(f"{key}: {value}")
