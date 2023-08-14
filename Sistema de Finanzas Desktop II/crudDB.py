import pandas as pd
import sqlite3

# Conectar el DataFrame con la base de datos
conn = sqlite3.connect('database.db')
cur = conn.cursor()

#Carga inicial
query = "SELECT * FROM Product"
InventarioDf = pd.read_sql_query(query, conn)

# Cargar datos de la tabla en el DataFrame
def Read():
    query = "SELECT * FROM Product"
    InventarioDf = pd.read_sql_query(query, conn)
    print('Muestra la tabla\n')
    print(InventarioDf)


def Create(name,unitPrice):
    global InventarioDf    
    newRow = {'name': name, 'unitPrice': unitPrice}
    
    # Agregar la nueva fila al DataFrame
    InventarioDf = pd.concat([InventarioDf, pd.DataFrame(newRow, index=[0])], ignore_index=True)
    
    
    # Insertar la nueva fila en la tabla
    query = f"INSERT INTO Product (name, unitPrice) VALUES ('{newRow['name']}', {newRow['unitPrice']})"
    cur.execute(query)
    conn.commit()


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
    query = f"UPDATE Product SET name = '{newRow['name']}', unitPrice = {newRow['unitPrice']} WHERE id = {pos + 1}"
    cur.execute(query)
    conn.commit()
    

def Delete(rowId):
    global InventarioDf

    # Eliminar la fila del DataFrame
    InventarioDf = InventarioDf[InventarioDf.index != rowId - 1].reset_index(drop=True)
    
    # Eliminar la fila de la tabla en la base de datos
    query = f"DELETE FROM Product WHERE id = {rowId}"
    cur.execute(query)
    conn.commit()

    print(f"Fila con ID {rowId} eliminada correctamente.")

        
      
Read()           
Create('primera',3232)
Create('aa',4444)
Create('xd',3232)
Create('xd',7777)
Read()
Update(1,'aa',3232)
Update(2,'aa',3232)
Update(3,'aa',3232)
Read()
Delete(2)
Read()

# Cerrar la conexión con la base de datos
conn.close()
