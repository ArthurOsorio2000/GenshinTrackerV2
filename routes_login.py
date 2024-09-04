from flask import *
from sqlalchemy import *
from online_database import *
from toolbox import *
from flask_login import *

LoginAPI = Blueprint('loginapi', __name__)

##routes
@LoginAPI.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200 

##wrapper test
@LoginAPI.route('/loginTest', methods=['GET'])
@login_required
def secretPage():
    return jsonify({"secret": "found"}), 418 

##guser test
@LoginAPI.route('/getcurrentuser', methods=['GET'])
def returnGUser():
    if g.user:
        return jsonify({"User": g.user.username}), 418
    return jsonify({"User": "guest"}), 418

##############################    account registration    ##############################
@LoginAPI.route("/register", methods=['POST'])
def Register():
    #get data from register data stream
    data = request.get_json()
    inputUsername = data.get('inputUsername')
    inputPassword = data.get('inputPassword')
    verifyInputPassword = data.get('verifyInputPassword')
    #query db if username has already been taken
    if FindUser(inputUsername):
        return jsonify({'Conflict': 'Username has already been taken :( sorryyyyyyyy'}), 409
    #matching password verification
    if inputPassword != verifyInputPassword:
        return jsonify({
        'Unauthorized': 'Passwords did not match.'
        }), 401
    #hash password with pepper, salt and something else
    #due to the userid being autoincrement, the user id does not have to be added - just add the username and password

    #before prod deployment implement salting and peppering password before hash
    hashedInputPassword = bcrypt.generate_password_hash(inputPassword).decode('utf-8')

    newUser = User_Profiles( 
        username = inputUsername,
        password = hashedInputPassword,
        role = 'user'
    )

    #add user to db
    db.session.add(newUser)
    db.session.commit()

    return jsonify({
        'success': 'User: [' + inputUsername + '] created!'
        }), 201


##############################    login    ##############################
@LoginAPI.route("/login", methods=['POST'])
def Login():
    #get login information from login screen data stream
    data = request.get_json()
    inputUsername = data.get('inputUsername')
    inputPassword = data.get('inputPassword')
    #look for existing user in db
    foundUser = FindUser(inputUsername)
    if foundUser:
        if bcrypt.check_password_hash(foundUser.password, inputPassword):
            session['user_id'] = foundUser.user_id
            return jsonify({"success" : "User [" + foundUser.username + "] has successfully logged in!"}), 201
        #user input wrong password
        return jsonify({"error": "Incorrect password."}), 401
    #user not found
    return jsonify({"error": "user does not exist."}), 404 


##############################    logout    ##############################
@LoginAPI.route('/logout', methods=['POST'])
def logout():
    # Clear the session data
    session.clear()
    return jsonify({"success" : "You have logged out successfully. See you again!"}), 201
