export interface CurrentWeatherData {
  city: string;
  date: string;
  temp_max: number;
  temp_min: number;
  temp_mean: number;
  humidity: number;
  rain: number;
  wind_max: number;
  pressure: number;
  cloud_cover: number;
  day_of_year: number;
  month: number;
  season: number;
}

export interface PredictionResponse {
  predicted_temp_max: number;
  rain_probability: number;
  rain_probability_percent: number;
  risk_level: "LOW" | "MODERATE" | "HIGH" | "VERY HIGH";
  advice: string;
}

export interface WeatherTrendPoint {
  date: string;
  temp: number;
  rainProb: number;
}
