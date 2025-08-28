
from Secante import Secante as sec

def secantegroup():
    it = 50
    err = 1e-5
    interv = (-10, 10)
    initial_guesses = (-5, 5)  # Dos valores iniciales para el método de secante

    eq = "exp(x) - x**4 - 2"
    a1 = sec(eq, initial_guesses, interv, it, err)
    a1.solve(print_table=True)
    a1.graf()

    eq = "x**3 + 4*x**2 - 10"
    a2 = sec(eq, initial_guesses, interv, it, err)
    a2.solve(print_table=True)
    a2.graf()

    eq = "(x+2)*(x+1)*(x)*((x-1)**3)*(x-2)"
    a3 = sec(eq, initial_guesses, interv, it, err)
    a3.solve(print_table=True)
    a3.graf()

    eq = "exp(x) - x**3 + 3*(x**2) - 2*x - 10"
    a4 = sec(eq, initial_guesses, interv, it, err)
    a4.solve(print_table=True)
    a4.graf()

    eq = "exp(2*x) +3*x -4"
    a5 = sec(eq, initial_guesses, interv, it, err)
    a5.solve(print_table=True)
    a5.graf()

def main():
    print("Ejecutando grupo de la Secante")
    secantegroup()
    print("Ejecuciones completadas.")

if __name__ == "__main__":
    main()
