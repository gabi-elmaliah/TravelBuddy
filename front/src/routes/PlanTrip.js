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
    const [tripDetails,setTripDetails]=useState(null);
    const [isPending,setIsPending]=useState(false);
    const [error,setError]=useState(null);


    useEffect(() => {
        console.log("StartDate has been set to:", startDate);
        console.log("EndDate has been set to:", endDate);
        // Any effect that needs to run when startDate or endDate changes
    }, [startDate, endDate]); 
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsPending(true);
        setError(null); 
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
            const response = await axios.post('http://localhost:5000/generate-tripsss', tripData,config);
            console.log("Response data:", response.data.trip);
            setTripDetails(JSON.parse(response.data.trip))
        } catch (error) {
            // Detailed error handling
            if (error.response) {
                // The request was made and the server responded with a status code
                // that falls outside the range of 2xx
                setError(`Error ${error.response.status}: ${error.response.data.message}`);
            } else if (error.request) {
                // The request was made but no response was received
                setError("Error: No response from the server.");
            } else {
                // Something happened in setting up the request that triggered an Error
                setError("Error: " + error.message);
            }
        } finally {
            setIsPending(false);  // Stop loading indicator regardless of the outcome
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
                {error &&  <div>{error}</div>}
                {isPending &&  <div>Loading...</div>}
                {error && <div className="error">{error}</div>}                
                <TripDetails trip={tripDetails} /> 
            </div>
        </div>
        <Footer/>
        </>   
    );
    }


    export default PlanTrip