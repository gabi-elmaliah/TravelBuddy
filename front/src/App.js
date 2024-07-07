import React, { useEffect, useState } from 'react';
import "./styles.css";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Home from "./routes/Home";
import About from "./routes/About";
import Service from "./routes/Service";
import Contact from "./routes/Contact";
import SignUp from "./routes/SignUp";
import Login from "./routes/Login";
import Questionnaire from "./routes/Questionnaire";
import PlanTrip from "./routes/PlanTrip";
import UserTripsPage from './routes/UserTripsPage';
import DailyTripPage from './routes/DailyTripPage';
import Navbar from "./components/Navbar";


export default function App() {

  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };
  return (
      <div className="App">
        <Navbar isAuthenticated={isAuthenticated} onLogout={handleLogout} />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/service" element={<Service />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/signup" element={<SignUp onLogin={handleLogin} />} />
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route path="/questionnaire" element={isAuthenticated ? <Questionnaire /> : <Navigate to="/login" />} />
          <Route path="/plantrip" element={isAuthenticated ? <PlanTrip /> : <Navigate to="/login" />} />
          <Route path="/userTrips" element={isAuthenticated ? <UserTripsPage /> : <Navigate to="/login" />} />
          <Route path="/dailytrip" element={isAuthenticated ? <DailyTripPage /> : <Navigate to="/login" />} />
        </Routes>
      </div>
  );
}
