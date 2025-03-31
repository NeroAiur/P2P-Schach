import sqlite3

TESTPATH = "db/game_history.db"

def connect_database(dbPath):
    try:
        connection = sqlite3.connect(dbPath)
        cursor = connection.cursor()
        
        return cursor
    except sqlite3.Error as e:
        code = e.sqlite_errorcode
        name = e.sqlite_errorname
        print(f"Error {code} while connecting to the database '{dbPath}': {name}")
        

if __name__ == "__main__":
    connect_database(dbPath=TESTPATH)