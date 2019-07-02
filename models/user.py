import sqlite3

from db import db

# This is NOT a resource
# This should be considered a helper class used to 
# store data about a user; with a few methods to easily
# retrieve info from a database

# This user model is actually an API (not a REST API), which
# exposes two endpoints
# The two methods (find_by_*) are an interface for other parts
# of the program
class UserModel(db.Model):

    # Telling SQLAlchemy about the tables that will be used
    __tablename__ = 'users'

    # Telling SQLAlchemy the columns of the table 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))  # max 80 characters
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        # Since column id is a primary key, it is auto implementing
        # SQLAlchemy does give self.id
        # We could add UUID (universally unique identitfiers)
        # if desired ourselves
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()    

    # Add ability to retrieve user objects from the db
    
    # Making this a class method as we were only referrceing 'User'
    # (now 'cls') and not 'self'
    @classmethod
    def find_by_username(cls, username):
        # Only one item will be returned below, as
        # username is unique
        # The first 'username' below is the column name,
        # the second is the arguement/variable name
        return cls.query.filter_by(username=username).first()
        

    @classmethod
    def find_by_id(cls, _id):
        # Need to call first() to get an actual row, as
        # an object is returned. Could also use .all()[0]
        return cls.query.filter_by(id=_id).first()

