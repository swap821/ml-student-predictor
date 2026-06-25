# Deployment Guide - ML Student Predictor

## Quick Deploy (Render + Vercel)

### Backend (Render)

1. Go to [render.com](https://render.com) → "New Web Service"
2. Connect your GitHub repo: `swap821/ml-student-predictor`
3. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt && python generate_dataset.py && python train_model.py`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120`
4. Click "Create Web Service"
5. Copy the service URL (e.g., `https://ml-student-predictor.onrender.com`)

### Frontend (Vercel)

1. Go to [vercel.com](https://vercel.com) → "Add New Project"
2. Import your GitHub repo: `swap821/ml-student-predictor`
3. Set **Framework Preset** to "Vite"
4. Set **Root Directory** to `frontend`
5. Add Environment Variable:
   - `VITE_API_URL` = your Render backend URL
6. Click "Deploy"

### One-Click Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/swap821/ml-student-predictor)

---

## Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
python generate_dataset.py  # Creates dataset
python train_model.py       # Trains and saves models
python app.py               # Starts Flask server on localhost:5000

# Frontend
cd frontend
npm install
npm run dev                 # Starts dev server on localhost:3000
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FLASK_ENV` | No | Set to `production` for deployment |
| `ALLOWED_ORIGINS` | Yes | Comma-separated CORS origins |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/predict` | POST | Predict exam score from student data |
| `/api/models` | GET | List available models and metrics |
| `/api/health` | GET | Health check |

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'sklearn'`
**Fix**: Run `pip install -r requirements.txt`

**Issue**: `FileNotFoundError: StudentPerformanceFactors.csv`
**Fix**: Run `python generate_dataset.py` first

**Issue**: Model file not found
**Fix**: Run `python train_model.py` to generate `models/best_model.pkl`
