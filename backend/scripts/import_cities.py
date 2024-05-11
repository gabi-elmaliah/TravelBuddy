from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import pandas as pd
import csv

Base = declarative_base()

class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)


class User(db.Model, UserMixin):
    id = Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    user_name = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    personality_profile = db.relationship('PersonalityProfile', backref='user', uselist=False, lazy='joined')
    preferences = db.relationship('UserPreferences', backref='user', uselist=False, lazy='joined')

class PersonalityProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
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

 
# Create an engine that stores data in the local directory's
engine = create_engine('sqlite:////home/gabriel/Gabis_Webasite/backend/instance/database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = scoped_session(Session)



def load_cities():


    excel_file_path = '/home/gabriel/cities_csv/worldcities.xlsx'

    # Load and preview the Excel data
    df = pd.read_excel(excel_file_path, engine='openpyxl')
    print(df.head())
# Import data into the database
    for index, row in df.iterrows():
        new_city = City(name=row['city'], country=row['country'])
        session.add(new_city)
    session.commit()
    session.close()

if __name__ == '__main__':
    load_cities()
    