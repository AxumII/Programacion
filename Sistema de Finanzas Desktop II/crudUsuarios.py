import pandas as pd
import sqlite3

# Conectar el DataFrame con la base de datos
conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Carga inicial
query = "SELECT * FROM Usuario"
UsuariosDf = pd.read_sql_query(query, conn)

def Create(userName, email, accessType):
    global UsuariosDf    
    newRow = {'userName': userName, 'email': email, 'accessType': accessType}
    
    # Agregar la nueva fila al DataFrame
    UsuariosDf = pd.concat([UsuariosDf, pd.DataFrame(newRow, index=[0])], ignore_index=True)
    
    # Insertar la nueva fila en la tabla
    query = f"INSERT INTO Usuario (userName, email, accessType) VALUES ('{newRow['userName']}', '{newRow['email']}', '{newRow['accessType']}')"
    cur.execute(query)
    conn.commit()

def ReadAll():
    query = "SELECT * FROM Usuario"
    UsuariosDf = pd.read_sql_query(query, conn)
    print('Muestra la tabla de Usuarios\n')
    print(UsuariosDf)

def ReadSingle(rowId):
    query = f"SELECT * FROM Usuario WHERE id = {rowId}"
    singleRow = pd.read_sql_query(query, conn)
    if len(singleRow) == 0:
        print(f"No se encontró ningún usuario con ID {rowId}.")
    else:
        print('Muestra un único usuario\n')
        print(singleRow)

def Update(pos, userName, email,accessType):
    global UsuariosDf

    # Extrae los datos actuales del usuario indicado
    oldRow = UsuariosDf.iloc[pos].to_dict()
    
    # Crea un diccionario con los nuevos valores proporcionados
    newRow = {'userName': userName, 'email': email, 'accessType': accessType}
    
    print("Usuario antiguo:")
    print(oldRow, "\n")
    
    print("Usuario nuevo:")
    print(newRow, "\n")
    
    # Actualizar el DataFrame
    UsuariosDf.loc[pos] = newRow
    
    # Actualizar el usuario en la tabla
    query = f"UPDATE Usuario SET userName = '{newRow['userName']}', email = '{newRow['email']}', accessType = '{newRow['accessType']}' WHERE id = {pos + 1}"
    cur.execute(query)
    conn.commit()

def DeleteSingle(rowId):
    global UsuariosDf

    # Eliminar el usuario del DataFrame
    UsuariosDf = UsuariosDf[UsuariosDf.index != rowId - 1].reset_index(drop=True)
    
    # Eliminar el usuario de la tabla en la base de datos
    query = f"DELETE FROM Usuario WHERE id = {rowId}"
    cur.execute(query)
    conn.commit()

    print(f"Usuario con ID {rowId} eliminado correctamente.")


"""# codigo prueba CRUD
ReadAll()
Create('usuario1', 'usuario1@example.com',2)
Create('usuario2', 'usuario2@example.com',1)
ReadAll()
Update(1, 'nuevo_usuario', 'nuevo@example.com',0)
ReadAll()
Delete(2)
ReadAll()
ReadSingle(2)"""

"""#Ejemplo funcional de creacion
ReadAll()
Create('usuario1', 'usuario1@example.com',2)
Create('usuario2', 'usuario2@example.com',1)
Create('usuario3', 'usuario3@example.com',1)
Create('usuario4', 'usuario4@example.com',1)"""
ReadAll()


conn.close()