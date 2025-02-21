import sympy as sp
import sympy.plotting as syp
import numpy as np

# ------------------------ SISTEMA DE ECUACIONES ------------------------

def sistemanxn(**valores):
    """
    Resuelve un sistema de 3 ecuaciones con 3 incógnitas.
    Permite sustitución parcial y deja las soluciones en función de los símbolos restantes.
    """
    var1, var2, var3 = sp.symbols('var1 var2 var3')
    a, b, c, d = sp.symbols('a b c d')

    ecuaciones = [
        var1 * a + (var2**2 + c) * 0.5 + var3 * var2 * b / d,
        var1 + var2 * d,
        var3 - (c / b) * var2 + var1
    ]

    # Sustituir solo los valores proporcionados sin afectar los demás símbolos
    ecuaciones_sustituidas = [ec.subs(valores) for ec in ecuaciones]

    print("\n🔹 Sistema de ecuaciones con sustituciones:")
    sp.pprint(ecuaciones_sustituidas)

    # Intentar resolver el sistema con los valores dados
    solucion = sp.solve(ecuaciones_sustituidas, (var1, var2, var3), dict=True)

    if solucion:
        print("\n✅ Solución del sistema:")
        sp.pprint(solucion)
    else:
        print("\n⚠️ No se pudo encontrar una solución exacta.")

def eq(**valores):
    """
    Evalúa una ecuación con la sustitución de valores proporcionados.
    Permite evaluaciones parciales sin necesidad de todos los valores.
    """
    var1, a = sp.symbols('var1 a')
    ec = var1 - var1**2 + a * var1  # Definir la ecuación original

    # Sustituir solo los valores proporcionados
    ec_sustituida = ec.subs(valores)

    print("\n🔹 Ecuación con sustituciones:")
    sp.pprint(ec_sustituida)

# ------------------------ CÁLCULO SIMBÓLICO ------------------------

def derivadas():
    x, y = sp.symbols('x y')
    f = x**2 * sp.sin(y)
    print("\nDerivadas parciales:")
    sp.pprint(sp.diff(f, x))
    sp.pprint(sp.diff(f, y))

def integrales():
    x = sp.Symbol('x')
    print("\nIntegral indefinida:")
    sp.pprint(sp.integrate(x**2 * sp.exp(x), x))

    print("\nIntegral definida de 0 a 2:")
    sp.pprint(sp.integrate(x**2, (x, 0, 2)))

def expandir_factorizar():
    x, y = sp.symbols('x y')
    expr = (x + y)**3
    print("\nExpansión:")
    sp.pprint(sp.expand(expr))

    print("\nFactorización:")
    sp.pprint(sp.factor(sp.expand(expr)))

def resolver_ecuacion():
    x = sp.Symbol('x')
    eq = x**2 - 5*x + 6
    print("\nSoluciones de la ecuación:")
    sp.pprint(sp.solve(eq, x))

def resolver_sistema():
    x, y = sp.symbols('x y')
    eq1 = x + y - 2
    eq2 = x**2 + y**2 - 4
    print("\nSolución del sistema:")
    sp.pprint(sp.solve((eq1, eq2), (x, y)))

def serie_taylor():
    x = sp.Symbol('x')
    f = sp.sin(x)
    print("\nSerie de Taylor hasta grado 6:")
    sp.pprint(sp.series(f, x, 0, 6))

def calcular_limite():
    x = sp.Symbol('x')
    print("\nLímite cuando x → 0:")
    sp.pprint(sp.limit(sp.sin(x)/x, x, 0))

def transformada_laplace():
    t, s = sp.symbols('t s')
    f = sp.exp(-t) * sp.sin(t)
    print("\nTransformada de Laplace:")
    sp.pprint(sp.laplace_transform(f, t, s))

def resolver_ecuacion_diferencial():
    t = sp.Symbol('t')
    f = sp.Function('f')
    diffeq = sp.Eq(f(t).diff(t, t) - 4*f(t), 0)
    print("\nSolución de la ecuación diferencial:")
    sp.pprint(sp.dsolve(diffeq, f(t)))

def simplificar_expresion():
    x = sp.Symbol('x')
    expr = (x**2 - 1) / (x - 1)
    print("\nExpresión simplificada:")
    sp.pprint(sp.simplify(expr))

def sympy_to_numpy(expr, var):
    """
    Convierte una expresión de SymPy a una función compatible con NumPy.

    :param expr: Expresión de SymPy a convertir.
    :param var: Variable simbólica de la expresión.
    :return: Función evaluable en NumPy.
    """
    return sp.lambdify(var, expr, modules=["numpy"])

def plotting():
    x = sp.Symbol('x')  # Definir variable simbólica
    expr1 = x**2 - 4  # Primera función
    expr2 = x**3 - x  # Segunda función para comparación

    # Generar gráfico con configuración corregida
    syp.plot(
        (expr1, (x, -3, 3), {"line_color": "red", "markers": [(-2, 0), (2, 0)], "nb_of_points": 1000}),  # Expresión 1
        (expr2, (x, -3, 3), {"line_color": "blue"}),  # Expresión 2
        title="Ejemplo de Configuración en SymPy",
        xlabel="Eje X",
        ylabel="Eje Y",
        legend=True
    )

# ------------------------ LLAMADA A FUNCIONES ------------------------

# Llamadas a los métodos iniciales
sistemanxn(c=4, a=2)  # Sustitución parcial en el sistema
eq(var1=2)  # Sustitución parcial en la ecuación

# Llamadas a métodos de cálculo simbólico
derivadas()
integrales()
expandir_factorizar()
resolver_ecuacion()
resolver_sistema()
serie_taylor()
calcular_limite()
transformada_laplace()
resolver_ecuacion_diferencial()
simplificar_expresion()

# Llamada al método SymPy a NumPy
x = sp.Symbol('x')
expr = sp.sin(x) + x**2  # Expresión simbólica
numpy_func = sympy_to_numpy(expr, x)  # Convertir a función de NumPy

# Evaluar en un array de NumPy
x_vals = np.linspace(-2, 2, 5)  # Valores de prueba en [-2, 2]
y_vals = numpy_func(x_vals)

print("\n🔹 Valores de entrada:", x_vals)
print("🔹 Valores evaluados:", y_vals)

# Llamar a la función de graficación
plotting()
