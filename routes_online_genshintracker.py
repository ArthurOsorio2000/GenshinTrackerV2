from flask import *
from sqlalchemy import *
from online_database import *
from toolbox import *

OnlineGenshinTrackerAPI = Blueprint('onlinegenshintrackerapi', __name__)

##routes
##################################       index page and datetime testing:       ##################################
@OnlineGenshinTrackerAPI.route("/")
def Index():
    currentTime = datetime.now().hour
    match currentTime:
        case currentTime if currentTime >= 0 and currentTime < 12:
            return "Good morning gamer ฅ^•ﻌ•^ฅ"
        case currentTime if currentTime >= 12 and currentTime < 19:
            return "Good afternoon gamer ฅ^•ﻌ•^ฅ"
        case _:
            return "Good evening gamer ฅ^•ﻌ•^ฅ"

#routing for all in a table
##data listing routes for testing:
@OnlineGenshinTrackerAPI.route('/getallusers')
def GetUserProfiles():
    allUsers = User_Profiles.query.all()
    return jsonify({'user profiles:': [user.username for user in allUsers]})

#get all character templates and details (presents in unordered JSON)
@OnlineGenshinTrackerAPI.route('/charactertemplates', methods = ['GET'])
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

##################################################      Create Functions     ################################################## 
#create user

#add character

#add region

#add weapon

#add talent

#################################################       user characters       #################################################
#testing user characters
#get all user characters
@OnlineGenshinTrackerAPI.route('/usercharacters')
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
@OnlineGenshinTrackerAPI.route('/<string:searchuserid>/getuser', methods=['GET'])
def GetUser(searchuserid):
    founduser = FindUser(searchuserid)
    #output if user is found
    if (founduser):
        return jsonify({ 
            'userid': founduser.user_id, 'username': founduser.username
        })
    #output if user does not exist/GetUser() returns None
    return jsonify({
        'error': 'User not found.'
    }), 404

#get g.user characters
#get all selected user's owned characters
@OnlineGenshinTrackerAPI.route('/getglobaluserchars', methods=['GET'])
def GetGlobalUserChars():
    foundUserOwnedChars = db.session.query(User_Characters).filter_by(user_id = g.user.user_id).all()
    #in order to lower code repetition, create a function to take a query and return a jsonify list
    ##return a jsonified for loop of all queried data
    ###intake a title
    ###intake a list of two item tuples - a string and an id for the codes in successful query
    ##if the length is not 0, for loop through the query processing a row for each tuple detail
    #if the length is 0, return a custom 404 error message

    if(len(foundUserOwnedChars) != 0):
        #output if user has one or more characters
        return jsonify({
            'username' : g.user.username,
            #information to return
            'user characters': [
                {
                    'char id': UserCharacter.char_id
                }for UserCharacter in foundUserOwnedChars
            ]
        })
    #output if length of owned characters is 0
    return jsonify({
    'error': 'No characters owned.'
}), 404

#get all selected user's owned characters
@OnlineGenshinTrackerAPI.route('/<string:searchuserid>/getuserchars', methods=['GET'])
def GetUserChars(searchuserid):
    foundUser = FindUser(searchuserid)
    if (foundUser):
        foundUserOwnedChars = db.session.query(User_Characters).filter_by(user_id = foundUser.user_id).all()
        #in order to lower code repetition, create a function to take a query and return a jsonify list
        ##return a jsonified for loop of all queried data
        ###intake a title
        ###intake a list of two item tuples - a string and an id for the codes in successful query
        ##if the length is not 0, for loop through the query processing a row for each tuple detail
        #if the length is 0, return a custom 404 error message

        if(len(foundUserOwnedChars) != 0):
            #output if user has one or more characters
            return jsonify({
                'username' : foundUser.username,
                #information to return
                'user characters': [
                    {
                        'char id': UserCharacter.char_id
                    }for UserCharacter in foundUserOwnedChars
                ]
            })
        #output if length of owned characters is 0
        return jsonify({
        'error': 'No characters owned.'
    }), 404
    #output if user does not exist
    return jsonify({
        'error': 'User not found.'
    }), 404


#testing joins
#get all characters that user has marked as tracked
@OnlineGenshinTrackerAPI.route('/<string:searchuserid>/gettrackeduserchars', methods=['GET'])
def GetUserCharacterTracking(searchuserid):
    foundUser = FindUser(searchuserid)
    if (foundUser):
        foundUserOwnedChars = db.session.query(User_Characters).filter_by(user_id = foundUser.user_id, is_tracked = True).all()
        if(len(foundUserOwnedChars) != 0):
            #output if user has one or more characters
            return jsonify({
                #information to return
                'username' : foundUser.username,
                'tracked user characters': [
                    {
                        'char id': UserCharacter.char_id
                    }for UserCharacter in foundUserOwnedChars
                ]
            })
        #output if length of owned characters is 0
        return jsonify({
        'error': 'No characters owned.'
        }), 404
    #output if user does not exist
    return jsonify({
        'error': 'User not found.'
    }), 404

################################################      Return All Functions     ################################################ 
#return all characters and details
@OnlineGenshinTrackerAPI.route('/getallchars', methods=['GET'])
def GetAllChars():
    return 0

#return details of all user owned characters
@OnlineGenshinTrackerAPI.route('/<string:searchuserid>/getallusercharacters', methods=['GET'])
def GetAllUserCharacters(searchuserid):
    foundUser = FindUser(searchuserid)
    if (foundUser):
        foundUserOwnedChars = db.session.query(
            User_Characters, Character_Templates
            #, Talent_Books, Regions, Weapon_Types, User_Profiles
            ).join(
                Character_Templates, User_Characters.char_id == Character_Templates.char_id
            ).filter(
                User_Characters.user_id == foundUser.user_id
            ).all()


        if(len(foundUserOwnedChars) != 0):
            #output if user has one or more characters
            return jsonify({
                #information to return
                'username' : foundUser.username, #<-- probably not necessary info
                'tracked user characters': [
                    {
                        'char id & profile pic path': UserCharacter.User_Characters.char_id,
                        'char name': UserCharacter.Character_Templates.char_name,
                        'tracked': UserCharacter.User_Characters.is_tracked,
                        'character level' : UserCharacter.User_Characters.char_level,
                        'normal attack level' : UserCharacter.User_Characters.normalatk_level,
                        'skill level' : UserCharacter.User_Characters.skill_level,
                        'burst level' : UserCharacter.User_Characters.burst_level,
                    }for UserCharacter in foundUserOwnedChars
                ]
            })
        #output if length of owned characters is 0
        return jsonify({
        'error': 'No characters owned.'
    }), 404
    #output if user does not exist
    return jsonify({
        'error': 'User not found.'
    }), 404

#prioritising tracked characters can be done in the frontend I think

################################################      Toolbox Functions      ##################################################
##sync offline database regions with online database
####rename to get new regions?
@OnlineGenshinTrackerAPI.route('/syncdown', methods=['GET'])
def SyncOnlineToOfflineDB():
    changeLog = SyncOfflineDB()
    ##changelogs
    if any(changeLog) == True:
        return jsonify({
        'New Regions': changeLog[0],
        'Deleted Regions': changeLog[1],
        'New Talent Books': changeLog[2],
        'Deleted Talent Books': changeLog[3],
        'New Characters': changeLog[4],
        'Deleted Characters': changeLog[5],
    }), 201
    return jsonify({
        'Success': 'No updates found :('
    }), 201