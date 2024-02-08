import pandas as pd
import sqlite3

# Conectar el DataFrame con la base de datos
conn = sqlite3.connect('database.db')
cur = conn.cursor()

#Carga inicial
query = "SELECT * FROM Inventario"
InventarioDf = pd.read_sql_query(query, conn)

# Cargar datos de la tabla en el DataFrame

def Create(name,unitPrice):
    global InventarioDf    
    newRow = {'name': name, 'unitPrice': unitPrice}
    
    # Agregar la nueva fila al DataFrame
    InventarioDf = pd.concat([InventarioDf, pd.DataFrame(newRow, index=[0])], ignore_index=True)
    
    
    # Insertar la nueva fila en la tabla
    query = f"INSERT INTO Inventario (name, unitPrice) VALUES ('{newRow['name']}', {newRow['unitPrice']})"
    cur.execute(query)
    conn.commit()

def ReadAll():
    query = "SELECT * FROM Inventario"
    InventarioDf = pd.read_sql_query(query, conn)
    print('Muestra la tabla\n')
    print(InventarioDf)

def ReadSingle(rowId):
    query = f"SELECT * FROM Inventario WHERE id = {rowId}"
    singleRow = pd.read_sql_query(query, conn)
    if len(singleRow) == 0:
        print(f"No se encontró ninguna fila con ID {rowId}.")
    else:
        print('Muestra una única fila\n')
        print(singleRow)

def Update(pos, name=None, unitPrice=None):
    global InventarioDf

    # Extrae los datos actuales de la fila indicada
    oldRow = InventarioDf.iloc[pos].to_dict()
    
    # Crea un diccionario con los nuevos valores proporcionados
    newRow = {'name': name, 'unitPrice': unitPrice}
    
    print("Fila antigua:")
    print(oldRow, "\n")
    
    print("Fila nueva:")
    print(newRow, "\n")
    
    # Actualizar el DataFrame
    InventarioDf.loc[pos] = newRow
    
    # Actualizar la fila en la tabla
    query = f"UPDATE Inventario SET name = '{newRow['name']}', unitPrice = {newRow['unitPrice']} WHERE id = {pos + 1}"
    cur.execute(query)
    conn.commit()
    
def DeleteSingle(rowId):
    global InventarioDf

    # Eliminar la fila del DataFrame
    InventarioDf = InventarioDf[InventarioDf.index != rowId - 1].reset_index(drop=True)
    
    # Eliminar la fila de la tabla en la base de datos
    query = f"DELETE FROM Inventario WHERE id = {rowId}"
    cur.execute(query)
    conn.commit()

    print(f"Fila con ID {rowId} eliminada correctamente.")

        
""" 
#codigo prueba CRUD     
ReadAll()           
Create('primera',3232)
Create('aa',4444)
Create('xd',3232)
Create('xd',7777)
ReadAll()
Update(1,'aa',3232)
Update(2,'aa',3232)
Update(3,'aa',3232)
ReadAll()
Delete(2)
ReadAll()
ReadSingle(2)"""
"""#Ejemplo funcional de creacion
ReadAll()
Create("Proda", 1000)
Create("Prodb",1500)
Create("Prodc",1750)
Create("Prodd",2000)
Create("Prode",1000)"""
ReadAll()

conn.close()
