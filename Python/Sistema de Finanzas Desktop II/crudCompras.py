import pandas as pd
import sqlite3

# Conectar el DataFrame con la base de datos
conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Carga inicial
query = "SELECT * FROM COMPRA"
ComprasDf = pd.read_sql_query(query, conn)

def Create(usuarioId, inventarioId):
    global ComprasDf
    newRow = {'usuarioId': usuarioId, 'inventarioId': inventarioId}

    # Agregar la nueva fila al DataFrame
    ComprasDf = pd.concat([ComprasDf, pd.DataFrame(newRow, index=[0])], ignore_index=True)

    # Insertar la nueva fila en la tabla
    query = f"INSERT INTO COMPRA (usuarioId, inventarioId) VALUES ({newRow['usuarioId']}, {newRow['inventarioId']})"
    cur.execute(query)
    conn.commit()

def ReadAll():
    query = "SELECT * FROM COMPRA"
    ComprasDf = pd.read_sql_query(query, conn)
    print('Muestra la tabla de Compras\n')
    print(ComprasDf)

def ReadSingle(usuarioId, inventarioId):
    query = f"SELECT * FROM COMPRA WHERE usuarioId = {usuarioId} AND inventarioId = {inventarioId}"
    singleCompra = pd.read_sql_query(query, conn)
    if len(singleCompra) == 0:
        print(f"No se encontró ninguna compra para Usuario ID {usuarioId} e Inventario ID {inventarioId}.")
    else:
        print('Muestra una única compra\n')
        print(singleCompra)

def Update(usuarioId, inventarioId, newInventarioId):
    global ComprasDf

    # Actualizar el DataFrame
    ComprasDf.loc[(ComprasDf['usuarioId'] == usuarioId) & (ComprasDf['inventarioId'] == inventarioId), 'inventarioId'] = newInventarioId

    # Actualizar la fila en la tabla
    query = f"UPDATE COMPRA SET inventarioId = {newInventarioId} WHERE usuarioId = {usuarioId} AND inventarioId = {inventarioId}"
    cur.execute(query)
    conn.commit()

def DeleteSingle(usuarioId, inventarioId):
    global ComprasDf

    # Eliminar la fila del DataFrame
    ComprasDf = ComprasDf[(ComprasDf['usuarioId'] != usuarioId) | (ComprasDf['inventarioId'] != inventarioId)].reset_index(drop=True)

    # Eliminar la fila de la tabla en la base de datos
    query = f"DELETE FROM COMPRA WHERE usuarioId = {usuarioId} AND inventarioId = {inventarioId}"
    cur.execute(query)
    conn.commit()

    print(f"Compra de Usuario ID {usuarioId} e Inventario ID {inventarioId} eliminada correctamente.")

"""# Ejemplo funcional de creacion
ReadAll()
Create(1,2)
Create(2,2)
Create(3,3)
Create(1,4)
Create(1,3)
Create(3,2)
Create(1,2)"""
ReadAll()


# Cerrar la conexión con la base de datos
conn.close()
