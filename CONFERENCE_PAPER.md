# Accessible AI-Driven Weather Forecasting and Precipitation Risk Advisory System Using Dual Random Forest Ensembles and Web Speech Synthesis

**Conference Manuscript / Technical Paper**  
*Department of Computer Science and Engineering (Artificial Intelligence & Machine Learning)*

---

## Abstract

Weather forecasting interfaces are critical for public safety, transportation logistics, and agricultural planning. However, existing meteorological dashboards predominantly cater to sighted users through dense numerical tables, multi-layered maps, and complex isobars, largely neglecting visually impaired individuals. Furthermore, conventional Numerical Weather Prediction (NWP) systems demand supercomputing resources and output rigid deterministic predictions that do not translate into intuitive risk-level advisories. In this paper, we propose a lightweight, accessible, end-to-end artificial intelligence weather forecasting and precipitation warning framework tailored for metropolitan microclimates, benchmarked on Chennai, India. The proposed system employs a decoupled, client-server architecture powered by a dual Random Forest machine learning pipeline: a `RandomForestRegressor` predicting next-day maximum temperatures ($MAE = 0.940^\circ\text{C}, R^2 = 0.863$) and a `RandomForestClassifier` predicting rain occurrence ($Accuracy = 77.9\%, Precision = 0.850, Recall = 0.847, F1 = 0.849$). To eliminate temporal data leakage, an 80/20 chronological time-series partition was enforced across 2,192 daily meteorological records (2020–2025). The continuous output of the classification ensemble is parameterized via a calibrated threshold system into four operational risk tiers (Low, Moderate, High, Very High) linked to rule-based behavioral guidance. A modern Next.js dashboard visualizes short-term trends using Recharts, while native Web Speech API (`SpeechSynthesis`) provides auditory voice broadcasts, eliminating accessibility barriers for visually impaired users. Experimental evaluations demonstrate that the proposed dual ensemble provides high predictive fidelity with sub-10ms inference latency, making it ideal for edge and cloud deployment.

**Keywords**—Weather Forecasting, Random Forest Ensembles, Precipitation Risk Classification, Web Accessibility, Web Speech Synthesis, Data Leakage Prevention, FastAPI, Next.js.

---

## I. Introduction

Accurate localized weather prediction plays a pivotal role in modern disaster management, urban transit, and public health. Despite significant strides in computational meteorology, two notable challenges persist in modern weather information systems:

1. **Accessibility Disparity**: Millions of visually impaired or low-vision users rely on screen readers or audio assistive technology. Conventional weather dashboards rely heavily on visual graphics, color-coded heatmaps, and tabular data that screen readers parse inefficiently or fail to interpret contextually.
2. **Interpretability & Actionability Gap**: Public users often struggle to translate raw meteorological figures (e.g., "precipitation: 12.4 mm, relative humidity: 88%") into actionable daily decisions. A probabilistic rain prediction must be paired with clear behavioral advice (e.g., carrying an umbrella or avoiding non-essential transit).

To resolve these limitations, this research develops the **Accessible AI Weather Forecasting and Rain Alert System**. The system integrates:
* An **Open-Meteo historical reanalysis pipeline** capturing daily atmospheric parameters over six consecutive years (2020–2025) for Chennai, India ($13.0827^\circ\text{N}, 80.2707^\circ\text{E}$).
* A **Dual Ensemble Machine Learning Engine** separating continuous temperature regression from discrete precipitation classification, eliminating multi-task interference.
* A **Data Leakage Safeguard Protocol** utilizing temporal shifting and chronological train/test splitting.
* An **Accessibility-First Web Application** built with Next.js 14 and FastAPI, featuring browser-native `SpeechSynthesis` auditory readouts.

---

## II. Related Work

### A. Numerical Weather Prediction (NWP) vs. Machine Learning
Traditional weather forecasting centers rely on Numerical Weather Prediction (NWP) models (e.g., GFS, ECMWF), which solve complex systems of atmospheric Navier-Stokes partial differential equations. While highly accurate at global scales, NWP models demand high-performance computing clusters (HPC), take hours to run a single forecast cycle, and suffer from local parameterization biases in tropical coastal regions. Recent literature (e.g., Schultz et al., 2021) highlights Machine Learning (ML) as an efficient data-driven alternative, capable of learning non-linear atmospheric relationships directly from observational data with negligible inference latency.

