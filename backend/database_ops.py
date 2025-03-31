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

def validate(cursor, username, password, switch):
    if switch == "user_creation":
        pass
    elif switch == "user_login":
        pass    

def add_user(cursor, username, password):
    if validate(cursor, username, password, "user_creation") == False:
        return 1
    else:
        uID = cursor.execute("SELECT MAX(ID) from user")
        cursor.execute(f"""INSERT INTO user(ID, user_name, password, elo)
                          VALUES {uID}, {username}, {password}, 0""")


if __name__ == "__main__":
    cursor = connect_database(dbPath=TESTPATH)