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


##########################################      Synchronisation Methods      ##########################################
##sync down from online database (mysql) to offline database (SQLite)
#need to update for talent books and character templates as well
#when loading all 3 sync options - sync in order of reliance: Regions -> Talent Books -> Character Templates
##sync regions from online db to offline db
def SyncOfflineDB():
    onlineDBSession = db.session

    SQLiteEngine = create_engine('sqlite:///local_db.sqlite3')
    Session = sessionmaker(bind=SQLiteEngine)
    offlineDBSession = Session()
    #the first one is for
    regionUpdates = False
    regionDeletions = False

    talentUpdates = False
    talentDeletions = False

    characterTemplatesUpdates = False
    characterTemplateDeletions = False
    
    try:
        #update regions
        regionUpdates = UpdateRegions(onlineDBSession, offlineDBSession)
        #update talent books
        talentUpdates = UpdateTalentBooks(onlineDBSession, offlineDBSession)

        #update character templates


        #compares rows to look for orphaned rows and delete them
        #do the same for talents and char templates
        #delete orphaned regions
        onlineRegionIDs = {row.region_id for row in onlineDBSession.query(Regions.region_id).all()}
        offlineRegionRows = offlineDBSession.query(Regions).all()

        for row in offlineRegionRows:
            if row.region_id not in onlineRegionIDs:
                offlineDBSession.delete(row)
                regionDeletions = True
        
        #delete orphaned talents
        onlineTalentIDs = {row.talent_id for row in onlineDBSession.query(Talent_Books.talent_id).all()}
        offlineTalentRows = offlineDBSession.query(Talent_Books).all()

        for row in offlineTalentRows:
            if row.talent_id not in onlineTalentIDs:
                offlineDBSession.delete(row)
                talentDeletions = True

        # Commit the changes to SQLite
        offlineDBSession.commit()

    except Exception as e:
        offlineDBSession.rollback()
        print(f"An error occurred: {e}")

    finally:
        # Close sessions
        onlineDBSession.close()
        offlineDBSession.close()
        updateFlag = (
            regionUpdates, regionDeletions,
            talentUpdates, talentDeletions,
            characterTemplatesUpdates, characterTemplateDeletions
        )
        return updateFlag





#update regions function
def UpdateRegions(onlineDBSession, offlineDBSession):
    regionUpdates = False
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
    return regionUpdates

#update talent books function
def UpdateTalentBooks(onlineDBSession, offlineDBSession):
    talentUpdates = False
    onlineData = onlineDBSession.query(Talent_Books).all()
    for row in onlineData:

        ##check if the record exists in sqlite
        existingRow = offlineDBSession.query(Talent_Books).filter_by(talent_id = row.talent_id).first()

        if existingRow:
            # Update existing record
            existingRow.talent_id = row.talent_id
            existingRow.talent_name = row.talent_name
            existingRow.region_id = row.region_id
        else:
            new_row = Talent_Books(
                talent_id = row.talent_id,
                talent_name = row.talent_name,
                region_id = row.region_id
                )
            offlineDBSession.add(new_row)
            talentUpdates = True
    return talentUpdates






############This is way too much work and way too fiddly and annoying to finish##########
###############  need to revisit to lower redundancy in above methods  ##################
# def updateLocalDB(onlineDBSession, offlineDBSession, Table, TableID):
#     updateDone = False
#     #update regions
#     #update rows in offline db to online db
#     onlineData = onlineDBSession.query(Table).all()

#     for row in onlineData:
#         ##check if the record exists in sqlite
#         existingRow = offlineDBSession.query(Table).filter(TableID == getattr(Table, TableID).key).first()
#         if existingRow:
#             # Update existing record
#             for column in Table.__table__.columns.keys():
#                 setattr(existingRow, column, getattr(existingRow, column))
#                 print(str(getattr(existingRow, column)) + " done")

#         else:
#             #Add new record if it doesn't exist
#             newRow = Table()
#             for column in Table.__table__.columns.keys():
#                 setattr(newRow, column, getattr(row, column))
#             offlineDBSession.add(newRow)
#             updateDone = True
#     print(TableID + " done")
#     return updateDone
