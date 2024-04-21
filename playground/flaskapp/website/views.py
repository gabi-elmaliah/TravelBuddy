from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from .models import User, Questionnaire
from flask_login import login_required, current_user
from website import db


views=Blueprint('views',__name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html",user=current_user)
@views.route('/questionnaire',methods=['GET', 'POST'] )
def questionnaire():
    if request.method=="POST":
        user_id = current_user.id
        age_range = request.form.get('ageRange')
        openness = request.form.get('openness')
        conscientiousness=request.form.get('conscientiousness')
        extraversion=request.form.get('extraversion')
        agreeableness=request.form.get('agreeableness')
        neuroticism=request.form.get('neuroticism')
        activity_preference=request.form.get('activityPreferences')
        activity_historical = 'historical_sites' in request.form
        activity_outdoor = 'outdoor_adventures' in request.form
        activity_beach = 'relaxing_beach' in request.form
        activity_cuisine = 'local_cuisine' in request.form
        activity_cultural = 'cultural_events' in request.form


        questionnaire_object=Questionnaire(
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
            activity_cultural=activity_cultural,
        )

        db.session.add(questionnaire_object)
        db.session.commit()
        return redirect(url_for('views.home'))
        
    return render_template("questionnaire.html")

        





     
     
    



