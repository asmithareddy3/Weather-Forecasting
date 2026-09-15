# Project Architecture & Workflow Diagrams
## Accessible AI Weather Forecasting and Rain Alert System

This document contains all system architecture diagrams, data pipelines, sequence flows, and risk decision structures formatted in **ASCII text**, **Unicode boxes**, and **Mermaid.js** diagrams ready to be copied into Overleaf, LaTeX, MS Word, or PowerPoint presentations.

---

## 1. High-Level System Architecture (End-to-End)

### Mermaid Diagram
```mermaid
graph TD
    subgraph Client_Tier [Client / Presentation Tier]
        User[User / Assistive Screen Reader]
        NextJS[Next.js 14 Web Dashboard]
        Voice[Web Speech API: SpeechSynthesis]
        Chart[Recharts Interactive Visualizer]
        Alert[Conditional Rain Alert Banner]
    end

    subgraph Data_Tier [Data Collection & Feature Pipeline]
        OpenMeteo[Open-Meteo Historical Archive API]
        RawData[chennai_weather.csv - 2,192 Days]
        FeatEng[Feature Engineering: day_of_year, month, season]
        SafeSplit[Data Leakage Safe Chronological Split 80/20]
    end

    subgraph ML_Tier [Machine Learning Ensemble Tier]
        TempModel[RandomForestRegressor - temp_max_tomorrow]
        RainModel[RandomForestClassifier - rain_tomorrow]
        Joblib[joblib Serialization: .pkl files]
    end

    subgraph API_Tier [Backend REST API Gateway]
        FastAPI[FastAPI REST Server: Uvicorn]
        Pydantic[Pydantic v2 Schema Validation]
        Service[WeatherPredictionService Singleton]
        Threshold[Rain Risk Categorizer & Advice Engine]
    end

    OpenMeteo --> RawData --> FeatEng --> SafeSplit
    SafeSplit --> TempModel & RainModel
    TempModel & RainModel --> Joblib
    Joblib --> Service

    User --> NextJS
    NextJS --> FastAPI
    FastAPI --> Pydantic --> Service --> Threshold
    Threshold --> FastAPI
    FastAPI --> NextJS
    NextJS --> Alert
    NextJS --> Chart
    NextJS --> Voice
```

---

## 2. Temporal Data Leakage Elimination & Pipeline Flow

```text
+-----------------------------------------------------------------------------------+
|                        CHRONOLOGICAL TIME-SERIES PIPELINE                         |
+-----------------------------------------------------------------------------------+
|  Date (t)   | Features X(t) [Temp, Rain, Press...] | Targets y(t) [Shifted to t+1]|
|-------------|--------------------------------------|------------------------------|
| 2020-01-01  | Max: 26.9°C, Rain: 6.6mm, Press...   | Temp_Next: 27.3°C, Rain_Next:1|
| 2020-01-02  | Max: 27.3°C, Rain: 2.3mm, Press...   | Temp_Next: 28.7°C, Rain_Next:1|
| 2020-01-03  | Max: 28.7°C, Rain: 1.6mm, Press...   | Temp_Next: 28.8°C, Rain_Next:1|
|     ...     |                 ...                  |             ...              |
| 2025-12-30  | Max: 29.2°C, Rain: 0.0mm, Press...   | Temp_Next: 29.5°C, Rain_Next:0|
| 2025-12-31  | [DROPPED: No known ground truth for next day]                        |
+-----------------------------------------------------------------------------------+
                                         │
                   Chronological 80/20 Split (NO SHUFFLE)
                                         │
        ┌────────────────────────────────┴────────────────────────────────┐
        ▼                                                                 ▼
Training Partition (80%)                                          Testing Partition (20%)
1,752 Daily Records                                              439 Daily Records
Jan 01, 2020 -> Oct 17, 2024                                     Oct 18, 2024 -> Dec 30, 2025
        │                                                                 │
        ▼                                                                 ▼
Model Training (Random Forest)                                   Unbiased Generalization Test
                                                                 MAE = 0.940°C, F1 = 0.849
```

---

## 3. Sequence Diagram of API Request & Inference Flow

### Mermaid Sequence Diagram
```mermaid
sequenceDiagram
    autonumber
    actor User as User / Assistive Technology
    participant UI as Next.js Dashboard
    participant API as Open-Meteo API
    participant Server as FastAPI Gateway
    participant Pydantic as Pydantic Validator
    participant Service as PredictionService
    participant Models as RF Models (.pkl)
    participant Speech as Web Speech API

    User->>UI: Opens Application
    UI->>API: GET /forecast (Fetch Live Chennai Weather)
    API-->>UI: Returns Current Day Observations
    UI->>Server: POST /predict (Today's Weather Features JSON)
    Server->>Pydantic: Validate Ranges (Humidity 0-100%, Press 800-1200)
    Pydantic-->>Server: Validation OK
    Server->>Service: predict(weather_features)
    Service->>Models: Regressor.predict(X)
    Models-->>Service: predicted_temp_max = 30.7 °C
    Service->>Models: Classifier.predict_proba(X)
    Models-->>Service: rain_probability = 0.78 (78%)
    Service->>Service: Evaluate Threshold (0.78 -> HIGH Risk)
    Service-->>Server: Returns Structured Prediction Dict
    Server-->>UI: 200 OK JSON Response
    UI->>UI: Render WeatherCard, PredictionCard & Recharts Graph
    opt Risk is HIGH or VERY HIGH
        UI->>UI: Display Animated Red/Orange RainAlert Banner
    end
    User->>UI: Clicks "Enable Voice Forecast"
    UI->>Speech: window.speechSynthesis.speak(utterance)
    Speech-->>User: Auditory Spoken Forecast Broadcast
```

---

## 4. Rain Risk Level Decision Logic

```text
                          ML-Estimated Rain Probability: P(Rain)
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    ▼                      ▼                      ▼
             0.00 <= P <= 0.30      0.31 <= P <= 0.60      0.61 <= P <= 0.80
                    │                      │                      │
             Risk: LOW              Risk: MODERATE         Risk: HIGH
             Advice: Outdoor        Advice: Keep an        Advice: Carry
             activities fine.       umbrella nearby.       an umbrella.
                    │                      │                      │
                    └──────────────────────┼──────────────────────┘
                                           │
                                           ▼
                                    0.81 <= P <= 1.00
                                           │
                                    Risk: VERY HIGH
                                    Advice: Avoid unnecessary
                                    outdoor travel.
```

---

## 5. Screen Reader & Accessibility Flow

```text
                           Keyboard Focus (Tab Key)
                                      │
                                      ▼
                        Voice Accessibility Button
                                      │
                 Does browser support window.speechSynthesis?
                                ├── No ──> Render Fallback Status
                                └── Yes ─> Create SpeechSynthesisUtterance
                                                  │
                                                  ▼
                                     Set Pitch: 1.0, Rate: 0.95
                                                  │
                                                  ▼
                                      Spoken Text Assembly:
"Tomorrow in Chennai, the predicted maximum temperature is [X] degrees Celsius.
 The estimated probability of rain is [Y] percent. Rain risk is [Z]. [Advice]"
                                                  │
                                                  ▼
                                       Audio Playback (Speakers)
```
