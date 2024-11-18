from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    bio = db.Column(db.String(300))
    pr = db.Column(db.String(150))
    social_media = db.Column(db.String(300))
    posts = db.relationship('Post', back_populates='user')

class WorkoutLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exercise = db.Column(db.String(100))  # Add this line
    reps = db.Column(db.Integer)          # Add this line
    weight = db.Column(db.Float)          # Add this line
    rpe = db.Column(db.Float)             # Add this line
    notes = db.Column(db.String(255))     # If needed for additional notes


class Group(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String(300))

    def __init__(self, name, description="", privacy_settings="public"):
        self.name = name
        self.description = description



class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    media_url = db.Column(db.String(500), nullable=False) 
    caption = db.Column(db.String(500), nullable=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  

    def __repr__(self):
        return f"<Post {self.id} by User {self.user_id}>"


class GroupMembers(db.Model):
    __tablename__ = 'group_members'
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)