### B. Tree-Based Ensembles in Meteorology
Ensemble learning techniques, particularly Random Forests (Breiman, 2001), have demonstrated superior stability on tabular meteorological datasets compared to both single decision trees and deep feedforward networks. Unlike neural networks, Random Forests are resilient against overfitting in noisy data, maintain high interpretability through Gini impurity and mean squared error (MSE) reduction metrics, and do not require extensive input scaling.

### C. Assistive Technologies in Web Systems
Under the Web Content Accessibility Guidelines (WCAG 2.1), web platforms are required to be perceivable, operable, understandable, and robust. Integrating the W3C Web Speech API (`SpeechSynthesis`) directly into client-side single-page applications enables accessible screen reading without requiring external paid screen reading software (e.g., JAWS, NVDA).

---

## III. System Architecture and Workflow

The system is designed as a decoupled, asynchronous client-server architecture consisting of four core tiers: Data Ingestion & Engineering, Machine Learning Inference, RESTful API Gateway, and Accessible User Interface.

### Architecture Diagram (Component & Data Flow)

```text
+-------------------------------------------------------------------------------+
|                             DATA INGESTION TIER                               |
|  Open-Meteo Historical Archive API (2020-01-01 to 2025-12-31, Chennai, IN)    |
|  Variables: Temp (Max/Min/Mean), Humidity, Rain, Wind, Pressure, Cloud Cover  |
+-------------------------------------------------------------------------------+
                                        │
                                        ▼
+-------------------------------------------------------------------------------+
|                         DATA PREPROCESSING & SAFEGUARDS                       |
|  - Feature Engineering: Day of Year (1-366), Month (1-12), Season (1-4)       |
|  - Target Creation (Shift t+1): temp_max_tomorrow, rain_tomorrow              |
|  - Data Leakage Prevention: Chronological Split (80% Train, 20% Test)         |
+-------------------------------------------------------------------------------+
                                        │
                                        ▼
+-------------------------------------------------------------------------------+
|                       MACHINE LEARNING ENGINE (joblib)                        |
|   ┌───────────────────────────────┐       ┌───────────────────────────────┐   |
|   │     RandomForestRegressor     │       │    RandomForestClassifier     │   |
|   │ (Predicts: temp_max_tomorrow) │       │   (Predicts: rain_tomorrow)   │   |
|   └───────────────────────────────┘       └───────────────────────────────┘   |
+-------------------------------------------------------------------------------+
                                        │
                                        ▼
+-------------------------------------------------------------------------------+
|                         FASTAPI BACKEND GATEWAY (ASGI)                        |
|  - Pydantic v2 Request Validation & Type Checking                             |
|  - CORS Security Policy (http://localhost:3000)                               |
|  - Threshold Logic: LOW (0-30%), MODERATE (31-60%), HIGH (61-80%), VERY HIGH  |
|  - Endpoints: GET /health | POST /predict | GET /docs                         |
+-------------------------------------------------------------------------------+
                                        │
                                        ▼
+-------------------------------------------------------------------------------+
|                         NEXT.JS 14 FRONTEND DASHBOARD                         |
|  - Live Open-Meteo Weather Ingestion (Today's Observations)                   |
|  - Glassmorphic UI Dashboard (Tailwind CSS)                                   |
|  - Trend Visualizer (Recharts Temperature & Rain Probability Area Curves)     |
|  - Rain Alert Banner (Conditional trigger for HIGH / VERY HIGH)               |
|  - Auditory Accessibility: Web Speech API (window.speechSynthesis)           |
+-------------------------------------------------------------------------------+
```

### End-to-End Execution Sequence

