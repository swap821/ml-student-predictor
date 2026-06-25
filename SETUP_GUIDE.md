# Setup Guide — Student Performance Predictor

## Prerequisites
- Python 3.9+ (download from python.org)
- Node.js 18+ (download from nodejs.org)
- Git (optional, for cloning)

## Step 1: Download the Dataset
1. Visit: https://www.kaggle.com/datasets/lainguyn123/student-performance-factors
2. Click "Download" (you need a free Kaggle account)
3. Extract the ZIP file
4. Copy `StudentPerformanceFactors.csv` to `backend/data/StudentPerformanceFactors.csv`

## Step 2: Set Up the Backend
```bash
# Navigate to backend folder
cd backend

# Create a Python virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train the ML models (this will take a few minutes)
python train_model.py

# Start the Flask server
python app.py
```
You should see: `Running on http://127.0.0.1:5000`

## Step 3: Set Up the Frontend
In a NEW terminal window:
```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```
You should see: `Local: http://localhost:5173`

Open http://localhost:5173 in your browser.

## Common Errors

### "No module named 'sklearn'"
Solution: Make sure you activated the virtual environment before installing packages.

### "File not found: StudentPerformanceFactors.csv"
Solution: The dataset CSV must be placed in `backend/data/` folder.

### Port already in use
If port 5000 is busy, edit `.env` to change the port. If port 5173 is busy, Vite will automatically use the next available port.

## Deployment

### Backend (Render.com)
1. Create a free account on render.com
2. Click "New Web Service"
3. Connect your GitHub repository
4. Set:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt && python train_model.py`
   - Start Command: `gunicorn app:app`
5. Click "Create Web Service"

### Frontend (Vercel.com)
1. Create a free account on vercel.com
2. Click "New Project"
3. Import your GitHub repository
4. Set Framework Preset to "Vite"
5. Set Root Directory to `frontend`
6. Click "Deploy"

## Next Steps
- Try different input values to see how predictions change
- Read the heavily commented code in `train_model.py` to understand how ML works
- Experiment with hyperparameters in the model training script