import sqlite3

def create_product_table():
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Product (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(50),
                        unitPrice REAL                            
                    )''')

    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    create_product_table()


    """cursor.execute('''CREATE TABLE IF NOT EXISTS Product (
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