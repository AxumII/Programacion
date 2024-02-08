import sqlite3
from producto import Producto
from enum import Enum

# Enumerado para prioridad
class Priority(Enum):
    Fundamental = 1
    High = 2
    Medium = 3
    Low = 4

# Enumerado para estado financiero
class FinancialState(Enum):
    Ingreso = 0
    Egreso = 1

# Enumerado para estado de ejecución
class ExecutionState(Enum):
    EnProgreso = 0
    Completado = 1

# Función para conectar a la base de datos
def connect_to_database():
    try:
        conexion = sqlite3.connect("database.db")
        print("Conexión exitosa a la base de datos.")
        return conexion
    except sqlite3.Error as error:
        print("Error al conectar a la base de datos:", error)
        return None

# Función para mostrar todos los productos en la base de datos
def show_all_products():
    conexion = connect_to_database()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Product")
        productos = cursor.fetchall()
        if productos:
            print("Lista de productos:")
            for producto in productos:
                print(f"ID: {producto[0]}, Nombre: {producto[1]}, Precio: {producto[2]}, Descripción: {producto[3]}, Cantidad: {producto[4]}, Fecha Límite: {producto[5]}, Prioridad: {producto[6]}, Estado Financiero: {FinancialState(producto[7]).name}, Estado de Ejecución: {ExecutionState(producto[8]).name}")
        else:
            print("No hay productos en la base de datos.")
        conexion.close()

# Función para agregar un nuevo producto a la base de datos
def add_product():
    name = input("Ingresa el nombre del producto: ")
    unitPrice = float(input("Ingresa el precio del producto: "))
    description = input("Ingresa la descripción del producto: ")
    quantity = int(input("Ingresa la cantidad del producto: "))
    limitDate = input("Ingresa la fecha límite del producto (formato: YYYY-MM-DD): ")

    # Pedimos al usuario que ingrese la prioridad y validamos la entrada usando el enumerado
    valid_priorities = ", ".join([f"{p.name} ({p.value})" for p in Priority])
    while True:
        try:
            priority = int(input(f"Ingresa la prioridad del producto ({valid_priorities}): "))
            priority = Priority(priority)
            break
        except ValueError:
            print("Opción inválida. Por favor, ingresa una opción válida.")

    # Pedimos al usuario que ingrese el estado financiero y validamos la entrada usando el enumerado
    valid_financial_states = ", ".join([f"{fs.name} ({fs.value})" for fs in FinancialState])
    while True:
        try:
            financial_state = int(input(f"Ingresa el estado financiero del producto (0 para Ingreso, 1 para Egreso): "))
            financial_state = FinancialState(financial_state)
            break
        except ValueError:
            print("Opción inválida. Por favor, ingresa una opción válida.")

    # Pedimos al usuario que ingrese el estado de ejecución y validamos la entrada usando el enumerado
    valid_execution_states = ", ".join([f"{es.name} ({es.value})" for es in ExecutionState])
    while True:
        try:
            execution_state = int(input(f"Ingresa el estado de ejecución del producto (0 para En Progreso, 1 para Completado): "))
            execution_state = ExecutionState(execution_state)
            break
        except ValueError:
            print("Opción inválida. Por favor, ingresa una opción válida.")

    producto = Producto(name, unitPrice, description, quantity, limitDate, priority.value, financial_state.value, execution_state.value)
    insert_product(producto)

# Función para agregar un nuevo producto a la base de datos
def insert_product(producto):
    conexion = connect_to_database()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Product (name, unitPrice, description, quantity, limitDate, priority, finanzStat, ejecStat) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (producto.name, producto.unitPrice, producto.description, producto.quantity, producto.limitDate, producto.priority, producto.finanzStat, producto.ejecStat))
        conexion.commit()
        print("Producto insertado correctamente.")
        conexion.close()

