from openai import OpenAI
import os
from dotenv import load_dotenv,find_dotenv
import datetime

_ = load_dotenv(find_dotenv())
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)

def create_prompt(personality_profile, user_preferences, destination, start_date, end_date):

   

    prompt = f"""
    Create a detailed trip itinerary in JSON format for a user with the following characteristics:

    Personality Profile:
    - Age: {personality_profile.age}
    - Openness: {personality_profile.openness}
    - Conscientiousness: {personality_profile.conscientiousness}
    - Extraversion: {personality_profile.extraversion}
    - Agreeableness: {personality_profile.agreeableness}
    - Neuroticism: {personality_profile.neuroticism}

    Preferences:
    - Historical Sites: {'Yes' if user_preferences.activity_historical else 'No'}
    - Outdoor Adventures: {'Yes' if user_preferences.activity_outdoor else 'No'}
    - Beach: {'Yes' if user_preferences.activity_beach else 'No'}
    - Local Cuisine and Shopping: {'Yes' if user_preferences.activity_cuisine else 'No'}
    - Cultural Events or Festivals: {'Yes' if user_preferences.activity_cultural else 'No'}

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



