import sqlite3
from flask import *
##find if character exists in locally owned database - return character or None
def OfflineFindUserCharID(searchUCID):
    connection = sqlite3.connect('local_db.sqlite3')
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM user_characters WHERE user_char_id = ?""", (searchUCID, ))
    foundUserChar = cursor.fetchone()
    ##temporary debugging prints
    if foundUserChar:
        connection.close()
        return foundUserChar
    else:
        print("No existing user character in local database")
        connection.close()
        return None
    
def OfflineFindCharTempID(searchUCID):
    connection = sqlite3.connect('local_db.sqlite3')
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM character_templates WHERE char_id = ?""", (searchUCID, ))
    foundUserChar = cursor.fetchone()
    ##temporary debugging prints
    if foundUserChar:
        connection.close()
        return foundUserChar
    else:
        print("No existing user character in local database")
        connection.close()
        return None


###################################   get character template details  ###################################


#0 = normal attack
#1 = skill
#2 = burst
def TapRaiseLevel(userCharID, talentIDNum):
    #connect to local database
    connection = sqlite3.connect('local_db.sqlite3')
    cursor = connection.cursor()
    #try to find user owned chracter
    cursor.execute("""SELECT * FROM user_characters WHERE user_char_id = ?""", (userCharID, ))
    foundUserChar = cursor.fetchone()

    #throw error if not owned = make this a try catch?
    if not foundUserChar:
        connection.close()
        return jsonify({
            "error" : "character not owned"
            }), 404

    #find the talent type by getting the int entered and adding two, skipping the usercharid and char level in row
    talentIndex = talentIDNum + 3 #this leads to a 3
    talentType = TalentParser(talentIDNum)

    if foundUserChar[talentIndex] >= 10:
        connection.close()
        return jsonify({
            "error" : f"{talentType} already maxed"
            }), 400

    #set corresponding talent up
    cursor.execute(f"UPDATE user_characters SET {talentType} = ? WHERE user_char_id = ?", (foundUserChar[talentIndex] + 1, userCharID))

    #commit changes and close the connection
    connection.commit()
    connection.close()

    return jsonify({
        "success" : "userchar [" + OfflineFindCharTempID(userCharID)[1] + f"] {talentType} increased: " + str(foundUserChar[talentIndex] + 1)
        }), 201

#0 = normal attack
#1 = skill
#2 = burst
def SlideRaiseLevel(userCharID, talentIDNum, charSkillChange):
    #connect to local database
    charSkillChange = int(charSkillChange)
    connection = sqlite3.connect('local_db.sqlite3')
    cursor = connection.cursor()
    #try to find user owned chracter
    cursor.execute("""SELECT * FROM user_characters WHERE user_char_id = ?""", (userCharID, ))
    foundUserChar = cursor.fetchone()

    if ((charSkillChange < 0) or (charSkillChange > 10)):
        connection.close()
        return jsonify({
            "error" : "skill level not allowed"
            }), 400

    if not foundUserChar:
        connection.close()
        return jsonify({
            "error" : "character not owned"
            }), 404

    talentIndex = talentIDNum + 3 #this leads to a 3
    talentType = TalentParser(talentIDNum)
    if talentType == None:
        return jsonify({
                "error" : "invalid skill ID: " + str(talentIndex)
                }), 401

    #change user skill based on input number
    cursor.execute(f"UPDATE user_characters SET {talentType} = ? WHERE user_char_id = ?", (charSkillChange, userCharID))

    connection.commit()
    connection.close()

    return jsonify({
        "success" : "userchar [" + OfflineFindCharTempID(userCharID)[1] + f"] {talentType} changed: " + str(charSkillChange)
        }), 201


def TalentParser(talentIDNum):
    talentType = ""
    match talentIDNum:
        case talentIDNum if talentIDNum == 0:
            talentType = "normalatk_level"
        case talentIDNum if talentIDNum == 1:
            talentType = "skill_level"
        case talentIDNum if talentIDNum == 2:
            talentType = "burst_level"
        case _:
            return None
    return talentType
