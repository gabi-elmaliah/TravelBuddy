from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for,send_from_directory,current_app
from .models import User,  PersonalityProfile,UserPreferences,Trip
from website import db, db_path
from .auth import token_required
from .clustering import update_user_clusters
import logging
from  .db_utils import get_user_data
from .trip_planner import generate_trip,create_prompt
from .utils import calculate_similarity

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

@routes.route('/top-users', methods=['GET'])
@token_required
def top_users(current_user):

    top_n = request.args.get('top_n', default=5, type=int)

    # Fetch current user's profile and preferences
    current_user_profile = PersonalityProfile.query.filter_by(user_id=current_user.id).first()
    current_user_prefs = UserPreferences.query.filter_by(user_id=current_user.id).first()

    if not current_user_profile or not current_user_prefs:
        return jsonify({'error': 'You have to fill the questionnaire'}), 404

    # Fetch all users in the same cluster
    cluster_users = User.query.filter(User.cluster == current_user.cluster, User.id != current_user.id).all()

    similarities = []
    
    for user in cluster_users: 
        user_profile = PersonalityProfile.query.filter_by(user_id=user.id).first()
        user_prefs = UserPreferences.query.filter_by(user_id=user.id).first()
        
        similarity = calculate_similarity(current_user_profile, user_profile, current_user_prefs, user_prefs)
        similarities.append((user, similarity))

    # Sort users by similarity
    similarities.sort(key=lambda x: x[1])
    
    # Select the top N users
    top_users = [user for user, _ in similarities[:top_n]]

    # Prepare the response
    response = []
    for user in top_users:
        response.append({
            'user_name': user.user_name,
            'email': user.email
        })

    return jsonify(response), 200


@routes.route('/like-trip', methods=['POST'])
@token_required
def like_trip(current_user):
    data = request.get_json()
    trip_details = data.get('trip_details')
    destination = data.get('destination')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if not trip_details or not destination or not start_date or not end_date:
        return jsonify({'error': 'All trip details are required'}), 400

    # Save the trip to the database
    new_trip = Trip(
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        details=trip_details
    )

    db.session.add(new_trip)
    current_user.liked_trips.append(new_trip)
    db.session.commit()

    return jsonify({'message': 'Trip liked and saved successfully'}), 200



    
    





@routes.route('/submit-questionnaire', methods=['POST'])
@token_required
def submit_questionnaire(current_user):
    data = request.get_json()
    # Validate the data
    required_fields = ['age', 'budget', 'openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism',
                       'activity_historical', 'activity_outdoor', 'activity_beach', 'activity_cuisine', 'activity_cultural']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    try:
        age = int(data['age'])
        budget = int(data['budget'])
        openness = int(data['openness'])
        conscientiousness = int(data['conscientiousness'])
        extraversion = int(data['extraversion'])
        agreeableness = int(data['agreeableness'])
        neuroticism = int(data['neuroticism'])
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

    
 














