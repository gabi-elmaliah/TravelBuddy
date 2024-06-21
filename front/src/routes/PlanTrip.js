
import  SearchBar  from "../components/SearchBar";
import "./PlanTrip.css"
import React from 'react';


function PlanTrip(){

    return(   
        <div className="PlanTrip">
            <div className="search-bar-container">
                <SearchBar/>
                <div>Results</div>
            </div>
          
        </div>



    );
    }


    export default PlanTrip