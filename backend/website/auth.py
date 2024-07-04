from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify, session,make_response, current_app
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import datetime
import bcrypt
import jwt
import re
from functools import wraps


auth=Blueprint('auth',__name__)



def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None

        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']
        if not token:
            return jsonify({"message":"Token is missing"}),401
        try:
            data=jwt.decode(token,current_app.config['SECRET_KEY'])
            print(data)
            current_user=User.query.filter_by(id=data['user_id']).first()
        except Exception as e :
            print(e)
            return jsonify({'message':'Token is invalid, Please log in again '}),403
        
        return f(current_user,*args,**kwargs)
    
    return decorated


        

        

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password must be filled'}), 401
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({'message': 'User does not exist'}), 401
    
    if check_password_hash(user.password,password):
        token=jwt.encode({'user_id':user.id,'user_name':user.user_name,'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=24)},current_app.config['SECRET_KEY'])
        return jsonify({'token':token.decode("UTF-8")})
    
        
    return jsonify({'message': 'Wrong password'}), 401
    
    
    




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
    token=jwt.encode({'user_id':new_user.id,'user_name':user.user_name,'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=24)},current_app.config['SECRET_KEY'])
    # db.session.close()
    return jsonify({'token':token.decode("UTF-8")}),201







    



    


    


