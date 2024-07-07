import React from 'react';
import Footer from "../components/Footer";
import Hero from "../components/Hero";
import Navbar from "../components/Navbar";
import DailyTripDetails from '../components/DailyTripDetails';

function Home() {

  
  return (
    <>
      <Hero
        cName="hero"
        heroImg="https://images.unsplash.com/photo-1539635278303-d4002c07eae3?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        title="Plan the perfect trip, find new friends for an unforgettable experience!"
        buttonText="Travel Plan"
        url="/login"
        btnClass="show"
      />
      
      <Footer />
    </>
  );
}

export default Home;
