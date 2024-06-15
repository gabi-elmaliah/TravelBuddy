import React,{ useState }  from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import "./LoginFormStyles.css";



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
        console.log(response.data.message);
        navigate('/questionnaire');  // Navigate to a protected route on successful login

      } else {
        setError(response.data.message);  // Set error message from response
      }
    } catch (error) {
      console.error('There was an error!', error.response.data.message);
      setError(error.response.data.message);  // Set error message from catch
    }
  };

  return (
    <div className="wrapper signIn">
      <div className="illustration"></div>
      <div className="form">
        <div className="heading">LOGIN</div>
        <form onSubmit={handleSubmit}>
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
          <button type="submit">Submit</button>
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