import { CurrentWeatherData, PredictionResponse, WeatherTrendPoint } from "@/types/weather";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
const CHENNAI_LAT = 13.0827;
const CHENNAI_LON = 80.2707;

function getSeasonCode(month: number): number {
  if (month === 1 || month === 2) return 1; // Winter
  if (month >= 3 && month <= 5) return 2;  // Summer
  if (month >= 6 && month <= 9) return 3;  // Monsoon
  return 4;                                // Post-monsoon
}

function getDayOfYear(date: Date): number {
  const start = new Date(date.getFullYear(), 0, 0);
  const diff = date.getTime() - start.getTime();
  const oneDay = 1000 * 60 * 60 * 24;
  return Math.floor(diff / oneDay);
}

export async function fetchLiveCurrentWeather(): Promise<{
  current: CurrentWeatherData;
  history: WeatherTrendPoint[];
}> {
  try {
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${CHENNAI_LAT}&longitude=${CHENNAI_LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,cloud_cover,precipitation&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum,wind_speed_10m_max,surface_pressure_mean,cloud_cover_mean&timezone=Asia%2FKolkata`;
    
    const res = await fetch(url);
    if (!res.ok) {
      throw new Error(`Open-Meteo API returned status ${res.status}`);
    }
    const data = await res.json();
    
    const today = new Date();
    const month = today.getMonth() + 1;
    const dayOfYear = getDayOfYear(today);
    const season = getSeasonCode(month);

    const daily = data.daily || {};
    const tempMax = daily.temperature_2m_max?.[0] ?? data.current?.temperature_2m ?? 31.5;
    const tempMin = daily.temperature_2m_min?.[0] ?? (tempMax - 5);
    const tempMean = daily.temperature_2m_mean?.[0] ?? ((tempMax + tempMin) / 2);
    const humidity = daily.relative_humidity_2m_mean?.[0] ?? data.current?.relative_humidity_2m ?? 75;
    const rain = daily.precipitation_sum?.[0] ?? data.current?.precipitation ?? 0.0;
    const windMax = daily.wind_speed_10m_max?.[0] ?? data.current?.wind_speed_10m ?? 14.5;
    const pressure = daily.surface_pressure_mean?.[0] ?? data.current?.surface_pressure ?? 1010.0;
    const cloudCover = daily.cloud_cover_mean?.[0] ?? data.current?.cloud_cover ?? 45;

    const currentWeather: CurrentWeatherData = {
      city: "Chennai, India",
      date: today.toISOString().split("T")[0],
      temp_max: tempMax,
      temp_min: tempMin,
      temp_mean: tempMean,
      humidity: humidity,
      rain: rain,
      wind_max: windMax,
      pressure: pressure,
      cloud_cover: cloudCover,
      day_of_year: dayOfYear,
      month: month,
      season: season
    };

    // Extract last 7 days trend for Recharts visualizer
    const history: WeatherTrendPoint[] = [];
    const dates: string[] = daily.time || [];
    const maxTemps: number[] = daily.temperature_2m_max || [];
    const rains: number[] = daily.precipitation_sum || [];

    for (let i = 0; i < Math.min(dates.length, 7); i++) {
      const d = new Date(dates[i]);
      const formattedDate = d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" });
      const estProb = Math.min(Math.round((rains[i] > 0 ? 50 + rains[i] * 5 : 15)), 98);
      history.push({
        date: formattedDate,
        temp: maxTemps[i] ?? tempMax,
        rainProb: estProb
      });
    }

    return { current: currentWeather, history };
  } catch (error) {
    console.warn("Failed to fetch live Open-Meteo weather, using realistic fallback data:", error);
    const today = new Date();
    const month = today.getMonth() + 1;
    const dayOfYear = getDayOfYear(today);
    
    const fallbackCurrent: CurrentWeatherData = {
      city: "Chennai, India",
      date: today.toISOString().split("T")[0],
      temp_max: 32.4,
      temp_min: 25.1,
      temp_mean: 28.7,
      humidity: 78,
      rain: 2.5,
      wind_max: 16.2,
      pressure: 1008.5,
      cloud_cover: 65,
      day_of_year: dayOfYear,
      month: month,
      season: getSeasonCode(month)
    };

    const fallbackHistory: WeatherTrendPoint[] = [
      { date: "Mon", temp: 31.0, rainProb: 20 },
      { date: "Tue", temp: 31.8, rainProb: 35 },
      { date: "Wed", temp: 32.4, rainProb: 65 },
      { date: "Thu", temp: 30.5, rainProb: 80 },
      { date: "Fri", temp: 31.2, rainProb: 45 },
      { date: "Sat", temp: 32.0, rainProb: 30 },
      { date: "Today", temp: 32.4, rainProb: 78 }
    ];

    return { current: fallbackCurrent, history: fallbackHistory };
  }
}

export async function fetchAIPrediction(weather: CurrentWeatherData): Promise<PredictionResponse> {
  const payload = {
    temp_max: weather.temp_max,
    temp_min: weather.temp_min,
    temp_mean: weather.temp_mean,
    humidity: weather.humidity,
    rain: weather.rain,
    wind_max: weather.wind_max,
    pressure: weather.pressure,
    cloud_cover: weather.cloud_cover,
    day_of_year: weather.day_of_year,
    month: weather.month,
    season: weather.season
  };

  const res = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`API error (${res.status}): ${errorText}`);
  }

  return res.json();
}
