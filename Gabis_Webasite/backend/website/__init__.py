from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_bcrypt import Bcrypt 


db = SQLAlchemy()
DB_NAME = "database.db"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)
 

def create_app():

    from .routes import routes
    from .auth import auth


    app.register_blueprint(routes,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")



    with app.app_context():
        db.create_all()


    return app


    
