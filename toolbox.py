from datetime import datetime
from sqlalchemy import *
from flask import *
from functools import wraps
from online_database import *
from flask_bcrypt import Bcrypt

#####################################      initialisations      #####################################
#initialise bcrypt in an external file because my code is throwing a tantrum
bcrypt = Bcrypt()


##########################################      tools      ##########################################
#genshintracker - find user based on UID and return either user info or None
def FindUserID(searchuserid):
    founduser = (
        db.session.query(User_Profiles)
        .filter(
            (User_Profiles.user_id == searchuserid)
        )
        .first()
    )
    return founduser

#Login - find user based on Username and return either user info or None
def FindUser(searchusername):
    founduser = (
        db.session.query(User_Profiles)
        .filter(
            (User_Profiles.username == searchusername)
        )
        .first()
    )
    return founduser

##function wrappers
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next = request.url))
        return f(*args, **kwargs)
    return decorated_function