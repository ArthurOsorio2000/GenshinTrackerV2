from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
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

##sync down from online database (mysql) to offline database (SQLite)
def SyncOfflineDB_Regions():
    onlineDBSession = db.session

    SQLiteEngine = create_engine('sqlite:///local_db.sqlite3')
    Session = sessionmaker(bind=SQLiteEngine)
    offlineDBSession = Session()
    #the first one is for
    regionUpdates = False
    regionDeletions = False
    try:
        #need to update for talent books and character templates as well

        #update rows in offline db to online db
        onlineData = onlineDBSession.query(Regions).all()
        
        for row in onlineData:
            ##check if the record exists in sqlite
            existingRow = offlineDBSession.query(Regions).filter_by(region_id = row.region_id).first()
            if existingRow:
                # Update existing record
                existingRow.region_id = row.region_id
                existingRow.region_name = row.region_name
            else:
                new_row = Regions(
                    region_id = row.region_id,
                    region_name = row.region_name
                    )
                offlineDBSession.add(new_row)
                regionUpdates = True

        #compares rows to look for orphaned rows and delete them
        onlineRegionIDs = {row.region_id for row in onlineDBSession.query(Regions.region_id).all()}
        offlineRegionRows = offlineDBSession.query(Regions).all()

        for row in offlineRegionRows:
            if row.region_id not in onlineRegionIDs:
                offlineDBSession.delete(row)
                regionDeletions = True

        # Commit the changes to SQLite
        offlineDBSession.commit()

    except Exception as e:
        offlineDBSession.rollback()
        print(f"An error occurred: {e}")

    finally:
        # Close sessions
        onlineDBSession.close()
        offlineDBSession.close()
        updateFlag = (regionUpdates, regionDeletions)
        return updateFlag
