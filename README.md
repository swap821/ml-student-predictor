# Student Performance Predictor

## Overview
AI-powered full-stack application that predicts student exam scores (0-100) based on study habits, attendance, and lifestyle factors. Built with Flask + Scikit-learn backend and React + Tailwind CSS frontend.

## Live Demo
[Coming soon — deploy and add link]

## Architecture
```
User Input (19 features)
    |
    v
React Dashboard
    |
    v
Flask API
    |
    v
Preprocessing (encoding + scaling)
    |
    v
ML Model (Random Forest / XGBoost / Linear Regression)
    |
    v
Predicted Exam Score (0-100)
```

## What Makes This Special
- **3 ML models compared**: Linear Regression, Random Forest, XGBoost — see which wins
- **19 input features**: From study hours to parental education
- **Interactive React dashboard**: Beautiful form with animated results
- **Model comparison charts**: Visualize which model performs best
- **Fully responsive**: Works on mobile, tablet, desktop

## Tech Stack
- Backend: Python, Flask, Scikit-learn, Pandas, NumPy
- Frontend: React, Tailwind CSS, Recharts, Framer Motion
- ML Models: Linear Regression, Random Forest, XGBoost

## Results (Example)
| Model | R² Score | MAE | RMSE |
|---|---|---|---|
| Linear Regression | ~0.85 | ~2.1 | ~2.8 |
| Random Forest | ~0.92 | ~1.4 | ~1.9 |
| XGBoost | ~0.93 | ~1.3 | ~1.8 |
*(Example values — actual results will vary)*

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+

### Step 1: Download Dataset
1. Go to https://www.kaggle.com/datasets/lainguyn123/student-performance-factors
2. Download the CSV
3. Place at `backend/data/StudentPerformanceFactors.csv`

### Step 2: Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python train_model.py      # Trains 3 models, saves best one
python app.py              # API on localhost:5000
```

### Step 3: Frontend Setup
```bash
cd frontend
npm install
npm run dev                # UI on localhost:5173
```

## Project Structure
```
ml-student-predictor/
├── README.md
├── SETUP_GUIDE.md
├── render.yaml
├── .gitignore
├── backend/
│   ├── app.py              ← Flask REST API
│   ├── train_model.py      ← Trains 3 ML models
│   ├── preprocess.py       ← Data preprocessing pipeline
│   ├── utils.py            ← Helper functions
│   ├── requirements.txt
│   ├── .env.example
│   ├── Procfile
│   ├── data/               ← Dataset goes here
│   └── models/             ← Trained models saved here
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── components/
    │   │   ├── InputForm.jsx
    │   │   ├── ResultCard.jsx
    │   │   └── ModelInfo.jsx
    │   └── api/client.js
    ├── index.html
    ├── package.json
    └── ...config files
```

## Key Learnings
- Random Forest and XGBoost outperform Linear Regression on tabular data with feature interactions
- Feature scaling is essential for distance-based algorithms
- One-hot encoding categorical variables improves model performance
- Cross-validation gives more reliable performance estimates than single train-test split

## Author
**Swapnil Kumar** — Full-Stack Developer & AI Enthusiast
- Portfolio: https://swapnil-kumar-portfolio016.vercel.app
- GitHub: https://github.com/swap821
- LinkedIn: https://linkedin.com/in/swapnil-kumar-73a68a308