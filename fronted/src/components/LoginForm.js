import React from "react";
import { Link } from "react-router-dom";
import "./LoginFormStyles.css";

const preventRefresh = (e) => {
  e.preventDefault();
};

export default function LoginForm() {
  return (
    <div className="wrapper signIn">
      <div className="illustration"></div>
      <div className="form">
        <div className="heading">LOGIN</div>
        <form>
          <div>
            <label htmlFor="e-mail"></label>
            <input type="email" id="e-mail" placeholder="Enter you mail" />
          </div>
          <div>
            <label htmlFor="password"></label>
            <input
              type="text"
              id="password"
              placeholder="Enter your password"
            />
          </div>
          <button type="submit" onClick={preventRefresh}>
            Submit
          </button>
        </form>
        <p>
          Don't have an account ? <Link to="/signup"> Sign Up </Link>
        </p>
      </div>
    </div>
  );
}
