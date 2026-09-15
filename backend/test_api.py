"""
FastAPI Endpoint Verification Script
Tests GET /health and POST /predict endpoints using FastAPI TestClient.
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    print("Testing GET /health...")
    response = client.get("/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.json()}")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["models_loaded"] is True
    print("GET /health PASSED!\n")


def test_predict_endpoint_high_rain():
    print("Testing POST /predict (High Rain Scenario)...")
    payload = {
        "temp_max": 29.5,
        "temp_min": 24.5,
        "temp_mean": 27.0,
        "humidity": 92.0,
        "rain": 18.5,
        "wind_max": 25.0,
        "pressure": 1005.0,
        "cloud_cover": 95.0,
        "day_of_year": 320,
        "month": 11,
        "season": 4
    }
    response = client.post("/predict", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert "predicted_temp_max" in data
    assert "rain_probability" in data
    assert "rain_probability_percent" in data
    assert "risk_level" in data
    assert "advice" in data
    print("POST /predict (High Rain) PASSED!\n")


def test_predict_endpoint_low_rain():
    print("Testing POST /predict (Low Rain Scenario)...")
    payload = {
        "temp_max": 33.5,
        "temp_min": 24.0,
        "temp_mean": 28.5,
        "humidity": 60.0,
        "rain": 0.0,
        "wind_max": 12.0,
        "pressure": 1012.0,
        "cloud_cover": 15.0,
        "day_of_year": 50,
        "month": 2,
        "season": 1
    }
    response = client.post("/predict", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert "predicted_temp_max" in data
    assert "risk_level" in data
    print("POST /predict (Low Rain) PASSED!\n")


def test_invalid_input():
    print("Testing POST /predict (Invalid Validation Failure)...")
    payload = {
        "temp_max": 33.5,
        # missing required fields
    }
    response = client.post("/predict", json=payload)
    print(f"Status Code: {response.status_code} (Expected 422)")
    assert response.status_code == 422
    print("Validation Test PASSED!\n")


if __name__ == "__main__":
    test_health_endpoint()
    test_predict_endpoint_high_rain()
    test_predict_endpoint_low_rain()
    test_invalid_input()
    print("ALL API ENDPOINT TESTS PASSED SUCCESSFULLY!")
