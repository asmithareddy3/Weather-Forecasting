"""
Prediction Service Module
Handles loading serialized models, feature alignment, model inference,
rain risk level categorization, and advice generation.
"""

import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple

# Threshold configuration for Rain Risk Level
RISK_THRESHOLDS = [
    (0.30, "LOW", "Low chance of rain. Outdoor activities should be fine."),
    (0.60, "MODERATE", "Moderate chance of rain. Keep an umbrella nearby."),
    (0.80, "HIGH", "High chance of rain. Carry an umbrella."),
    (1.00, "VERY HIGH", "Very high chance of rain. Consider avoiding unnecessary outdoor activities.")
]


class WeatherPredictionService:
    def __init__(self, models_dir: str = None):
        if models_dir is None:
            models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
        
        self.models_dir = os.path.abspath(models_dir)
        self.temp_model = None
        self.rain_model = None
        self.feature_columns = []
        self._load_models()

    def _load_models(self) -> None:
        """
        Loads serialized joblib models and feature columns list.
        """
        temp_path = os.path.join(self.models_dir, "temp_model.pkl")
        rain_path = os.path.join(self.models_dir, "rain_model.pkl")
        cols_path = os.path.join(self.models_dir, "feature_columns.pkl")

        if not (os.path.exists(temp_path) and os.path.exists(rain_path) and os.path.exists(cols_path)):
            raise FileNotFoundError(
                f"Model files missing in {self.models_dir}. Please run train_models.py first."
            )

        try:
            self.temp_model = joblib.load(temp_path)
            self.rain_model = joblib.load(rain_path)
            self.feature_columns = joblib.load(cols_path)
            print(f"Successfully loaded models from {self.models_dir}")
        except Exception as e:
            raise RuntimeError(f"Error loading serialized model files: {e}")

    def get_risk_and_advice(self, rain_prob: float) -> Tuple[str, str]:
        """
        Determines risk level and advice based on rain probability threshold configuration.
        """
        for threshold, risk_level, advice in RISK_THRESHOLDS:
            if rain_prob <= threshold:
                return risk_level, advice
        return "VERY HIGH", "Very high chance of rain. Consider avoiding unnecessary outdoor activities."

    def predict(self, weather_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Accepts dictionary of input features, formats array in exact column order,
        and computes predictions.
        """
        if not self.temp_model or not self.rain_model:
            raise RuntimeError("Models are not loaded.")

        # Ensure features are arranged in exact order used during training
        feature_vector = []
        for col in self.feature_columns:
            if col not in weather_features:
                raise ValueError(f"Missing required feature field: '{col}'")
            feature_vector.append(weather_features[col])

        # Convert to 1-row DataFrame with explicit feature column names
        X = pd.DataFrame([[weather_features[col] for col in self.feature_columns]], columns=self.feature_columns)

        # 1. Temperature Prediction (Regression)
        pred_temp = float(self.temp_model.predict(X)[0])
        pred_temp_rounded = round(pred_temp, 1)

        # 2. Rain Probability Prediction (Classification)
        # predict_proba returns [[prob_no_rain, prob_rain]]
        probabilities = self.rain_model.predict_proba(X)[0]
        rain_prob = float(probabilities[1])  # Class 1 probability
        rain_prob_rounded = round(rain_prob, 2)
        rain_prob_pct = int(round(rain_prob * 100))

        # 3. Categorize Risk & Advice
        risk_level, advice = self.get_risk_and_advice(rain_prob)

        return {
            "predicted_temp_max": pred_temp_rounded,
            "rain_probability": rain_prob_rounded,
            "rain_probability_percent": rain_prob_pct,
            "risk_level": risk_level,
            "advice": advice
        }


# Singleton service instance
_service_instance = None

def get_prediction_service() -> WeatherPredictionService:
    global _service_instance
    if _service_instance is None:
        _service_instance = WeatherPredictionService()
    return _service_instance
