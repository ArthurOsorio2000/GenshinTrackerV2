from flask import jsonify
from database_mysql import app, User_Profiles

##routes
#index page:
@app.route("/")
def index():
    return "Good evening gamer ฅ^•ﻌ•^ฅ"

@app.route("/holly")
def holly():
    return "<p>Love u Holly!</p>"

#routing test
@app.route('/users')
def get_users():
    users = User_Profiles.query.all()
    return jsonify({'users': [user.username for user in users]})