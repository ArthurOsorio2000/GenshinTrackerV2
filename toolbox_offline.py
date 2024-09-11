import sqlite3
from flask import *
##find if character exists in locally owned database - return character or None
def OfflineFindUserCharID(searchUCID):
    connection = sqlite3.connect('local_db.sqlite3')
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM user_characters WHERE user_char_id = ?""", (searchUCID))
    foundUserChar = cursor.fetchone()
    ##temporary debugging prints
    if foundUserChar:
        print(foundUserChar[1])
        connection.close()
        return foundUserChar
    else:
        print("No existing user character in local database")
        connection.close()
        return None
    
def OfflineFindCharTempID(searchUCID):
    connection = sqlite3.connect('local_db.sqlite3')
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM character_templates WHERE char_id = ?""", (searchUCID))
    foundUserChar = cursor.fetchone()
    ##temporary debugging prints
    if foundUserChar:
        print(foundUserChar[1])
        connection.close()
        return foundUserChar
    else:
        print("No existing user character in local database")
        connection.close()
        return None

def FindInOfflineDB(TableID, SearchID):
    connection = sqlite3.connect('local_db.sqlite3')
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM character_templates WHERE ? = ?""", (TableID, SearchID))
    foundRow = cursor.fetchone()
    ##temporary debugging prints
    if foundRow:
        print(foundRow[1])
        connection.close()
        return foundRow
    else:
        print("No item found in db")
        connection.close()
        return None
