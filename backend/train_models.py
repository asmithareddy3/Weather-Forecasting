"""
Model Training, Evaluation, and Serialization Script
Builds two independent machine learning models:
1. RandomForestRegressor for Temperature Prediction (temp_max_tomorrow)
2. RandomForestClassifier for Rain Prediction (rain_tomorrow)

Uses an 80/20 Chronological Train/Test Split (No Random Shuffling).
Saves trained models and feature column lists via joblib.
"""

import os
import joblib
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import (
    mean_absolute_error,
    root_mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

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


def load_processed_data(data_path: str) -> pd.DataFrame:
    """
    Loads preprocessed dataset from backend/data/chennai_processed.csv
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Processed dataset not found at {data_path}. Run preprocess.py first.")
    df = pd.read_csv(data_path)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").reset_index(drop=True)


def split_chronological(
    df: pd.DataFrame, train_ratio: float = 0.80
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series, pd.Series]:
    """
    Splits time-series data chronologically (80% older -> Train, 20% newer -> Test).
    Do NOT randomly shuffle to avoid data leakage across time boundaries.
    """
    split_idx = int(len(df) * train_ratio)
    
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]
    
    X_train = train_df[FEATURE_COLUMNS]
    X_test = test_df[FEATURE_COLUMNS]
    
    y_temp_train = train_df["temp_max_tomorrow"]
    y_temp_test = test_df["temp_max_tomorrow"]
    
    y_rain_train = train_df["rain_tomorrow"]
    y_rain_test = test_df["rain_tomorrow"]

    print(f"Chronological Split Complete:")
    print(f"  Training set : {len(train_df)} rows ({train_df['date'].min().strftime('%Y-%m-%d')} to {train_df['date'].max().strftime('%Y-%m-%d')})")
    print(f"  Testing set  : {len(test_df)} rows ({test_df['date'].min().strftime('%Y-%m-%d')} to {test_df['date'].max().strftime('%Y-%m-%d')})")

    return X_train, X_test, y_temp_train, y_temp_test, y_rain_train, y_rain_test


def train_temperature_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestRegressor:
    """
    Trains RandomForestRegressor for tomorrow's maximum temperature.
    """
    print("\nTraining RandomForestRegressor for Temperature Prediction...")
    temp_model = RandomForestRegressor(
        n_estimators=100,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )
    temp_model.fit(X_train, y_train)
    return temp_model


def evaluate_temperature_model(model: RandomForestRegressor, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
    """
    Evaluates temperature regression model using MAE, RMSE, and R2 score.
    """
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    metrics = {"MAE": float(mae), "RMSE": float(rmse), "R2": float(r2)}
    
    print("\n" + "="*50)
    print("TEMPERATURE REGRESSION MODEL EVALUATION (Tomorrow's Max Temp)")
    print("="*50)
    print(f"Mean Absolute Error (MAE) : {mae:.3f} °C")
    print(f"Root Mean Squared Error (RMSE) : {rmse:.3f} °C")
    print(f"R² Score (Coefficient of Determination) : {r2:.3f}")
    
    # Feature Importance
    importances = pd.Series(model.feature_importances_, index=FEATURE_COLUMNS).sort_values(ascending=False)
    print("\nTop Temperature Feature Importances:")
    print(importances.head(5).to_string())
    
    return metrics


def train_rain_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """
    Trains RandomForestClassifier for tomorrow's rain occurrence (0 or 1).
    """
    print("\nTraining RandomForestClassifier for Rain Prediction...")
    rain_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    rain_model.fit(X_train, y_train)
    return rain_model


def evaluate_rain_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, Any]:
    """
    Evaluates rain classification model using Accuracy, Precision, Recall, F1, and predict_proba.
    """
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]  # ML-estimated probability of rain (Class 1)
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    report = classification_report(y_test, y_pred, target_names=["No Rain (0)", "Rain (1)"])
    
    print("\n" + "="*50)
    print("RAIN CLASSIFICATION MODEL EVALUATION (Tomorrow's Rain)")
    print("="*50)
    print(f"Accuracy  : {acc:.3f} ({acc*100:.1f}%)")
    print(f"Precision : {prec:.3f}")
    print(f"Recall    : {rec:.3f}")
    print(f"F1-Score  : {f1:.3f}")
    print("\nClassification Report:\n", report)
    
    print(f"Sample ML-Estimated Rain Probabilities (predict_proba):")
    sample_prob_df = pd.DataFrame({"Actual_Rain": y_test.values[:5], "Predicted_Prob": np.round(y_proba[:5], 3)})
    print(sample_prob_df.to_string(index=False))
    
    metrics = {
        "Accuracy": float(acc),
        "Precision": float(prec),
        "Recall": float(rec),
        "F1": float(f1),
    }
    return metrics


def save_serialized_models(
    temp_model: RandomForestRegressor,
    rain_model: RandomForestClassifier,
    feature_columns: list,
    output_dir: str = "models"
) -> None:
    """
    Saves trained models and feature columns list using joblib into backend/models/
    """
    base_dir = os.path.join(os.path.dirname(__file__), output_dir)
    os.makedirs(base_dir, exist_ok=True)
    
    temp_path = os.path.join(base_dir, "temp_model.pkl")
    rain_path = os.path.join(base_dir, "rain_model.pkl")
    cols_path = os.path.join(base_dir, "feature_columns.pkl")
    
    joblib.dump(temp_model, temp_path)
    joblib.dump(rain_model, rain_path)
    joblib.dump(feature_columns, cols_path)
    
    print("\n" + "="*50)
    print("MODEL SERIALIZATION COMPLETE")
    print("="*50)
    print(f"Saved Temperature Model : {os.path.abspath(temp_path)}")
    print(f"Saved Rain Model        : {os.path.abspath(rain_path)}")
    print(f"Saved Feature Columns   : {os.path.abspath(cols_path)}")
    
    # Also sync to root models directory
    root_models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
    os.makedirs(root_models_dir, exist_ok=True)
    joblib.dump(temp_model, os.path.join(root_models_dir, "temp_model.pkl"))
    joblib.dump(rain_model, os.path.join(root_models_dir, "rain_model.pkl"))
    joblib.dump(feature_columns, os.path.join(root_models_dir, "feature_columns.pkl"))
    print(f"Synced copy to root     : {root_models_dir}")


def main():
    data_path = os.path.join(os.path.dirname(__file__), "data", "chennai_processed.csv")
    df = load_processed_data(data_path)
    
    X_train, X_test, y_temp_train, y_temp_test, y_rain_train, y_rain_test = split_chronological(df)
    
    # Train & Evaluate Temperature Model
    temp_model = train_temperature_model(X_train, y_temp_train)
    evaluate_temperature_model(temp_model, X_test, y_temp_test)
    
    # Train & Evaluate Rain Model
    rain_model = train_rain_model(X_train, y_rain_train)
    evaluate_rain_model(rain_model, X_test, y_rain_test)
    
    # Serialize Models
    save_serialized_models(temp_model, rain_model, FEATURE_COLUMNS)


if __name__ == "__main__":
    main()
