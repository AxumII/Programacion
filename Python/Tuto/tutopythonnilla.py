class TutoPythonNilla:
    def __init__(self, input1, input2):
        # Inputs de la clase
        self.input1 = input1
        self.input2 = input2

        # Constantes como atributos de la clase
        self.int1 = 3
        self.float1 = 100.0
        self.string1 = "textolargo"
        self.lista1 = [1, 2, 3, 4, 5, 6, 7]

    def tiposdedatos(self):
        print("=== TIPOS DE DATOS INICIALES ===")
        print(f"int1: {self.int1} (tipo: {type(self.int1)})")
        print(f"float1: {self.float1} (tipo: {type(self.float1)})")
        print(f"string1: {self.string1} (tipo: {type(self.string1)})")
        print(f"lista1: {self.lista1} (tipo: {type(self.lista1)})")

        # Conversión de tipos numéricos
        print("\n=== CONVERSIÓN DE TIPOS ===")
        print(f"float1 → int: {int(self.float1)} (tipo: {type(int(self.float1))})")
        print(f"int1 → float: {float(self.int1)} (tipo: {type(float(self.int1))})")

        # Operaciones con string
        print("\n=== OPERACIONES CON STRING ===")
        palabras = self.string1.split()
        print(f"Separar string en lista de palabras: {palabras}")
        print(f"Primera palabra: {palabras[0]}")
        print(f"String en mayúsculas: {self.string1.upper()}")
        print(f"String reemplazando 'prueba' por 'ejemplo': {self.string1.replace('prueba', 'ejemplo')}")
        print(f"String como lista de caracteres: {list(self.string1)}")

        # Métodos básicos de listas
        print("\n=== MÉTODOS BÁSICOS DE LISTAS ===")
        print("Lista original:", self.lista1)
        self.lista1.append(99)
        print("append(99):", self.lista1)
        elemento = self.lista1.pop()
        print(f"pop() → elemento eliminado: {elemento}, lista actual: {self.lista1}")
        self.lista1.insert(2, 500)
        print("insert(2, 500):", self.lista1)
        self.lista1.remove(500)
        print("remove(500):", self.lista1)
        self.lista1.sort()
        print("sort():", self.lista1)
        self.lista1.reverse()
        print("reverse():", self.lista1)

        # Slicing y acceso avanzado
        print("\n=== SLICING E ÍNDICES ===")
        print("Primeros 3 elementos:", self.lista1[:3])
        print("Elementos desde el índice 2:", self.lista1[2:])
        print("Elementos del índice 1 al 4:", self.lista1[1:5])
        print("Lista con salto de 2 en 2:", self.lista1[::2])
        print("Último elemento:", self.lista1[-1])
        print("Penúltimo elemento:", self.lista1[-2])
        print("Cantidad de veces que aparece el 2:", self.lista1.count(2))


        # Ejemplos con format()
        print("\n=== EJEMPLOS DE .format() ===")
        nombre = "Juan"
        edad = 30
        pi = 3.14159265

        print("Hola, mi nombre es {} y tengo {} años".format(nombre, edad))
        print("Edad: {1}, Nombre: {0}".format(nombre, edad))
        print("Nombre: {n}, Edad: {e}".format(n=nombre, e=edad))
        print("Pi con 2 decimales: {:.2f}".format(pi))
        print("Número con ceros: {:05d}".format(42))
        print("Porcentaje: {:.1%}".format(0.2567))
        print("{:<10} alineado a la izquierda".format("Hi"))
        print("{:>10} alineado a la derecha".format("Hi"))
        print("{:^10} centrado".format("Hi"))

    def condicionales(self):
        print("\n=== IF / ELIF / ELSE ===")
        if self.int1 > 10:
            print("int1 es mayor que 10")
        elif self.int1 == 10:
            print("int1 es igual a 10")
        else:
            print("int1 es menor que 10")

        print("\n=== WHILE ===")
        contador = 0
        while contador < 3:
            print(f"contador = {contador}")
            contador += 1

        print("\n=== MATCH / CASE ===")
        opcion = self.int1
        match opcion:
            case 1:
                print("Opción 1")
            case 3:
                print("Opción 3")
            case _:
                print("Opción no reconocida")

        print("\n=== IN ===")
        if 4 in self.lista1:
            print("El número 4 está en la lista")

        print("\n=== RANGE ===")
        for i in range(1, 6):
            print(f"Iteración {i}")

        print("\n=== BREAK ===")
        for i in range(10):
            if i == 5:
                print("Se encontró el 5, saliendo del bucle")
                break
            print(i)

        print("\n=== CONTINUE ===")
        numeros = [1, 2, 3, 4, 5, 6]
        for n in numeros:
            if n % 2 == 0:
                print(f"{n} es par, se salta el resto de la iteración")
                continue
            print(f"Procesando número impar: {n}")

    def operadores(self):
        print("\n=== OPERADORES BINARIOS ===")
        a, b = 5, 3
        print(f"{a} & {b} (AND bit a bit) = {a & b}")
        print(f"{a} | {b} (OR bit a bit) = {a | b}")
        print(f"{a} ^ {b} (XOR bit a bit) = {a ^ b}")
        print(f"{a} << 1 (desplazamiento a la izquierda) = {a << 1}")
        print(f"{a} >> 1 (desplazamiento a la derecha) = {a >> 1}")

        print("\n=== OPERADORES LÓGICOS ===")
        x, y = True, False
        print(f"{x} and {y} = {x and y}")
        print(f"{x} or {y} = {x or y}")
        print(f"not {x} = {not x}")

        print("\n=== OPERADORES ARITMÉTICOS ===")
        print(f"{a} + {b} = {a + b}")
        print(f"{a} - {b} = {a - b}")
        print(f"{a} * {b} = {a * b}")
        print(f"{a} / {b} = {a / b}")
        print(f"{a} // {b} (división entera) = {a // b}")
        print(f"{a} % {b} (módulo) = {a % b}")
        print(f"{a} ** {b} (potencia) = {a ** b}")

    def argumentos(self):
        print("\n=== DEMOSTRACIÓN DE PARÁMETROS / Y * ===")

        # Función de ejemplo con posiciones y keywords
        def f(pos1, pos2, /, pos_or_kwd, *, kwd1, kwd2):
            print(f"pos1 = {pos1}")
            print(f"pos2 = {pos2}")
            print(f"pos_or_kwd = {pos_or_kwd}")
            print(f"kwd1 = {kwd1}")
            print(f"kwd2 = {kwd2}")

        # ✅ Ejemplo correcto (posicionales y keywords)
        print("\n--- Ejemplo correcto ---")
        f(1, 2, 3, kwd1=4, kwd2=5)

        # ✅ También válido pasar pos_or_kwd como keyword
        print("\n--- pos_or_kwd como keyword ---")
        f(10, 20, pos_or_kwd=30, kwd1=40, kwd2=50)

        # ❌ Ejemplo incorrecto: intentar pasar pos1 y pos2 como keyword
        print("\n--- Ejemplo incorrecto (pos1 como keyword) ---")
        try:
            f(pos1=1, pos2=2, pos_or_kwd=3, kwd1=4, kwd2=5)
        except TypeError as e:
            print("Error:", e)

        print("\n=== USO DE **kwargs (solo keywords variables) ===")
        def mostrar_datos(**kwargs):
            for clave, valor in kwargs.items():
                print(f"{clave} = {valor}")

        mostrar_datos(nombre="Juan", edad=25, ciudad="Madrid")

        print("\n=== USO DE *args y **kwargs combinados ===")
        def ejemplo_mixto(a, b, *args, **kwargs):
            print(f"a = {a}, b = {b}")
            print("args:", args)
            print("kwargs:", kwargs)

        ejemplo_mixto(1, 2, 3, 4, 5, nombre="Ana", ciudad="Sevilla")

    def errores(self):
        print("\n=== MANEJO DE ERRORES Y EXCEPCIONES ===")

        # Ejemplo 1: Manejar división por cero
        print("\n--- ZeroDivisionError ---")
        try:
            resultado = 10 / 0
        except ZeroDivisionError as e:
            print("Error:", e)

        # Ejemplo 2: Conversión de tipo inválida
        print("\n--- ValueError ---")
        try:
            numero = int("hola")
        except ValueError as e:
            print("Error:", e)

        # Ejemplo 3: Archivo inexistente
        print("\n--- FileNotFoundError ---")
        try:
            with open("archivo_inexistente.txt", "r") as f:
                contenido = f.read()
        except FileNotFoundError as e:
            print("Error:", e)

        # Ejemplo 4: Uso de else y finally
        print("\n--- Uso de else y finally ---")
        try:
            numero = int("123")
        except ValueError:
            print("Error al convertir")
        else:
            print("Conversión exitosa, número =", numero)
        finally:
            print("Bloque finally: se ejecuta siempre")

        # Ejemplo 5: Capturar múltiples excepciones
        print("\n--- Captura múltiple ---")
        try:
            x = int("12.5")  # ValueError
        except (ValueError, TypeError) as e:
            print("Error capturado:", e)

        # Ejemplo 6: Lanzar una excepción manualmente
        print("\n--- Lanzar excepción manualmente ---")
        try:
            raise RuntimeError("Este es un error forzado")
        except RuntimeError as e:
            print("Error personalizado:", e)

        # Ejemplo 7: Excepción personalizada
        print("\n--- Excepción personalizada ---")
        class MiError(Exception):
            """Excepción definida por el usuario"""
            def __init__(self, mensaje, codigo):
                super().__init__(mensaje)
                self.codigo = codigo

        try:
            # Simulamos una validación fallida
            valor = -10
            if valor < 0:
                raise MiError("El valor no puede ser negativo", codigo=400)
        except MiError as e:
            print(f"Error personalizado capturado: {e} (código {e.codigo})")



# Ejemplo de uso
t = TutoPythonNilla("entrada1", "entrada2")
t.tiposdedatos()
t.condicionales()
t.operadores()
t.argumentos()
t.errores()
