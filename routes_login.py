from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import *
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
    inputUsername = data.get('inputUsername')
    inputPassword = data.get('inputPassword')
    verifyInputPassword = data.get('verifyInputPassword')
    #free username verification
    if FindUser(inputUsername):
        return jsonify({'Conflict': 'Username already exsits.'}), 409
    #matching password verification
    if inputPassword != verifyInputPassword:
        return jsonify({
        'Unauthorized': 'Passwords did not match.'
        }), 401
    #hash password with pepper, salt and something else
    #due to the userid being autoincrement, the user id does not have to be added - just add the username and password
    hashedInputPassword = bcrypt.generate_password_hash(inputPassword).decode('utf-8')

    newUser = User_Profiles( 
        username = inputUsername,
        password = hashedInputPassword
    )

    db.session.add(newUser)
    db.session.commit()

    return jsonify({
        'success': 'User: [' + inputUsername + '] created!'
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