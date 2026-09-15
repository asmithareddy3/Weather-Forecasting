"""
FastAPI Main Application Module
Provides REST API endpoints for weather predictions, health status, and automatic Swagger docs.
"""

import os
import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from services.prediction_service import get_prediction_service, WeatherPredictionService

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weather_api")

app = FastAPI(
    title="Accessible AI Weather Forecasting API",
    description="REST API delivering ML temperature predictions, rain probabilities, and accessibility advice for Chennai, India.",
    version="1.0.0"
)

# CORS Configuration
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    frontend_url
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Input Validation Schema
class WeatherPredictionRequest(BaseModel):
    temp_max: float = Field(..., description="Maximum temperature in °C", ge=-10.0, le=60.0, example=32.5)
    temp_min: float = Field(..., description="Minimum temperature in °C", ge=-20.0, le=50.0, example=25.0)
    temp_mean: float = Field(..., description="Mean temperature in °C", ge=-15.0, le=55.0, example=28.7)
    humidity: float = Field(..., description="Mean relative humidity percentage", ge=0.0, le=100.0, example=78.0)
    rain: float = Field(..., description="Precipitation sum in mm", ge=0.0, le=500.0, example=2.5)
    wind_max: float = Field(..., description="Maximum wind speed in km/h", ge=0.0, le=250.0, example=15.2)
    pressure: float = Field(..., description="Mean surface pressure in hPa", ge=800.0, le=1200.0, example=1008.5)
    cloud_cover: float = Field(..., description="Mean cloud cover percentage", ge=0.0, le=100.0, example=65.0)
    day_of_year: int = Field(..., description="Day of the year (1-366)", ge=1, le=366, example=285)
    month: int = Field(..., description="Month of the year (1-12)", ge=1, le=12, example=10)
    season: int = Field(..., description="Season code (1:Winter, 2:Summer, 3:Monsoon, 4:Post-monsoon)", ge=1, le=4, example=4)

    @field_validator("temp_max")
    def validate_temp_range(cls, v, values):
        return v


# Pydantic Response Schema
class WeatherPredictionResponse(BaseModel):
    predicted_temp_max: float = Field(..., description="Tomorrow's predicted maximum temperature in °C", example=30.7)
    rain_probability: float = Field(..., description="ML-estimated rain probability (0.0 - 1.0)", example=0.78)
    rain_probability_percent: int = Field(..., description="ML-estimated rain probability percentage (0 - 100%)", example=78)
    risk_level: str = Field(..., description="Rain risk level category (LOW, MODERATE, HIGH, VERY HIGH)", example="HIGH")
    advice: str = Field(..., description="Simple weather advice for users", example="High chance of rain. Carry an umbrella.")


class HealthCheckResponse(BaseModel):
    status: str
    city: str
    models_loaded: bool


@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
def health_check():
    """
    Health check endpoint to verify server status and model loading.
    """
    try:
        service = get_prediction_service()
        models_ok = service.temp_model is not None and service.rain_model is not None
        return {
            "status": "healthy",
            "city": "Chennai, India",
            "models_loaded": models_ok
        }
    except Exception as e:
        logger.error(f"Health check warning: {e}")
        return {
            "status": "degraded",
            "city": "Chennai, India",
            "models_loaded": False
        }


@app.post("/predict", response_model=WeatherPredictionResponse, tags=["Prediction"])
def predict_weather(request: WeatherPredictionRequest):
    """
    Predicts tomorrow's maximum temperature, rain probability, risk level, and accessibility advice.
    """
    try:
        service = get_prediction_service()
        input_data = request.model_dump()
        prediction = service.predict(input_data)
        return prediction
    except ValueError as ve:
        logger.warning(f"Invalid input data: {ve}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except RuntimeError as re:
        logger.error(f"Prediction runtime error: {re}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Prediction service unavailable.")
    except Exception as e:
        logger.error(f"Unhandled error during prediction: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
