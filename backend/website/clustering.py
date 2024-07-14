import sqlite3
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from datetime import datetime

def convert_ordinal_to_date(ordinal_series):
    reference_date = datetime.strptime('2000-01-01', '%Y-%m-%d')  # Using January 1, 2000 as reference
    return ordinal_series.apply(lambda x: (reference_date + pd.Timedelta(days=x)).strftime('%Y-%m-%d'))

def convert_date_to_ordinal(date_series):
    reference_date = datetime.strptime('2000-01-01', '%Y-%m-%d')  # Using January 1, 2000 as reference
    date_series.head(30)
    return date_series.apply(lambda x: (datetime.strptime(x, '%Y-%m-%d') - reference_date).days)

def calculate_cluster_means(original_data, clustered_data):
    original_data['cluster'] = clustered_data['cluster']
    
    # Specify the attributes used in clustering
    attributes = ['age', 'openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism',
                  'budget', 'activity_historical', 'activity_outdoor', 'activity_beach', 'activity_cuisine', 'activity_cultural',
                  'intended_start_date', 'intended_end_date']

    # Ensure dates are converted to ordinal form
    original_data['intended_start_date'] = convert_date_to_ordinal(original_data['intended_start_date'])
    original_data['intended_end_date'] = convert_date_to_ordinal(original_data['intended_end_date'])
    
    # Calculate means for specified attributes
    cluster_means = original_data.groupby('cluster')[attributes].mean()
    cluster_means = cluster_means.round()

    # Convert the ordinal dates back to the original date format
    cluster_means['intended_start_date'] = convert_ordinal_to_date(cluster_means['intended_start_date'])
    cluster_means['intended_end_date'] = convert_ordinal_to_date(cluster_means['intended_end_date'])
    
    return cluster_means



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
        up.activity_cultural,
        up.intended_destination,
        up.intended_start_date,
        up.intended_end_date
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
    print("Fetched data:")
    print(data_df.head())
    return data_df

def preprocess_data(data_df):
    # Convert dates to ordinal based on a reference date
    data_df.isna().sum()
    data_df['intended_start_date'] = convert_date_to_ordinal(data_df['intended_start_date'])
    data_df['intended_end_date'] = convert_date_to_ordinal(data_df['intended_end_date'])


    features_to_scale = ['age', 'openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism',
                         'budget', 'activity_historical', 'activity_outdoor', 'activity_beach', 'activity_cuisine', 'activity_cultural',
                         'intended_start_date', 'intended_end_date']

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(data_df[features_to_scale])

    for i, col in enumerate(features_to_scale):
        data_df[col] = scaled_features[:, i]
    
    return data_df

def determine_n_clusters(group_size):
    if group_size < 10:
        return 2
    elif group_size < 20:
        return 3
    elif group_size < 50:
        return 4
    else:
        return 5
def assign_groups(data_df):
    data_df['group'] = data_df.groupby(['cluster']).cumcount() // 7 + 1
    return data_df

def cluster_users_by_destination(data_df):
    results = []
    cluster_offset = 0  # Initialize cluster offset

    for destination, group in data_df.groupby('intended_destination'):

        if len(group) < 2:
            continue  # Skip clustering if there are fewer than 2 samples
        
        features_to_scale = ['age', 'openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism',
                             'budget', 'activity_historical', 'activity_outdoor', 'activity_beach', 'activity_cuisine', 'activity_cultural',
                             'intended_start_date', 'intended_end_date']
        
        n_clusters = determine_n_clusters(len(group))
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        kmeans.fit(group[features_to_scale])
        group['cluster'] = kmeans.labels_ + cluster_offset  # Adjust cluster labels to be unique
        
        results.append(group)
        
        cluster_offset += n_clusters  # Update cluster offset for next destination

    return pd.concat(results)

def assign_groups(data_df):
    data_df['group'] = data_df.groupby(['cluster']).cumcount() // 7 + 1
    return data_df



def update_user_clusters_and_groups(db_path, data_df):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for index, row in data_df.iterrows():
        user_id = row['user_id']
        cluster_label = row['cluster']
        group_number = row['group']
        cursor.execute('UPDATE user SET cluster = ?, `group` = ? WHERE id = ?', (cluster_label, group_number, user_id))
    conn.commit()
    conn.close()



# Main function to perform the entire clustering process
def update_user_clusters(db_path):
    data_df = fetch_user_data(db_path)
    print("Fetched data:")
    data_df.tail(5)
    
    original_data = data_df.copy()  # Preserve original data for mean calculation
    print("original Data")
    original_data.head()
    
    preprocessed_data = preprocess_data(data_df.copy())
    print("Preprocessed data:")
    preprocessed_data.head(5)
    
    clustered_data = cluster_users_by_destination(preprocessed_data)
    grouped_data = assign_groups(clustered_data)
    
    update_user_clusters_and_groups(db_path, grouped_data)
    
    print("Clustered and grouped data:")
    grouped_data.head(5)
    
    cluster_means = calculate_cluster_means(original_data, grouped_data)
    print("Cluster means:")
    print(cluster_means)

    return cluster_means, original_data