from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    bio = db.Column(db.String(300))
    pr = db.Column(db.String(150))
    social_media = db.Column(db.String(300))
    profile_picture = db.Column(db.String(150))
    posts = db.relationship('Post', back_populates='user',lazy='dynamic')
    workout_logs = db.relationship('WorkoutLog', back_populates='user', lazy='dynamic')
    group_memberships = db.relationship('GroupMembers', back_populates='user')


class WorkoutLog(db.Model):
    __tablename__ = "workout_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    exercise = db.Column(db.String(100))
    reps = db.Column(db.Integer)
    weight = db.Column(db.Float)
    rpe = db.Column(db.Float)
    notes = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates='workout_logs')


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String(300))
    privacy_settings = db.Column(db.String(300))
    members = db.relationship('GroupMembers', back_populates='group')


class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    media_url = db.Column(db.String(500), nullable=False) 
    caption = db.Column(db.String(500), nullable=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    user = db.relationship('User', back_populates='posts')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  

    def __repr__(self):
        return f"<Post {self.id} by User {self.user_id}>"

    def __init__(self, user_id, caption="", media_url=""):
        self.user_id = user_id
        self.content = caption
        self.media_url = media_url


class GroupMembers(db.Model):
    __tablename__ = "group_members"
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    
    group = db.relationship('Group', back_populates='members')
    user = db.relationship('User', back_populates='group_memberships')


class Exercise(db.Model):
    __tablename__ = "exercise"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    details = db.Column(db.String(255))
    weight = db.Column(db.Float)
    rpe = db.Column(db.Float)

    sets = db.relationship("Set", back_populates='exercise', lazy=True)


class Set(db.Model):
    __tablename__ = "sets"

    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.id"))
    weight = db.Column(db.Float)
    reps = db.Column(db.Integer)
    rpe = db.Column(db.Float)
    exercise = db.relationship("Exercise", back_populates="sets")