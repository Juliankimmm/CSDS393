from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    bio = db.Column(db.String(300))
    pr = db.Column(db.String(150))
    social_media = db.Column(db.String(300))

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

    """
    privacy_settings = db.Column(db.String(50)) 
    members = db.relationship('User', secondary=group_members, lazy='dynamic')
    """

    def __init__(self, name, description="", privacy_settings="public"):
        self.name = name
        self.description = description

    # Getters
    def get_group_name(self):
        return self.name

    def get_group_description(self):
        return self.description

    def get_group_privacy_settings(self):
        return self.privacy_settings

    def get_group_members(self):
        return self.members.all() 

    def get_member_requests(self):
        return self.member_requests

    # Setters
    def set_group_name(self, name):
        self.name = name

    def set_group_description(self, description):
        self.description = description

    def set_group_privacy_settings(self, privacy_settings):
        self.privacy_settings = privacy_settings

    def set_group_members(self, members):
        self.members = members 

    def set_member_requests(self, member_requests):
        self.member_requests = member_requests 


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.String(300))
    media_url = db.Column(db.String(300))

    def __init__(self, user_id, content="", media_url=""):
        self.user_id = user_id
        self.content = content 
        self.media_url = media_url

    # Getter methods
    def get_id(self):
        return self.id

    def get_user_id(self):
        return self.user_id

    def get_content(self):
        return self.content

    def get_media_url(self):
        return self.media_url
    
    # Setter methods
    def set_content(self, content):
        self.content = content

    def set_media_url(self, media_url):
        self.media_url = media_url
    


class GroupMembers(db.Model):
    __tablename__ = 'group_members'
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
