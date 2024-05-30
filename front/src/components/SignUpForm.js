import React from "react";
import { Link } from "react-router-dom";
import "./SignUpFormStyles.css";

export default function SignUpForm() {
  return (
    <div className="wrapper signUp">
      <div className="form">
        <div className="heading">CREATE AN ACCOUNT</div>
        <form>
          <div>
            <label htmlFor="name"></label>
            <input type="text" id="name" placeholder="Enter your name" />
          </div>
          <div>
            <label htmlFor="name"></label>
            <input type="text" id="name" placeholder="Enter your mail" />
          </div>
          <div>
            <label htmlFor="password"></label>
            <input
              type="password"
              id="password"
              placeholder="Enter you password"
            />
          </div>
          <button type="submit">Submit</button>
          <a href="/" className="or"></a>
        </form>
        <p>
          Have an account ? <Link to="/login"> Login </Link>
        </p>
      </div>
    </div>
  );
}
