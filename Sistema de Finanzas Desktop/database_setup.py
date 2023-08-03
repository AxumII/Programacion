import sqlite3

def create_product_table():
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Product (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        unitPrice REAL NOT NULL,
                        description TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        limitDate DATE NOT NULL,
                        priority INTEGER NOT NULL,
                        finanzStat BLOB NOT NULL,
                        ejecStat BLOB NOT NULL
                    )''')

    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    create_product_table()
