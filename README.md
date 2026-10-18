# 🌡️ Climate Hazard Analyzer

A climate intelligence web application that analyzes historical temperature data and identifies extreme heat risks for a selected location and date range.

## 📌 Overview

Climate Hazard Analyzer combines a React-based frontend with a FastAPI backend to help users explore historical temperature patterns and understand potential extreme heat risks.

Users can enter geographic coordinates and a date range to analyze temperature data and view the resulting climate risk indicators.

## ✨ Features

- 📍 Location-based climate analysis using latitude and longitude
- 📅 Customizable date range for historical analysis
- 🌡️ Average maximum temperature analysis
- 🔥 Identification and counting of extreme heat days
- 📊 Extreme heat percentage and highest temperature metrics
- ⚠️ Heat risk classification
- 📈 Results presented through a web interface
- 🔌 REST API built with FastAPI

## 🛠️ Tech Stack

**Frontend**
- React
- Vite
- JavaScript
- CSS

**Backend**
- Python
- FastAPI
- Pandas
- HTTPX

## 📂 Project Structure

```text
climate-hazard-analyzer/
├── backend/
│   ├── main.py
│   └── main_backup.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── .gitignore
└── README.md
```

## ⚙️ Getting Started

### Prerequisites

Install the following before running the project:

- Python 3.10 or a compatible version
- Node.js and npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Roshnisinha/climate-hazard-analyzer.git
cd climate-hazard-analyzer
```

### 2. Set Up the Backend

Open a terminal in the project folder and run:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```bash
pip install fastapi uvicorn pandas httpx
```

Start the API server:

```bash
python -m uvicorn main:app --reload
```

The backend should be available at:

- API: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

### 3. Set Up the Frontend

Open a second terminal in the project folder and run:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed in the terminal, usually:

http://localhost:5173

Keep both backend and frontend terminals running while using the application.

## 📊 Analysis Outputs

The application can display climate indicators such as:

- Average maximum temperature
- Highest recorded temperature in the selected period
- Number of extreme heat days
- Percentage of extreme heat days
- Overall heat risk classification

Results depend on the selected location, date range, available weather data, and configured risk thresholds.

## 🎯 Project Objective

The goal of this project is to make historical temperature analysis more accessible and provide a starting point for understanding extreme heat exposure using a simple web application.

## 🔮 Future Improvements

- Interactive maps for selecting locations
- More detailed historical climate visualizations
- Downloadable analysis reports
- Additional climate hazard indicators
- Deployment to a public hosting platform

## 👩‍💻 Author

**Roshni Sinha**

GitHub: [@Roshnisinha](https://github.com/Roshnisinha)

## 📄 License

A license has not yet been specified for this project.