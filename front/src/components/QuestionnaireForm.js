import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from "react-router-dom";

const QuestionnaireForm = () => {
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
  const navigate = useNavigate();

  const handlePreferenceChange = (e) => {
    setPreferences({
      ...preferences,
      [e.target.name]: e.target.checked,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

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
      activity_cultural:preferences.cultural
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
      console.error('There was an error submitting the questionnaire:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>What is your age:</label>
        <input
          type="number"
          value={age}
          onChange={(e) => setAge(e.target.value)}
        />
      </div>
      <div>
        <label>Rate your budget:</label>
        <select value={budget} onChange={(e) => setBudget(e.target.value)}>
          <option value="1">Low</option>
          <option value="2">Medium</option>
          <option value="3">High</option>
        </select>
      </div>
      <div>
        <label>I enjoy trying new things and experiencing variety in life</label>
        <select value={openness} onChange={(e) => setOpenness(e.target.value)}>
          <option value="1">Strongly disagree</option>
          <option value="2">Disagree</option>
          <option value="3">Neutral</option>
          <option value="4">Agree</option>
          <option value="5">Strongly agree</option>
        </select>
      </div>
      <div>
        <label>I like to plan things in advance and am well-organized</label>
        <select value={conscientiousness} onChange={(e) => setConscientiousness(e.target.value)}>
          <option value="1">Strongly disagree</option>
          <option value="2">Disagree</option>
          <option value="3">Neutral</option>
          <option value="4">Agree</option>
          <option value="5">Strongly agree</option>
        </select>
      </div>
      <div>
        <label>EI feel energized when interacting with a lot of peoplextraversion</label>
        <select value={extraversion} onChange={(e) => setExtraversion(e.target.value)}>
          <option value="1">Strongly disagree</option>
          <option value="2">Disagree</option>
          <option value="3">Neutral</option>
          <option value="4">Agree</option>
          <option value="5">Strongly agree</option>
        </select>
      </div>
      <div>
        <label>I consider myself empathetic and cooperative with others</label>
        <select value={agreeableness} onChange={(e) => setAgreeableness(e.target.value)}>
          <option value="1">Strongly disagree</option>
          <option value="2">Disagree</option>
          <option value="3">Neutral</option>
          <option value="4">Agree</option>
          <option value="5">Strongly agree</option>
        </select>
      </div>
      <div>
        <label>I often feel anxious or easily get upset over small things</label>
        <select value={neuroticism} onChange={(e) => setNeuroticism(e.target.value)}>
          <option value="1">Strongly disagree</option>
          <option value="2">Disagree</option>
          <option value="3">Neutral</option>
          <option value="4">Agree</option>
          <option value="5">Strongly agree</option>
        </select>
      </div>
      <div>
        <label>Travel Preferences:</label>
        <div>
          <input
            type="checkbox"
            name="historical"
            checked={preferences.historical}
            onChange={handlePreferenceChange}
          />
          <label>Exploring historical sites</label>
        </div>
        <div>
          <input
            type="checkbox"
            name="outdoor"
            checked={preferences.outdoor}
            onChange={handlePreferenceChange}
          />
          <label>Engaging in outdoor adventures (e.g., hiking, rafting)</label>
        </div>
        <div>
          <input
            type="checkbox"
            name="beach"
            checked={preferences.beach}
            onChange={handlePreferenceChange}
          />
          <label>Relaxing on a beach</label>
        </div>
        <div>
          <input
            type="checkbox"
            name="cuisine"
            checked={preferences.cuisine}
            onChange={handlePreferenceChange}
          />
          <label>Experiencing local cuisine and shopping</label>
        </div>
        <div>
          <input
            type="checkbox"
            name="cultural"
            checked={preferences.cultural}
            onChange={handlePreferenceChange}
          />
          <label>Participating in cultural events or festivals</label>
        </div>
      </div>
      <button type="submit">Submit</button>
    </form>
  );
};

export default QuestionnaireForm;
