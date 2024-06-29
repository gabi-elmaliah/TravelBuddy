from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
from website.models import Trip, DailyTrip  # Assuming this imports the SQLAlchemy model
from website import db
import json


_ = load_dotenv(find_dotenv())
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)

def create_prompt_for_cluster(cluster_means, destination, start_date, end_date):

   

    prompt = f"""
     Create a detailed trip itinerary in JSON format for a group with the following average characteristics:

    Personality Profile:
    - Age: {cluster_means['age']}
    - Openness: {cluster_means['openness']}
    - Conscientiousness: {cluster_means['conscientiousness']}
    - Extraversion: {cluster_means['extraversion']}
    - Agreeableness: {cluster_means['agreeableness']}
    - Neuroticism: {cluster_means['neuroticism']}

    Preferences:
      Preferences:
    - Historical Sites: {'Yes' if cluster_means['activity_historical'] > 0.5 else 'No'}
    - Outdoor Adventures: {'Yes' if cluster_means['activity_outdoor'] > 0.5 else 'No'}
    - Beach: {'Yes' if cluster_means['activity_beach'] > 0.5 else 'No'}
    - Local Cuisine and Shopping: {'Yes' if cluster_means['activity_cuisine'] > 0.5 else 'No'}
    - Cultural Events or Festivals: {'Yes' if cluster_means['activity_cultural'] > 0.5 else 'No'}

    Destination: {destination}
    Dates: From {start_date} to {end_date}

    Provide the response in the following JSON format:
    

    {{
        "trip_details": 
        [
            {{
                // This is an example template. Please create similar entries for each day of the trip. 
                "day": "Example Day", // from the first day till the last day
                 "date": "Date Object", 
            
                 //Please provide a plan for each day that includes one or two activities:
                "activities": [
                    {{
                        "time": "Example time ", // example time
                        "activity": "Visit Historical Museum", // example activity
                        //example description
                        "description": {{
                            "overview": "Explore the rich history of the city at the Historical Museum.",  
                            "historical_significance": "The museum houses artifacts dating back to the Roman era.",
                            "tips": "Arrive early to avoid crowds. Don't miss the ancient coin exhibit.",
                            "location_details": "Located in the city center, easily accessible by public transport."
                        }}
                    }},
                    ...
                ]
            }},
            ...
        ]
    }}
    
    """
    return prompt



def generate_trip(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user","content":prompt}

        ]
    )

    trip_details= response.choices[0].message.content
    return trip_details

def store_trip(cluster_id, trip_details, destination, start_date, end_date):
    daily_trip = DailyTrip(
        cluster_id=cluster_id,
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        details=json.dumps(trip_details)
    )
    db.session.add(daily_trip)
    db.session.commit()

def generate_trips_for_clusters(cluster_means, original_data):
    destinations = original_data.groupby('cluster')['intended_destination'].first()
    start_dates = cluster_means['intended_start_date']
    end_dates = cluster_means['intended_end_date']
    trips = {}
    for cluster_id, means in cluster_means.iterrows():
        destination = destinations[cluster_id]
        start_date = start_dates[cluster_id]
        start_date_py=datetime.strptime(start_date,'%Y-%m-%d')
        print("the type of dates is :  ", type(start_date))
        print(f'The start date is {start_date}')
        end_date = end_dates[cluster_id]
        end_date_py=datetime.strptime(end_date,'%Y-%m-%d')
        prompt = create_prompt_for_cluster(means, destination, start_date, end_date)
        trip_details = generate_trip(prompt)
        store_trip(cluster_id, trip_details, destination, start_date_py, end_date_py)
        trips[cluster_id] = trip_details
    return trips

    

def get_all_trips_in_dates(start_date_str, end_date_str):
    # Convert the string dates to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    # Calculate the dates for one week before and one week after
    one_week_before = start_date - timedelta(days=7)
    one_week_after = end_date + timedelta(days=7)

    # Query trips that fall within the extended date range
    trips = Trip.query.filter(Trip.start_date >= one_week_before, Trip.end_date <= one_week_after).all()
    return trips


def get_destinations(name):
    # Query the Trip table to find all entries with the specified destination name
    trips = Trip.query.filter_by(destination=name).all()
    
    # Check if any trips were found
    if trips:
        # Use the serialize method from the Trip model
        trips_info = [trip.serialize() for trip in trips]
        return trips_info  # Return the list of serialized dictionaries directly
    else:
        return []  # Return an empty list if no trips were found
    


