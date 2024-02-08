import sqlite3

def create_product_table():
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS INVENTARIO (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(50),
                        unitPrice REAL                            
                    )''')

    conexion.commit()
    
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS USUARIO (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        userName VARCHAR(20),
                        email VARCHAR(30),                        
                        accessType INTEGER
                   )''')
    
    conexion.commit()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS COMPRA (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        usuarioId INTEGER,
                        inventarioId INTEGER,
                        FOREIGN KEY (usuarioId) REFERENCES USUARIO(id),
                        FOREIGN KEY (inventarioId) REFERENCES INVENTARIO(id)
                    )''')

    conexion.commit()
    
    
    
    
    
    
    
    
    conexion.close()
    
    
    
    
    

if __name__ == "__main__":
    create_product_table()


    """cursor.execute('''CREATE TABLE IF NOT EXISTS Inventario (
        
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(50),
                        unitPrice REAL   ,
                        description VARCHAR(50) ,
                        quantity INTEGER ,
                        limitDate DATE   ,
                        priority INTEGER ,
                        finanzStat BLOB  ,
                        ejecStat BLOB    
                    )''')
    """
    
    
    """cursor.execute('''CREATE TABLE IF NOT EXISTS USUARIO (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        userName VARCHAR(20),
                        email VARCHAR(30)
                        passwordHashed VARCHAR(128),
                        salt VARCHAR(32),
                        accessType INTEGER
                   )''')"""