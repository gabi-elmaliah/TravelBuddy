import React from 'react';
import Footer from "../components/Footer";
import UserTrips from '../components/UserTripsComponent';

function UserTripsPage() {
  
  return (
    <div className="App">
      <div className="main-content">
        <UserTrips />
      </div>
      <Footer />
    </div>
  );
}

export default UserTripsPage;