import sympy as sp


def Calculo():
    def derivadas():
        x, y = sp.symbols('x y')
        f = x**2 * sp.sin(y)
        print("\n🔹 Derivadas parciales:")
        print("∂f/∂x =")
        sp.pprint(sp.diff(f, x))
        print("∂f/∂y =")
        sp.pprint(sp.diff(f, y))

    def integrales():
        x = sp.Symbol('x')
        print("\n🔹 Integral indefinida de x^2 * e^x:")
        sp.pprint(sp.integrate(x**2 * sp.exp(x), x))

        print("\n🔹 Integral definida de x^2 de 0 a 2:")
        sp.pprint(sp.integrate(x**2, (x, 0, 2)))

    def calcular_limite():
        x = sp.Symbol('x')
        print("\n🔹 Límite de sin(x)/x cuando x → 0:")
        sp.pprint(sp.limit(sp.sin(x)/x, x, 0))

    def resolver_ecuacion_diferencial():
        t = sp.Symbol('t')
        f = sp.Function('f')
        diffeq = sp.Eq(f(t).diff(t, t) - 4*f(t), 0)
        print("\n🔹 Solución de la ecuación diferencial:")
        sp.pprint(sp.dsolve(diffeq, f(t)))

    # Ejecutar funciones
    derivadas()
    integrales()
    calcular_limite()
    resolver_ecuacion_diferencial()


def S_Ec():
    def sistemanxn(**valores):
        var1, var2, var3 = sp.symbols('var1 var2 var3')
        a, b, c, d = sp.symbols('a b c d')

        ecuaciones = [
            var1 * a + (var2**2 + c) * 0.5 + var3 * var2 * b / d,
            var1 + var2 * d,
            var3 - (c / b) * var2 + var1
        ]

        ecuaciones_sustituidas = [ec.subs(valores) for ec in ecuaciones]

        print("\n🔹 Sistema de ecuaciones con sustituciones:")
        sp.pprint(ecuaciones_sustituidas)

        solucion = sp.solve(ecuaciones_sustituidas, (var1, var2, var3), dict=True)

        if solucion:
            print("\n✅ Solución del sistema:")
            sp.pprint(solucion)
        else:
            print("\n⚠️ No se pudo encontrar una solución exacta.")

    def eq(**valores):
        var1, a = sp.symbols('var1 a')
        ec = var1 - var1**2 + a * var1

        ec_sustituida = ec.subs(valores)

        print("\n🔹 Ecuación con sustituciones:")
        sp.pprint(ec_sustituida)

    def expandir_factorizar():
        x, y = sp.symbols('x y')
        expr = (x + y)**3
        print("\n🔹 Expansión:")
        sp.pprint(sp.expand(expr))

        print("\n🔹 Factorización:")
        sp.pprint(sp.factor(sp.expand(expr)))

    def resolver_ecuacion():
        x = sp.Symbol('x')
        eq = x**2 - 5*x + 6
        print("\n🔹 Soluciones de la ecuación:")
        sp.pprint(sp.solve(eq, x))

    def resolver_sistema():
        x, y = sp.symbols('x y')
        eq1 = x + y - 2
        eq2 = x**2 + y**2 - 4
        print("\n🔹 Solución del sistema no lineal:")
        sp.pprint(sp.solve((eq1, eq2), (x, y)))

    def simplificar_expresion():
        x = sp.Symbol('x')
        expr = (x**2 - 1) / (x - 1)
        print("\n🔹 Expresión simplificada:")
        sp.pprint(sp.simplify(expr))

    # Ejecutar todas las funciones internas
    sistemanxn(a=1, b=2, c=3, d=1)
    eq(var1=2, a=1)
    expandir_factorizar()
    resolver_ecuacion()
    resolver_sistema()
    simplificar_expresion()


def A_S():
    # Variables de tiempo y frecuencia
    t, s, w, n, z = sp.symbols('t s w n z', real=True)
    f = sp.Function('f')

    # 🔷 Transformada de Fourier (tiempo continuo)
    expr_ft = sp.exp(-t) * sp.Heaviside(t)
    fourier_trans = sp.fourier_transform(expr_ft, t, w)
    print("\n🔹 Fourier (tiempo continuo):")
    print("f(t) = e^(-t)·u(t)")
    sp.pprint(fourier_trans)

    # 🔷 Transformada de Fourier (tiempo discreto - DTFT)
    expr_dft = sp.Pow(0.5, n) * sp.Heaviside(n)
    dtft = sp.summation(expr_dft * sp.exp(-sp.I * w * n), (n, 0, sp.oo))
    print("\n🔹 Fourier Discreta (DTFT):")
    print("x[n] = (0.5)^n·u[n]")
    sp.pprint(dtft)

    # 🔷 Transformada de Laplace (tiempo continuo)
    expr_lap = sp.exp(-2*t) * sp.Heaviside(t)
    laplace = sp.laplace_transform(expr_lap, t, s, noconds=True)
    print("\n🔹 Laplace (tiempo continuo):")
    print("f(t) = e^(-2t)·u(t)")
    sp.pprint(laplace)

    # 🔷 Transformada Z (tiempo discreto)
    expr_z = sp.Pow(0.7, n) * sp.Heaviside(n)
    z_trans = sp.summation(expr_z * z**(-n), (n, 0, sp.oo))
    print("\n🔹 Transformada Z:")
    print("x[n] = (0.7)^n·u[n]")
    sp.pprint(z_trans)


# 🟢 LLAMADAS FINALES PARA QUE TODO SE EJECUTE
A_S()
Calculo()
S_Ec()
