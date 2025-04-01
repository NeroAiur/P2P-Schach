# Database Connection Module
# --------------------------
# Needs to be called first - the generated cursor is needed
# as a credential in every single database operation
def connect_database(dbPath):
    import sqlite3
    try:
        connection = sqlite3.connect(dbPath)
        cursor = connection.cursor()
        
        return cursor
    except sqlite3.Error as e:
        code = e.sqlite_errorcode
        name = e.sqlite_errorname
        print(f"Error {code} while connecting to the database '{dbPath}': {name}")


# Validation Module
# --------------------------
# switch is either "user_creation" or "user_login"
# in case of creation - returns True if there is no database-row with the given username
# in case of login - returns True if there is a database-row with given username and password-hash
def validate(cursor, username, password, switch):
    if switch == "user_creation":
        cursor.execute("SELECT user_name FROM user")
        rows = cursor.fetchall()
        for row in rows:
            if row[0] == username:
                return False
        
        return True
        
    elif switch == "user_login":
        cursor.execute("SELECT user_name, password_hash FROM user")
        rows = cursor.fetchall()
        for row in rows:
            if row[0] == username and row[1] == password:
                return True
        
        return False
            
# Add-User Module
# --------------------------
# when called will first validate that the username isn't taken already
# will then create a new database entry with an incremented ID and the username and password given
def add_user(cursor, username, password):
    if validate(cursor, username, password, "user_creation") == False:
        return 1
    else:
        # fetchone() always returns a tuple, therefore we need to get the first index
        # of that tuple and increment it by 1
        uID = cursor.execute("SELECT MAX(ID) FROM user").fetchone()[0] + 1
        cursor.execute(f"""INSERT INTO user(ID, user_name, password_hash, elo)
                          VALUES {uID}, {username}, {password}, 0""")
        return 0


# Testing
# --------------------------
# will only be called if you run this file directly
if __name__ == "__main__":
    # Test-Parameters
    TESTPATH = "db/user.db"
    TESTUSER = "testomana"
    TESTPW = "b3uz21r3tw904r"
    
    cursor = connect_database(dbPath=TESTPATH)
    print(validate(cursor, TESTUSER, TESTPW, "user_login"))