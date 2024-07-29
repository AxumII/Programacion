from Biseccion import Biseccion as bis
from Regla_Falsa import ReglaFalsa as rf
from Newton import Newton as nw
from NewtonFaster import AcceleratedNewton as anw


def primgrupo():
    it = 50
    err = 1e-5
    interv = (-10,10)


    
    eq = "exp(x) - x**4 - 2"
    a1 = bis(eq, interv, it, err)
    a1.solve(print_table=True)
    a1.graf()


    eq = "x**3 + 4*x**2 - 10"
    a2 = bis(eq, interv)
    a2.solve(print_table=True)
    a2.graf()
   

    eq = "(x+2)*(x+1)*(x)*((x-1)**3)*(x-2)"
    a3 = bis(eq, interv)
    a3.solve(print_table=True)
    a3.graf()

    eq = "exp(x) - x**3 + 3*(x**2) - 2*x - 10"
    a4 = bis(eq, interv)
    a4.solve(print_table=True)
    a4.graf()

    eq = "exp(2*x) +3*x -4"
    a5 = bis(eq, interv)
    a5.solve(print_table=True)
    a5.graf()

    
def seggrupo():
    it = 50
    err = 1e-5
    interv = (-10,10)


    
    eq = "exp(x) - x**4 - 2"
    a1 = rf(eq, interv, it, err)
    a1.solve(print_table=True)
    a1.graf()


    eq = "x**3 + 4*x**2 - 10"
    a2 = rf(eq, interv)
    a2.solve(print_table=True)
    a2.graf()
   

    eq = "(x+2)*(x+1)*(x)*((x-1)**3)*(x-2)"
    a3 = rf(eq, interv)
    a3.solve(print_table=True)
    a3.graf()

    eq = "exp(x) - x**3 + 3*(x**2) - 2*x - 10"
    a4 = rf(eq, interv)
    a4.solve(print_table=True)
    a4.graf()

    eq = "exp(2*x) +3*x -4"
    a5 = rf(eq, interv)
    a5.solve(print_table=True)
    a5.graf()





def nwgrupo():
    it = 50
    err = 1e-5
    interv = (-10,10)
    pinit = -5


    
    eq = "exp(x) - x**4 - 2"
    a1 = nw(eq, pinit,interv, it, err)
    a1.solve(print_table=True)
    a1.graf()


    eq = "x**3 + 4*x**2 - 10"
    a2 = nw(eq,pinit, interv)
    a2.solve(print_table=True)
    a2.graf()
   

    eq = "(x+2)*(x+1)*(x)*((x-1)**3)*(x-2)"
    a3 = nw(eq,pinit, interv)
    a3.solve(print_table=True)
    a3.graf()

    eq = "exp(x) - x**3 + 3*(x**2) - 2*x - 10"
    a4 = nw(eq,pinit, interv)
    a4.solve(print_table=True)
    a4.graf()

    eq = "exp(2*x) +3*x -4"
    a5 = nw(eq,pinit, interv)
    a5.solve(print_table=True)
    a5.graf()

    eq = "((x - 3)**2) * (x+1)"
    a6 = nw(eq, pinit, interv, it, err)
    a6.solve(print_table=True)
    a6.graf()


def tareanw():

    eq = "(2414707.2*x*(450-0.822*x*(255))) - 265000000  "
    ini = 100
    intervalo = (0, 10)
    iteraciones = 100  
    error_tol = 1e-5

    concreto = nw(eq, ini, intervalo, iteraciones, error_tol)
    concreto.solve(print_table=True)
    concreto.graf()


    eq = " x**3 - 3*x + 2  "
    ini = 10
    intervalo = (-10, 10)
    iteraciones = 100  
    error_tol = 1e-5

    ej = nw(eq, ini, intervalo, iteraciones, error_tol)
    ej.solve(print_table=True)
    ej.graf()

    eq = " x* exp(-x)  "
    ini = 10
    intervalo = (-10, 10)
    iteraciones = 100  
    error_tol = 1e-5

    ej2 = nw(eq, ini, intervalo, iteraciones, error_tol)
    ej2.solve(print_table=True)
    ej2.graf()


def anwgrupo():
    it = 50
    err = 1e-5
    interv = (-10, 10)
    pinit = -5
    multiplicity = 2  # Asumimos multiplicidad 1 para simplificar, ajusta según sea necesario

    eq = "exp(x) - x**4 - 2"
    a1 = anw(eq, pinit, interv, multiplicity, it, err)
    a1.solve(print_table=True)
    a1.graf()

    eq = "x**3 + 4*x**2 - 10"
    a2 = anw(eq, pinit, interv, multiplicity, it, err)
    a2.solve(print_table=True)
    a2.graf()

    eq = "(x+2)*(x+1)*(x)*((x-1)**3)*(x-2)"
    a3 = anw(eq, pinit, interv, multiplicity, it, err)
    a3.solve(print_table=True)
    a3.graf()

    eq = "exp(x) - x**3 + 3*(x**2) - 2*x - 10"
    a4 = anw(eq, pinit, interv, multiplicity, it, err)
    a4.solve(print_table=True)
    a4.graf()

    eq = "exp(2*x) +3*x -4"
    a5 = anw(eq, pinit, interv, multiplicity, it, err)
    a5.solve(print_table=True)
    a5.graf()

    eq = "((x - 3)**2) * (x+1)"
    a6 = anw(eq, pinit, interv, multiplicity, it, err)
    a6.solve(print_table=True)
    a6.graf()




#primgrupo()

#seggrupo()

nwgrupo()

#tareanw()
    
anwgrupo()
    


print("XD")