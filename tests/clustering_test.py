import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('/home/gabriel/TravelBuddy/Gabis_Webasite/backend/instance/database.db')

# Define the SQL query
query = """
SELECT 
    pp.age_range, 
    pp.openness, 
    pp.conscientiousness, 
    pp.extraversion, 
    pp.agreeableness, 
    pp.neuroticism,
    up.activity_historical,
    up.activity_outdoor,
    up.activity_beach,
    up.activity_cuisine,
    up.activity_cultural
FROM 
    user u
JOIN 
    personality_profile pp ON u.id = pp.user_id
JOIN 
    user_preferences up ON u.id = up.user_id;
"""

# Execute the query and load the data into a DataFrame
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()


# Display the first few rows of the DataFrame
print(df.head())