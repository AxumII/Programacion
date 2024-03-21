import sympy as sp
import numpy as np



def opb():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    suma = a + b
    resta = a - b
    producto = a * b
    division = a / b
    print(suma, resta, producto, division)

def deriv():
    x, y, z = sp.symbols('x y z')#las define como variables

    #derivada basica de primer orden
    dv1 = sp.diff(sp.cos(x),x)
    #derivada basica de n orden
    n = 2
    dv2 = sp.diff(sp.cos(x),x,n)
    #derivada en varias variables, se ponen despues de la expresion las variables con las que se desea derivar
    dv3 = sp.diff((y**4)*sp.cos(x),x,y)
    #esta forma no la evalua pero no se si esta bien escrita
    dv4 = sp.Derivative((y**4)*sp.cos(x),x,y)
    
    print(dv1)
    print(dv2)
    print(dv3)
    print(dv4)
    
def integ():
    x, y, z = sp.symbols('x y z')#las define como variables   
    
    #integral basica indefinida
    i1 = sp.integrate(x**2,x)
    #integral basica definida
    i2 = sp.integrate(x**2,(x,0,50))
    #integral iterada de varias variables e impropia
    i3 = sp.integrate(x*(y**2)*sp.exp(-x), (x, 1, sp.oo), (y, 0, 5))
    
    print(i1)
    print(i2)
    print(i3)
    
