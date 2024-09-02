from flask import *
from sqlalchemy import *
from database import *
from toolbox import *
from functools import wraps
from flask_login import *

LoginAPI = Blueprint('loginapi', __name__)

@LoginAPI.before_request
def load_user():
    g.user = None

##function wrappers
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next = request.url))
        return f(*args, **kwargs)
    return decorated_function

##routes
@LoginAPI.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200 

##wrapper test
@LoginAPI.route('/loginTest', methods=['GET'])
@login_required
def secretPage():
    return jsonify({"secret": "found"}), 418 


##############################    account registration    ##############################
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

    #before prod deployment implement salting and peppering password before hash
    hashedInputPassword = bcrypt.generate_password_hash(inputPassword).decode('utf-8')

    newUser = User_Profiles( 
        username = inputUsername,
        password = hashedInputPassword
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
    data = request.get_json()
    inputUsername = data.get('inputUsername')
    inputPassword = data.get('inputPassword')
    foundUser = FindUser(inputUsername)
    if foundUser:
        if bcrypt.check_password_hash(foundUser.password, inputPassword):
            g.User = foundUser
            return jsonify({"success" : "You have successfully logged in!"}), 201
        return jsonify({"error": "Incorrect password."}), 401
    return jsonify({"error": "user does not exist."}), 404 