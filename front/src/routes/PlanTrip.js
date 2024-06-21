import React, { useState } from 'react';
import   SearchBar  from "../components/SearchBar";
import SearchResultsList from '../components/SearchResultsList';
import "./PlanTrip.css"



function PlanTrip(){
    const [results, setResults] = useState([]);

    return(   
        <div className="PlanTrip">
            <div className="search-bar-container">
                <SearchBar setResults={setResults} />
                <SearchResultsList results={results} />
            </div>
          
        </div>



    );
    }


    export default PlanTrip