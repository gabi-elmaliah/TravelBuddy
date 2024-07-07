import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './UserTripsComponent.css';
import TripDetailsModal from './TripDetailsModal.js';
import cities from '../cities.js';

export default function UserTrips()
{
    const [trips, setTrips] = useState([]);
    const [selectedTrip, setSelectedTrip] = useState(null);
    const [error, setError] = useState(null);
    const [message, setMessage] = useState(null); 
    const [loading, setLoading] = useState(true); 

    const currentUserToken = localStorage.getItem('token');

    useEffect(() => {
        const fetchTrips = async () => {
            try {
                const response = await axios.get('http://localhost:5000/user-trips', {
                    headers: {
                        'Content-Type': 'application/json',
                        'x-access-token': currentUserToken
                    }
                });
                if (response.data.message) {
                    setMessage(response.data.message);
                } else {
                    setTrips(response.data.trips);
                    setMessage(null); // Reset message state if trips are fetched
                }
                setError(null); // Reset error state if fetch is successful
            } catch (error) {
                // Detailed error handling
                if (error.response) {
                    setError(`Error ${error.response.status}: ${error.response.data.message}`);
                } else if (error.request) {
                    setError("Error: No response from the server.");
                } else {
                    setError("Error: " + error.message);
                }
                console.error('Error fetching trips:', error);
            } finally {
                setLoading(false); // Set loading to false once fetch is complete
            }
        };

        fetchTrips();
    }, [currentUserToken]);


    const handleCardClick = (trip) => {
        if (selectedTrip && selectedTrip.id === trip.id) {
            setSelectedTrip(null); 
        } else {
            setSelectedTrip(trip); 
        }
    };

    const handleDeleteClick = async (e,tripId) => {
        e.stopPropagation(); //
        try {
            const response = await axios.delete(`http://localhost:5000/unlike-trip/${tripId}`, {
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-token': currentUserToken
                }
            });
            if (response.status === 200) {
                setTrips(trips.filter(trip => trip.id !== tripId)); // Remove trip from state
            } else {
                console.error('Error unliking trip:', response.data);
            }
        } catch (error) {
            console.error('Error unliking trip:', error);
        }
    };



    const getCityImage = (cityName) => {
        const city = cities.find(city => city.name === cityName);
        return city ? city.imageUrl : 'https://example.com/images/default.jpg'; // Default image if not found
    };

    if (loading) {
        return <div>Loading...</div>; // Loading state
    }
    
    if (message) {
        return <div className="message">{message}</div>; // Message state
    }


    if (error) {
        return <div className="error-message">{error}</div>; // Error state
    }

   
    return (
        <>

            <div className="user-trips">
                <h1>My Trips</h1>
                <div className="cards-container">
                    {trips.map(trip => (
                        <div className="card" key={trip.id} onClick={() => handleCardClick(trip)}>
                            <img src={getCityImage(trip.destination)} alt={trip.destination} className="card-image" />
                            <h2>{trip.destination}</h2>
                            <p>{trip.start_date} - {trip.end_date}</p>
                            <button className="delete-button" onClick={(e) => handleDeleteClick(e,trip.id)}>Delete</button>
                        </div>
                    ))}
                </div>
                {selectedTrip && (
                    <TripDetailsModal trip={selectedTrip} onClose={() => setSelectedTrip(null)} />
                )}
            </div>
        </>
    );





}

