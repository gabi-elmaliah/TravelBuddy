from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .utils import get_database_path 
from flask_cors import CORS
from flask_migrate import Migrate


db_path =get_database_path()
db = SQLAlchemy()


 
def create_app():


    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    db.init_app(app)

    migrate = Migrate(app, db)

    # Import your models here
    from .models import User, PersonalityProfile, UserPreferences, Trip, DailyTrip, JoinedTrip


    from .routes import routes
    from .auth import auth


    app.register_blueprint(routes,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")



    with app.app_context():
        db.create_all()


    return app





    
