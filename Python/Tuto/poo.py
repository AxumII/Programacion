from abc import ABC, abstractmethod

# ====== Abstracción ======
class Animal(ABC):
    def __init__(self, nombre):
        self.nombre = nombre      # Atributo público
        self._energia = 100       # Atributo protegido (convención)
        self.__edad = 0           # Atributo privado

    @abstractmethod
    def sonido(self):
        """Método abstracto que deben implementar las subclases"""
        pass

    def comer(self, comida):
        self._energia += 10
        print(f"{self.nombre} come {comida}. Energía: {self._energia}")

    def _descansar(self):
        """Método protegido (puede usarse dentro y por subclases)"""
        self._energia += 5
        print(f"{self.nombre} descansa. Energía: {self._energia}")

    def mostrar_edad(self):
        print(f"{self.nombre} tiene {self.__edad} años")

    def cumplir_años(self):
        self.__edad += 1
        print(f"{self.nombre} ahora tiene {self.__edad} años")


# ====== Herencia + Polimorfismo ======
class Perro(Animal):
    def sonido(self):
        print(f"{self.nombre} dice: ¡Guau!")

    def correr(self):
        self._energia -= 15
        print(f"{self.nombre} corre feliz. Energía: {self._energia}")


class Gato(Animal):
    def sonido(self):
        print(f"{self.nombre} dice: ¡Miau!")

    def trepar(self):
        self._energia -= 8
        print(f"{self.nombre} trepa a un árbol. Energía: {self._energia}")


# ====== Ejemplo de uso ======
def ejemplo_poo():
    print("=== Creando animales ===")
    perro = Perro("Rex")
    gato = Gato("Misu")

    print("\n=== Polimorfismo ===")
    for animal in [perro, gato]:
        animal.sonido()  # Mismo método, distinto comportamiento

    print("\n=== Encapsulamiento ===")
    perro.comer("croquetas")
    gato.comer("pescado")
    perro._descansar()  # Uso de método protegido
    perro.mostrar_edad()
    perro.cumplir_años()

    print("\n=== Métodos propios ===")
    perro.correr()
    gato.trepar()


# Ejecutar ejemplo
ejemplo_poo()
