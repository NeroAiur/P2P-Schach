# Database Connection Module
# --------------------------
# Needs to be called first - the generated cursor is needed
# as a credential in every single database operation
def connect_database(dbPath):
    import sqlite3
    try:
        connection = sqlite3.connect(dbPath)
        return connection
    except sqlite3.Error as e:
        code = e.sqlite_errorcode
        name = e.sqlite_errorname
        print(f"Error {code} while connecting to the database '{dbPath}': {name}")


# Validation Module
# --------------------------
# switch is either "user_creation" or "user_login"
# in case of creation - returns True if there is no database-row with the given username
# in case of login - returns True if there is a database-row with given username and password-hash
def validate(dbPath, username, password, switch):
    connection = connect_database(dbPath)
    cursor = connection.cursor()
    if switch == "user_creation":
        cursor.execute("SELECT user_name FROM user")
        rows = cursor.fetchall()
        for row in rows:
            if row[0] == username:
                return False
        
        connection.close()
        return True
        
    elif switch == "user_login":
        cursor.execute("SELECT user_name, password_hash FROM user")
        rows = cursor.fetchall()
        for row in rows:
            if row[0] == username and row[1] == password:
                return True
        
        connection.close()
        return False
            
# Add-User Module
# --------------------------
# when called will first validate that the username isn't taken already
# will then create a new database entry with an incremented ID and the username and password given
def add_user(dbPath, username, password):
    connection = connect_database(dbPath)
    cursor = connection.cursor()
    
    if validate(dbPath, username, password, "user_creation") == False:
        connection.close()
        return 1
    else:
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        # fetchone() always returns a tuple, therefore we need to get the first index
        # of that tuple and increment it by 1
        uID = cursor.execute("SELECT MAX(ID) FROM user").fetchone()[0] + 1
        print(f"id: {uID}\nuser_name: {username}\npassword: {password}")
        cursor.execute("INSERT INTO user(ID, user_name, password_hash, elo) VALUES (?, ?, ?, ?)", (uID, username, password, 0))
        connection.close()
        return 0

def get_uID(dbPath, username, password):
    connection = connect_database(dbPath)
    cursor = connection.cursor()
    cursor.execute("SELECT ID, user_name, password_hash FROM user")
    rows = cursor.fetchall()
    
    for row in rows:
        if row[1] == username and row[2] == password:
            return row[0]

# Testing
# --------------------------
# will only be called if you run this file directly
if __name__ == "__main__":
    # Test-Parameters
    TESTPATH = "db/user.db"
    TESTUSER = "testomana"
    TESTPW = "b3uz21r3tw904r"

    print(validate(TESTPATH, TESTUSER, TESTPW, "user_login"))