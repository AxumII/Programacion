from collections import deque, Counter, namedtuple, defaultdict, OrderedDict

class EstructurasDemo:
    def estructuras_base(self):
        print("\n=== LISTAS BÁSICAS ===")
        lista = [1, 2, 3]
        print("Lista inicial:", lista)

        # Pila (stack) LIFO
        lista.append(4)
        print("Push:", lista)
        lista.pop()
        print("Pop:", lista)

        # Cola (queue) FIFO
        lista.append(4)
        lista.append(5)
        print("Cola antes de dequeue:", lista)
        lista.pop(0)
        print("Cola después de dequeue:", lista)

        print("\n=== DICCIONARIOS ===")
        dic = {"nombre": "Juan", "edad": 30}
        dic["ciudad"] = "Madrid"
        print("Diccionario:", dic)
        print("Claves:", list(dic.keys()))
        print("Valores:", list(dic.values()))
        print("Items:", list(dic.items()))

        print("\n=== CONJUNTOS (set) ===")
        conjunto = {1, 2, 3, 2}
        print("Conjunto (sin duplicados):", conjunto)
        conjunto.add(4)
        conjunto.remove(2)
        print("Conjunto después de cambios:", conjunto)
        print("¿Contiene 3?:", 3 in conjunto)

        print("\n=== LINKED LIST SIMPLE ===")
        class Nodo:
            def __init__(self, dato):
                self.dato = dato
                self.siguiente = None

        nodo1 = Nodo(1)
        nodo2 = Nodo(2)
        nodo3 = Nodo(3)

        nodo1.siguiente = nodo2
        nodo2.siguiente = nodo3

        actual = nodo1
        while actual:
            print("Nodo:", actual.dato)
            actual = actual.siguiente

        print("\n=== USO DE PUNTEROS (referencias) ===")
        a = [1, 2]
        b = a  # b apunta al mismo objeto que a
        b.append(3)
        print("Lista a:", a)
        print("Lista b:", b)

    def usando_collections(self):
        print("\n=== deque ===")
        d = deque()
        d.append("A")
        d.append("B")
        d.appendleft("C")
        print("Deque:", d)
        d.pop()
        print("Después de pop:", d)
        d.popleft()
        print("Después de popleft:", d)

        print("\n=== Counter ===")
        letras = ['a', 'b', 'a', 'c', 'b', 'a']
        conteo = Counter(letras)
        print("Conteo:", conteo)
        print("Más común:", conteo.most_common(1))

        print("\n=== namedtuple ===")
        Persona = namedtuple("Persona", ["nombre", "edad"])
        p1 = Persona("Juan", 30)
        print("Persona:", p1.nombre, p1.edad)

        print("\n=== defaultdict ===")
        dd = defaultdict(int)
        dd["uno"] += 1
        print("Defaultdict:", dd)
        print("Valor inexistente:", dd["dos"])  # Devuelve 0

        print("\n=== OrderedDict ===")
        od = OrderedDict()
        od["a"] = 1
        od["b"] = 2
        od["c"] = 3
        print("OrderedDict:", od)

    def arboles(self):
        print("\n=== ÁRBOL BINARIO DE BÚSQUEDA ===")

        class NodoBinario:
            def __init__(self, valor):
                self.valor = valor
                self.izq = None
                self.der = None

        class ArbolBinario:
            def __init__(self):
                self.raiz = None

            def insertar(self, valor):
                if self.raiz is None:
                    self.raiz = NodoBinario(valor)
                else:
                    self._insertar_rec(self.raiz, valor)

            def _insertar_rec(self, nodo, valor):
                if valor < nodo.valor:
                    if nodo.izq is None:
                        nodo.izq = NodoBinario(valor)
                    else:
                        self._insertar_rec(nodo.izq, valor)
                else:
                    if nodo.der is None:
                        nodo.der = NodoBinario(valor)
                    else:
                        self._insertar_rec(nodo.der, valor)

            def inorden(self, nodo):
                if nodo:
                    self.inorden(nodo.izq)
                    print(nodo.valor, end=" ")
                    self.inorden(nodo.der)

        bst = ArbolBinario()
        for num in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
            bst.insertar(num)
        print("Recorrido inorden (ordenado):")
        bst.inorden(bst.raiz)
        print()

        print("\n=== HEAP (MIN HEAP) ===")
        heap = []
        for val in [5, 3, 8, 1, 6]:
            heapq.heappush(heap, val)
        print("Heap interno:", heap)
        print("Extraer mínimo:", heapq.heappop(heap))
        print("Heap después:", heap)

        print("\n=== ÁRBOL N-ARIO ===")

        class NodoNario:
            def __init__(self, valor):
                self.valor = valor
                self.hijos = []

            def agregar_hijo(self, nodo):
                self.hijos.append(nodo)

        def imprimir_arbol_nario(nodo, nivel=0):
            print("  " * nivel + str(nodo.valor))
            for hijo in nodo.hijos:
                imprimir_arbol_nario(hijo, nivel + 1)

        raiz = NodoNario("A")
        nodo_b = NodoNario("B")
        nodo_c = NodoNario("C")
        nodo_d = NodoNario("D")
        raiz.agregar_hijo(nodo_b)
        raiz.agregar_hijo(nodo_c)
        nodo_b.agregar_hijo(nodo_d)

        imprimir_arbol_nario(raiz)

# Ejecución de prueba
demo = EstructurasDemo()
demo.estructuras_base()
demo.usando_collections()
demo.arboles()
