from datetime import datetime
from sqlalchemy import *
from flask import Blueprint, jsonify
from database import *

def FindUser(searchuserid):
    founduser = (
        db.session.query(User_Profiles)
        .filter(
            (User_Profiles.user_id == searchuserid)
        )
        .first()
    )
    return founduser