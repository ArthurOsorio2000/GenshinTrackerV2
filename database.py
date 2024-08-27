from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Character(db.Model):
    __tablename__ = "Characters"

    userid = db.Column(db.Integer, primary_key = True)

class CharacterTalents(db.Model):
    __tablename__ = "Character Talents"

    talentid = db.Column(db.Integer, primary_key = True)

class regions(db.Model):
    __tablename__ = "Regions"

    regionid = db.Column(db.Integer, primary_key = True)
