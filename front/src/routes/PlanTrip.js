import React, {useState,useEffect} from 'react';
import  SearchBar  from "../components/SearchBar";
import SearchResultsList from '../components/SearchResultsList';
import "./PlanTrip.css";
import Navbar from "../components/Navbar";
import CalendarCfg from '../components/Calendar';
import 'react-calendar/dist/Calendar.css';
import Footer from '../components/Footer';
import TripDetails from '../components/TripDetails';
import AboutUs from '../components/AboutUs';
import axios from "axios";





function PlanTrip(){
    const [results, setResults] = useState([]);
    const [startDate, setStartDate] = useState(new Date());
    const [endDate, setEndDate] = useState(new Date());
    const [destination,setDestination]=useState("");
    const [tripDetails,setTripDetails]=useState(null)

    useEffect(() => {
        console.log("StartDate has been set to:", startDate);
        console.log("EndDate has been set to:", endDate);
        // Any effect that needs to run when startDate or endDate changes
    }, [startDate, endDate]); 
    



    

    const handleSubmit = async (e) => {
        e.preventDefault();
        const tripData = {
          destination:destination,  
          start_date: startDate,
          end_date: endDate
        };

        const config={
            headers:{
                'Content-Type': 'application/json',  // Specifies the content type of the request body
                'x-access-token': localStorage.getItem('token')
            }
        }


        try {
            const response = await axios.post('http://localhost:5000/generate-trip', tripData,config);
            console.log("Response data:", response.data.trip);
            console.log(typeof(response.data.trip))
            setTripDetails(JSON.parse(response.data.trip))
          } catch (error) {
            console.log("Error fetching trip data:", error);
          }
       
      };

    return(   
        <>
        <Navbar />
        <div className="PlanTrip">
            <div className="search-bar-container">
                <SearchBar setResults={setResults}  inputValue={destination} setInputValue={setDestination} />
                <SearchResultsList results={results} setDestination={setDestination} />
                <CalendarCfg  setStartDate={setStartDate} setEndDate={setEndDate} />
                <form onSubmit={handleSubmit}  >
                    <button type="submit" className="create-trip-btn">Create Me a Trip</button>
                </form>
                <TripDetails trip={tripDetails} /> 
            </div>
        </div>
        <Footer/>
        </>   
    );
    }


    export default PlanTrip