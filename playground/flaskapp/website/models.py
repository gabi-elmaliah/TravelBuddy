from . import db
from flask_login import UserMixin




class User(db.Model,UserMixin):
    id=db.Column(db.Integer(),primary_key=True)
    email = db.Column(db.String(150),nullable=False, unique=True)
    password = db.Column(db.String(150),nullable=False)
    first_name = db.Column(db.String(150),nullable=False)
    questionnaire = db.relationship('Questionnaire', backref='user', uselist=False)
    

class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Ensuring the user_id is linked to the User table's ID
    age_range = db.Column(db.String(10))
    openness = db.Column(db.Integer)
    conscientiousness = db.Column(db.Integer)
    extraversion = db.Column(db.Integer)
    agreeableness = db.Column(db.Integer)
    neuroticism = db.Column(db.Integer)
    activity_historical = db.Column(db.Boolean)
    activity_outdoor = db.Column(db.Boolean)
    activity_beach = db.Column(db.Boolean)
    activity_cuisine = db.Column(db.Boolean)
    activity_cultural = db.Column(db.Boolean)
    cluster_id = db.Column(db.Integer, nullable=True) 


    