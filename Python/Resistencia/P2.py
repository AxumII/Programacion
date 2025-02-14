import sympy as sp

class P2:
    def __init__(self, d=None, G=None, Tao_max=None, L1=None, L2=None, T=None, rEng1=None, rEng2=None):
        # Asignar variables iniciales con valores simbólicos si no se proporcionan
        self.d = d if d is not None else sp.Symbol('d')
        self.G = G if G is not None else sp.Symbol('G')
        self.Tao_max = Tao_max if Tao_max is not None else sp.Symbol('Tao_max')
        self.L1 = L1 if L1 is not None else sp.Symbol('L1')
        self.L2 = L2 if L2 is not None else sp.Symbol('L2')
        self.T = T if T is not None else sp.Symbol('T')
        self.rEng1 = rEng1 if rEng1 is not None else sp.Symbol('rEng1')
        self.rEng2 = rEng2 if rEng2 is not None else sp.Symbol('rEng2')

    def calcular_simbolico(self):
        # Definir símbolos
        d, G, Tao_max, L1, L2, T, Tc, Te, rEng1, rEng2 = sp.symbols('d G Tao_max L1 L2 T Tc Te rEng1 rEng2')
        
        # Definir constantes geométricas
        b = 2.5 * d
        c1, c2 = 0.208, 0.1406
        rab = 2 * d / 2
        rbc = d / 2

        # Momentos de inercia
        Jab = (1 / 2) * sp.pi * rab**4
        Jbc = (1 / 2) * sp.pi * rbc**4

        # Ángulos de torsión
        theta_ab = (T * L1) / (Jab * G)
        theta_bc = (Tc * L2) / (Jbc * G)
        theta_de = (Te * L2) / (c2 * b**4 * G)
        
        
        #Hiperestaticidad
        Solucion = sp.linsolve([T - Te*(rEng1 / rEng2) - Tc , theta_bc*rEng1 - theta_de*rEng2 ],(Tc, Te))
        S1,S2 = Solucion
        
       #Falta abstraer terminos y ya resolver ya que eso resuelve la hiperestaticidad y lo demas ya es solo reemplazar
        
        # Ángulo total
         
        theta_a = theta_de * (rEng1 / rEng2) + theta_ab 
        theta_a2 = theta_bc + theta_ab

        # Esfuerzos cortantes
        tao_ab = (T * rab) / Jab
        tao_bc = (Tc * rbc) / Jbc
        tao_de = (Te /(c1*b**3) )

        # Factores de seguridad
        FS_ab = Tao_max / tao_ab
        FS_bc = Tao_max / tao_bc
        FS_de = Tao_max / tao_de

        

        
        

        # Resultados simbólicos
        

        return {
            'Momento polar de inercia AB (Jab)': Jab,
            'Momento polar de inercia BC (Jbc)': Jbc,            
            'Factor de seguridad en AB (FS_ab)': FS_ab,
            'Factor de seguridad en BC (FS_bc)': FS_bc,
            'Factor de seguridad en DE (FS_de)': FS_de,
            'Esfuerzo cortante en AB (tao_ab)': tao_ab,
            'Esfuerzo cortante en BC (tao_bc)': tao_bc,
            'Esfuerzo cortante en DE (tao_de)': tao_de,
            'Ángulo de torsión en A camino 1(theta_a)': theta_a,
            'Ángulo de torsión en A camino 2(theta_a)': theta_a2
        }

    def calcular_numerico(self):
        # Obtener resultados simbólicos
        resultados_simbolicos = self.calcular_simbolico()

        # Crear sustituciones
        sustituciones = {
            sp.Symbol('d'): self.d,
            sp.Symbol('G'): self.G,
            sp.Symbol('Tao_max'): self.Tao_max,
            sp.Symbol('L1'): self.L1,
            sp.Symbol('L2'): self.L2,
            sp.Symbol('T'): self.T,
            sp.Symbol('rEng1'): self.rEng1,
            sp.Symbol('rEng2'): self.rEng2,
            sp.pi: 3.141592653589793  # Sustituir pi por su valor numérico
        }

        # Evaluar resultados numéricos
        resultados_numericos = {}
        for key, expr in resultados_simbolicos.items():
            valor = expr.subs(sustituciones)
            resultados_numericos[key] = valor.evalf() if valor.free_symbols == set() else valor

        return resultados_numericos

# Crear instancia de la clase y calcular resultados
modelo = P2(d=0.05, G=206e9, Tao_max=82e6, T = 2000, L1=1, L2=2, rEng1=0.3, rEng2=0.3)
resultados_simbolicos = modelo.calcular_simbolico()
print("Resultados Simbólicos:")
for key, value in resultados_simbolicos.items():
    print(f"{key}: {value}")

resultados_numericos = modelo.calcular_numerico()
print("\nResultados Numéricos:")
for key, value in resultados_numericos.items():
    
    print(f"{key}: {value}")