def edo():
    print("aca van algunas EDO, no estan todas, solo lo comun en problemas del dia a dia")
    
    def solve_separable():
        #Caso comun 1. Separable
        """ dy/dx = x*y """   
        
        # Declarar las variables    
        x = sp.symbols('x')
        y = sp.Function('y')(x)
        # Definir la EDO: Primero se define la funcion y en diff la independiente, luego se pone el termino a resolver
        edo = sp.Eq(y.diff(x), x**2 * y)
        # Resolver la EDO
        sol = sp.dsolve(edo, y) #requiere dos parametros, la edo y la dependiente
        # Mostrar la solución general
        print("Solución general:", sol)
        
        #Para poner condiciones iniciales se añade un parametro en estos casos simples
        sol = sp.dsolve(edo, y, ics={y.subs(x, 0): 1}) #y(O) = 1 es la condicion inicial
        print("Solución con condiciones iniciales:", sol)
    
    def solve_linear_second_order():
        #Caso 2 comun. Lineales
        """Caso segundo orden:          y′′(x)  +  2y′(x)  +  y(x)  =  x """
        #este software resuelve facilmente tanto homogeneas como no homogeneas
        
        # Declarar las variables
        x = sp.symbols('x')    
        y = sp.Function('y')(x)
        # Definir la EDO
        edo = y.diff(x, x) + 2*y.diff(x) + y - x
        # Resolver la EDO
        sol = sp.dsolve(edo, y)
        # Mostrar la solución general
        print("Solución general:", sol)
        """Condiciones iniciales:    y(0)=1     y′(0)=0"""
        #para poner condiciones iniciales aca requiere indicar mas especificamente en un tercer argumento llamado ics
        #ics contiene las n condiciones iniciales, aunque aca seran dos
        #ics es un diccionario que guarda como valor la condicion y la key como el valor de la condicion
        #y.subs(x,0): 1              es la condicion inicial y(0) = 1
        #y.diff(x).subs(x, 0): 0     es la condicion inicial de y'(0) = 0       
        sol = sp.dsolve(edo, y, ics={y.subs(x, 0): 1, y.diff(x).subs(x, 0): 0})
        # Mostrar la solución particular con las condiciones iniciales
        print("Solución particular:", sol)      
    
    def solve_linear_third_order():
        """Caso tercer orden     y′′′ (x) −  3y′′(x) +   3y′(x)  −  y(x)  =  e^x   """
        #aca aplican cosas para n orden
        # Declarar las variables
        x = sp.symbols('x')    
        y = sp.Function('y')(x)
        # Definir la EDO
        edo = y.diff(x, x, x) - 3*y.diff(x, x) + 3*y.diff(x) - y - sp.exp(x)
        # Resolver la EDO
        sol = sp.dsolve(edo, y)
        # Mostrar la solución general
        print("Solución general:", sol)
        """Condiciones iniciales: y(0)=1, y′(0)=2,  y′′(0)=3 """         
        # en este caso se pone solo un parametro mas en el diff de 2 orden en la condicion inicial
        sol = sp.dsolve(edo, y, ics={y.subs(x, 0): 1, y.diff(x).subs(x, 0): 2, y.diff(x, 2).subs(x, 0): 3})
        # Mostrar la solución particular con las condiciones iniciales
        print("Solución particular con condiciones iniciales:", sol) 
        
    def solve_cauchy_euler():
        """Ejemplo Cauchy Euler  "x^3 y''''(x) + 3x^2 y'''(x) - 6xy''(x) + 6y'(x) - 6y(x) = 0" """
        # Declarar las variables
        x = sp.symbols('x')    
        y = sp.Function('y')(x)    
        # Definir la EDO de Cauchy-Euler de cuarto grado
        edo = x**3 * y.diff(x, x, x, x) + 3 * x**2 * y.diff(x, x, x) - 6 * x * y.diff(x, x) + 6 * y.diff(x) - 6 * y
        # Resolver la EDO
        sol = sp.dsolve(edo, y)
        # Mostrar la solución general
        print("Solución general:", sol)    
        """Condiciones Iniciales y(1) = 1, y'(1) = 2, y''(1) = 3, y'''(1) = 4"""    
        # Resolver la EDO con condiciones iniciales y(1) = 1, y'(1) = 2, y''(1) = 3, y'''(1) = 4
        sol = sp.dsolve(edo, y, ics={y.subs(x, 1): 1, y.diff(x).subs(x, 1): 2, y.diff(x, x).subs(x, 1): 3, y.diff(x, x, x).subs(x, 1): 4})
        # Mostrar la solución particular con las condiciones iniciales
        print("Solución particular con condiciones iniciales:", sol)
        
    def wronskian():
        #consiste en una matriz nxn donde verticalmente estan las funciones de soluciones y horizontalmente la n derivada
        #permite determinar si son soluciones LI o LD y asi saber si faltan soluciones, ademas de ser util para operar con su determinante y no tener que usar todas las soluciones

        print("Ejemplo 1:         x,x**2,x**3")       
        # Declarar la variable
        x = sp.symbols('x')
        # Declarar las funciones
        f1 = x
        f2 = x**2
        f3 = x**3
        # Calcular el Wronskiano
        wronskian = sp.wronskian([f1, f2, f3], x)
        # Mostrar el Wronskiano
        print("Wronskiano:", wronskian)     
        # Comprobar si el Wronskiano es no nulo en x = 0     
        if wronskian != 0:            
            print("Las funciones son linealmente independientes.")
        else:
            print("Las funciones son linealmente dependientes.")            
            
        print("Ejemplo 2:    x,x**2,2*x")       
        # Declarar las funciones
        g1 = x
        g2 = x**2
        g3 = 2*x
        # Calcular el Wronskiano
        wronskian = sp.wronskian([g1, g2, g3], x)
        
        # Mostrar el Wronskiano
        print("Wronskiano:", wronskian)
        # Comprobar si el Wronskiano es no nulo en x = 0
        if wronskian != 0:
            print("Las funciones son linealmente independientes.")
        else:
            print("Las funciones son linealmente dependientes.")
            
    def solve_edo_systems():
        
        """
        Primero que todo es necesario poner al sistema de EDO en su forma normal (Todo sistema se expresa de esta forma)
        https://www.youtube.com/watch?v=GC47SD5bIPU&list=PL9SnRnlzoyX2AdKEvB0yIfkSEuCuQr4AK&index=3
        
        Ya con esto es posible evaluar los distintos casos
        """        
        
        def caso1():
            """
            Caso 1: Sistema lineal homogéneo
            x' = 2x + y
            y' = -x + 3y
            """
            print("Caso 1: Sistema lineal homogéneo")            
            # Declarar las variables
            t = sp.symbols('t')            
            # Declarar las funciones x(t) y y(t)
            x = sp.Function('x')(t)
            y = sp.Function('y')(t)            
            # Definir las EDOs
            edo1 = sp.Eq(x.diff(t), 2*x + y)
            edo2 = sp.Eq(y.diff(t), -x + 3*y)            
            # Resolver el sistema
            sol = sp.dsolve([edo1, edo2])            
            # Mostrar la solución general del sistema
            print("Solución general del sistema:")
            print(sol)

        def caso2():
            """
            Caso 2: Sistema lineal no homogéneo
            x' = 2x + y + e^t
            y' = -x + 3y - sin(t)
            """
            print("\nCaso 2: Sistema lineal no homogéneo")            
            # Declarar las variables
            t = sp.symbols('t')            
            # Declarar las funciones x(t) y y(t)
            x = sp.Function('x')(t)
            y = sp.Function('y')(t)            
            # Definir las EDOs
            edo1 = sp.Eq(x.diff(t), 2*x + y + sp.exp(t))
            edo2 = sp.Eq(y.diff(t), -x + 3*y - sp.sin(t))            
            # Resolver el sistema
            sol = sp.dsolve([edo1, edo2])            
            # Mostrar la solución general del sistema
            print("Solución general del sistema:")
            print(sol)

       
            
        def caso1_con_iniciales():
            """
            Caso 1 con condiciones iniciales
            x(0) = 1, y(0) = 2
            """
            print("\nCaso 1 con condiciones iniciales")
            
            t = sp.symbols('t')
            x = sp.Function('x')(t)
            y = sp.Function('y')(t)
            
            edo1 = sp.Eq(x.diff(t), 2*x + y)
            edo2 = sp.Eq(y.diff(t), -x + 3*y)
            
            # Condiciones iniciales
            condiciones_iniciales = {x.subs(t, 0): 1, y.subs(t, 0): 2}
            
            sol = sp.dsolve([edo1, edo2], ics=condiciones_iniciales)
            print("Solución con condiciones iniciales:")
            print(sol)  
            
            
        def caso2_con_iniciales():
            """
            Caso 2 con condiciones iniciales
            x(0) = 1, y(0) = 2
            """
            print("\nCaso 2 con condiciones iniciales")
            
            t = sp.symbols('t')
            x = sp.Function('x')(t)
            y = sp.Function('y')(t)
            
            edo1 = sp.Eq(x.diff(t), 2*x + y + sp.exp(t))
            edo2 = sp.Eq(y.diff(t), -x + 3*y - sp.sin(t))
            
            # Condiciones iniciales
            condiciones_iniciales = {x.subs(t, 0): 1, y.subs(t, 0): 2}
            
            sol = sp.dsolve([edo1, edo2], ics=condiciones_iniciales)
            print("Solución con condiciones iniciales:")
            print(sol)

        
            
            
            

        caso1()
        caso2()        
        caso1_con_iniciales()
        caso2_con_iniciales()
        

    
            
    #############################################################
    
