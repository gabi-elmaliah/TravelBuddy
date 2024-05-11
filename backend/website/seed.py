from . import db, create_app
from .models import User, PersonalityProfile, UserPreferences
from werkzeug.security import generate_password_hash
import random


app = create_app()

def generate_random_data():
    # Define the possible age ranges
    
    # Randomly select an age range
    age_range = random.randint(1,6)
    # Generate random values for personality traits
    traits = {
        'openness': random.randint(1, 5),
        'conscientiousness': random.randint(1, 5),
        'extraversion': random.randint(1, 5),
        'agreeableness': random.randint(1, 5),
        'neuroticism': random.randint(1, 5)
    }

    # Generate random preferences
    preferences = {
        'activity_historical': bool(random.getrandbits(1)),
        'activity_outdoor': bool(random.getrandbits(1)),
        'activity_beach': bool(random.getrandbits(1)),
        'activity_cuisine': bool(random.getrandbits(1)),
        'activity_cultural': bool(random.getrandbits(1))
    }

    return age_range, traits, preferences

def add_users(n):

    with app.app_context():  # Ensure the Flask app context is active
        for i in range(n):
            age_range, traits, prefs = generate_random_data()

            # Create a new user instance
            user = User(
                email=f'user{i}@example.com',  # Ensure uniqueness
                user_name=f'User{i}',
                password=generate_password_hash(f'ga21029{i}', method='pbkdf2:sha256')
            )
            db.session.add(user)
            db.session.flush()  # Flush to get the user ID

            # Create a personality profile including the age range
            personality = PersonalityProfile(
                user_id=user.id,
                age_range=age_range,
                **traits
            )

            # Create user preferences
            preferences = UserPreferences(
                user_id=user.id,
                **prefs
            )

            db.session.add(personality)
            db.session.add(preferences)
        db.session.commit()

if __name__ == '__main__':
    add_users(100)