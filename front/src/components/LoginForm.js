
import React,{ useState }  from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import "./LoginFormStyles.css";
import Button from '@mui/material/Button'; 



const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null); // State to store error message
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();  // Prevents the default form submission behavior

    try {
      const response = await axios.post('http://localhost:5000/login', {
        email: email,
        password: password,
      });

      if (response.status === 200) {
        // Save the token to localStorage
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('user_name', response.data.user_name);
        console.log(response.data.message);
        navigate('/');  // Navigate to a protected route on successful login

      } else {
        setError(response.data.message);  // Set error message from response
      }
    } catch (error) {
      // Check if the response exists in the error object
      if (error.response) {
        // Handle the case where the server responds with a status outside the 2xx range
        setError("Login failed: " + error.response.data.message);
      } else if (error.request) {
        // Handle the case where the request was made but no response was received
        setError("No response from the server. Please try again later.");
      } else {
        // Handle other errors like setting up the request that triggered an Error
        setError("Error: " + error.message);
      }
      console.error('Error during form submission:', error);
    }
  };

  return (
    <div className="wrapper signIn">
      <div className="illustration"></div>
      <div className="form">
        <div className="heading">LOGIN</div>
        <form  onSubmit={handleSubmit} >
          <div>
            <label htmlFor="e-mail"></label>
            <input
              type="email"
              id="e-mail"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div>
            <label htmlFor="password"></label>
            <input
              type="password"
              id="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <Button  type="submit" variant="contained" color="primary">Login</Button>
        </form>
        {error && <div className="error">{error}</div>} {/* Display error message */}
        <p>
          Don't have an account? <Link to="/signup">Sign Up</Link>
        </p>
      </div>
    </div>
  );
};

export default LoginForm;