import pandas as pd
from connection import connect_to_database

# Crear DataFrame desde la base de datos
def create_dataframe():
    conexion = connect_to_database()
    query = "SELECT * FROM Product"
    dataframe = pd.read_sql_query(query, conexion)
    conexion.close()
    return dataframe

# Guardar DataFrame en la base de datos
def save_dataframe_to_database(dataframe):
    conexion = connect_to_database()
    dataframe.to_sql("Product", conexion, index=False, if_exists="replace")
    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    product_df = create_dataframe()

    while True:
        print("\n*** Opciones ***")
        print("1. Mostrar todos los productos")
        print("2. Agregar un nuevo producto")
        print("3. Actualizar un producto")
        print("4. Eliminar un producto")
        print("5. Salir")

        choice = input("\nIngresa el número de opción que deseas realizar: ")

        if choice == "1":
            print(product_df)
        elif choice == "2":
            # Agregar un nuevo producto al DataFrame
            new_product = {
                "name": input("Ingresa el nombre del nuevo producto: "),
                "unitPrice": float(input("Ingresa el precio del nuevo producto: ")),
                "description": input("Ingresa la descripción del nuevo producto: "),
                "quantity": int(input("Ingresa la cantidad del nuevo producto: ")),
                "limitDate": input("Ingresa la fecha límite del nuevo producto (formato: YYYY-MM-DD): "),
                "priority": int(input("Ingresa la prioridad del nuevo producto: ")),
                "finanzStat": int(input("Ingresa el estado financiero del nuevo producto (0 para Ingreso, 1 para Egreso): ")),
                "ejecStat": int(input("Ingresa el estado de ejecución del nuevo producto (0 para En Progreso, 1 para Completado): "))
            }
            product_df = pd.concat([product_df, pd.DataFrame([new_product])], ignore_index=True)
            print("Nuevo producto agregado al DataFrame.")
        elif choice == "3":
            # Actualizar un producto en el DataFrame
            product_id = int(input("Ingresa el ID del producto que deseas actualizar: "))
            column_name = input("Ingresa el nombre de la columna que deseas actualizar: ")
            new_value = input("Ingresa el nuevo valor: ")
            product_df.loc[product_df['id'] == product_id, column_name] = new_value
            print("Producto actualizado en el DataFrame.")
        elif choice == "4":
            # Eliminar un producto del DataFrame
            product_id = int(input("Ingresa el ID del producto que deseas eliminar: "))
            product_df = product_df[product_df['id'] != product_id]
            print("Producto eliminado del DataFrame.")
        elif choice == "5":
            save_dataframe_to_database(product_df)
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Por favor, ingresa una opción válida.")
