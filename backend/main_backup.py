from datetime import date
import httpx
import pandas as pd
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(
    title="Climate Hazard Analyzer API",
    description="Historical weather and heatwave trend analysis",
    version="1.0.0",
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

    today = date.today()
    if end_date > today:
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
            data = response.json()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail="Weather data provider request failed",
        ) from exc

    daily = data.get("daily") or {}
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