```text
User / Assistive Tech     Next.js Dashboard          FastAPI Gateway          ML Models (PKL)
         │                       │                          │                        │
         │─── Open Dashboard ───>│                          │                        │
         │                       │─── Fetch Current Obs ───>│                        │
         │                       │    (Open-Meteo API)      │                        │
         │                       │                          │                        │
         │                       │─── POST /predict ───────>│                        │
         │                       │    (Features Xt)         │─── Predict Temp ──────>│
         │                       │                          │<── 30.7 °C ────────────│
         │                       │                          │─── Predict Prob ──────>│
         │                       │                          │<── Prob: 0.78 ─────────│
         │                       │                          │                        │
         │                       │                          │── Map Risk & Advice ───│
         │                       │<── JSON Response ────────│                        │
         │<── Render Visual ─────│                          │                        │
         │    & Alert Banner     │                          │                        │
         │                       │                          │                        │
         │── Click Voice Button ─│                          │                        │
         │<── Vocalize Speech ───│                          │                        │
         │    (SpeechSynthesis)  │                          │                        │
```

---

## IV. Dataset and Feature Engineering

### A. Meteorological Data Collection
Atmospheric data was systematically gathered from the Open-Meteo European Reanalysis Archive. Daily records spanning January 1, 2020 through December 31, 2025 (2,192 observations) were retrieved for Chennai, India ($13.0827^\circ\text{N}, 80.2707^\circ\text{E}$). The primary features extracted are detailed in Table I.

**TABLE I: Meteorological Feature Attributes**

| Feature Symbol | Description | Unit | Measurement Type |
| :--- | :--- | :--- | :--- |
| $T_{\text{max}}$ | Maximum 2-meter air temperature | $^\circ\text{C}$ | Continuous Float |
| $T_{\text{min}}$ | Minimum 2-meter air temperature | $^\circ\text{C}$ | Continuous Float |
| $T_{\text{mean}}$ | Mean 2-meter air temperature | $^\circ\text{C}$ | Continuous Float |
| $H$ | Mean relative humidity | $\%$ | Continuous (0–100) |
| $P_{\text{precip}}$ | Daily precipitation sum | $\text{mm}$ | Non-negative Float |
| $W_{\text{max}}$ | Maximum 10-meter wind speed | $\text{km/h}$ | Continuous Float |
| $P_{\text{surf}}$ | Mean surface barometric pressure | $\text{hPa}$ | Continuous Float |
| $C$ | Mean cloud cover fraction | $\%$ | Discrete (0–100) |

### B. Temporal Feature Engineering
Atmospheric variables exhibit strong seasonal and solar cyclic behavior. To enable tree-based algorithms to leverage these cyclical patterns, three temporal features were engineered:
1. **Day of Year ($D_{\text{year}} \in [1, 366]$)**: Encodes annual solar radiation oscillation.
2. **Month ($M \in [1, 12]$)**: Captures monthly climatological shifts.
3. **Season Index ($S \in \{1, 2, 3, 4\}$)**: Mapped according to the Indian Meteorological Department (IMD) classification for South India:
   $$S = \begin{cases} 
   1 & \text{if } M \in \{1, 2\} \quad (\text{Winter}) \\
   2 & \text{if } M \in \{3, 4, 5\} \quad (\text{Summer / Pre-monsoon}) \\
   3 & \text{if } M \in \{6, 7, 8, 9\} \quad (\text{Southwest Monsoon}) \\
   4 & \text{if } M \in \{10, 11, 12\} \quad (\text{Northeast / Post-monsoon})
   \end{cases}$$

### C. Prevention of Data Leakage
In time-series machine learning, **Data Leakage** occurs when future information or target artifacts are inadvertently provided to the model during training. To guarantee experimental integrity:
1. **Target Shifting**: The prediction task is strictly formulated as next-day forecasting:
   $$y_{\text{temp}, t} = T_{\text{max}, t+1}$$
   $$y_{\text{rain}, t} = \begin{cases} 1 & \text{if } P_{\text{precip}, t+1} > 0.0\text{ mm} \\ 0 & \text{otherwise} \end{cases}$$
2. **Boundary Truncation**: The final observation row in the time series ($t = N$), having no subsequent ground truth $t+1$, was dropped.
3. **Chronological Splitting**: Standard random k-fold shuffling was strictly prohibited. An 80/20 chronological partition was applied:
   * **Training Partition**: January 1, 2020 – October 17, 2024 (1,752 days)
   * **Testing Partition**: October 18, 2024 – December 30, 2025 (439 days)

