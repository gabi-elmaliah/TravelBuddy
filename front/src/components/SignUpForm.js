
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import "./SignUpFormStyles.css";
import Button from '@mui/material/Button'; 


export default function SignUpForm() {
  const [email, setEmail] = useState("");
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null); // State to store error message
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevents the default form submission behavior

    try {
      const response = await axios.post('http://localhost:5000/sign-up', {
        email: email,
        user_name: userName,
        password: password,
      });

      if (response.status === 201) {
        // Save the token to localStorage
        localStorage.setItem('token', response.data.token);
        console.log("User created successfully");
        navigate('/questionnaire'); // Navigate to the home page on successful sign-up
      } else {
        setError(response.data.error); // Set error message from response
      }
    } catch (error) {
      console.error('There was an error!', error);
      if (error.response) {
        setError(error.response.data.error); // Set error message from catch
      } else {
        setError('An unexpected error occurred. Please try again later.');
      }
    }
  };
  return (
    <div className="wrapper signUp">
      <div className="form">
        <div className="heading">CREATE AN ACCOUNT</div>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="userName">Name</label>
            <input
              type="text"
              id="userName"
              placeholder="Enter your name"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
            />
          </div>
          <div>
            <label htmlFor="email">Email</label>
            <input
              type="text"
              id="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div>
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <Button  type="submit" variant="contained" color="primary">SignUp</Button>
          {error && <div className="error">{error}</div>} {/* Display error message */}
        </form>
        <div className="LoginLink">
          <p>
            Don't have an account? <Link to="/login">Login</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
