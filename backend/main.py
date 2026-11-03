
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
import httpx
import pandas as pd
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(
    title="Climate Hazard Analyzer API",
    description="API for climate hazard analysis",
    version="1.1.0",
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
    return {
        "message": "Climate Hazard Analyzer API is running",
        "version": "1.1.0",
    }


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

    except (httpx.HTTPError, ValueError) as exc:
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

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df = df.dropna(subset=["date", "temperature_max"])
    df = df.sort_values("date").reset_index(drop=True)

    if df.empty:
        raise HTTPException(
            status_code=502,
            detail="No valid temperature data returned",
        )

    expected_days = (end_date - start_date).days + 1
    records_returned = len(df)
    missing_days = max(expected_days - records_returned, 0)

    return {
        "location": {
            "latitude": latitude,
            "longitude": longitude,
        },
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "unit": "°C",
        "records_returned": records_returned,
        "expected_days": expected_days,
        "missing_days": missing_days,
        "data": [
            {
                "date": row.date.strftime("%Y-%m-%d"),
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

    # Prepare chronological weather records
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    temperatures = df["temperature_max"]

    # Basic temperature statistics
    total_days = len(df)
    expected_days = weather["expected_days"]

    average_temperature = round(float(temperatures.mean()), 2)
    highest_temperature = round(float(temperatures.max()), 2)
    lowest_temperature = round(float(temperatures.min()), 2)

    # Extreme heat analysis
    extreme_flags = temperatures >= 35

    extreme_heat_days = int(extreme_flags.sum())

    heat_percentage = round(
        extreme_heat_days / total_days * 100, 2
    )

    # Consecutive heatwave analysis
    # A heatwave is defined here as 3+ consecutive days >= 35°C.
    date_gap = df["date"].diff().dt.days

    new_group = (
        (~extreme_flags) | (date_gap.ne(1))
    )

    group_ids = new_group.cumsum()

    heatwave_durations = (
        df.loc[extreme_flags]
        .groupby(group_ids[extreme_flags])
        .size()
    )
    heatwave_count = int(
        (heatwave_durations >= 3).sum()
    )

    valid_heatwave_durations = heatwave_durations[
        heatwave_durations >= 3
    ]

    longest_heatwave = (
        int(valid_heatwave_durations.max())
        if not valid_heatwave_durations.empty
        else 0
    )

    # Heat risk classification
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
        "expected_days": expected_days,
        "missing_days": weather["missing_days"],
        "data_coverage_percentage": round(
            total_days / expected_days * 100, 2
        ),
        "analysis": {
            "average_max_temperature": average_temperature,
            "highest_temperature": highest_temperature,
            "lowest_daily_max_temperature": lowest_temperature,
            "extreme_heat_days": extreme_heat_days,
            "extreme_heat_percentage": heat_percentage,
            "heatwave_count": heatwave_count,
            "longest_heatwave_days": longest_heatwave,
        },
        "unit": "°C",
        "risk_level": risk_level,
    }
