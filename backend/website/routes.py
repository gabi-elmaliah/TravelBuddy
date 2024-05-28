from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from .models import User,  PersonalityProfile,UserPreferences
from website import db, db_path
from .auth import token_required
from .clustering import update_user_clusters
import logging
from  .db_utils import get_user_data
from .trip_planner import generate_trip,create_prompt

routes=Blueprint('routes',__name__)


         
@routes.route('/generate-trip', methods=['POST'])
@token_required
def make_trip(current_user):
    data = request.get_json()
    destination = data.get('destination')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if not destination or not start_date or not end_date:
        return jsonify({'error': 'Destination, start date, and end date are required'}), 400
    
    # Get user data
    user, personality_profile, user_preferences = get_user_data(current_user.id)

    # Create prompt for OpenAI API
    prompt =create_prompt(personality_profile, user_preferences, destination, start_date, end_date)
    print(type(prompt))
    # Generate trip details using OpenAI API
    try:
        trip_details =generate_trip(prompt)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Return the generated trip details
    return jsonify({
        'message': 'Trip generated successfully',
        'trip': trip_details
    }), 200





@routes.route('/submit-questionnaire', methods=['POST'])
@token_required
def submit_questionnaire(current_user):
    data = request.get_json()
    logging.debug("read from json")
    # Validate the data
    required_fields = ['age', 'budget', 'openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism',
                       'activity_historical', 'activity_outdoor', 'activity_beach', 'activity_cuisine', 'activity_cultural']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    print("before try")
    try:
        age = data['age']
        budget = data['budget']
        openness = data['openness']
        conscientiousness = data['conscientiousness']
        extraversion = data['extraversion']
        agreeableness = data['agreeableness']
        neuroticism = data['neuroticism']
        activity_historical = data['activity_historical']
        activity_outdoor = data['activity_outdoor']
        activity_beach = data['activity_beach']
        activity_cuisine = data['activity_cuisine']
        activity_cultural = data['activity_cultural']

        # Create or update PersonalityProfile
        print("personality profile")
        personality_profile = PersonalityProfile.query.filter_by(user_id=current_user.id).first()
        if not personality_profile:
            personality_profile = PersonalityProfile(user_id=current_user.id)
            db.session.add(personality_profile)
        
        personality_profile.age = age
        personality_profile.budget = budget
        personality_profile.openness = openness
        personality_profile.conscientiousness = conscientiousness
        personality_profile.extraversion = extraversion
        personality_profile.agreeableness = agreeableness
        personality_profile.neuroticism = neuroticism

        # Create or update UserPreferences
        print("prefences")
        preferences = UserPreferences.query.filter_by(user_id=current_user.id).first()
        if not preferences:
            preferences = UserPreferences(user_id=current_user.id)
            db.session.add(preferences)
        
        preferences.activity_historical = activity_historical
        preferences.activity_outdoor = activity_outdoor
        preferences.activity_beach = activity_beach
        preferences.activity_cuisine = activity_cuisine
        preferences.activity_cultural = activity_cultural

        db.session.commit()

        print("clustering:")
        update_user_clusters(db_path)

        return jsonify({'message': 'Questionnaire submitted successfully'}), 200

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    
 














