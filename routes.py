from flask import Blueprint, jsonify
from database_mysql import User_Profiles

main_blueprint = Blueprint('main_blueprint', __name__)

##routes
#index page:
@main_blueprint.route("/")
def index():
    return "Good evening gamer ฅ^•ﻌ•^ฅ"

@main_blueprint.route("/holly")
def holly():
    return "<p>Love u Holly!</p>"

#routing test
@main_blueprint.route('/users')
def get_users():
    users = User_Profiles.query.all()
    return jsonify({'users': [user.username for user in users]})