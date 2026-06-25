# Deploy to Render (Backend)

1. Go to https://dashboard.render.com/
2. Click "New +" → "Web Service"
3. Connect GitHub repo: `swap821/ml-student-predictor`
4. Configure:
   - **Name**: `ml-student-predictor-api`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt && python generate_dataset.py && python train_model.py`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120`
5. Add Environment Variable:
   - `ALLOWED_ORIGINS` = `https://ml-student-predictor.vercel.app,http://localhost:5173`
6. Click "Create Web Service"

Your backend URL will be: `https://ml-student-predictor-api.onrender.com`
