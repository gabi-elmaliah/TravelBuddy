import React, { useEffect, useState } from 'react';
import './DailyTripDetails.css'
import axios from 'axios';

export default function DailyTripDetails() {
    const [tripDetails, setTripDetails] = useState([]);
    const [groupMembers, setGroupMembers] = useState([]);
    const [error, setError] = useState(null);
    const [destination,setDestination]=useState("")
    const [startDate, setStartDate] = useState(new Date());
    const [endDate, setEndDate] = useState(new Date());
    const [loading, setLoading] = useState(true);



    useEffect(() => {

        console.log('useEffect running'); // Add this log to ensure useEffect is running
        // Fetch the trip details from your backend API using axios
        async function fetchTripDetails() {
          try {

            console.log('Fetching trip details...'); // Add this log to ensure fetchTripDetails is called

            const response = await axios.get('http://localhost:5000/daily-trip',{

              headers: {
                'x-access-token': localStorage.getItem('token'), // Assuming token is stored in localStorage
              },

            }); 

            console.log('Response received:', response); // Log the response


            const data = response.data;
            console.log('Response data:', data); // Log the response data

            if (data.trip) {
              console.log('Un Parsed trip details:',data.trip.details); 
              const parsedDetails = JSON.parse(data.trip.details);
              const parsedTripDetails=JSON.parse(parsedDetails);

              console.log('Parsed trip details:', parsedTripDetails); // Log the parsed trip details

              setTripDetails(parsedTripDetails.trip_details);
              setStartDate(new Date(data.trip.start_date).toLocaleDateString());
              setEndDate(new Date(data.trip.end_date).toLocaleDateString());
              setDestination(data.trip.destination)
              setGroupMembers(data.group_members);
              console.log("Trip Details:",tripDetails )

          } else {
              setTripDetails(null);
          }
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
          finally{
            setLoading(false);
          }
        }
        fetchTripDetails();
      }, []);


    if (loading) {
      return <div>Loading...</div>;
  }
    
      
    if (!tripDetails) {
      return <div className="no-trip-message">You don't have a trip assigned yet. You will have a trip after tomorrow.</div>;
  }


      if (error) {
        return <div className="error-message">{error}</div>;
    }


      return (
        <div className="trip-details">
          <h2>Trip Details</h2>
          <p><strong>Destination:</strong> {destination}</p>
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