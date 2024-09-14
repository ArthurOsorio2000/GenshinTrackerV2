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



###################################   manip chars in offline db  ###################################
@OfflineGenshinTrackerAPI.route("/offline/addnewchar", methods=['POST'])
def CreateNewChar():
    #get data from register data stream
    data = request.get_json()
    userCharID = data.get('inputUserCharID')

    #check if character already exists. if true: update account, if false - check if character is an existing template,
    #if false, reject application. If true, add row

    if OfflineFindCharTempID(userCharID):
        if OfflineFindUserCharID(userCharID) == None:
            print("character [" + userCharID + "] does not currently belong to user. adding character now.")
            ##connect to local db
            connection = sqlite3.connect('local_db.sqlite3')
            cursor = connection.cursor()

            cursor.execute("""INSERT INTO user_characters
                (user_char_id, is_tracked, char_level, normalatk_level, skill_level, burst_level)
                values (?, ?, ?, ?, ?, ?)""",
                (userCharID, False, 0, 0, 0, 0))
            connection.commit()
            connection.close()

            return jsonify({
                "success" : "User now owns: [" + OfflineFindCharTempID(userCharID)[1] + "]"
                }), 201
        return jsonify({
        "error" : "User already owns character: " + OfflineFindCharTempID(userCharID)[1]
        }), 404
    return jsonify({
        "error" : "Character Template " + str(userCharID) + " does not exist."
        }), 404


##drop owned characters
@OfflineGenshinTrackerAPI.route("/offline/dropchar", methods=['POST'])
def DropChar():
    #get data from register data stream
    data = request.get_json()
    userCharID = data.get('inputUserCharID')

    if OfflineFindUserCharID(userCharID):
        print("character [" + userCharID + "] dropping from owned character table.")
        ##connect to local db
        connection = sqlite3.connect('local_db.sqlite3')
        cursor = connection.cursor()

        cursor.execute("""DELETE FROM user_characters WHERE user_char_id = ?""", (userCharID, ))
        connection.commit()
        connection.close()
        return jsonify({
            "success" : "Character [" + OfflineFindCharTempID(userCharID)[1] + "] removed from owned chars :("
            }), 201
    return jsonify({
            "error" : "User character not found."
            }), 404
        

    


##create buttons to iterate on existing characters

##track/untrack char
##flip flop or button replace?
@OfflineGenshinTrackerAPI.route("/offline/fliptracking", methods=['POST'])
def FlipTrack():
    data = request.get_json()
    userCharID = data.get('inputUserCharID')

    connection = sqlite3.connect('local_db.sqlite3')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM user_characters WHERE user_char_id = ?""", (userCharID, ))
    foundUserChar = cursor.fetchone()

    if not foundUserChar:
        connection.close()
        return jsonify({
            "error" : "character not owned"
            }), 404

    tracking = not foundUserChar[1]
    cursor.execute("""UPDATE user_characters SET is_tracked = ? WHERE user_char_id = ?""", (tracking, userCharID))

    connection.commit()
    connection.close()   

    return jsonify({
        "success" : "userchar [" + OfflineFindCharTempID(userCharID)[1] + "] tracked: " + str(bool(tracking))
        }), 201

########################################## Change skill numbers ##########################################
####front end remember to only activate on negative edge
##raise normal attack level
##make sure level stays under 10 
@OfflineGenshinTrackerAPI.route("/offline/tapraisenalevel", methods=['POST'])
def TapRaiseNALevel():
        data = request.get_json()
        userCharID = data.get('inputUserCharID')
        return TapRaiseLevel(userCharID, 0)

##(or 13? - variable for constellations? +2 with consts for skill and burst? Should this be done in the front end?)
##raise skill level
@OfflineGenshinTrackerAPI.route("/offline/tapraiseskilllevel", methods=['POST'])
def TapRaiseSkillLevel():
        data = request.get_json()
        userCharID = data.get('inputUserCharID')
        return TapRaiseLevel(userCharID, 1)

##raise burst level
@OfflineGenshinTrackerAPI.route("/offline/tapraiseburstlevel", methods=['POST'])
def TapRaiseBurstLevel():
        data = request.get_json()
        userCharID = data.get('inputUserCharID')
        return TapRaiseLevel(userCharID, 2)

########################################## Change skill numbers ##########################################
##numerically change normal attack level
##make sure level stays between 0 and 10(13?)
@OfflineGenshinTrackerAPI.route("/offline/changenalvl", methods=['POST'])
def ChangeNALevel():
    data = request.get_json()
    userCharID = data.get('inputUserCharID')
    charSkillChange = data.get('inputCharSkillChange')
    return SlideRaiseLevel(userCharID, 0, charSkillChange)

##numerically change skill level
@OfflineGenshinTrackerAPI.route("/offline/changeskilllvl", methods=['POST'])
def ChangeSkillLevel():
    data = request.get_json()
    userCharID = data.get('inputUserCharID')
    charSkillChange = data.get('inputCharSkillChange')
    return SlideRaiseLevel(userCharID, 1, charSkillChange)

##numerically change burst level
@OfflineGenshinTrackerAPI.route("/offline/changeburstlvl", methods=['POST'])
def ChangeBurstLevel():
    data = request.get_json()
    userCharID = data.get('inputUserCharID')
    charSkillChange = data.get('inputCharSkillChange')
    return SlideRaiseLevel(userCharID, 2, charSkillChange)

