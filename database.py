from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Database modelling

# CREATE TABLE user_profiles(
# 	user_id INT NOT NULL,
# 	username VARCHAR (50),
# 	#password VARCHAR (50),
# 	primary key (user_id)
# );

class User_Profiles(db.Model):
    __tablename__ = "user_profiles"

    user_id = db.Column(db.Integer, primary_key = True, nullable = False)
    username = db.Column(db.String(255), nullable = False)

    def __repr__(self):
        return f'<User id {self.user_id} | Username: {self.username}>'

# CREATE TABLE weapon_types(
# 	weapon_id INT NOT NULL,
# 	weapon_type VARCHAR (100),
# 	#could I add farming materials for these, too?
# 	PRIMARY KEY (weapon_id)
# );

class Weapon_Types(db.Model):
    __tablename__ = "weapon_types"

    weapon_id = db.Column(db.Integer, primary_key = True, nullable = False)
    weapon_type = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<weapon id {self.weapon_id} | weapon type: {self.weapon_type}>'

# CREATE TABLE regions(
# 	region_id INT NOT NULL,
#     region_name VARCHAR (100),
#     primary key (region_id)
# );

class Regions(db.Model):
    __tablename__ = "regions"

    region_id = db.Column(db.Integer, primary_key = True)
    region_name = db.Column(db.String(255))

    def __repr__(self):
        return f'<region id {self.region_id} | region name: {self.region_name}>'

# CREATE TABLE talent_books(
# 	talent_id INT NOT NULL,
#     talent_name VARCHAR (100),
#     region_id INT NOT NULL,
#     PRIMARY KEY (talent_id),
#     FOREIGN KEY (region_id) REFERENCES regions(region_id)
# );

class Talent_Books(db.Model):
    __tablename__ = "talent_books"

    talent_id = db.Column(db.Integer, primary_key = True)
    talent_name = db.Column(db.String(255))
    region_id = db.Column(db.Integer, db.ForeignKey('Regions.region_id'))
    
    def __repr__(self):
        return f'<talent id {self.region_id} | talent name: {self.talent_name} | talent region id: {self.region_id}>'
    

# CREATE TABLE character_templates(
# 	char_id INT NOT NULL,
#     char_name VARCHAR (100),
#     normalatk_name VARCHAR (100),
#     skill_name VARCHAR (100),
#     burst_name VARCHAR (100),
#     talent_id INT NOT NULL,
#     weapon_id INT NOT NULL,
#     region_id INT NOT NULL,
#     PRIMARY KEY(char_id),
#     FOREIGN KEY (talent_id) REFERENCES talent_books(talent_id),
#     FOREIGN KEY (weapon_id) REFERENCES weapon_types(weapon_id),
#     FOREIGN KEY (region_id) REFERENCES regions(region_id)
# );

class Character_Templates(db.Model):
    __tablename__ = "character_templates"

    char_id = db.Column(db.Integer, primary_key = True)
    char_name = db.Column(db.String(255), nullable = False)
    normalatk_name = db.Column(db.String(255))
    skill_name = db.Column(db.String(255))
    burst_name = db.Column(db.String(255))
    talent_id = db.Column(db.Integer, db.ForeignKey('talent_books.talent_id'), nullable = False)
    weapon_id = db.Column(db.Integer, db.ForeignKey('weapon_types.weapon_id'), nullable = False)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.region_id'), nullable = False)

    def __repr__(self):
        return f'<character id {self.char_id} | character name: {self.char_name} \nnormal attack name: {self.normalatk_name} | skill name: {self.skill_name} | burst name: {self.burst_name} \ntalent id {self.talent_id} | weapon id: {self.weapon_id} | region id: {self.region_id}>'

# CREATE TABLE user_characters(
# 	user_id INT NOT NULL,
#     char_id INT NOT NULL,
#     char_level INT,
#     normalatk_level INT,
#     skill_level INT,
#     burst_level INT,
#     #weapon INT, <--- need to make a whole new database with individual weapons :(
#     PRIMARY KEY (user_id, char_id),
#     FOREIGN KEY (user_id) REFERENCES user_profiles(user_id),
# 	FOREIGN KEY (char_id) REFERENCES character_templates(char_id)
# );

class User_Characters(db.Model):
    __tablename__ = "user_characters"

    user_id = db.Column(db.Integer, db.ForeignKey('user_profiles.user_id'), primary_key = True)
    char_id = db.Column(db.Integer, db.ForeignKey('character_templates.char_id'), primary_key = True)
    is_tracked = db.Column(db.Boolean, nullable = False)
    char_level = db.Column(db.String(255))
    normalatk_level = db.Column(db.Integer)
    skill_level = db.Column(db.Integer)
    burst_level = db.Column(db.Integer)
    #user_weapon_id = db.Column(???) <--- same as above: possibly extensible feature

    def __repr__(self):
        return f'<user id {self.user_id} | character id: {self.char_id}  | character level: {self.char_level}\nnormal attack level: {self.normalatk_level} | skill level: {self.skill_level} | burst level: {self.burst_level}>'