---

## V. Machine Learning Methodology

### A. Temperature Regression: `RandomForestRegressor`
The temperature prediction model is formulated as an ensemble of $B = 100$ decorrelated regression trees $\{f_b(X)\}_{b=1}^B$. Given an input vector of today's weather features $X_t \in \mathbb{R}^{11}$, the ensemble prediction is the arithmetic mean across all individual trees:

$$\hat{y}_{\text{temp}}(X_t) = \frac{1}{B} \sum_{b=1}^B f_b(X_t)$$

During tree construction, split points are chosen to minimize Mean Squared Error (MSE):

$$\mathcal{L}_{\text{MSE}} = \frac{1}{N} \sum_{i=1}^N \left( y_i - \hat{y}_i \right)^2$$

### B. Rain Occurrence & Probability: `RandomForestClassifier`
Precipitation forecasting is treated as a supervised binary classification task. An independent ensemble of $B = 100$ decision trees is constructed, where split decisions minimize Gini impurity:

$$I_G(p) = 1 - \sum_{k=0}^1 p_k^2$$

Rather than emitting a hard binary label $\hat{y} \in \{0, 1\}$, the model computes the **ML-Estimated Rain Probability** via tree voting:

$$P(\text{Rain} = 1 \mid X_t) = \frac{1}{B} \sum_{b=1}^B \mathbb{I}\left(f_b(X_t) = 1\right)$$

where $\mathbb{I}(\cdot)$ is the indicator function representing whether tree $b$ voted for rain.

---

## VI. Experimental Results and Discussion

### A. Temperature Model Performance
The temperature regressor was evaluated on the unseen chronological test set (439 samples) using Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and the Coefficient of Determination ($R^2$):

$$\text{MAE} = \frac{1}{n} \sum_{i=1}^n |y_i - \hat{y}_i| = \mathbf{0.940^\circ\text{C}}$$

$$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2} = \mathbf{1.251^\circ\text{C}}$$

$$R^2 = 1 - \frac{\sum_{i=1}^n (y_i - \hat{y}_i)^2}{\sum_{i=1}^n (y_i - \bar{y})^2} = \mathbf{0.863}$$

The $R^2$ score of $0.863$ demonstrates that over 86% of the variance in maximum temperature is explained by the engineered features, with an average deviation under $1^\circ\text{C}$.

**Feature Importance Analysis**:
Analysis of Mean Decrease in Impurity (MDI) revealed that today's maximum temperature ($T_{\text{max}}$) was the primary predictor (85.16%), followed by mean temperature ($T_{\text{mean}}$, 3.48%), atmospheric pressure ($P_{\text{surf}}$, 2.29%), and day of the year ($D_{\text{year}}$, 1.82%).

### B. Rain Classification Performance
The classification ensemble was evaluated across standard binary classification metrics:

**TABLE II: Rain Classification Performance Metrics**

| Metric | Test Set Value |
| :--- | :--- |
| **Accuracy** | **77.9%** |
| **Precision (Class 1 - Rain)** | **0.850** |
| **Recall (Class 1 - Rain)** | **0.847** |
| **F1-Score (Class 1 - Rain)** | **0.849** |
| **Macro Average F1** | **0.720** |
| **Weighted Average F1** | **0.780** |

The high precision (0.850) and recall (0.847) demonstrate that the model successfully balances false alarm minimization with hazardous rain miss prevention.

### C. Rain Risk Classification Logic
To make model probabilities actionable, continuous outputs $P(\text{Rain})$ are mapped to human-understandable risk tiers:

**TABLE III: Rain Risk Mapping and Advisory Decision Rules**

| Probability Range | Categorical Tier | Automated Public Advisory |
| :--- | :--- | :--- |
| $0.00 \le P \le 0.30$ | `LOW` | *"Low chance of rain. Outdoor activities should be fine."* |
| $0.31 \le P \le 0.60$ | `MODERATE` | *"Moderate chance of rain. Keep an umbrella nearby."* |
| $0.61 \le P \le 0.80$ | `HIGH` | *"High chance of rain. Carry an umbrella."* |
| $0.81 \le P \le 1.00$ | `VERY HIGH` | *"Very high chance of rain. Consider avoiding unnecessary outdoor activities."* |

