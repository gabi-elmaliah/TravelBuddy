import React, { useState } from 'react';
import axios from 'axios';

const TopUsersSelector = () => {
    const [topCount, setTopCount] = useState(5); // Default to top 5
    const [users, setUsers] = useState([]);
  
    const handleChange = async (event) => {
      setTopCount(event.target.value);
      const response = await axios.get(`http://localhost:5000/top-users?top_n=${topCount}`, {
        headers: {
          'x-access-token': localStorage.getItem('token') // Ensure the token is sent in the request
        }
      });
      setUsers(response.data); // Assuming the response data is the array of users
    };
  
    return (
      <div>
        <select onChange={handleChange} value={topCount}>
          <option value="5">Top 5</option>
          <option value="10">Top 10</option>
        </select>
        <div>
          {users.map((user, index) => (
            <div key={index}>
              <p>{user.user_name} - {user.email}</p>
            </div>
          ))}
        </div>
      </div>
    );
  };
  
  export default TopUsersSelector;
  








