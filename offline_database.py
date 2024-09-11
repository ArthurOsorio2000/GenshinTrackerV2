import sqlite3

connection = sqlite3.connect('local_db.sqlite3')
cursor = connection.cursor()

#create weapon types table
cursor.execute("""CREATE TABLE  weapon_types(
    weapon_id INT NOT NULL,
	weapon_type VARCHAR (255),
	PRIMARY KEY (weapon_id)
);""")

#create regions table
cursor.execute("""CREATE TABLE  regions(
    region_id INT NOT NULL,
    region_name VARCHAR (255),
    primary key (region_id)
);""")

#create talent books table
cursor.execute("""CREATE TABLE  talent_books(
    talent_id INT NOT NULL,
    talent_name VARCHAR (255),
    region_id INT NOT NULL,
    PRIMARY KEY (talent_id),
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);""")

cursor.execute("""CREATE TABLE character_templates(
	char_id INT NOT NULL,
    char_name VARCHAR (255),
    normalatk_name VARCHAR (255),
    skill_name VARCHAR (255),
    burst_name VARCHAR (255),
    talent_id INT NOT NULL,
    weapon_id INT NOT NULL,
    region_id INT NOT NULL,
    PRIMARY KEY(char_id),
    FOREIGN KEY (talent_id) REFERENCES talent_books(talent_id),
    FOREIGN KEY (weapon_id) REFERENCES weapon_types(weapon_id),
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);""")

####if I wanted to create a guest user 0, and when an account is registered or signed into, how would I then reassign all
####user characters locally assigned to guest user 0 to the registered/signed into user?

####Below table still needs an assignment for user_id - hardcode as 0 or create a default offline user when signed in as guest,
####and pull from offline default account?

cursor.execute("""CREATE TABLE user_characters(
    user_char_id INT NOT NULL,
    is_tracked BOOLEAN,
    char_level INT,
    normalatk_level INT,
    skill_level INT,
    burst_level INT,
    PRIMARY KEY (user_char_id),
	FOREIGN KEY (user_char_id) REFERENCES character_templates(char_id)
);""")

cursor.execute("""INSERT INTO weapon_types(weapon_id, weapon_type)
	VALUES
    (0, 'Bow'),
    (1, 'Catalyst'),
    (2, 'Claymore'),
    (3, 'Polearm'),
    (4, 'Sword');
""")

cursor.execute("""INSERT INTO regions(region_id, region_name)
	VALUES
	(0, 'Khaenriah'),
    (1, 'Mondstadt'),
    (2, 'Liyue'),
    (3, 'Inazuma'),
    (4, 'Sumeru'),
    (5, 'Fontaine'),
    (6, 'Natlan'),
    (7, 'Snezhnaya'),
    (8, 'Celestia');
""")

cursor.execute("""INSERT INTO talent_books(talent_id, talent_name, region_id)
	VALUES
    (0, 'Freedom', 1),
    (1, 'Resistance', 1),
    (2, 'Ballad', 1);
""")

cursor.execute("""INSERT INTO character_templates(char_id, char_name, normalatk_name, skill_name, burst_name, talent_id, weapon_id, region_id)
	VALUES
    (1, 'Aloy', 'Rapid Fire', 'Frozen Wilds', 'Prophecies of Dawn', 0, 0, 1),
    (8, 'Bennett', 'Strike of Fortune', 'Passion Overload', 'Fantastic Voyage', 1, 4, 1),
    (15, 'Fischl', 'Bolts of Downfall', 'Nightrider', 'Midnight Phantasmagoria', 2, 0, 1);
""")


cursor.execute("SELECT * FROM weapon_types")
print(cursor.fetchall())

cursor.execute("SELECT * FROM regions")
print(cursor.fetchall())

cursor.execute("SELECT * FROM talent_books")
print(cursor.fetchall())

cursor.execute("SELECT * FROM character_templates")
print(cursor.fetchall())

connection.commit()
connection.close()