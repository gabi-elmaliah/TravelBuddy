# main.py

from website.trip_planner import generate_trips_for_clusters
from website.clustering import update_user_clusters

from website import db_path,create_app


# Create the Flask application
app = create_app()

# Run the script within the application context
with app.app_context():
    # Perform clustering and get cluster means
    cluster_means, original_data = update_user_clusters(db_path)

    # Generate trips for each cluster
    trips = generate_trips_for_clusters(cluster_means, original_data)

    # Output the generated trips for verification
    for cluster_id, trip in trips.items():
        print(f"Cluster {cluster_id}:")
        print(trip)

    