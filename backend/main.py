from fastapi.middleware.cors import CORSMiddleware
from datetime import date
import httpx
import pandas as pd
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(
    title="Climate Hazard Analyzer API",
    description="API for climate hazard analysis",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://climate-hazard-analyzer-lzqhn2pye-roshnisinha1.vercel.app",
        "https://climate-hazard-analyzer-r71lms7io-roshnisinha1.vercel.app",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Climate Hazard Analyzer API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/weather")
async def get_weather(
    latitude: float = Query(19.9975, ge=-90, le=90),
    longitude: float = Query(73.7898, ge=-180, le=180),
    start_date: date = Query(date(2015, 1, 1)),
    end_date: date = Query(date(2020, 12, 31)),
):
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date must be before or equal to end_date",
        )

    if end_date > date.today():
        raise HTTPException(
            status_code=400,
            detail="end_date cannot be in the future",
        )

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily": "temperature_2m_max",
        "timezone": "auto",
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            weather = response.json()

    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail="Weather data provider request failed",
        ) from exc

    daily = weather.get("daily") or {}
    dates = daily.get("time") or []
    temperatures = daily.get("temperature_2m_max") or []

    if not dates or len(dates) != len(temperatures):
        raise HTTPException(
            status_code=502,
            detail="Weather provider returned incomplete daily data",
        )

    df = pd.DataFrame({
        "date": dates,
        "temperature_max": temperatures,
    })

    df["temperature_max"] = pd.to_numeric(
        df["temperature_max"], errors="coerce"
    )

    df = df.dropna(subset=["temperature_max"])

    if df.empty:
        raise HTTPException(
            status_code=502,
            detail="No valid temperature data returned",
        )

    return {
        "location": {
            "latitude": latitude,
            "longitude": longitude,
        },
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "unit": "°C",
        "records_returned": len(df),
        "data": [
            {
                "date": row.date,
                "temperature_max": round(
                    float(row.temperature_max), 2
                ),
            }
            for row in df.itertuples(index=False)
        ],
    }


@app.get("/analyze")
async def analyze(
    latitude: float = Query(19.9975, ge=-90, le=90),
    longitude: float = Query(73.7898, ge=-180, le=180),
    start_date: date = Query(date(2015, 1, 1)),
    end_date: date = Query(date(2020, 12, 31)),
):
    weather = await get_weather(
        latitude=latitude,
        longitude=longitude,
        start_date=start_date,
        end_date=end_date,
    )

    df = pd.DataFrame(weather["data"])

    if df.empty:
        raise HTTPException(
            status_code=502,
            detail="No temperature data available for analysis",
        )

    temperatures = df["temperature_max"]

    extreme_heat_days = int((temperatures >= 35).sum())
    total_days = len(df)

    heat_percentage = round(
        extreme_heat_days / total_days * 100, 2
    )

    average_temperature = round(float(temperatures.mean()), 2)
    highest_temperature = round(float(temperatures.max()), 2)
    lowest_temperature = round(float(temperatures.min()), 2)

    # Demonstration-only heat risk classification
    if heat_percentage < 5:
        risk_level = "Low"
    elif heat_percentage < 15:
        risk_level = "Moderate"
    else:
        risk_level = "High"

    return {
        "location": weather["location"],
        "period": {
            "start_date": weather["start_date"],
            "end_date": weather["end_date"],
        },
        "total_days": total_days,
        "analysis": {
            "average_max_temperature": average_temperature,
            "highest_temperature": highest_temperature,
            "lowest_daily_max_temperature": lowest_temperature,
            "extreme_heat_days": extreme_heat_days,
            "extreme_heat_percentage": heat_percentage,
        },
        "unit": "°C",
        "risk_level": risk_level,
    }
