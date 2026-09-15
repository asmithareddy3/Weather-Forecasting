# Accessible AI Weather Forecasting and Rain Alert System

Final-Year B.Tech CSE (AI/ML) Capstone Project.

An intelligent, accessible, production-style weather forecasting and rain alert web application powered by Machine Learning and browser-based speech synthesis, initially customized for **Chennai, India**.

---

## 📌 Project Overview

Traditional weather applications present dense tables and charts that are difficult to interpret quickly and often inaccessible to visually impaired users. This project solves these challenges by combining:
1. **Machine Learning Weather Forecasting**:
   - **Tomorrow's Maximum Temperature (°C)** predicted via a `RandomForestRegressor`.
   - **Tomorrow's Rain Probability (%) & Risk Level** predicted via a `RandomForestClassifier`.
2. **Actionable Weather Intelligence**: Transparent risk threshold classification (`LOW`, `MODERATE`, `HIGH`, `VERY HIGH`) with plain-language advice (e.g., *"High chance of rain. Carry an umbrella."*).
3. **Auditory Voice Accessibility**: Integrated **Web Speech API (`SpeechSynthesis`)** providing one-click spoken audio forecasts tailored for visually impaired users.
4. **Modern Responsive UI**: Dark glassmorphic dashboard built with Next.js, React, Tailwind CSS, and Recharts.

---

## 🏛️ System Architecture

```text
               User (Browser / Screen Reader)
                            │
                            ▼
             Next.js 14 Frontend (React + TypeScript)
              ├── Weather Dashboard UI (Tailwind CSS)
              ├── Trend Visualizer (Recharts)
              └── Voice Forecast (Browser SpeechSynthesis API)
                            │
               REST API Request (JSON)
                            ▼
               FastAPI Backend (Python 3.11)
              ├── Pydantic Input Validation
              ├── CORS Middleware (Security)
              └── Prediction Service
                     │               │
                     ▼               ▼
           RandomForestRegressor   RandomForestClassifier
           (Tomorrow's Max Temp)   (Tomorrow's Rain Prob)
                     │               │
                     └───────┬───────┘
                             ▼
                 Risk Categorization & Advice
                             │
                  Structured JSON Response
```

### Historical Data & Training Pipeline:
```text
Open-Meteo Archive API ──> Raw CSV (2020–2025) ──> Data Cleaning & Imputation
                                                              │
                                                              ▼
Serialized Models (.pkl) <── Model Evaluation <── Chronological Split (80/20)
(temp_model & rain_model)   (MAE, RMSE, R², F1)   (No Random Shuffling!)
```

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | FastAPI (0.141) | Asynchronous, high-performance REST API with automatic OpenAPI Swagger docs |
| **Server** | Uvicorn | ASGI web server for asynchronous request handling |
| **Data Validation** | Pydantic v2 | Strict request/response schema validation and type coercion |
| **Machine Learning** | scikit-learn (1.9) | `RandomForestRegressor` and `RandomForestClassifier` |
| **Data Processing** | pandas (3.0), NumPy | Time-series data cleaning, feature engineering, and shifting |
| **Serialization** | joblib (1.6) | Efficient persistence of trained ML models and feature column order |
| **Frontend Framework** | Next.js 14 (App Router) | Server/Client components, optimized production builds |
| **Language** | TypeScript | Strong static typing across UI components and API callers |
| **Styling** | Tailwind CSS | Modern dark glassmorphism, responsive grid layouts |
| **Data Visualization** | Recharts (2.12) | Interactive temperature and rain probability trend charts |
| **Icons** | Lucide React | Modern iconography for meteorological metrics |
| **Accessibility** | Web Speech API | Client-side `window.speechSynthesis` for spoken audio forecasts |

---

## 📊 Dataset & Feature Engineering

### 1. Data Collection
- **Source**: Open-Meteo Historical Weather Archive API.
- **Location**: Chennai, India (Latitude: `13.0827`, Longitude: `80.2707`).
- **Date Range**: 2020-01-01 through 2025-12-31 (**2,192 daily records**).
- **Core Meteorological Variables**:
  `temp_max`, `temp_min`, `temp_mean`, `humidity`, `rain`, `wind_max`, `pressure`, `cloud_cover`.

### 2. Feature Engineering
- `day_of_year`: (1–366) Captures annual cyclical solar patterns.
- `month`: (1–12) Captures monthly macro-climate trends.
- `season`: Numeric Indian meteorological seasons (1: Winter, 2: Summer, 3: Southwest Monsoon, 4: Northeast Post-monsoon).

### 3. Next-Day Target Creation & Prevention of Data Leakage
- `temp_max_tomorrow` = $temp\_max_{t+1}$
- `rain_tomorrow` = $1\text{ if }rain_{t+1} > 0\text{ else }0$
- **Data Leakage Safeguard**: Input features strictly use today's ($t$) observations. Tomorrow's features ($t+1$) are never provided as inputs during training or inference. The final record was safely dropped.

---

## 🤖 Machine Learning Models & Results

