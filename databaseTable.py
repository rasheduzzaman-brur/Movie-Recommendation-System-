from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#Create User Table
class User(db.Model,UserMixin):   #userMixin include some methods in this class
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable = False)
    history = db.relationship('History', backref='user')

#Create UserToMovie Table
class History (db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    movie = db.Column(db.String(80), nullable = False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)