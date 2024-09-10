from flask import *
from sqlalchemy import *
from online_database import *
from toolbox import *
import sqlite3

OfflineGenshinTrackerAPI = Blueprint('offlinegenshintrackerapi', __name__)

##routes
@OfflineGenshinTrackerAPI.route('/offlinehealth', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200 

@OfflineGenshinTrackerAPI.route("/offline/createnewchar", methods=['POST'])
def CreateNewChar():
    #get data from register data stream
    data = request.get_json()
    userCharID = data.get('inputUserCharID')

    #check if character already exists. if true: update account, if false - check if character is an existing template,
    #if false, reject application. If true, add row
    if not offlineFindUserCharID(userCharID):
        ##get usercharacter details from json
        isTracked = data.get('inputIsTracked')
        charLevel = data.get('inputCharLevel')
        normalAtkLevel = data.get('inputNormalAtkLevel')
        skillLevel = data.get('inputSkillLevel')
        burstLevel = data.get('inputBurstLevel')

        ##connect to local db
        connection = sqlite3.connect('local_db.sqlite3')
        cursor = connection.cursor()

        #
        cursor.execute("""INSERT INTO user_characters (user_Char_id, is_tracked, char_Level, normalatk_level, skill_level, burst_level)
            values (?, ?, ?, ?, ?, ?)""",
            (userCharID, isTracked, charLevel, normalAtkLevel, skillLevel, burstLevel))
        connection.commit()
        connection.close()

    return jsonify({
        "success" : "User owns new character"
        }), 201

