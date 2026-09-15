# Complete Cloud Hosting & Deployment Guide
## "Accessible AI Weather Forecasting and Rain Alert System"

This step-by-step guide explains how to deploy both the **FastAPI Backend** and the **Next.js Frontend** to free cloud hosting platforms for your final-year college project presentation.

---

## 🗺️ Recommended Hosting Stack

* **Frontend**: **Vercel** (Free, built by the creators of Next.js, zero-config deployment)
* **Backend**: **Render** (Free tier Web Service for Python 3.11 & FastAPI) or **Railway** / **Hugging Face Spaces**
* **Repository**: **GitHub** (Acts as the source for automatic deployments)

---

## Step 1: Push Your Code to GitHub

1. Open PowerShell in your project root (`c:\DMPA`):
```powershell
cd c:\DMPA
git init
git add .
git commit -m "feat: complete accessible ai weather forecasting system"
```

2. Go to [GitHub.com](https://github.com) and click **New Repository**:
   * Repository name: `Accessible-AI-Weather-Forecasting`
   * Visibility: **Public** or **Private**
   * Do not initialize with a README (we already have one).

3. Link and push your local code:
```powershell
git branch -M main
git remote add origin https://github.com/<your-username>/Accessible-AI-Weather-Forecasting.git
git push -u origin main
```

---

## Step 2: Deploy Backend to Render (Free Python Host)

1. Go to [render.com](https://render.com) and sign up / log in with your GitHub account.
2. In the Render Dashboard, click **New +** $\rightarrow$ **Web Service**.
3. Choose **Build and deploy from a Git repository**, click **Next**, and select your GitHub repository.
4. Configure the Web Service settings:
   * **Name**: `weatherai-backend` (or your preferred name)
   * **Region**: *Singapore* or *Frankfurt* (Singapore is closest to India for lowest latency)
   * **Branch**: `main`
   * **Root Directory**: `backend` *(Crucial!)*
   * **Runtime**: `Python 3`
   * **Build Command**:
     ```bash
     pip install --upgrade pip && pip install -r requirements.txt
     ```
   * **Start Command**:
     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
   * **Instance Type**: `Free`
5. **Environment Variables**:
   Under the **Environment Variables** section, add:
   * `PYTHON_VERSION` = `3.11.9`
   * `FRONTEND_URL` = `*` *(or your Vercel URL once deployed)*
6. Click **Create Web Service**.
7. Wait ~2–3 minutes for the build to finish. Once live, Render will give you a public URL such as:
   `https://weatherai-backend-xxxx.onrender.com`
8. **Verify Backend Health**:
   Open in browser:
   `https://weatherai-backend-xxxx.onrender.com/health`
   Expected response:
   ```json
   {"status":"healthy","city":"Chennai, India","models_loaded":true}
   ```
   Interactive Swagger docs are live at:
   `https://weatherai-backend-xxxx.onrender.com/docs`

---

## Step 3: Deploy Frontend to Vercel (Next.js)

1. Go to [vercel.com](https://vercel.com) and log in with your GitHub account.
2. Click **Add New...** $\rightarrow$ **Project**.
3. Import your GitHub repository: `Accessible-AI-Weather-Forecasting`.
4. In the Project Configuration screen:
   * **Project Name**: `weatherai-accessible`
   * **Framework Preset**: `Next.js`
   * **Root Directory**: Click **Edit** and select `frontend` *(Crucial!)*
5. **Environment Variables**:
   Expand the **Environment Variables** section and add:
   * **Key**: `NEXT_PUBLIC_API_URL`
   * **Value**: Your Render backend URL (e.g., `https://weatherai-backend-xxxx.onrender.com`)
   *(Make sure there is no trailing slash at the end)*
6. Click **Deploy**.
7. In ~60 seconds, your site will be live! Vercel will provide an SSL-secured URL like:
   `https://weatherai-accessible.vercel.app`

---

## Step 4: Final Connection & CORS Adjustment

Once Vercel gives you your production frontend URL (e.g. `https://weatherai-accessible.vercel.app`):
1. Go back to [render.com](https://render.com) $\rightarrow$ Your backend Web Service $\rightarrow$ **Environment**.
2. Update:
   * `FRONTEND_URL` = `https://weatherai-accessible.vercel.app`
3. Click **Save Changes**. Render will automatically redeploy with the updated CORS policy.

---

## Step 5: Demonstration Checklist for External Viva

Before your project presentation / evaluation:
- [ ] Open the live Vercel URL on your laptop and phone to demonstrate **Responsive Layout**.
- [ ] Verify that current weather loads from Open-Meteo for Chennai.
- [ ] Verify that **Tomorrow's AI Prediction** displays both the predicted maximum temperature and rain risk badge.
- [ ] Click the **"Enable Voice Forecast"** button in front of the examiners to demonstrate auditory speech accessibility.
- [ ] Open the backend Swagger documentation URL (`https://your-backend.onrender.com/docs`) on a second tab to show interactive REST API endpoints (`GET /health` and `POST /predict`).
