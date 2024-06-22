import React,{useState} from 'react'
import { FaSearch } from "react-icons/fa";
import cities from "../cities.js"
import "./SearchBar.css"


const SearchBar=({setResults,setInputValue,inputValue})=> 
  {
  
    const fetchData = (value) => {
      if (!value) {
        setResults([]);
        return;
      }
  
      const lowercasedValue = value.toLowerCase();
      const results = cities.filter(city =>
        city.name.toLowerCase().includes(lowercasedValue)
      );
      setResults(results);
    };

    // eslint-disable-next-line
    const handleChange=(value)=>{
        setInputValue(value)
        fetchData(value)
    };


    return (
      <div className="input-wrapper">
        <FaSearch id="search-icon" />
        <input
          placeholder="Type to search..."
          value={inputValue}
          onChange={(e) => handleChange(e.target.value)}
        />
      </div>
    );


};
  
export default SearchBar
