from . import db
from flask_login import UserMixin


user_trips = db.Table('user_trips',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('trip_id', db.Integer, db.ForeignKey('trip.id'), primary_key=True)
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    user_name = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False) 
    cluster=db.Column(db.Integer)
    group = db.Column(db.Integer)  # New column added
    personality_profile = db.relationship('PersonalityProfile', backref='user', uselist=False, lazy='joined')
    preferences = db.relationship('UserPreferences', backref='user', uselist=False, lazy='joined')
    liked_trips = db.relationship('Trip', secondary=user_trips, backref='liked_by')

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

    # New fields for trip intentions
    intended_destination = db.Column(db.String(150))
    intended_start_date = db.Column(db.Date)
    intended_end_date = db.Column(db.Date)





class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(150), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    details = db.Column(db.Text, nullable=False)

    # Optionally link trips to clusters or individual user preferences
    #cluster_id = db.Column(db.Integer, db.ForeignKey('user.cluster'))


    def serialize(self):
        return {
            'id': self.id,
            'destination': self.destination,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'details': self.details
        }

class DailyTrip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cluster_id = db.Column(db.Integer, nullable=False)
    destination = db.Column(db.String(150), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    details = db.Column(db.Text, nullable=False)
# Helper function to fetch users in the same group
def get_users_in_group(group_number):
    return User.query.filter_by(group=group_number).all()

# Helper function to fetch trips for a group
def get_trips_for_group(group_number):
    return DailyTrip.query.filter_by(group=group_number).all()
    



    
    










