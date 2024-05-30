import sqlite3
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def fetch_user_data(db_path):
    # Connect to the SQLite database SSS
    conn = sqlite3.connect(db_path)
    
    query = """
    SELECT 
        u.id AS user_id, 
        pp.age,
        pp.openness, 
        pp.conscientiousness, 
        pp.extraversion, 
        pp.agreeableness, 
        pp.neuroticism,
        pp.budget,
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
        user_preferences up ON u.id = up.user_id
    """
    
    # Read data into a DataFrame
    data_df = pd.read_sql(query, conn)
    conn.close()
    return data_df

def preprocess_data(data_df):
    features_to_scale = ['age', 'openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism',
                         'budget', 'activity_historical', 'activity_outdoor', 'activity_beach', 'activity_cuisine', 'activity_cultural']

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(data_df[features_to_scale])

    for i, col in enumerate(features_to_scale):
        data_df[col] = scaled_features[:, i]
    
    return data_df

def cluster_and_update_db(db_path, data_df, n_clusters=5):
    features_to_scale = ['age', 'openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism',
                         'budget', 'activity_historical', 'activity_outdoor', 'activity_beach', 'activity_cuisine', 'activity_cultural']

    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans.fit(data_df[features_to_scale])
    data_df['cluster'] = kmeans.labels_

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor() 
    
    for index, row in data_df.iterrows():
        print(row['user_id'])
        user_id = row['user_id']
        cluster_label = row['cluster']
        conn.execute('UPDATE user SET cluster = ? WHERE id = ?', (cluster_label, user_id))
    conn.commit() # Create a cursor object to interact with the database
    
    # Fetch and print data from the user table
    print("User Table:")
    cursor.execute("SELECT * FROM user")  # Execute an SQL command to fetch all rows from the user table
    rows = cursor.fetchall()  # Fetch all rows from the executed query
    for row in rows:
        print(row)  # Print each row
    
    # Close the database connection
    conn.close()  # Close the connection to the database

    return data_df[['user_id', 'cluster']]



def update_user_clusters(db_path):
    # Fetch data from the database
    data_df = fetch_user_data(db_path)
    print("Fetched data:")
    print(data_df.tail(5))  # Display the first few rows of the DataFrame
    
    # Preprocess the data
    data_df = preprocess_data(data_df)
    print("Preprocessed data:")
    print(data_df.tail(5))  # Display the first few rows of the preprocessed DataFrame
    
    # Apply K-means clustering and update the database
    clustered_data = cluster_and_update_db(db_path, data_df)
    print("Clustered data:")
    print(clustered_data.tail(5))  # Display the updated DataFrame with clusters
    