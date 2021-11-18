from . import db #from this package import db
from flask_login import UserMixin 
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True) #creates unique primary key integer
    data = db.Column(db.String(10000)) # 10,000 character long string allowed
    date = db.Column(db.DateTime(timezone=True), default=func.now()) # Stores timezone information and gets current date and time to
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #stores id as integer which is a foreign key (of another database) this note stores the user id
    # You have to put the class in lower case when you are referencing a foreign database


class User(db.Model, UserMixin): # db.Model is the model shown below and it provides the structure for what the database holds
    id = db.Column(db.Integer, primary_key=True) #creates unique primary key integer
    email = db.Column(db.String(150), unique=True) #stores email if unique
    password = db.Column(db.String(150)) # stores string password
    first_name = db.Column(db.String(150)) #stores string first_name
    notes = db.relationship('Note') # this will store something like a list for the notes that have been associated with that specific user so that 
    # each user can find their notes