def laplaceT():
    #Tambien se puede hacer transformadas de laplace y todo lo que conlleva  
    s, t = sp.symbols('s t')
    
    def laplace1():
        #aca realiza la transformada de 
        print("f(t) = e^(-2t) * cos(3t) \n")
        f = sp.exp(-2*t) * sp.cos(3*t)
        laplace_f = sp.laplace_transform(f, t, s)
        print("Transformada de Laplace de f:", laplace_f)
                    
    def invLaplace():
        #aca realiza la transformada inversa de otra funcion
        print("F(s) = 1/( s*(s + 2)) \n")
        F = 1 / (s * (s + 2))
        inverse_laplace_F = sp.inverse_laplace_transform(F, s, t)
        print("Transformada inversa de Laplace de F:", inverse_laplace_F)
            
    def convolucion():
        s, t, tau = sp.symbols('s t tau')
        #aca se realiza la convolucion de dos funciones 
        print("f(t) = e^(-2t) * u(t) \n g(t) = e^(-t) * u(t)\n")
        f = sp.exp(-2*t) * sp.Heaviside(t)
        g = sp.exp(-t) * sp.Heaviside(t)
        convolution_result_1 = sp.integrate(f.subs(t, t - tau) * g, (tau, 0, t))
        print("Resultado de la convolución de f y g:", convolution_result_1)
    
    laplace1()
    invLaplace()
    convolucion()
    
def otros():  
    #aca puse como hacer algunas cosas como funciones heaviside, dirac, trozos y el uso de estas con laplace
    t, a, s = sp.symbols('t a s')
    
    #Heaviside
    print("H(t-3)")
    u3 = sp.Heaviside(t-3)
    print(u3)
    
    #Delta de Dirac
    print("δ(x - 2)")
    δ2 = sp.DiracDelta(t-2)
    print(δ2)
    
    #Trozos de ambas
    print("f(t) = t, para t < 2\n 0, para t >= 2\n δ(t - 3), para cualquier t")
    trozo = sp.Piecewise((t, t < 2), (0, t >= 2)) + sp.DiracDelta(t - 3)
    print(trozo)

    #laplace de una H
    print("L[H(t-3)]") 
    laplaceu3 = sp.laplace_transform(u3,t,s)
    print(laplaceu3)
    
    #convolucion con H
    t, a, tau = sp.symbols('t a tau')
    print("u3 * rectangular")
    rectangular = sp.Heaviside(t + 1) - sp.Heaviside(t - 1)
    # Calcular convolución
    conv = sp.integrate(u3.subs(t, tau) * rectangular.subs(t, t - tau), (tau, -float('inf'), float('inf')))
    print(conv)
    

####################################################################################################