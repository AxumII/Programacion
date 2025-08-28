class LambdasIteratorsComprehensions:
    def usar_lambdas(self):
        print("\n=== LAMBDAS ===")
        # Lambda básica
        suma = lambda x, y: x + y
        print("Suma 5 + 3:", suma(5, 3))

        # Lambda con sorted
        datos = [(1, "b"), (3, "a"), (2, "c")]
        ordenado = sorted(datos, key=lambda x: x[1])
        print("Ordenado por segunda columna:", ordenado)

        # Lambda con map
        numeros = [1, 2, 3, 4]
        cuadrados = list(map(lambda x: x**2, numeros))
        print("Cuadrados:", cuadrados)

        # Lambda con filter
        pares = list(filter(lambda x: x % 2 == 0, numeros))
        print("Pares:", pares)

    def usar_iterators(self):
        print("\n=== ITERADORES ===")
        lista = [10, 20, 30]
        it = iter(lista)
        print("Usando next():", next(it))
        print("Usando next():", next(it))
        print("Usando next():", next(it))

        # Iterador personalizado
        class Contador:
            def __init__(self, limite):
                self.limite = limite
                self.contador = 0
            def __iter__(self):
                return self
            def __next__(self):
                if self.contador < self.limite:
                    self.contador += 1
                    return self.contador
                else:
                    raise StopIteration

        print("\nIterador personalizado:")
        for num in Contador(5):
            print(num, end=" ")
        print()

    def usar_comprehensions(self):
        print("\n=== COMPREHENSIONS ===")
        # List comprehension
        cuadrados = [x**2 for x in range(5)]
        print("Lista de cuadrados:", cuadrados)

        # Set comprehension
        letras = {letra for letra in "programacion"}
        print("Conjunto de letras únicas:", letras)

        # Dict comprehension
        cuadrados_dict = {x: x**2 for x in range(5)}
        print("Diccionario de cuadrados:", cuadrados_dict)

        # Generator comprehension
        generador = (x**2 for x in range(5))
        print("Generador:", list(generador))


# Ejecución de ejemplo
demo = LambdasIteratorsComprehensions()
demo.usar_lambdas()
demo.usar_iterators()
demo.usar_comprehensions()
