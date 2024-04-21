from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify, session,make_response
from .models import User, Answer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db,app
import datetime
import bcrypt
import jwt
import re
from functools import wraps


auth=Blueprint('auth',__name__)

questions = [
    {
        "id": 1,
        "text": "Select an age range:",
        "options": ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
    },
    {
        "id": 2,
        "text": "I enjoy trying new things and experiencing variety in life:",
        "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
    },
    {
        "id": 3,
        "text": "I like to plan things in advance and am well-organized:",
        "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
    },
    {
        "id": 4,
        "text": "I feel energized when interacting with a lot of people:",
        "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
    },
    {
        "id": 5,
        "text": "I consider myself empathetic and cooperative with others:",
        "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
    },
    {
        "id": 6,
        "text": "I often feel anxious or easily get upset over small things:",
        "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
    },
    {
        "id": 7,
        "text": "Which of these activities interest you the most during a vacation? (Select all that apply)",
        "options": ["Exploring historical sites", "Engaging in outdoor adventures", "Relaxing on the beach", "Experiencing local cuisine and shopping", "Participating in cultural events or festivals"]
    }
]


def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None

        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']
        if not token:
            return jsonify({"message":"Token is missing"})
        try:
            data=jwt.decode(token,app.config['SECRET_KEY'])
            print(data)
            current_user=User.query.filter_by(id=data['user_id']).first()
        except Exception as e :
            print(e)
            return jsonify({'message':'Token is invalid '})
        
        return f(current_user,*args,**kwargs)
    
    return decorated


        

        

@auth.route('/login', methods=['POST'])
def login():
    
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return make_response('Could not verify',401,{"WWW-Autenthicate":"Basic Realm=Login required"})
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return make_response('Could not verify',401,{"WWW-Autenthicate":"Basic Realm=Login required"})
    
    if check_password_hash(user.password,password):
        token=jwt.encode({'user_id':user.id,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        return jsonify({'token':token.decode("UTF-8")})
    
    
    




@auth.route('/sign-up',methods=['POST'])
def sign_up():
    data=request.get_json()
    email = data.get('email')
    user_name = data.get('user_name')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'error': 'Email already in use'}), 409 
    new_user = User(email=email, user_name=user_name, password=generate_password_hash(password, method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()
    print(new_user)
    token=jwt.encode({'user_id':new_user.id,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
    db.session.close()
    return jsonify({'token':token.decode("UTF-8")}),201


@auth.route('/questionnaire',methods=['POST'] )
@token_required
def create_answer(current_user):
    answers=request.get_json()
    user_id = current_user.id
    age_range =answers.get('age_range')
    openness = answers.get('openness')
    conscientiousness = answers.get('conscientiousness')
    extraversion =answers.get('extraversion')
    agreeableness = answers.get('agreeableness')
    neuroticism = answers.get('neuroticism')
    activity_historical = answers.get('activity_historical')
    activity_outdoor = answers.get('activity_outdoor')
    activity_beach = answers.get('activity_beach')
    activity_cuisine =answers.get('activity_cusine')
    activity_cultural =answers.get('cultural')

    answer_object=Answer(
            user_id=user_id, 
            age_range=age_range,
            openness=openness,
            conscientiousness=conscientiousness,
            extraversion=extraversion,
            agreeableness=agreeableness,
            neuroticism=neuroticism,
            activity_historical=activity_historical,
            activity_outdoor=activity_outdoor,
            activity_beach=activity_beach,
            activity_cuisine=activity_cuisine,
            activity_cultural=activity_cultural
        )
    
    db.session.add(answer_object)
    db.session.commit()
    session.close()
    return jsonify({'message': 'Answer created successfully'}), 201

@auth.route('/questionnaire',methods=['Get'] )
@token_required
def get_questions(current_user):
    return jsonify({'questions':questions})


auth.route('/favoriteLocation',methods=['GET'])
@token_required

def get_favorite_location(current_user):


    return 




    



    


    


