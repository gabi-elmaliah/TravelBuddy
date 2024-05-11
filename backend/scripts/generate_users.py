from sqlalchemy import create_engine, Column, Integer, String,Boolean,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session,relationship
import pandas as pd
import csv

Base = declarative_base()


class User(Base):

    __tablename__="users"
    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True, nullable=False)
    user_name = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    personality_profile = relationship('PersonalityProfile', backref='user', uselist=False, lazy='joined')
    preferences = relationship('UserPreferences', backref='user', uselist=False, lazy='joined')
    trip_likes = relationship('UserTripLikes', backref='user', lazy='dynamic')

class PersonalityProfile(Base):

    __tablename__="personality_profile"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)
    age_range = Column(String(10))
    openness = Column(Integer)
    conscientiousness = Column(Integer)
    extraversion = Column(Integer)
    agreeableness = Column(Integer)
    neuroticism = Column(Integer)

class UserPreferences(Base):


    __tablename__="personality_preferences"



    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,ForeignKey('user.id'), nullable=False)
    activity_historical = Column(Boolean)
    activity_outdoor = Column(Boolean)
    activity_beach = Column(Boolean)
    activity_cuisine = Column(Boolean)
    activity_cultural = Column(Boolean)