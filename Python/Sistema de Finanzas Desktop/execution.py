from connection import execute_operation

# Main loop para la interacción con la consola
if __name__ == "__main__":
    while True:
        print("\n*** Opciones ***")
        print("1. Mostrar todos los productos")
        print("2. Agregar un nuevo producto")
        print("3. Eliminar un producto")
        print("4. Actualizar un producto")
        print("5. Salir")

        choice = input("\nIngresa el número de opción que deseas realizar: ")

        if choice == "1":
            execute_operation("show_all_products")
        elif choice == "2":
            execute_operation("add_product")
        elif choice == "3":
            execute_operation("delete_product")
        elif choice == "4":
            execute_operation("update_product")
        elif choice == "5":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Por favor, ingresa una opción válida.")
