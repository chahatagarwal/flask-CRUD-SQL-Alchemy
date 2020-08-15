#Create a model with fields id(pk), username(unique), useremail, password
from user import db
import datetime
from user import app

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    useremail = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)