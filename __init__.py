from routes_genshintracker import GenshinTrackerAPI
from routes_login import LoginAPI
from toolbox import bcrypt
from online_database import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import *
from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    #create connection to mysql database
    load_dotenv()  # Load environment variables from .env file to protect user details
    login_manager = LoginManager() #create login manager

    app = Flask(__name__)

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

    login_manager.init_app(app)

    #register api routes through blueprint from routes | api = blueprint
    app.register_blueprint(GenshinTrackerAPI)
    app.register_blueprint(LoginAPI)

    # Quick test configuration. Please use proper Flask configuration options
    # in production settings, and use a separate file or environment variables
    # to manage the secret key!
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    return app