An **80/20 Chronological Train/Test Split** was strictly enforced (Train: 1,752 days, Test: 439 days) to respect time-series causality without random shuffling.

### Model 1: Temperature Regressor (`RandomForestRegressor`)
* **Target**: Tomorrow's Maximum Temperature (°C)
* **MAE (Mean Absolute Error)**: **`0.940 °C`** (Average prediction deviation under 1°C)
* **RMSE (Root Mean Squared Error)**: **`1.251 °C`**
* **$R^2$ Score**: **`0.863`** (Explains 86.3% of temperature variance)
* **Top Predictive Feature**: Today's `temp_max` (85.2% relative importance)

### Model 2: Rain Classifier (`RandomForestClassifier`)
* **Target**: Tomorrow's Rain Occurrence (Binary: 0 or 1)
* **Accuracy**: **`77.9%`**
* **Precision**: **`0.850`** (85% of predicted rain days materialized)
* **Recall**: **`0.847`** (84.7% of actual rain days correctly detected)
* **F1-Score**: **`0.849`**
* **Probability Output**: Computed via `predict_proba(X)` to provide continuous **"ML-estimated rain probability"** (0–100%).

---

## ⚖️ Rain Risk Threshold Logic

| Probability Range | Risk Level | Actionable User Advice |
| :--- | :--- | :--- |
| **0% – 30%** | `LOW` | *"Low chance of rain. Outdoor activities should be fine."* |
| **31% – 60%** | `MODERATE` | *"Moderate chance of rain. Keep an umbrella nearby."* |
| **61% – 80%** | `HIGH` | *"High chance of rain. Carry an umbrella."* |
| **81% – 100%** | `VERY HIGH` | *"Very high chance of rain. Consider avoiding unnecessary outdoor activities."* |

---

## 🚀 Installation & Local Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ & npm
- Git

### 1. Clone the Repository
```powershell
git clone <your-repo-url>
cd DMPA
```

---

### 2. Backend Setup (FastAPI)

```powershell
# Navigate to backend directory
cd backend

# Create & activate Python virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Upgrade pip & install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# (Optional) Retrain models or re-fetch data if needed
python fetch_data.py
python preprocess.py
python train_models.py

# Run API endpoint tests
python test_api.py

# Start the FastAPI server
python -m uvicorn main:app --reload --port 8000
```
- API Base URL: `http://127.0.0.1:8000`
- Interactive Swagger Docs: `http://127.0.0.1:8000/docs`
- Health Check: `http://127.0.0.1:8000/health`

---

### 3. Frontend Setup (Next.js)

Open a second PowerShell terminal:
```powershell
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# (Optional) Verify production build
npm run build

# Start Next.js development server
npm run dev
```
- Open browser at: `http://localhost:3000`

---

## 📡 REST API Documentation

### `GET /health`
Verifies backend operational status and model readiness.
```json
{
  "status": "healthy",
  "city": "Chennai, India",
  "models_loaded": true
}
```

### `POST /predict`
Submits current daily weather observations to generate next-day predictions.

**Request Body**:
```json
{
  "temp_max": 32.4,
  "temp_min": 25.1,
  "temp_mean": 28.7,
  "humidity": 78.0,
  "rain": 2.5,
  "wind_max": 16.2,
  "pressure": 1008.5,
  "cloud_cover": 65.0,
  "day_of_year": 285,
  "month": 10,
  "season": 4
}
```

**Response Body**:
```json
{
  "predicted_temp_max": 31.8,
  "rain_probability": 0.82,
  "rain_probability_percent": 82,
  "risk_level": "VERY HIGH",
  "advice": "Very high chance of rain. Consider avoiding unnecessary outdoor activities."
}
```

---

## 🔒 Environment Variables

### Backend (`backend/.env`):
```env
PORT=8000
FRONTEND_URL=http://localhost:3000
```

### Frontend (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

---

## 📸 Screenshots Section Placeholder

> *Placeholder for project presentation screenshots:*
> 1. Main WeatherAI Dashboard (Dark Glassmorphic UI)
> 2. Tomorrow's AI Prediction Card & High Rain Alert Banner
> 3. Weekly Temperature & Rain Trend Area Chart
> 4. Auditory Voice Forecast in Action with SpeechSynthesis

---

## 🔮 Future Enhancements

1. **Multi-City Support**: Seamlessly expand beyond Chennai by integrating a centralized city coordinates dropdown (e.g., Bengaluru, Mumbai, Delhi, Hyderabad).
2. **Hourly Deep Learning Models**: Implement an LSTM/Transformer architecture for 24-hour granular precipitation step forecasting.
3. **Multilingual Voice Output**: Support regional Indian languages (Tamil, Hindi, Telugu) in the browser `SpeechSynthesisUtterance`.
4. **Progressive Web App (PWA)**: Offline caching and push notification rain alarms for morning commutes.

---

## 🎓 Author & Viva Information

- **Student Name**: Asmitha G
- **Degree**: Final-Year B.Tech Computer Science and Engineering (AI & ML)
- **Project Topic**: Accessible AI Weather Forecasting and Rain Alert System
- **Academic Year**: 2025–2026
