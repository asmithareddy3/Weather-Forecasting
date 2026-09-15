"""
Open-Meteo Historical Weather Data Collection Script
Target City: Chennai, India (Lat: 13.0827, Lon: 80.2707)
Date Range: 2020-01-01 to 2025-12-31
"""

import os
import requests
import pandas as pd
from typing import Dict, Any

# Centralized City Configuration
CITIES: Dict[str, Dict[str, Any]] = {
    "chennai": {
        "name": "Chennai",
        "country": "India",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "filename": "chennai_weather.csv"
    }
}

OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

REQUIRED_DAILY_VARS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "relative_humidity_2m_mean",
    "precipitation_sum",
    "wind_speed_10m_max",
    "surface_pressure_mean",
    "cloud_cover_mean"
]

COLUMN_MAPPING = {
    "time": "date",
    "temperature_2m_max": "temp_max",
    "temperature_2m_min": "temp_min",
    "temperature_2m_mean": "temp_mean",
    "relative_humidity_2m_mean": "humidity",
    "precipitation_sum": "rain",
    "wind_speed_10m_max": "wind_max",
    "surface_pressure_mean": "pressure",
    "cloud_cover_mean": "cloud_cover"
}


def fetch_historical_weather(
    city_key: str = "chennai",
    start_date: str = "2020-01-01",
    end_date: str = "2025-12-31"
) -> pd.DataFrame:
    """
    Fetches daily weather historical data from Open-Meteo API.
    Performs data cleaning, renaming, missing value handling, and validation.
    """
    if city_key not in CITIES:
        raise ValueError(f"City '{city_key}' is not configured.")
    
    city_info = CITIES[city_key]
    print(f"Fetching historical weather data for {city_info['name']} ({start_date} to {end_date})...")

    params = {
        "latitude": city_info["latitude"],
        "longitude": city_info["longitude"],
        "start_date": start_date,
        "end_date": end_date,
        "daily": ",".join(REQUIRED_DAILY_VARS),
        "timezone": "Asia/Kolkata"
    }

    try:
        response = requests.get(OPEN_METEO_ARCHIVE_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch data from Open-Meteo API: {e}")

    if "daily" not in data:
        raise ValueError("Open-Meteo response does not contain 'daily' data field.")

    # Convert API response to pandas DataFrame
    df = pd.DataFrame(data["daily"])
    
    # Rename columns to target names
    df = df.rename(columns=COLUMN_MAPPING)

    # Convert date to datetime and format string YYYY-MM-DD
    df["date"] = pd.to_datetime(df["date"])
    
    # Drop duplicates by date
    initial_len = len(df)
    df = df.drop_duplicates(subset=["date"]).sort_values("date").reset_index(drop=True)
    if len(df) < initial_len:
        print(f"Removed {initial_len - len(df)} duplicate date rows.")

    # Cast numerical columns
    numeric_cols = ["temp_max", "temp_min", "temp_mean", "humidity", "rain", "wind_max", "pressure", "cloud_cover"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Check missing values & interpolate numeric features
    missing_counts = df[numeric_cols].isnull().sum()
    if missing_counts.sum() > 0:
        print(f"Missing values detected:\n{missing_counts[missing_counts > 0]}")
        print("Filling missing values using forward-fill and backward-fill...")
        df[numeric_cols] = df[numeric_cols].ffill().bfill()

    # Convert date back to string format YYYY-MM-DD
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    print(f"Data collection successful! Collected {len(df)} daily records.")
    return df


def save_dataset(df: pd.DataFrame, city_key: str = "chennai") -> str:
    """
    Saves cleaned dataframe to backend/data/ directory.
    """
    city_info = CITIES[city_key]
    output_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, city_info["filename"])
    df.to_csv(filepath, index=False)
    print(f"Saved dataset to: {os.path.abspath(filepath)}")
    return filepath


if __name__ == "__main__":
    df = fetch_historical_weather(city_key="chennai", start_date="2020-01-01", end_date="2025-12-31")
    save_dataset(df, city_key="chennai")
    
    print("\nDataset Summary Preview:")
    print(df.head())
    print("\nDataset Info:")
    print(df.info())
