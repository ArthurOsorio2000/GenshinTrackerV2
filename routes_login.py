from sqlalchemy import *
from flask import Blueprint, jsonify, request
from database import *
from toolbox import *

LoginAPI = Blueprint('loginapi', __name__)

@LoginAPI.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200 

##############################    register account    ##############################
@LoginAPI.route("/register", methods=['POST'])
def Register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    passwordVerify = data.get('passwordVerify')
    #free username verification
    userExists = db.session.query(User_Profiles).filter(
        User_Profiles.username == username
    ).first()
    if userExists:
        return jsonify({'Conflict': 'Username already exsits.'}), 409
    #matching password verification
    if password != passwordVerify:
        return jsonify({
        'Unauthorized': 'Passwords did not match.'
        }), 401
    #pass only if username does not already exist and passwords match
    #hash password with pepper, salt and something else
    #give user_id - make sure the user ID does not change. optionally if user is missing, instead of getting length of users+1,
    #take the empty user id first, before using userlength+1
    
    return jsonify({
        'success': 'User: [' + username + '] created!'
        }), 201


##############################    login    ##############################

@LoginAPI.route("/login", methods=['POST'])
def Login():
    currentTime = datetime.now().hour
    match currentTime:
        case currentTime if currentTime >= 0 and currentTime < 12:
            return "Good morning nerd ฅ^•ﻌ•^ฅ"
        case currentTime if currentTime >= 12 and currentTime < 19:
            return "Good afternoon nerd ฅ^•ﻌ•^ฅ"
        case _:
            return "Good evening nerd ฅ^•ﻌ•^ฅ"