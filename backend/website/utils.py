import os 
import numpy as np





def get_project_root():
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def get_database_path():
    project_root = get_project_root()
    instance_dir = os.path.join(project_root, 'instance')
    
    # Ensure the instance directory exists
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir, exist_ok=True)
    
    return os.path.join(instance_dir, 'database.db')



def calculate_similarity(user1_profile, user2_profile, user1_prefs, user2_prefs):
    profile_attributes = ['age', 'openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism', 'budget']
    prefs_attributes = ['activity_historical', 'activity_outdoor', 'activity_beach', 'activity_cuisine', 'activity_cultural']
    
    profile_diff = np.array([getattr(user1_profile, attr) - getattr(user2_profile, attr) for attr in profile_attributes])
    prefs_diff = np.array([getattr(user1_prefs, attr) - getattr(user2_prefs, attr) for attr in prefs_attributes])
    
    distance = np.linalg.norm(profile_diff) + np.linalg.norm(prefs_diff)
    return distance
