from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for,send_from_directory,current_app
from .models import User,  PersonalityProfile,UserPreferences,Trip,DailyTrip,JoinedTrip,user_trips
from website import db, db_path
from .auth import token_required
from .clustering import update_user_clusters
from datetime import datetime
from  .db_utils import get_user_data
from .trip_planner import generate_trip,create_prompt
from .utils import calculate_similarity,parse_iso_date
import json
import logging
from sqlalchemy.exc import SQLAlchemyError



routes=Blueprint('routes',__name__)



         
@routes.route('/generate-trip', methods=['POST'])
@token_required
def make_trip(current_user):
    data = request.get_json()
    destination = data.get('destination')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')

    if not destination or not start_date_str or not end_date_str:
        return jsonify({'error': 'Destination, start date, and end date are required'}), 400
    
    try:
        # Convert string dates to datetime objects and then to date objects
        start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%S.%fZ").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M:%S.%fZ").date()


        # Get user data
        user, personality_profile, user_preferences = get_user_data(current_user.id)
        if not personality_profile or not user_preferences:
            return jsonify({'error': 'Personality profile and user preferences are required'}), 400

        # Create prompt for OpenAI API
        prompt = create_prompt(personality_profile, user_preferences, destination, start_date, end_date)
        logging.info(f"Prompt created: {prompt}")
        
        # Generate trip details using OpenAI API
        trip_details = generate_trip(prompt)
        logging.info(f"Generated trip details: {trip_details}")

        new_trip = Trip(
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            details=trip_details  # Store the JSON string
        )
        db.session.add(new_trip)
        db.session.commit()
        logging.info(f"New trip committed to database with ID: {new_trip.id}")

    except Exception as e:
        logging.error(f"Error in make_trip: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    # Return the generated trip details
    return jsonify({
        'message': 'Trip generated successfully',
        'trip': {
            'id': new_trip.id,
            'details': trip_details
        }
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
    try:
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        trip_id = data['tripid']  # Assuming tripid is sent from the frontend
        trip = Trip.query.get(trip_id)

        if not trip:
            return jsonify({'error': 'Trip not found'}), 404

        if trip in current_user.liked_trips:
            return jsonify({'message': 'Trip already liked'}), 200

        current_user.liked_trips.append(trip)
        db.session.commit()

        return jsonify({'message': 'Trip liked successfully'}), 200

    except KeyError as e:
        db.session.rollback()
        return jsonify({'error': 'Missing necessary parameter: ' + str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error: ' + str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error processing request: ' + str(e)}), 500

@routes.route('/unlike-trip/<int:trip_id>', methods=['DELETE'])
@token_required
def unlike_trip(current_user, trip_id):
    try:
        print(f"User {current_user.id} attempting to unlike trip {trip_id}")
        trip = Trip.query.get(trip_id)
        if not trip:
            print(f"Trip with ID {trip_id} not found")
            return jsonify({'error': 'Trip not found'}), 404

        if trip not in current_user.liked_trips:
            print(f"Trip with ID {trip_id} not liked by user {current_user.id}")
            return jsonify({'error': 'Trip not liked by user'}), 400

        current_user.liked_trips.remove(trip)
        db.session.commit()
        print(f"Trip with ID {trip_id} unliked successfully")
        return jsonify({'message': 'Trip unliked successfully'}), 200
    except Exception as e:
        print(f"Error unliking trip: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@routes.route('/daily-trip', methods=['GET'])
@token_required
def get_daily_trip(current_user):
    user = current_user
    daily_trip = DailyTrip.query.filter_by(cluster_id=user.cluster).first()
    if not daily_trip:
         return jsonify({"message": "You don't have a trip assigned yet. Please fill out the questionnaire, and you'll get your trip tomorrow."}), 200

    group_members = User.query.filter_by(cluster=user.cluster, group=user.group).all()
    group_member_info = [{'user_name': member.user_name, 'email': member.email} for member in group_members]

    joined_members = JoinedTrip.query.filter_by(trip_id=daily_trip.id).all()
    joined_member_info = [{"user_name": User.query.get(j.user_id).user_name} for j in joined_members if User.query.get(j.user_id).group == current_user.group and User.query.get(j.user_id).cluster == current_user.cluster]


    return jsonify({
        "trip": {
            "id": daily_trip.id,
            "destination": daily_trip.destination,
            "start_date": daily_trip.start_date.isoformat(),
            "end_date": daily_trip.end_date.isoformat(),
            "details": daily_trip.details
        },
        "group_members": group_member_info,
        "joined_members": joined_member_info
    })

@routes.route('/submit-questionnaire', methods=['POST'])
@token_required
def submit_questionnaire(current_user):
    data = request.get_json()
    print(data)
    # Validate the data
    required_fields = ['age', 'budget', 'openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism',
                       'activity_historical', 'activity_outdoor', 'activity_beach', 'activity_cuisine', 'activity_cultural','destination',
                       'start_date','end_date']
    
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
        destination=data['destination']
        start_date_str=data['start_date']
        end_date_str=data['end_date']


        # Convert date strings to date objects (strip the time part)
        start_date = datetime.strptime(start_date_str.split('T')[0], '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str.split('T')[0], '%Y-%m-%d').date()

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
        preferences.intended_destination = destination
        preferences.intended_start_date = start_date
        preferences.intended_end_date = end_date


        db.session.commit()

        return jsonify({'message': 'Questionnaire submitted successfully'}), 200

    except Exception as e:
        print("Error occurred:", str(e))  # Log error
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    
 
@routes.route('/join-trip', methods=['POST'])
@token_required
def join_trip(current_user):
    data = request.get_json()
    trip_id = data.get('trip_id')

    if not trip_id:
        return jsonify({'error': 'Trip ID is required'}), 400

    # Check if the user already joined the trip
    existing_join = JoinedTrip.query.filter_by(user_id=current_user.id, trip_id=trip_id).first()
    if existing_join:
        return jsonify({'message': 'You have already joined this trip'}), 200

    # Create a new join entry
    new_join = JoinedTrip(user_id=current_user.id, trip_id=trip_id)
    db.session.add(new_join)
    db.session.commit()

    return jsonify({'message': 'Trip joined successfully'}), 200


@routes.route('/user-trips', methods=['GET'])
@token_required
def user_trips(current_user):
    try:
        trips = current_user.liked_trips

        if not trips:
            return jsonify({'message': 'You do not have any trips yet.'}), 200

        trips_data = [{
            'id': trip.id,
            'destination': trip.destination,
            'start_date': trip.start_date.strftime('%Y-%m-%d'),
            'end_date': trip.end_date.strftime('%Y-%m-%d'),
            'details': trip.details
        } for trip in trips]
        
        return jsonify({'trips': trips_data}), 200
    

    except Exception as e:
        logging.error(f"Error fetching user trips: {str(e)}")
        return jsonify({'error': 'Error fetching trips'}), 500














