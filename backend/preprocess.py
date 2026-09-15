"""
Feature Engineering and Preprocessing Script
Transforms raw weather data into ML-ready datasets with Next-Day Targets.

Features Engineered:
- day_of_year (1-366)
- month (1-12)
- season (1: Winter, 2: Summer, 3: Monsoon, 4: Post-monsoon)

Targets Created (Next Day / Tomorrow):
- temp_max_tomorrow (Float target for RandomForestRegressor)
- rain_tomorrow (Binary 0/1 target for RandomForestClassifier)
"""

import os
import pandas as pd
import numpy as np
from typing import Tuple

FEATURE_COLUMNS = [
    "temp_max",
    "temp_min",
    "temp_mean",
    "humidity",
    "rain",
    "wind_max",
    "pressure",
    "cloud_cover",
    "day_of_year",
    "month",
    "season"
]


def get_season_code(month: int) -> int:
    """
    Map month to numeric season code for India/Chennai climate:
    1: Winter (Jan - Feb)
    2: Summer (Mar - May)
    3: Monsoon (Jun - Sep)
    4: Post-monsoon (Oct - Dec)
    """
    if month in [1, 2]:
        return 1  # Winter
    elif month in [3, 4, 5]:
        return 2  # Summer
    elif month in [6, 7, 8, 9]:
        return 3  # Monsoon
    else:
        return 4  # Post-monsoon


def preprocess_data(raw_csv_path: str) -> pd.DataFrame:
    """
    Loads raw CSV data, performs feature engineering, shifts target labels to tomorrow,
    and removes invalid rows.
    """
    if not os.path.exists(raw_csv_path):
        raise FileNotFoundError(f"Input file not found at: {raw_csv_path}")

    print(f"Loading raw dataset from {raw_csv_path}...")
    df = pd.read_csv(raw_csv_path)

    # Ensure dates are parsed and sorted chronologically
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # 1. Feature Engineering
    df["day_of_year"] = df["date"].dt.dayofyear
    df["month"] = df["date"].dt.month
    df["season"] = df["month"].apply(get_season_code)

    # 2. Target Creation (Next-Day Shifting)
    # Target temp_max_tomorrow is today's +1 index temp_max
    df["temp_max_tomorrow"] = df["temp_max"].shift(-1)
    
    # Target rain_tomorrow is 1 if next day's precipitation > 0, else 0
    next_day_rain = df["rain"].shift(-1)
    df["rain_tomorrow"] = np.where(next_day_rain > 0.0, 1, 0)

    # 3. Drop the very last row where tomorrow's target is NaN due to shifting
    initial_count = len(df)
    df = df.dropna(subset=["temp_max_tomorrow"]).reset_index(drop=True)
    df["rain_tomorrow"] = df["rain_tomorrow"].astype(int)

    print(f"Feature engineering complete. Kept {len(df)} samples (dropped {initial_count - len(df)} row with unknown tomorrow).")
    print(f"Rain distribution (Tomorrow): {df['rain_tomorrow'].value_counts().to_dict()}")

    return df


def save_processed_data(df: pd.DataFrame, output_filename: str = "chennai_processed.csv") -> str:
    """
    Saves preprocessed dataframe into backend/data/
    """
    output_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, output_filename)
    
    # Save formatted date string YYYY-MM-DD
    save_df = df.copy()
    save_df["date"] = save_df["date"].dt.strftime("%Y-%m-%d")
    save_df.to_csv(filepath, index=False)
    
    print(f"Saved processed dataset to: {os.path.abspath(filepath)}")
    return filepath


if __name__ == "__main__":
    raw_path = os.path.join(os.path.dirname(__file__), "data", "chennai_weather.csv")
    df_processed = preprocess_data(raw_path)
    save_processed_data(df_processed)
    
    print("\nProcessed Dataset Sample (Today vs Tomorrow targets):")
    cols_to_show = ["date", "temp_max", "rain", "day_of_year", "month", "season", "temp_max_tomorrow", "rain_tomorrow"]
    print(df_processed[cols_to_show].head())
