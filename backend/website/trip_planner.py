from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now you can safely retrieve the API key
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")
client = OpenAI(api_key=api_key)

def generate_trip_suggestion(user, data):
    # Combine the two functions to handle the full trip suggestion generation
    description = create_trip_description(user, data)
    suggestion = ask_openai_for_trip(description)
    return suggestion

def ask_openai_for_trip(prompt):
    try:
        # Assuming the 'client' has been set up with your OpenAI API key
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a travel guide the generate trips in JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error querying OpenAI: {e}")
        return "Sorry, I couldn't generate a trip suggestion right now."
    

def create_trip_description(user,data):
    personality = user.personality_profile
    preferences = user.preferences

    personality_desc = ""
    if personality:
        traits = [
            f"openness level of {personality.openness}" if personality.openness else "",
            f"conscientiousness level of {personality.conscientiousness}" if personality.conscientiousness else "",
            f"extraversion level of {personality.extraversion}" if personality.extraversion else "",
            f"agreeableness level of {personality.agreeableness}" if personality.agreeableness else "",
            f"neuroticism level of {personality.neuroticism}" if personality.neuroticism else ""
        ]
        # Filter out empty strings and join with commas
        personality_desc = " with a " + ", ".join(filter(None, traits))


        # Construct the preferences description
    preferences_desc = ""
    if preferences:
        preferred_activities = []
        if preferences.activity_historical:
            preferred_activities.append("historical sites")
        if preferences.activity_outdoor:
            preferred_activities.append("outdoor activities")
        if preferences.activity_beach:
            preferred_activities.append("beach relaxation")
        if preferences.activity_cuisine:
            preferred_activities.append("local cuisines")
        if preferences.activity_cultural:
            preferred_activities.append("cultural events")

        if preferred_activities:
            preferences_desc = " who enjoys " + ", ".join(preferred_activities)
     # Destination and dates
    destination = data.get('destination', 'a destination')
    start_date = data.get('start_date', 'a start date')
    end_date = data.get('end_date', 'an end date')

    # Combine all parts into one description
    trip_description = f"Create a travel plan for a person{personality_desc}{preferences_desc}, traveling to {destination} from {start_date} to {end_date}. Suggest activities, dining options, and local experiences that would suit their preferences and personality."
    
    return trip_description
        



    