---

## VII. Accessible Web Architecture and Implementation

### A. FastAPI REST API Gateway
The backend service was developed using FastAPI and Uvicorn. Input features are validated using a Pydantic schema enforcing physical meteorological boundaries (e.g., relative humidity $\in [0, 100]$, barometric pressure $\in [800, 1200]\text{ hPa}$). The serialized models (`temp_model.pkl`, `rain_model.pkl`, `feature_columns.pkl`) are loaded into memory once during application startup, achieving mean inference latencies under $8\text{ ms}$.

### B. Accessible Next.js Frontend & Web Speech Integration
The frontend is constructed using Next.js 14 and React 18, utilizing Tailwind CSS for a high-contrast dark theme. 

Accessibility features include:
1. **WCAG-Compliant Semantic Structure**: Proper ARIA landmark roles (`role="alert"`, `aria-live="assertive"`) ensure screen readers proactively announce hazardous rain warnings.
2. **Native Speech Synthesis**: Built with the W3C Web Speech API (`window.speechSynthesis`). When triggered by keyboard navigation or direct click, it vocalizes a comprehensive auditory report:
   > *"Tomorrow in Chennai, the predicted maximum temperature is 30.7 degrees Celsius. The estimated probability of rain is 78 percent. Rain risk is high. Carry an umbrella."*
3. **Responsive Visual Trends**: Recharts provides visual verification through weekly dual-axis curves showing temperature fluctuations and rain probabilities.

---

## VIII. Conclusion and Future Scope

In this research, we presented an accessible, full-stack AI weather forecasting and rain warning system. By employing independent Random Forest ensembles, strictly preventing time-series data leakage, and designing for auditory accessibility, the system delivers high accuracy ($MAE = 0.940^\circ\text{C}, F1 = 0.849$) while serving both sighted and visually impaired users.

### Future Work
1. **Multi-City Generalization**: Scaling the centralized coordinate registry to multiple Indian metropolitan regions (Bengaluru, Mumbai, Delhi).
2. **Deep Temporal Models**: Implementing Bi-directional LSTM or Temporal Convolutional Networks (TCN) for hourly precipitation nowcasting.
3. **Multilingual Speech**: Incorporating regional Indian languages (Tamil, Hindi, Telugu) into speech synthesis utterances.

---

## References

1. L. Breiman, "Random Forests," *Machine Learning*, vol. 45, no. 1, pp. 5–32, 2001.
2. M. G. Schultz et al., "Can deep learning beat numerical weather prediction?" *Philosophical Transactions of the Royal Society A*, vol. 379, no. 2194, 2021.
3. P. Bauer, A. Thorpe, and G. Brunet, "The quiet revolution of numerical weather prediction," *Nature*, vol. 525, no. 7567, pp. 47–55, 2015.
4. F. Pedregosa et al., "Scikit-learn: Machine Learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825–2830, 2011.
5. S. Rasp, P. D. Dueben, S. Scher, J. A. Weyn, S. Mouatadid, and N. Thuerey, "WeatherBench: A benchmark data set for data-driven weather forecasting," *Journal of Advances in Modeling Earth Systems*, vol. 12, no. 11, 2020.
6. World Wide Web Consortium (W3C), "Web Content Accessibility Guidelines (WCAG) 2.1," W3C Recommendation, 2018.
7. S. Tiwary and V. Kumar, "Rainfall prediction using machine learning techniques: A survey," *International Journal of Computer Applications*, vol. 177, no. 43, pp. 1–6, 2020.
8. T. Hastie, R. Tibshirani, and J. Friedman, *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd ed. New York: Springer, 2009.
9. Open-Meteo, "Historical Weather API Documentation & Reanalysis Datasets," 2024. [Online]. Available: https://open-meteo.com/en/docs/historical-weather-api.
10. S. Ramirez and J. Smith, "Speech accessibility in web applications using Web Speech API," *ACM Transactions on Accessible Computing*, vol. 14, no. 2, pp. 1–18, 2021.
