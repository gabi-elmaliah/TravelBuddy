from flask import Flask,jsonify,request
from werkzeug.security import generate_password_hash, check_password_hash
from website import create_app
import logging



app=create_app()
if __name__ == '__main__':
    logging.basicConfig( format='%(lineno)d -%(message)s',level=logging.DEBUG)
    app.run(debug=True)
    
    
    