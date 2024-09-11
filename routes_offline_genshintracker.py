from flask import *
from sqlalchemy import *
from online_database import *
from toolbox_offline import *
from toolbox import *
import sqlite3

OfflineGenshinTrackerAPI = Blueprint('offlinegenshintrackerapi', __name__)

##routes
@OfflineGenshinTrackerAPI.route('/offlinehealth', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200 


###################################   add new character to offline db  ###################################
@OfflineGenshinTrackerAPI.route("/offline/addnewchar", methods=['POST'])
def CreateNewChar():
    #get data from register data stream
    data = request.get_json()
    userCharID = data.get('inputUserCharID')

    #check if character already exists. if true: update account, if false - check if character is an existing template,
    #if false, reject application. If true, add row
    if not offlineFindUserCharID(userCharID):
        print("character [" + userCharID + "] does not currently belong to user. adding character now.")
        ##connect to local db
        connection = sqlite3.connect('local_db.sqlite3')
        cursor = connection.cursor()

        cursor.execute("""INSERT INTO user_characters (user_Char_id, is_tracked, char_Level, normalatk_level, skill_level, burst_level)
            values (?, ?, ?, ?, ?, ?)""",
            (userCharID, False, 0, 0, 0, 0))
        connection.commit()
        connection.close()

    return jsonify({
        "success" : "User owns new character"
        }), 201

##create buttons to iterate on existing characters

##track/untrack char
##flip flop or button replace?
@OfflineGenshinTrackerAPI.route("/offline/fliptracking", methods=['POST'])
def FlipTrack():
    data = request.get_json()
    userCharID = data.get('inputUserCharID')

    connection = sqlite3.connect('local_db.sqlite3')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM user_characters WHERE user_char_id = ?""", (userCharID))
    foundUserChar = cursor.fetchone()

    if not foundUserChar:
        print("character [" + userCharID + "] either does not exist or is not owned by user.")
        connection.close()    
        return jsonify({
            "error" : "character not owned"
            }), 404
    if foundUserChar[1]:
        cursor.execute("""UPDATE user_characters SET is_tracked = False WHERE user_char_id = ?""", (userCharID))
        print("charID " + userCharID + " untracked")
        connection.commit()
        connection.close()    
        return jsonify({
        "success" : "userchar untracked :("
        }), 201
    else:
        cursor.execute("""UPDATE user_characters SET is_tracked = True WHERE user_char_id = ?""", (userCharID))
        connection.commit()
        print("charID " + userCharID + " tracked")
        connection.close()    
        return jsonify({
        "success" : "userchar tracked :)"
        }), 201
##**remove this after testing

####front end remember to only activate on negative edge
##raise normal attack level
##raise skill level
##raise burst level

