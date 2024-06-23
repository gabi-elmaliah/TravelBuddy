import React from 'react';
import "./TripDetails.css"
import LikeButton from './LikeButton';


export default function TripDetails({trip,currentUserToken})
{
    if (!trip) return null;  // Render nothing if no trip data is available

    return (
        <div>
            <h1>Trip to: {trip.destination}</h1>
            <div>
                {trip.trip_details.map((day, index) => (
                    <div key={index} className="day">
                        <h3>Day {day.day}</h3>
                        {day.activities.map((activity, idx) => (
                            <div key={idx} className="activity">
                                <p>Time: {activity.time}</p>
                                <p>Activity: {activity.activity}</p>
                                <p>Description: {activity.description.overview}</p>
                            </div>
                        ))}
                    </div>
                ))}
            </div>
            <LikeButton tripDetails={{
                    destination: trip.destination,
                    start_date: trip.start_date,
                    end_date: trip.end_date,
                    trip_details: trip.trip_details
                    }} userToken={currentUserToken} />
            
        </div>
    );

 
}