def update_product():
    id = int(input("Ingresa el ID del producto que deseas actualizar: "))
    conexion = connect_to_database()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Product WHERE id = ?", (id,))
        producto = cursor.fetchone()
        if producto:
            print(f"Producto encontrado. Información actual:\nID: {producto[0]}, Nombre: {producto[1]}, Precio: {producto[2]}, Descripción: {producto[3]}, Cantidad: {producto[4]}, Fecha Límite: {producto[5]}, Prioridad: {Priority(producto[6]).name}, Estado Financiero: {FinancialState(producto[7]).name}, Estado de Ejecución: {ExecutionState(producto[8]).name}")
            name = input(f"Ingresa el nuevo nombre del producto (o deja en blanco para mantenerlo): ({producto[1]}) ")
            unitPrice = input(f"Ingresa el nuevo precio del producto (o deja en blanco para mantenerlo): ({producto[2]}) ")
            description = input(f"Ingresa la nueva descripción del producto (o deja en blanco para mantenerla): ({producto[3]}) ")
            quantity = input(f"Ingresa la nueva cantidad del producto (o deja en blanco para mantenerla): ({producto[4]}) ")
            limitDate = input(f"Ingresa la nueva fecha límite del producto (formato: YYYY-MM-DD) (o deja en blanco para mantenerla): ({producto[5]}) ")

            # Pedimos al usuario que ingrese la nueva prioridad y validamos la entrada usando el enumerado
            valid_priorities = ", ".join([f"{p.name} ({p.value})" for p in Priority])
            while True:
                try:
                    priority_input = input(f"Ingresa la nueva prioridad del producto ({valid_priorities}) (o deja en blanco para mantenerla): ")
                    if priority_input == "":
                        priority = Priority(producto[6])
                    else:
                        priority = Priority(int(priority_input))
                    break
                except ValueError:
                    print("Prioridad inválida. Por favor, ingresa una opción válida.")

            # Pedimos al usuario que ingrese el nuevo estado financiero y validamos la entrada usando el enumerado
            valid_financial_states = ", ".join([f"{fs.name} ({fs.value})" for fs in FinancialState])
            while True:
                try:
                    financial_state_input = input(f"Ingresa el nuevo estado financiero del producto ({valid_financial_states}) (0 para Ingreso, 1 para Egreso) (o deja en blanco para mantenerlo): ")
                    if financial_state_input == "":
                        financial_state = FinancialState(producto[7])
                    else:
                        financial_state = FinancialState(int(financial_state_input))
                    break
                except ValueError:
                    print("Estado financiero inválido. Por favor, ingresa una opción válida.")

            # Pedimos al usuario que ingrese el nuevo estado de ejecución y validamos la entrada usando el enumerado
            valid_execution_states = ", ".join([f"{es.name} ({es.value})" for es in ExecutionState])
            while True:
                try:
                    execution_state_input = input(f"Ingresa el nuevo estado de ejecución del producto ({valid_execution_states}) (0 para En Progreso, 1 para Completado) (o deja en blanco para mantenerlo): ")
                    if execution_state_input == "":
                        execution_state = ExecutionState(producto[8])
                    else:
                        execution_state = ExecutionState(int(execution_state_input))
                    break
                except ValueError:
                    print("Estado de ejecución inválido. Por favor, ingresa una opción válida.")

            cursor.execute("UPDATE Product SET name = COALESCE(?, name), unitPrice = COALESCE(?, unitPrice), description = COALESCE(?, description), quantity = COALESCE(?, quantity), limitDate = COALESCE(?, limitDate), priority = COALESCE(?, priority), finanzStat = COALESCE(?, finanzStat), ejecStat = COALESCE(?, ejecStat) WHERE id = ?",
                           (name, unitPrice, description, quantity, limitDate, priority.value, financial_state.value, execution_state.value, id))
            conexion.commit()
            print("Producto actualizado correctamente.")
        else:
            print("No se encontró un producto con el ID proporcionado.")
        conexion.close()

# Función para eliminar un producto de la base de datos
def delete_product():
    id = int(input("Ingresa el ID del producto que deseas eliminar: "))
    conexion = connect_to_database()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM Product WHERE id = ?", (id,))
            if cursor.rowcount == 0:
                print("No se encontró un producto con el ID proporcionado.")
            else:
                print("Producto eliminado correctamente.")
            conexion.commit()
        except sqlite3.OperationalError as error:
            print(f"Error al eliminar el producto: {error}")
        finally:
            conexion.close()

# Función para ejecutar las operaciones según el nombre proporcionado
def execute_operation(operation_name):
    if operation_name == "show_all_products":
        show_all_products()
    elif operation_name == "add_product":
        add_product()
    elif operation_name == "delete_product":
        delete_product()
    elif operation_name == "update_product":
        update_product()
    else:
        print("Operación inválida. Por favor, ingresa una operación válida.")
