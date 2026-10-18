import { useState } from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";
import "./App.css";

const API_URL = "https://climate-hazard-analyzer-api-243w.onrender.com";
function App() {
  const [latitude, setLatitude] = useState("19.9975");
  const [longitude, setLongitude] = useState("73.7898");
  const [startDate, setStartDate] = useState("2015-01-01");
  const [endDate, setEndDate] = useState("2020-12-31");
  const [result, setResult] = useState(null);
  const [weatherData, setWeatherData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function fetchJson(url) {
    const response = await fetch(url);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : `Request failed (${response.status})`
      );
    }

    return data;
  }

  async function analyzeClimate(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    setWeatherData([]);

    const lat = Number(latitude);
    const lon = Number(longitude);
    const today = new Date().toISOString().slice(0, 10);

    if (
      latitude.trim() === "" ||
      longitude.trim() === "" ||
      !Number.isFinite(lat) ||
      !Number.isFinite(lon) ||
      lat < -90 ||
      lat > 90 ||
      lon < -180 ||
      lon > 180
    ) {
      setError(
        "Enter a valid latitude (-90 to 90) and longitude (-180 to 180)."
      );
      setLoading(false);
      return;
    }

    if (!startDate || !endDate || startDate > endDate) {
      setError("Please select a valid date range.");
      setLoading(false);
      return;
    }

    if (endDate > today) {
      setError("End date cannot be in the future.");
      setLoading(false);
      return;
    }

    try {
      const params = new URLSearchParams({
        latitude: String(lat),
        longitude: String(lon),
        start_date: startDate,
        end_date: endDate,
      });

      const [analysisData, weather] = await Promise.all([
        fetchJson(`${API_URL}/analyze?${params.toString()}`),
        fetchJson(`${API_URL}/weather?${params.toString()}`),
      ]);

      setResult(analysisData);
      setWeatherData(weather.data || []);
    } catch (err) {
      setError(
        err.message || "Unable to connect to the backend API."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container">
      <header>
        <p className="eyebrow">CLIMATE INTELLIGENCE</p>
        <h1>Climate Hazard Analyzer</h1>
        <p>Analyze historical temperatures and extreme heat risk.</p>
      </header>

      <section className="panel">
        <h2>Configure Analysis</h2>

        <form onSubmit={analyzeClimate}>
          <div className="form-grid">
            <label>
              Latitude
              <input
                type="number"
                step="any"
                min="-90"
                max="90"
                value={latitude}
                onChange={(e) => setLatitude(e.target.value)}
                required
              />
            </label>

            <label>
              Longitude
              <input
                type="number"
                step="any"
                min="-180"
                max="180"
                value={longitude}
                onChange={(e) => setLongitude(e.target.value)}
                required
              />
            </label>

            <label>
              Start Date
              <input
                type="date"
                value={startDate}
                max={endDate || todayDate()}
                onChange={(e) => setStartDate(e.target.value)}
                required
              />
            </label>

            <label>
              End Date
              <input
                type="date"
                value={endDate}
                min={startDate || undefined}
                max={todayDate()}
                onChange={(e) => setEndDate(e.target.value)}
                required
              />
            </label>
          </div>

          <button type="submit" disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Climate"}
          </button>
        </form>

        {error && <p className="error">{error}</p>}
      </section>

      {result && (
        <>
          <section className="summary">
            <div className="stat">
              <span>Average Max Temperature</span>
              <strong>
                {result.analysis.average_max_temperature}°C
              </strong>
            </div>

            <div className="stat">
              <span>Highest Temperature</span>
              <strong>{result.analysis.highest_temperature}°C</strong>
            </div>

            <div className="stat">
              <span>Extreme Heat Days</span>
              <strong>{result.analysis.extreme_heat_days}</strong>
            </div>

            <div className="stat">
              <span>Extreme Heat Percentage</span>
              <strong>
                {result.analysis.extreme_heat_percentage}%
              </strong>
            </div>
          </section>

          <section className="panel">
            <h2>Historical Temperature Trend</h2>
            <p>
              Daily maximum temperature from{" "}
              {result.period.start_date} to {result.period.end_date}.
            </p>

            {weatherData.length > 0 ? (
              <div style={{ width: "100%", height: 360 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={weatherData}
                    margin={{
                      top: 15,
                      right: 20,
                      left: 10,
                      bottom: 10,
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="date"
                      tickFormatter={(date) => date.slice(0, 7)}
                      interval={Math.max(
                        0,
                        Math.ceil(weatherData.length / 8) - 1
                      )}
                      minTickGap={20}
                    />
                    <YAxis
                      domain={["auto", "auto"]}
                      label={{
                        value: "Temperature (°C)",
                        angle: -90,
                        position: "insideLeft",
                      }}
                    />
                    <Tooltip
                      labelFormatter={(date) => `Date: ${date}`}
                      formatter={(value) => [
                        `${value} °C`,
                        "Max temperature",
                      ]}
                    />
                    <Line
                      type="monotone"
                      dataKey="temperature_max"
                      name="Max temperature"
                      stroke="#2563eb"
                      strokeWidth={2}
                      dot={false}
                      activeDot={{ r: 4 }}
                      isAnimationActive={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <p>No temperature data available for this period.</p>
            )}
          </section>

          <section className="panel">
            <h2>Risk Assessment</h2>
            <span
              className={`risk risk-${result.risk_level.toLowerCase()}`}
            >
              {result.risk_level} Risk
            </span>
            <p>
              Coordinates: {result.location.latitude},{" "}
              {result.location.longitude}
            </p>
            <p>
              Period: {result.period.start_date} to{" "}
              {result.period.end_date}
            </p>
            <p>Total days analyzed: {result.total_days}</p>
            <p>Temperature unit: {result.unit}</p>
          </section>
        </>
      )}
    </main>
  );
}

function todayDate() {
  return new Date().toISOString().slice(0, 10);
}

export default App;
