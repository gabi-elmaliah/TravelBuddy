# TravelBuddy

**TravelBuddy** is a personalized trip planning web application that uses user personality and travel preferences to generate customized trip itineraries.

## Tech Stack

- **Frontend**: React, Axios
- **Backend**: Flask, SQLAlchemy
- **Database**: SQLite
- **API**: OpenAI GPT API (for trip generation)
- **Authentication**: JWT
- **Styling**: CSS (custom)

## Features

- User registration and login with JWT

- Personality and travel preferences questionnaire

- User clustering using the KMeans algorithm

- View top 5 or 10 similar users

- Generate AI-based trip itineraries using OpenAI

- Save and view liked trips

- Dashboard for questionnaire results and trip suggestions

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/gabi-elmaliah/TravelBuddy.git
cd TravelBuddy
```

### 2. Backend Setup (Flask)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

- The backend runs at: <http://localhost:5000>
- The SQLite database will be auto-generated at backend/instance/database.db

### 3. Frontend Setup (React)

```bash
Copy
Edit
cd front
npm install
npm start
```

### 4. Environment Configuration

Create a .env file in the backend/ directory with the following content:

OPENAI_API_KEY=your_openai_api_key_here

## API Endpoints

### Authentication

| Endpoint       | Method | Description                    |
|----------------|--------|--------------------------------|
| `/sign-up`     | POST   | Create a new user              |
| `/login`       | POST   | Authenticate user & return JWT |

---

### User Profile & Questionnaire

| Endpoint                  | Method | Auth Required | Description                                  |
|---------------------------|--------|----------------|----------------------------------------------|
| `/submit-questionnaire`   | POST   | ✅ Yes         | Submit user’s personality and preferences     |

---

### Trip Generation & Preferences

| Endpoint           | Method | Auth Required | Description                                     |
|--------------------|--------|----------------|-------------------------------------------------|
| `/generate-trip`   | POST   | ✅ Yes         | Generate a trip using OpenAI                    |
| `/like-trip`       | POST   | ✅ Yes         | Like a generated trip                           |
| `/unlike-trip/<id>`| DELETE | ✅ Yes         | Remove a liked trip                             |
| `/user-trips`      | GET    | ✅ Yes         | Get list of trips liked by the user             |

---

### Clustering & Social Features

| Endpoint           | Method | Auth Required | Description                                     |
|--------------------|--------|----------------|-------------------------------------------------|
| `/top-users`       | GET    | ✅ Yes         | Get top N most similar users in the same cluster|
| `/daily-trip`      | GET    | ✅ Yes         | Get the assigned daily trip based on cluster    |
| `/join-trip`       | POST   | ✅ Yes         | Join a group trip                               |
