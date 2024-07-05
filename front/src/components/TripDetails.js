import React from 'react';
import "./TripDetails.css"
import LikeButton from './LikeButton';


export default function TripDetails({trip,destination,startDate,endDate})
{
    if (!trip) return null;  // Render nothing if no trip data is available

    return (
        <div>
            <h1>Trip to: {destination}</h1>
            <div>
                {trip.trip_details.map((day, index) => (
                    <div key={index} className="day">
                        <h3>{day.day}</h3>
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
        
        </div>
    );

 
}