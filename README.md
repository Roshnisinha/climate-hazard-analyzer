# 🌡️ Climate Hazard Analyzer

A full-stack climate intelligence application that analyzes historical temperature data, detects extreme heat events, and classifies heat risk for a selected geographic location and date range.

**Live Demo:** [Climate Hazard Analyzer](https://climate-hazard-analyzer-oorx.vercel.app/)

**Backend API:** [Render API](https://climate-hazard-analyzer-6vcw.onrender.com)

**API Documentation:** [Interactive Swagger Docs](https://climate-hazard-analyzer-6vcw.onrender.com/docs)

**Health Check:** [API Health](https://climate-hazard-analyzer-6vcw.onrender.com/health)

---

## 📌 Overview

Climate Hazard Analyzer is a full-stack web application designed to make historical temperature analysis accessible through an interactive interface.

Users can enter latitude and longitude coordinates and select a date range to retrieve historical weather data. The backend processes daily maximum temperatures, calculates extreme heat indicators, identifies heatwave events, and assigns an overall heat risk level.

The application uses historical weather data from the Open-Meteo API and processes it using Python and Pandas.

## ✨ Features

- 📍 Location-based analysis using latitude and longitude.
- 📅 Custom date range selection.
- 🌡️ Average, highest, and lowest daily maximum temperature calculations.
- 🔥 Detection and counting of extreme heat days.
- 📊 Extreme heat percentage calculation.
- 🌞 Heatwave detection based on consecutive extreme heat days.
- ⚠️ Automated heat risk classification.
- 📈 Interactive climate data visualization.
- 📋 Historical weather data retrieval through REST APIs.
- ✅ Data coverage and missing-day statistics.
- 🔌 FastAPI backend with interactive API documentation.
- 🌐 Production deployment using Vercel and Render.

## 🛠️ Tech Stack

### Frontend
- React
- JavaScript
- Vite
- Recharts
- CSS

### Backend
- Python
- FastAPI
- Pandas
- HTTPX
- Uvicorn

### External API
- [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)

### Deployment
- Vercel – Frontend hosting
- Render – Backend hosting
- GitHub – Version control

## 🧠 Analysis Methodology

The application analyzes daily maximum temperature records and calculates climate indicators using the following rules.

### 1. Extreme Heat Detection

A day is classified as an extreme heat day when its maximum temperature is greater than or equal to 35°C.

### 2. Heatwave Detection

A heatwave is defined as three or more consecutive days with maximum temperatures greater than or equal to 35°C.

The backend calculates:
- Total number of heatwave events.
- Duration of each qualifying heatwave.
- Longest heatwave duration.

### 3. Heat Risk Classification

Risk levels are assigned according to the percentage of extreme heat days.

| Extreme Heat Percentage | Risk Level |
|---|---|
| Below 5% | Low |
| 5% to below 15% | Moderate |
| 15% or above | High |

### 4. Data Coverage

The backend calculates data coverage by comparing the number of valid temperature records returned with the expected number of calendar days in the selected date range.

## 📊 Sample Analysis Result

The following is an actual successful production API response for Nashik, India.

**Location:** 19.9975° N, 73.7898° E  
**Period:** January 2015 – December 2020

| Metric | Result |
|---|---:|
| Total Days | 2,192 |
| Expected Days | 2,192 |
| Missing Days | 0 |
| Data Coverage | 100% |
| Average Maximum Temperature | 30.02°C |
| Highest Temperature | 41.7°C |
| Lowest Daily Maximum Temperature | 21.9°C |
| Extreme Heat Days | 380 |
| Extreme Heat Percentage | 17.34% |
| Heatwave Count | 22 |
| Longest Heatwave | 51 days |
| Risk Level | High |

## 🔌 API Endpoints

The backend exposes the following REST API endpoints.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message and version |
| GET | `/health` | Health check |
| GET | `/weather` | Retrieve historical daily weather data |
| GET | `/analyze` | Analyze temperature data and calculate heat risk |

### Analyze Endpoint

**Request:**

```http
GET /analyze?latitude=19.9975&longitude=73.7898&start_date=2015-01-01&end_date=2020-12-31
```

**Query Parameters:**

| Parameter | Type | Description |
|---|---|---|
| latitude | Float | Latitude between -90 and 90 |
| longitude | Float | Longitude between -180 and 180 |
| start_date | Date | Start date in YYYY-MM-DD format |
| end_date | Date | End date in YYYY-MM-DD format |

**Example Response:**

```json
{
  "location": {
    "latitude": 19.9975,
    "longitude": 73.7898
  },
  "period": {
    "start_date": "2015-01-01",
    "end_date": "2020-12-31"
  },
  "total_days": 2192,
  "expected_days": 2192,
  "missing_days": 0,
  "data_coverage_percentage": 100,
  "analysis": {
    "average_max_temperature": 30.02,
    "highest_temperature": 41.7,
    "lowest_daily_max_temperature": 21.9,
    "extreme_heat_days": 380,
    "extreme_heat_percentage": 17.34,
    "heatwave_count": 22,
    "longest_heatwave_days": 51
  },
  "unit": "°C",
  "risk_level": "High"
}
```

**API Response Codes:**
- `200` – Successful response.
- `400` – Invalid date range or future end date.
- `422` – Query parameter validation error.
- `502` – Weather provider or data processing error.

## 📂 Project Structure

```text
climate-hazard-analyzer/
│
├── backend/
│   ├── main.py
│   └── main_backup.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

## ⚙️ Getting Started

Follow these instructions to run the project locally.

### Prerequisites

- Python 3.10 or compatible version
- Node.js and npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Roshnisinha/climate-hazard-analyzer.git

cd climate-hazard-analyzer
```

### 2. Set Up the Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install fastapi uvicorn pandas httpx
```

Start the backend server:

```bash
python -m uvicorn main:app --reload
```

The backend will be available at:

- API: http://127.0.0.1:8000
- Swagger Documentation: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/health

### 3. Set Up the Frontend

Open a second terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open the local URL displayed in the terminal, usually:

http://localhost:5173

Keep both backend and frontend servers running while using the application.

## 🚀 Deployment

The application is deployed using:

**Frontend – Vercel**

https://climate-hazard-analyzer-oorx.vercel.app/

**Backend – Render**

https://climate-hazard-analyzer-6vcw.onrender.com

The backend uses FastAPI and is configured with CORS to allow requests from the production frontend and local development origins.

## 🧪 Production Verification

The production application and API were tested using historical weather data for multiple geographic locations, including:

- Nashik, India
- Delhi, India

The Nashik API analysis returned HTTP 200 with 100% data coverage for the selected 2015–2020 period.

## 🔮 Future Improvements

- Interactive map-based location selection.
- More detailed climate trend visualizations.
- Downloadable climate analysis reports.
- Additional climate hazard indicators.
- Historical comparisons across multiple locations.
- Improved data quality and analysis features.

## 👩‍💻 Author

**Roshni Sinha**

Software Engineer | Full Stack Developer

[GitHub Profile](https://github.com/Roshnisinha)

[Project Repository](https://github.com/Roshnisinha/climate-hazard-analyzer)

## 📄 License

No license has been specified for this project yet.
