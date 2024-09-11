import sqlite3

##find if character exists in locally owned database - return character or None
def offlineFindUserCharID(searchUCID):
    connection = sqlite3.connect('local_db.sqlite3')
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM user_characters WHERE user_char_id = ?""", (searchUCID))
    foundUserChar = cursor.fetchone()
    ##temporary debugging prints
    if foundUserChar:
        print(foundUserChar[1])
    else:
        print("No existing user character in local database")
    connection.close()    

    return foundUserChar