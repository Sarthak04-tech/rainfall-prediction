# RainFall AI Predictor

A modern, AI-powered web application for predicting annual rainfall based on monthly data. Built with Flask, Scikit-Learn, and Chart.js.

## Features
- **Accurate Predictions**: Uses Random Forest Regression trained on 115 years of Indian rainfall data.
- **Dynamic Visualization**: Integrated Chart.js to compare your input with historical averages in real-time.
- **Modern UI**: Sleek, responsive design with glassmorphism and smooth animations.
- **Rainfall Categorization**: Automatically categorizes predictions (Low, Normal, High, Extreme).

## Tech Stack
- **Backend**: Python, Flask
- **ML**: Scikit-Learn, Pandas, NumPy
- **Frontend**: HTML5, Vanilla CSS3 (Custom Design), JavaScript (ES6+), Chart.js

## One-Click Launch (Windows)

Simply double-click:
- **`START.bat`**: Automatically checks Python, creates/activates virtual environment, installs dependencies, checks file integrity, launches the application server, and opens your default browser at `http://127.0.0.1:5000`.
- **`STOP.bat`**: Safely stops any server running on port 5000.

---

## Manual Setup Instructions

### 1. Prerequisites
- Python 3.8+
- pip (Python package manager)

### 2. Installation
Clone or navigate to the repository and install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Model & Data Preparation
- Trained model: `model_unzipped/rainfall_model.pkl` (extracted from `rainfall_model.zip` if needed)
- Dataset: `dataset/rainfall in india 1901-2015.csv`

### 4. Running the App
Start the app:
```bash
python app.py
```
Open your browser at `http://127.0.0.1:5000`.

## Deployment on Render

This project includes a ready-to-use [`render.yaml`](render.yaml) blueprint specification for 1-click deployment.

### Option A: Via Render Blueprint (Recommended)
1. Go to [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** > **Blueprint**.
3. Connect your GitHub repository: `https://github.com/Sarthak04-tech/rainfall-prediction`.
4. Render will automatically read `render.yaml` and configure:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Health Check Path**: `/health`
5. Click **Apply**.

### Option B: Manual Web Service Setup
1. Go to **New +** > **Web Service**.
2. Select your repository `Sarthak04-tech/rainfall-prediction`.
3. Configure the settings:
   - **Name**: `rainfall-prediction`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Health Check Path**: `/health`
4. Click **Deploy Web Service**.

## Model Evaluation
- Model: Random Forest Regressor
- Features: 17 meteorological features (`YEAR`, 12 months, and 4 quarterly aggregates)
- Metrics on complete historical dataset (4,090 subdivisions/years):
  - **MAE**: 21.59 mm
  - **RMSE**: 51.05 mm
  - **R² Score**: 0.9968

## License
MIT
