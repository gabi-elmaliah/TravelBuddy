import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHeart as farHeart } from '@fortawesome/free-regular-svg-icons';
import { faHeart as fasHeart } from '@fortawesome/free-solid-svg-icons';
import axios from "axios";



export default function LikeButton({tripDetails,userToken})
{
    const [liked, setLiked] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState(null);

    const toggleLike = async () => {
        if (liked) {
            setLiked(false);  // Optionally handle unlike
        } else {
            setIsSubmitting(true);
            try {
                const response = await axios.post('http://localhost:5000/like-trip', tripDetails, {
                    headers: {
                        'Content-Type': 'application/json',
                        'x-access-token': userToken 
                    }
                });
                setLiked(true);
                console.log(response.data.message);
            } catch (error) {
                if (error.response) {
                    // The request was made and the server responded with a status code
                    // that falls outside the range of 2xx
                    console.error('Error:', error.response.status, error.response.data);
                  } else if (error.request) {
                    // The request was made but no response was received
                    console.error('Request Error:', error.request);
                  } else {
                    // Something happened in setting up the request that triggered an Error
                    console.error('Error:', error.message);
                  }
                  console.error('Config:', error.config);
            } finally {
                setIsSubmitting(false);
            }
        }
    };

    return (
        <div>
            <button onClick={toggleLike} style={{ border: 'none', background: 'none' ,fontSize: '40px' }}>
                {liked ? <FontAwesomeIcon icon={fasHeart} style={{ color: 'red' }} />
                    : <FontAwesomeIcon icon={farHeart} style={{ color: 'red' , fontSize: '40px' }} />}
            </button>
            {isSubmitting && <span>Loading...</span>}
            {error && <div>Error: {error}</div>}        
        </div>
  );


}