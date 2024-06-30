import React, { useEffect, useState } from 'react';
import './DailyTripDetails.css'
import axios from 'axios';

export default function DailyTripDetails({setEndDate,setStartDate}) {
    const [tripDetails, setTripDetails] = useState(null);
    const [groupMembers, setGroupMembers] = useState([]);
    const [error, setError] = useState(null);


    useEffect(() => {
        // Fetch the trip details from your backend API using axios
        async function fetchTripDetails() {
          try {
            const response = await axios.get('http://localhost:5000/daily_trip'); 
            const data = response.data;
            setTripDetails(JSON.parse(response.data.trip.details));
            setGroupMembers(data.group_members);
          } catch (error) {
             // Detailed error handling
            if (error.response) {
            // The request was made and the server responded with a status code
            // that falls outside the range of 2xx
            setError(`Error ${error.response.status}: ${error.response.data.message}`);
          } else if (error.request) {
            // The request was made but no response was received
            setError("Error: No response from the server.");
          } else {
            // Something happened in setting up the request that triggered an Error
            setError("Error: " + error.message);
          }
          }
        }
        fetchTripDetails();
      }, []);
    
      if (!tripDetails) {
        return <div>Loading...</div>;
      }

      return (
        <div className="trip-details">
          <h2>Trip Details</h2>
          <p><strong>Start Date:</strong> {new Date(startDate).toLocaleDateString()}</p>
          <p><strong>End Date:</strong> {new Date(endDate).toLocaleDateString()}</p>
          <div className="trip-info">
            {tripDetails.map((day, dayIndex) => (
              <div key={dayIndex} className="trip-day">
                <h3>Day {dayIndex + 1}</h3>
                <div className="activities">
                  <h4>Activities:</h4>
                  {day.activities.map((activity, activityIndex) => (
                    <div key={activityIndex} className="activity">
                      <p><strong>Time:</strong> {activity.time}</p>
                      <p><strong>Activity:</strong> {activity.activity}</p>
                      <p><strong>Description:</strong> {activity.description.overview}</p>
                      <p><strong>Historical Significance:</strong> {activity.description.historical_significance}</p>
                      <p><strong>Tips:</strong> {activity.description.tips}</p>
                      <p><strong>Location Details:</strong> {activity.description.location_details}</p>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
          <div className="group-members">
            <h3>Group Members:</h3>
            {groupMembers.map((member, index) => (
              <p key={index}>{member.user_name} ({member.email})</p>
            ))}
          </div>
        </div>
      );

      




}