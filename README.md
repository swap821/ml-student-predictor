# ML Student Predictor

**Live Demo:** [https://63dcmrawskzy4.kimi.page](https://63dcmrawskzy4.kimi.page)

AI-powered full-stack application that predicts student exam scores (0-100) based on study habits, attendance, and lifestyle factors. Built with Flask + Scikit-learn backend and React + Tailwind CSS frontend.

## Architecture
```
User Input (19 features) → React Dashboard → Flask API → Preprocessing → ML Model → Predicted Score
```

## What Makes This Special
- **3 ML models compared**: Linear Regression, Random Forest, XGBoost — see which wins
- **19 input features**: From study hours to parental education
- **Interactive React dashboard**: Beautiful form with animated results
- **Model comparison charts**: Visualize which model performs best

## Tech Stack
- Backend: Python, Flask, Scikit-learn, Pandas, NumPy
- Frontend: React, Tailwind CSS, Recharts, Framer Motion
- ML Models: Linear Regression, Random Forest, XGBoost

## Results
| Model | R² Score | MAE | RMSE |
|---|---|---|---|
| Linear Regression | 0.58 | 5.27 | 7.15 |
| **Random Forest** | **0.63** | **4.32** | **6.75** |
| Gradient Boosting | 0.62 | 4.45 | 6.79 |

## Quick Start
```bash
cd backend
pip install -r requirements.txt
python generate_dataset.py
python train_model.py
python app.py              # API on localhost:5000
cd ../frontend
npm install && npm run dev  # UI on localhost:5173
```

## Deploy
- Backend: [Deploy to Render](https://render.com/deploy?repo=https://github.com/swap821/ml-student-predictor)
- See `DEPLOYMENT.md` for full instructions

## Author
**Swapnil Kumar** — [Portfolio](https://swapnil-kumar-portfolio016.vercel.app) | [GitHub](https://github.com/swap821)
