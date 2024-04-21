from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from .models import User, Answer, City
from flask_login import login_required, current_user
from website import db,app


routes=Blueprint('routes',__name__)


@app.route('/search_cities', methods=['GET'])
def search_destinations():
    query = request.args.get('query', '')  # Get the search term from the query string
    if query:
        cities = City.query.filter(City.name.like(f'%{query}%')).all()  # Search for cities that match the query
        return jsonify([{'id': city.id, 'name': city.name, 'country': city.country} for city in cities])
    else:
        return jsonify({'message': 'No query provided'}), 400
    
 














