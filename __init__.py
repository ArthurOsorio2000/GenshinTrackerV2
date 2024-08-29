import os
from dotenv import load_dotenv
from flask import Flask
from routes import main_blueprint
from database_mysql import db

def create_app():
    load_dotenv()  # Load environment variables from .env file to protect user details

    app = Flask(__name__)

    #use below app.config instead to work with local database
    ##############!!!!!!!!!!!!!!!!BE CAREFUL NOT TO UPLOAD PASSWORD TO GITHUB!!!!!!!!!!!!!!!!##############
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<username>:<password>@<host>/<dbname>'
    ##############!!!!!!!!!!!!!!!!BE CAREFUL NOT TO UPLOAD PASSWORD TO GITHUB!!!!!!!!!!!!!!!!##############

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('GENSHINPROJECTV2_DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register the blueprint
    app.register_blueprint(main_blueprint)

    return app