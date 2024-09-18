import sympy as sp

def lagrange_interpolation(x_values, y_values, x):
    """
    Calcula la interpolación de Lagrange para un conjunto de puntos.
    
    :param x_values: Lista de valores de x conocidos.
    :param y_values: Lista de valores de y conocidos (correspondientes a los x_values).
    :param x: Valor de x en el que se desea interpolar.
    :return: Valor de y interpolado en el valor x.
    """
    assert len(x_values) == len(y_values), "Las listas de valores x y y deben tener la misma longitud."
    
    n = len(x_values)
    result = 0
    
    for i in range(n):
        term = y_values[i]
        for j in range(n):
            if j != i:
                term *= (x - x_values[j]) / (x_values[i] - x_values[j])
        result += term
    
    return result

def lagrange_polynomial(x_values, y_values):
    """
    Calcula el polinomio de Lagrange para un conjunto de puntos.
    
    :param x_values: Lista de valores de x conocidos.
    :param y_values: Lista de valores de y conocidos (correspondientes a los x_values).
    :return: El polinomio de Lagrange.
    """
    x = sp.symbols('x')
    n = len(x_values)
    lagrange_poly = 0
    
    for i in range(n):
        term = y_values[i]
        for j in range(n):
            if j != i:
                term *= (x - x_values[j]) / (x_values[i] - x_values[j])
        lagrange_poly += term

    return sp.simplify(lagrange_poly)

def lagrange_polynomial_with_steps(x_values, y_values):
    """
    Calcula el polinomio de Lagrange y muestra el desarrollo paso a paso.
    
    :param x_values: Lista de valores de x conocidos.
    :param y_values: Lista de valores de y conocidos (correspondientes a los x_values).
    :return: El polinomio de Lagrange y el desarrollo de cada término.
    """
    x = sp.symbols('x')
    n = len(x_values)
    lagrange_poly = 0
    steps = []

    # Desarrollo del polinomio
    for i in range(n):
        term = y_values[i]
        numerator = 1
        denominator = 1
        step_str = f"L_{i}(x) = {y_values[i]} * "

        # Construir cada término del polinomio L_i(x)
        for j in range(n):
            if j != i:
                numerator *= (x - x_values[j])
                denominator *= (x_values[i] - x_values[j])
                step_str += f"(x - {x_values[j]}) / ({x_values[i]} - {x_values[j]}) * "
        
        term = term * numerator / denominator
        lagrange_poly += term

        step_str = step_str.rstrip(" * ")  # Eliminar el último asterisco innecesario
        steps.append(f"{step_str} = {sp.simplify(term)}")

    return sp.simplify(lagrange_poly), steps


# Ejemplo de uso
x_vals = [2.5, 10, 12.5]
y_vals = [4.97, 0.61, 0.3]

x_interpolado = 4.4
y_interpolado = lagrange_interpolation(x_vals, y_vals, x_interpolado)

print(f"El valor interpolado en x = {x_interpolado} es y = {y_interpolado}")

polinomio = lagrange_polynomial(x_vals, y_vals)
print(f"El polinomio de Lagrange es: {polinomio}")

polinomio, desarrollo = lagrange_polynomial_with_steps(x_vals, y_vals)

print(f"El polinomio de Lagrange es: {polinomio}\n")
print("Desarrollo de cada término:")
for paso in desarrollo:
    print(paso)