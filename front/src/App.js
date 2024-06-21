import React from 'react';
import "./styles.css";
import { Route, Routes } from "react-router-dom";
import Home from "./routes/Home";
import About from "./routes/About";
import Service from "./routes/Service";
import Contact from "./routes/Contact";
import SignUp from "./routes/SignUp";
import Login from "./routes/Login";
import Questionnaire from "./routes/Questionnaire";
import PlanTrip from "./routes/PlanTrip";

export default function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/service" element={<Service />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<Login/>} />
        <Route path="/questionnaire" element={<Questionnaire/>} /> 
        <Route path="/plantrip" element={<PlanTrip/>} /> 

      </Routes>

    </div>
  );
}
