import React,{useState} from 'react'
import { FaSearch } from "react-icons/fa";
import "./SearchBar.css"
import axios from 'axios';


const SearchBar=()=> 
    {
    const [input,setInput]=useState("");


    const fetchData = (value) => 
    {

        axios.get('http/v1/geo/places?limit=5&offset=0?namePrefix={value}')
        .then(res=>console.log(res.data))
    };

    const handleChange=(value)=>{
        setInput(value)
        fetchData(value)
    };
    



  return (
    <div className='input-wrapper'>
           <FaSearch id="search-icon" />
           <input placeholder="select a city" value={input} onChange={(e)=>setInput(e.target.value)} />
    </div>
  );
};

export default SearchBar
