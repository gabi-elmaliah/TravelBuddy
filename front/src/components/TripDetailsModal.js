import React from 'react';
import './TripDetailsModal.css';

const TripDetailsModal = ({ trip,onClose }) => {
    return (
        <div className="modal-content" onClick={onClose} >
            <h2>Trip to {trip.destination}</h2>
            <p>{trip.start_date} - {trip.end_date}</p>
            <div className="trip-details">
                {trip.details && JSON.parse(trip.details).trip_details.map((day, index) => (
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
};

export default TripDetailsModal;