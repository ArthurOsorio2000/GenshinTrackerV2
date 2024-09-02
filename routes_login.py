from sqlalchemy import *
from flask import Blueprint, jsonify
from database import *
from toolbox import *

LoginAPI = Blueprint('loginapi', __name__)

@LoginAPI.route("/register", methods=['POST'])
def Register():
    return 0

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