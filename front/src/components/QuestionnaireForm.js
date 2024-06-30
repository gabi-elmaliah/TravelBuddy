
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import './QuestionnaireForm.css'; // Import the CSS module
import CalendarCfg from './Calendar';
import 'react-calendar/dist/Calendar.css';
import SearchBar from "./SearchBar";
import cities from "../cities"
import SearchResultsList from './SearchResultsList';


const QuestionnaireForm = () => {
  const navigate = useNavigate();
  const [age, setAge] = useState('');
  const [budget, setBudget] = useState('');
  const [openness, setOpenness] = useState('');
  const [conscientiousness, setConscientiousness] = useState('');
  const [extraversion, setExtraversion] = useState('');
  const [agreeableness, setAgreeableness] = useState('');
  const [neuroticism, setNeuroticism] = useState('');
  const [preferences, setPreferences] = useState({
    historical: false,
    outdoor: false,
    beach: false,
    cuisine: false,
    cultural: false,
  });
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [results, setResults] = useState([]);
  const [showResults, setShowResults] = useState(false);
  const [destination, setDestination] = useState('');
  const [error, setError] = useState('');


  const handleSetDestination = (destination) => {
    setDestination(destination);
    setShowResults(false); // Hide the results list when a destination is selected
};


  
  const handlePreferenceChange = (e) => {
    setPreferences({
      ...preferences,
      [e.target.name]: e.target.checked,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
     // Validate required fields
     if (!age || !destination) {
      setError('Age and destination are required fields.');
      return;
    }

     // Validate age range
     if (age < 20 || age > 60) {
      setError('Age must be between 20 and 60.');
      return;
    }

     // Validate destination
     const validDestinations = cities.map(city => city.name);
     if (!validDestinations.includes(destination)) {
       setError('Please select a valid destination from the list.');
       return;
     }

     // Validate start date and end date
    if (!startDate || !endDate) {
      setError('Please select both start date and end date.');
      return;
    }

    const data = {
      age,
      budget,
      openness,
      conscientiousness,
      extraversion,
      agreeableness,
      neuroticism,
      activity_historical: preferences.historical,
      activity_outdoor: preferences.outdoor,
      activity_beach:preferences.beach,
      activity_cuisine: preferences.cuisine,
      activity_cultural:preferences.cultural,
      destination:destination,  
      start_date: startDate,
      end_date: endDate
    };

    try {
      const response = await axios.post('http://localhost:5000/submit-questionnaire', data, 
        {
        headers: {
          'Content-Type': 'application/json',
          'x-access-token': localStorage.getItem('token'), // Assuming token is stored in localStorage
        },
      });

      if (response.status === 200) {
        console.log('Questionnaire submitted successfully');
        navigate('/');
      }
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
    }
  };

  return (

    <>

<div className="questionnaire-form-element search-bar-container">
        <label>Destination:</label>
        <SearchBar 
          setResults={setResults}
          setInputValue={setDestination}
          inputValue={destination}
          setShowResults={setShowResults}
        />
        {showResults && <SearchResultsList results={results} setDestination={handleSetDestination} />}
        <label>Select the Dates of the trip</label>
        <CalendarCfg setStartDate={setStartDate} setEndDate={setEndDate} />
  </div>





  <form onSubmit={handleSubmit} className="questionnaire-form-container">

<div className="questionnaire-form-element">
  <label>What is your age:</label>
  <input 
    type="number" 
    min={18} 
    max={60} 
    value={age} 
    onChange={(e) => setAge(e.target.value)} 
    className="questionnaire-age-input" 
    placeholder="Type your age…" 
  />
</div>

<div className="questionnaire-form-element">
  <label>Rate your budget:</label>
  <select value={budget} onChange={(e) => setBudget(e.target.value)} className="questionnaire-select-input">
    <option value="1">Low</option>
    <option value="2">Medium</option>
    <option value="3">High</option>
  </select>
</div>

<div className="questionnaire-form-element">
  <label>I enjoy trying new things and experiencing variety in life</label>
  <select value={openness} onChange={(e) => setOpenness(e.target.value)} className="questionnaire-select-input">
    <option value="1">Strongly disagree</option>
    <option value="2">Disagree</option>
    <option value="3">Neutral</option>
    <option value="4">Agree</option>
    <option value="5">Strongly agree</option>
  </select>
</div>

<div className="questionnaire-form-element">
  <label>I like to plan things in advance and am well-organized</label>
  <select value={conscientiousness} onChange={(e) => setConscientiousness(e.target.value)} className="questionnaire-select-input">
    <option value="1">Strongly disagree</option>
    <option value="2">Disagree</option>
    <option value="3">Neutral</option>
    <option value="4">Agree</option>
    <option value="5">Strongly agree</option>
  </select>
</div>

<div className="questionnaire-form-element">
  <label>I feel energized when interacting with a lot of people</label>
  <select value={extraversion} onChange={(e) => setExtraversion(e.target.value)} className="questionnaire-select-input">
    <option value="1">Strongly disagree</option>
    <option value="2">Disagree</option>
    <option value="3">Neutral</option>
    <option value="4">Agree</option>
    <option value="5">Strongly agree</option>
  </select>
</div>

<div className="questionnaire-form-element">
  <label>I consider myself empathetic and cooperative with others</label>
  <select value={agreeableness} onChange={(e) => setAgreeableness(e.target.value)} className="questionnaire-select-input">
    <option value="1">Strongly disagree</option>
    <option value="2">Disagree</option>
    <option value="3">Neutral</option>
    <option value="4">Agree</option>
    <option value="5">Strongly agree</option>
  </select>
</div>

<div className="questionnaire-form-element">
  <label>I often feel anxious or easily get upset over small things</label>
  <select value={neuroticism} onChange={(e) => setNeuroticism(e.target.value)} className="questionnaire-select-input">
    <option value="1">Strongly disagree</option>
    <option value="2">Disagree</option>
    <option value="3">Neutral</option>
    <option value="4">Agree</option>
    <option value="5">Strongly agree</option>
  </select>
</div>

<div className="questionnaire-form-element">
  <label>Travel Preferences:</label>
  <div className="questionnaire-preferences-container">
    <div className="questionnaire-preference-item">
      <input
        type="checkbox"
        name="historical"
        checked={preferences.historical}
        onChange={handlePreferenceChange}
      />
      <label>Exploring historical sites</label>
    </div>
    <div className="questionnaire-preference-item">
      <input
        type="checkbox"
        name="outdoor"
        checked={preferences.outdoor}
        onChange={handlePreferenceChange}
      />
      <label>Engaging in outdoor adventures (e.g., hiking, rafting)</label>
    </div>
    <div className="questionnaire-preference-item">
      <input
        type="checkbox"
        name="beach"
        checked={preferences.beach}
        onChange={handlePreferenceChange}
      />
      <label>Relaxing on a beach</label>
    </div>
    <div className="questionnaire-preference-item">
      <input
        type="checkbox"
        name="cuisine"
        checked={preferences.cuisine}
        onChange={handlePreferenceChange}
      />
      <label>Experiencing local cuisine and shopping</label>
    </div>
    <div className="questionnaire-preference-item">
      <input
        type="checkbox"
        name="cultural"
        checked={preferences.cultural}
        onChange={handlePreferenceChange}
      />
      <label>Participating in cultural events or festivals</label>
    </div>
  </div>
</div>

{error && <div className="error-message">{error}</div>}
<button type="submit" className="questionnaire-form-button">Submit</button>

</form>



    
    </>

    
    


    
    
  );
};

export default QuestionnaireForm;
