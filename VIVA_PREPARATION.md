# Comprehensive Viva Preparation Guide
## "Accessible AI Weather Forecasting and Rain Alert System"
### Final-Year B.Tech CSE (AI/ML) Project

This reference document contains clear, simple, and high-scoring answers to all the questions external and internal examiners are likely to ask during your final project viva.

---

### Table of Contents
1. [Core Machine Learning Architecture](#1-core-machine-learning-architecture)
2. [Data Engineering & Prevention of Leakage](#2-data-engineering--prevention-of-leakage)
3. [Evaluation Metrics & Probabilities](#3-evaluation-metrics--probabilities)
4. [Backend, API & System Design](#4-backend-api--system-design)
5. [Frontend & Voice Accessibility](#5-frontend--voice-accessibility)
6. [Scalability & Multi-City Extension](#6-scalability--multi-city-extension)

---

### 1. Core Machine Learning Architecture

#### Q1: Why did you choose Random Forest instead of Linear Regression or deep neural networks?
* **Answer**:
  * Weather phenomena are inherently non-linear (e.g., higher humidity does not linearly increase rainfall unless surface pressure and cloud cover align). Linear regression fails to capture these complex interactions.
  * Neural networks require huge datasets (hundreds of thousands of rows) and extensive hyperparameter tuning. With 2,192 daily tabular records, Random Forest provides higher accuracy, resists overfitting via bagging (bootstrap aggregating), requires no feature scaling, and handles tabular data exceptionally well.

#### Q2: Why did you build TWO separate models instead of one single multi-output model?
* **Answer**:
  * Temperature forecasting is a **continuous regression** problem (predicting a real number like 30.7°C), optimizing Mean Squared Error.
  * Rain forecasting is a **binary classification** problem (predicting rain vs no rain with probability), optimizing log-loss/entropy.
  * Decoupling into `RandomForestRegressor` and `RandomForestClassifier` allows each algorithm to optimize its own loss function and tree split criteria independently.

#### Q3: Why is temperature prediction treated as regression and rain as classification?
* **Answer**:
  * **Regression for Temperature**: Temperature takes continuous numerical values. We need precise numerical values (e.g., 32.4°C vs 33.1°C).
  * **Classification for Rain**: Daily precipitation amounts are heavily skewed (many zero-rain days). For an actionable public advisory, citizens primarily need to know *"Will it rain tomorrow, and with what confidence?"* rather than guessing exact millimeter fractions.

---

### 2. Data Engineering & Prevention of Leakage

#### Q4: Why did you use an 80/20 Chronological Train/Test Split instead of standard random shuffling?
* **Answer**:
  * Weather is **time-series** data where adjacent days are autocorrelated. If we shuffle data randomly, day $t-1$ and day $t+1$ would be in the training set while day $t$ is in the test set. The model would effectively "peek" into the future, creating severe artificial inflation of test accuracy.
  * Chronological splitting (training on 2020–2024 and testing on 2024–2025) simulates realistic production conditions where past data predicts an unseen future.

#### Q5: What is Data Leakage and how did you prevent it?
* **Answer**:
  * **Data Leakage** happens when information from the target or the future is accidentally fed into the model during training, giving unrealistic performance that fails in production.
  * **Prevention**: We strictly aligned today's observations ($X_t$) to tomorrow's targets ($y_{t+1}$). Tomorrow's weather features (like tomorrow's humidity or pressure) are never included in the input feature matrix $X$. The final row of the dataset was dropped because tomorrow's ground truth was unknown.

#### Q6: Why did you engineer `day_of_year`, `month`, and `season` features?
* **Answer**:
  * Tree algorithms evaluate features independently at each split and cannot automatically extract cyclical date patterns from a raw timestamp.
  * Providing `day_of_year` (1–366) captures solar radiation cycles, while `season` (1: Winter, 2: Summer, 3: Southwest Monsoon, 4: Northeast Post-monsoon) explicitly signals Chennai's intense late-year monsoon patterns.

---

### 3. Evaluation Metrics & Probabilities

#### Q7: What is MAE and what did your temperature model achieve?
* **Answer**:
  * **MAE (Mean Absolute Error)** measures the average magnitude of errors between predicted and actual temperatures:
    $$\text{MAE} = \frac{1}{n}\sum_{i=1}^{n}|y_i - \hat{y}_i|$$
  * Our model achieved an **MAE of 0.940°C**, meaning our predictions deviate by less than 1°C on average.

#### Q8: What are Precision, Recall, and F1-score for your rain model?
* **Answer**:
  * **Precision (85.0%)**: Out of all days our model predicted rain, 85% actually experienced rain (minimizes false alarms).
  * **Recall (84.7%)**: Out of all days that actually rained, our model correctly identified 84.7% (minimizes missed rain events).
  * **F1-Score (0.849)**: The harmonic mean of precision and recall ($\frac{2 \cdot P \cdot R}{P + R}$), proving balanced performance.

#### Q9: Why use `predict_proba()` instead of binary `predict()`?
* **Answer**:
  * In weather forecasting, a binary 0 or 1 is too rigid. `predict_proba()` calculates the percentage of trees in the Random Forest that voted for rain (e.g., 78 out of 100 trees $\rightarrow$ 78% probability).
  * We term this **"ML-estimated rain probability"** and use it to map directly into public safety risk categories (`LOW`, `MODERATE`, `HIGH`, `VERY HIGH`).

---

### 4. Backend, API & System Design

#### Q10: Why did you choose FastAPI over Flask or Django?
* **Answer**:
  * **Asynchronous Performance**: Built on ASGI (Starlette) for high concurrency.
  * **Automatic Data Validation**: Pydantic v2 automatically validates request payloads and returns HTTP 422 if data types or ranges are invalid.
  * **Automatic Swagger UI**: Generates interactive OpenAPI documentation at `/docs` without third-party plugins.

#### Q11: How is model serialization handled?
* **Answer**:
  * We use `joblib.dump()` to serialize the trained models into `temp_model.pkl`, `rain_model.pkl`, and `feature_columns.pkl`.
  * FastAPI loads these files into memory **once** on startup using a singleton service pattern, avoiding retraining on each request and delivering sub-10ms inference times.

---

### 5. Frontend & Voice Accessibility

#### Q12: How does the frontend communicate with the FastAPI backend?
* **Answer**:
  * The Next.js frontend calls `POST /predict` using standard HTTP `fetch`.
  * The request payload contains validated JSON features. FastAPI validates and scores the features, and returns JSON containing predicted temperature, rain percentage, risk level, and advice.
  * CORS middleware is configured to secure cross-origin communication between `http://localhost:3000` and `http://127.0.0.1:8000`.

#### Q13: How does the Voice Accessibility feature work?
* **Answer**:
  * It uses the browser's native **Web Speech API (`window.speechSynthesis`)** and `SpeechSynthesisUtterance`.
  * When triggered by the user, it parses the prediction into a clear audio statement:
    *"Tomorrow in Chennai, the predicted maximum temperature is 30.7 degrees Celsius. The estimated probability of rain is 78 percent. Rain risk is high. Carry an umbrella."*
  * It adheres to accessibility standards by requiring explicit user interaction to initiate audio, preventing unexpected playback.

---

### 6. Scalability & Multi-City Extension

#### Q14: How can this system be scaled to support multiple cities?
* **Answer**:
  * In `fetch_data.py`, city metadata is stored in a centralized configuration dictionary (`latitude`, `longitude`, `filename`).
  * To support Bengaluru, Mumbai, or Delhi, we simply add their coordinates to the registry, run automated data ingestion, and train localized model weights.
  * The frontend already uses centralized API constants and can render a city selection dropdown dynamically.
