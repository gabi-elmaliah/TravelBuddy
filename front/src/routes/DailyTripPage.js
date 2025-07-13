import React from 'react';
import Footer from "../components/Footer";
import DailyTripDetails from '../components/DailyTripDetails';

function DailyTripPage() {

  
  return (
    <div className="App">
      <div className="main-content">
        <DailyTripDetails />
      </div>
      <Footer />
    </div>
  );
}

export default DailyTripPage;
