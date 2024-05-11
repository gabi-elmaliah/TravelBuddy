from . import db
from flask_login import UserMixin



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    user_name = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    cluster_number=db.Column(db.Integer)
    personality_profile = db.relationship('PersonalityProfile', backref='user', uselist=False, lazy='joined')
    preferences = db.relationship('UserPreferences', backref='user', uselist=False, lazy='joined')
    trip_likes = db.relationship('UserTripLikes', backref='user', lazy='dynamic')

class PersonalityProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    age_range = db.Column(db.String(10))
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

class TripTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date=db.Column(db.Integer, primary_key=True)
    end_date=db.Column(db.Integer, nullable=False)
    destination = db.Column(db.String(150), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    base_activities = db.Column(db.String(500))
    description = db.Column(db.String(1000))
    liked_by = db.relationship('UserTripLikes', backref='trip_template', lazy='dynamic')

class UserTripLikes(db.Model):
    d = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    trip_template_id = db.Column(db.Integer, db.ForeignKey('trip_template.id'))



class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)







