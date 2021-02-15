import sys
sys.path.append('./modules')

from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os 

from config_database import SetDatabase

# Create an instance of SetDatabase class with json configuration
database_config = SetDatabase('./config_main_database.json')

db_string = database_config.get_database_string()

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app, database_path=db_string):

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Class to abstract books table into database

'''

class Book(db.Model):

    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    rating = Column(Integer)

    def __init__(self, title, author, rating):

        self.title = title
        self.author = author
        self.rating = rating

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'rating': self.rating
        }