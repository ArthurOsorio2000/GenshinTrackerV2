from datetime import datetime
from sqlalchemy import *
from flask import Blueprint, jsonify
from database import *
from flask_bcrypt import Bcrypt

#initialise bcrypt in an external file because my code is throwing a tantrum
bcrypt = Bcrypt()


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