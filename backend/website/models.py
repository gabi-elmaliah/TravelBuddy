from . import db
from flask_login import UserMixin



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    user_name = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False) 
    cluster=db.Column(db.Integer)
    trip_id=db.Column(db.Integer,db.ForeignKey('trip.id'))
    personality_profile = db.relationship('PersonalityProfile', backref='user', uselist=False, lazy='joined')
    preferences = db.relationship('UserPreferences', backref='user', uselist=False, lazy='joined')

class PersonalityProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    age = db.Column(db.Integer)
    budget = db.Column(db.Integer, nullable=True)
    openness = db.Column(db.Integer)
    conscientiousness = db.Column(db.Integer)
    extraversion = db.Column(db.Integer)
    agreeableness = db.Column(db.Integer)
    neuroticism = db.Column(db.Integer)

class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity_historical = db.Column(db.Boolean)
    activity_outdoor = db.Column(db.Boolean)
    activity_beach = db.Column(db.Boolean)
    activity_cuisine = db.Column(db.Boolean)
    activity_cultural = db.Column(db.Boolean)

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(150), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    details = db.Column(db.Text, nullable=False)
    user=db.relationship('User', backref='trip')
    
    










