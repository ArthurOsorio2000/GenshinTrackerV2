from flask import Blueprint, jsonify
from database import *

api = Blueprint('api', __name__)

##routes
#index page:
@api.route("/")
def index():
    return "Good evening gamer ฅ^•ﻌ•^ฅ"

@api.route("/holly")
def holly():
    return "<p>Love u Holly!</p>"

#routing
##data listing routes for testing:
@api.route('/userprofiles')
def getUserProfiles():
    allUsers = User_Profiles.query.all()
    return jsonify({'user profiles:': [user.username for user in allUsers]})

#get all character templates and details (presents in unordered JSON)
@api.route('/charactertemplates', method = ['GET'])
def getCharacterTemplates():
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

#testing user characters
@api.route('/usercharacters')
def getUserCharacters():
    userCharacters = User_Characters.query.all()
    return jsonify({'user created characters:': [characterName.user_id for characterName in userCharacters]})