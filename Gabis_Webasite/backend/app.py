from flask import Flask,jsonify,request
from werkzeug.security import generate_password_hash, check_password_hash
from website import create_app
from flask_cors import CORS




app=create_app()
if __name__ == '__main__':
    app.run()
    