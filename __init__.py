from routes_genshintracker import GenshinTrackerAPI
from routes_login import LoginAPI
from toolbox import bcrypt
from database import db

from dotenv import load_dotenv
from flask import *
import os

def create_app():
    #create connection to mysql database
    load_dotenv()  # Load environment variables from .env file to protect user details

    app = Flask(__name__)

    @app.before_request
    def load_user():
        g.user = None

    bcrypt.init_app(app)
    

    #use below app.config instead for direct connection to database without hidden information - be careful when pushing to github

    ##############!!!!!!!!!!!!!!!!BE CAREFUL NOT TO UPLOAD PASSWORD TO GITHUB!!!!!!!!!!!!!!!!##############
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<username>:<password>@<host>/<dbname>'
    ##############!!!!!!!!!!!!!!!!BE CAREFUL NOT TO UPLOAD PASSWORD TO GITHUB!!!!!!!!!!!!!!!!##############

    #connect to Database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('GENSHINPROJECTV2_DATABASE_URL')
    #turn off tracking to lower resource allocation
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #initialise sqlalchemy database models from database | db = sqlalchemy
    db.init_app(app)

    #register api routes through blueprint from routes | api = blueprint
    app.register_blueprint(GenshinTrackerAPI)
    app.register_blueprint(LoginAPI)

    return app