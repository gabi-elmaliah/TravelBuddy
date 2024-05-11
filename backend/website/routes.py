from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from .models import User,  PersonalityProfile,UserPreferences,City
from website import db
from .auth import token_required
from .trip_planner import generate_trip_suggestion



routes=Blueprint('routes',__name__)

routes.route('/planTrip', methods=['POST'])
token_required
def plan_trip(current_user):
     data = request.get_json()
     destenation=data['destenation']
     start_data=data['start_date']
     end_data=data['end_date']
     
    
    
@routes.route('/generate-trip', methods=['POST'])
@token_required
def generate_trip(current_user):
    data = request.get_json()
    trip_suggestion = generate_trip_suggestion(current_user, data)
    return jsonify({'tripSuggestion': trip_suggestion}), 200



@routes.route('/search_cities', methods=['GET'])
@token_required
def search_destinations(current_user):
    query = request.args.get('query', '')  # Get the search term from the query string
    if query:
        cities = City.query.filter(City.name.like(f'%{query}%')).all()  # Search for cities that match the query
        return jsonify([{'id': city.id, 'name': city.name, 'country': city.country} for city in cities])
    else:
        return jsonify({'message': 'No query provided'}), 400
    

@routes.route('/submit-questionnaire', methods=['POST'])
@token_required
def submit_questionnaire(current_user):
    # Retrieve data from request
    data = request.get_json()
    return handle_questionnaire_submission(data, current_user)

def handle_questionnaire_submission(data, user):
    try:
        # Retrieve or create a PersonalityProfile for the user
        personality = PersonalityProfile.query.filter_by(user_id=user.id).first()
        if not personality:
            personality = PersonalityProfile(user_id=user.id)
            db.session.add(personality)

        # Update personality traits and age range
        personality_traits = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']
        for trait in personality_traits:
            if trait in data:
                setattr(personality, trait, data[trait])

        # Update age range
        if 'age_range' in data:
            personality.age_range = data['age_range']

        # Retrieve or create UserPreferences for the user
        preferences = UserPreferences.query.filter_by(user_id=user.id).first()
        if not preferences:
            preferences = UserPreferences(user_id=user.id)
            db.session.add(preferences)

        # Update user preferences
        preference_fields = ['activity_historical', 'activity_outdoor', 'activity_beach', 'activity_cuisine', 'activity_cultural']
        for field in preference_fields:
            if field in data:
                setattr(preferences, field, bool(data[field]))

        db.session.commit()
        return jsonify({'message': 'Questionnaire answers updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to submit questionnaire answers', 'details': str(e)}), 500

    
 














