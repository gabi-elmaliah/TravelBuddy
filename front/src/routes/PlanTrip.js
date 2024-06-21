
import React, {useState} from 'react';
import  SearchBar  from "../components/SearchBar";
import SearchResultsList from '../components/SearchResultsList';
import "./PlanTrip.css";
import Navbar from "../components/Navbar";
import CalendarCfg from '../components/Calendar';
import 'react-calendar/dist/Calendar.css';
import Footer from '../components/Footer';


function PlanTrip(){
    const [results, setResults] = useState([]);

    return(   
        <>
        <Navbar />

        <div className="PlanTrip">
            <div className="search-bar-container">
            <SearchBar setResults={setResults} />
            <SearchResultsList results={results} />
            <CalendarCfg/>
            </div>
        </div>
        <Footer/>
        </>   
    );
    }


    export default PlanTrip