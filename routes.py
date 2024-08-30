from datetime import datetime
from flask import Blueprint, jsonify
from database import *

api = Blueprint('api', __name__)

##routes
#index page and datetime testing:
@api.route("/")
def Index():
    currentTime = datetime.now().hour
    match currentTime:
        case currentTime if currentTime >= 0 and currentTime < 12:
            return "Good morning gamer ฅ^•ﻌ•^ฅ"
        case currentTime if currentTime >= 12 and currentTime < 7:
            return "Good afternoon gamer ฅ^•ﻌ•^ฅ"
        case _:
            print("Good evening gamer ฅ^•ﻌ•^ฅ")

#routing
##data listing routes for testing:
@api.route('/userprofiles')
def GetUserProfiles():
    allUsers = User_Profiles.query.all()
    return jsonify({'user profiles:': [user.username for user in allUsers]})

#get all character templates and details (presents in unordered JSON)
@api.route('/charactertemplates', methods = ['GET'])
def GetCharacterTemplates():
    allCharacterTemplates = Character_Templates.query.all()
    return jsonify({
        'character templates:': [
            {
                'char id': characterTemplate.char_id, 'char name': characterTemplate.char_name,
                'normalatk name': characterTemplate.normalatk_name, 'skill_name': characterTemplate.skill_name,
                'burst name': characterTemplate.burst_name, 'talent id': characterTemplate.talent_id,
                'weapon id': characterTemplate.weapon_id, 'region id': characterTemplate.region_id
            }for characterTemplate in allCharacterTemplates
        ]
    })


##############################################  user characters  ##############################################
#testing user characters
#get all user characters
@api.route('/usercharacters')
def GetUserCharacters():
    userCharacters = User_Characters.query.all() #<-- I might have to user inner joins to create a table with the relevant information
    return jsonify({
        'user created characters:': [
            {
            'user id': userCharacter.user_id, 'char id': userCharacter.char_id,
            'is tracked?': userCharacter.is_tracked
            }for userCharacter in userCharacters
        ]
    })

#get user
@api.route('/getuser/<string:searchuserid>', methods=['GET'])
def GetUser(searchuserid):
    founduser = (
        db.session.query(User_Profiles)
        .filter(
            (User_Profiles.user_id == searchuserid)
        )
        .all()
    )
    if (founduser):
        return jsonify({'user from userid': [
                {
                    'username' : founduser.username
                }
            ]
        })
    return jsonify({'error': 'User not found.'}), 404

#get selected user's characters
@api.route('/getuserchars/<string:searchuserid>', methods=['GET'])
def GetUserChars(searchuserid):
    return 0


#testing joins
#get all characters that user has marked as tracked
@api.route('/usercharactertracking/<string:searchuserid>')
def GetUserCharacterTracking():
    userCharacters = db.session.query() #<-- I might have to user inner joins to create a table with the relevant information
    return jsonify({
        'user created characters:': [
            {
            'user id': userCharacter.user_id, 'char id': userCharacter.char_id,
            'is tracked?': userCharacter.is_tracked
            }for userCharacter in userCharacters
        ]
    })