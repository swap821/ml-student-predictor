# 📊 ML Student Performance Predictor

**Live Demo:** [https://ml-student-predictor.vercel.app](https://ml-student-predictor.vercel.app) *(deploy after setup)*

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

A full-stack machine learning application that predicts student exam scores (0-100) based on study habits, attendance, sleep patterns, and lifestyle factors. Trains and compares 3 regression models — **Linear Regression**, **Random Forest**, and **Gradient Boosting** — with automated model selection and feature importance visualization.

This project demonstrates the complete ML pipeline: data preprocessing, model training, cross-validation comparison, hyperparameter tuning, feature importance analysis, and deployment as a REST API with an interactive React dashboard.

---

# ✨ Key Features

## 🤖 3-Model Comparison Pipeline
- Trains Linear Regression, Random Forest, and Gradient Boosting simultaneously
- Automated cross-validation to select the best-performing model
- Side-by-side metrics comparison (R², MAE, RMSE)

## 📈 Feature Importance Analysis
- Identifies which factors most influence exam scores
- Interactive bar chart visualization of feature weights
- Data-driven insights for students and educators

## 🎯 Interactive Prediction Dashboard
- 19-input feature form (study hours, attendance, sleep, tutoring, etc.)
- Real-time score prediction with color-coded results
- Animated result cards with performance interpretation

## 📊 Model Performance Visualization
- Recharts-powered comparison charts
- Confusion matrix-style performance breakdown
- Training vs validation metrics

## 🔄 Automated Model Selection
- Best model saved automatically based on cross-validation scores
- Model persistence with joblib for fast API inference
- Easy retraining with new data

---

# 🛠️ Tech Stack

## Backend (`/backend`)
- Python 3.11
- Flask (REST API)
- scikit-learn (ML models & preprocessing)
- XGBoost (Gradient Boosting)
- Pandas & NumPy (data manipulation)
- joblib (model serialization)

## Frontend (`/frontend`)
- React 18
- Vite
- Tailwind CSS
- Recharts (data visualization)
- Framer Motion (animations)

---

# 📂 Project Structure

```plaintext
ml-student-predictor/
│
├── backend/                     # Flask API Server
│   ├── models/                  # Trained model artifacts (.pkl)
│   ├── data/                    # Dataset & synthetic data generator
│   ├── train_model.py           # Model training pipeline
│   ├── preprocess.py            # Data preprocessing & encoding
│   ├── utils.py                 # Helper functions
│   ├── app.py                   # Flask API endpoints
│   ├── generate_dataset.py      # Synthetic dataset generator
│   ├── requirements.txt         # Python dependencies
│   └── Procfile                 # Render deployment config
│
├── frontend/                    # React Application
│   ├── src/
│   │   ├── components/          # UI Components
│   │   │   ├── InputForm.jsx    # 19-field prediction form
│   │   │   ├── ResultCard.jsx   # Animated prediction result
│   │   │   └── ModelComparison.jsx  # Model metrics charts
│   │   ├── App.jsx              # Main Application
│   │   └── main.jsx             # Entry point
│   ├── package.json
│   └── vite.config.js
│
├── render.yaml                  # Render blueprint
├── vercel.json                  # Vercel deployment config
└── README.md
```

---

# 🚀 Getting Started

## 📌 Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/swap821/ml-student-predictor.git
cd ml-student-predictor
```

---

# 🔧 Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

---

## 🏋️ Train the Models

```bash
# Generate synthetic dataset (if you don't have the Kaggle dataset)
python generate_dataset.py

# Train all 3 models — automatically picks the best one
python train_model.py
```

**Output:** Saves `best_model.pkl` and `preprocessors.pkl` in `backend/models/`

**Sample Results:**

| Model | R² Score | MAE | RMSE | Status |
|---|---|---|---|---|
| Linear Regression | 0.58 | 5.27 | 7.15 | Baseline |
| **Random Forest** | **0.63** | **4.32** | **6.75** | **Best** |
| Gradient Boosting | 0.62 | 4.45 | 6.79 | Runner-up |

---

## ▶️ Start the Flask API

```bash
python app.py
```

API runs at `http://localhost:5000`

### API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/predict` | POST | Predict exam score from student data |
| `/api/models` | GET | Get trained models & their metrics |
| `/api/health` | GET | Health check |

### Example Prediction Request

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Hours_Studied": 25,
    "Attendance": 90,
    "Parental_Involvement": "High",
    "Access_to_Resources": "High",
    "Extracurricular_Activities": "Yes",
    "Sleep_Hours": 7.5,
    "Previous_Scores": 80,
    "Motivation_Level": "High",
    "Internet_Access": "Yes",
    "Tutoring_Sessions": 5,
    "Family_Income": "Medium",
    "Teacher_Quality": "High",
    "School_Type": "Private",
    "Peer_Influence": "Positive",
    "Physical_Activity": 3,
    "Learning_Disabilities": "No",
    "Parental_Education_Level": "College",
    "Distance_from_Home": "Near",
    "Gender": "Male"
  }'
```

**Response:**
```json
{
  "predicted_score": 87.5,
  "model_used": "Random Forest",
  "confidence": "high"
}
```

---

# 🎨 Frontend Setup

Open a second terminal:

```bash
cd frontend
npm install
```

## ▶️ Start the Development Server

```bash
npm run dev
```

Frontend runs at `http://localhost:5173`

---

# 🌍 Deployment

## Backend — Render

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Connect your GitHub repo: `swap821/ml-student-predictor`
4. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt && python generate_dataset.py && python train_model.py`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120`
5. Add Environment Variable:
   - `ALLOWED_ORIGINS` = `https://ml-student-predictor.vercel.app,http://localhost:5173`
6. Click **Create Web Service**

## Frontend — Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click **Add New Project** → Import `ml-student-predictor`
3. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
4. Add Environment Variable:
   - `VITE_API_URL` = `https://ml-student-predictor-api.onrender.com`
5. Click **Deploy**

---

# 🧠 ML Concepts Demonstrated

This project demonstrates understanding of:

- **Supervised Learning**: Regression task with continuous target
- **Feature Engineering**: Label encoding, standard scaling, train-test split
- **Model Comparison**: Training multiple models and selecting the best
- **Cross-Validation**: K-fold CV for robust model evaluation
- **Feature Importance**: Understanding which features drive predictions
- **Model Serialization**: Saving/loading trained models for production
- **REST API Deployment**: Serving ML models via Flask
- **Full-Stack Integration**: Connecting React frontend to Python ML backend

---

# 🚀 Future Improvements

- [ ] Upload real Kaggle StudentPerformanceFactors.csv dataset
- [ ] Hyperparameter tuning with GridSearchCV
- [ ] Add SHAP values for individual prediction explainability
- [ ] Model performance monitoring over time
- [ ] Support for custom dataset uploads
- [ ] Export predictions as CSV
- [ ] Docker containerization
- [ ] CI/CD with GitHub Actions for auto-retraining

---

# 👨‍💻 Author

## Swapnil Kumar

- GitHub: https://github.com/swap821
- LinkedIn: https://www.linkedin.com/in/swapnil-kumar-73a68a308
- Portfolio: https://swapnil-kumar-portfolio016.vercel.app

---

# ⭐ Project Goal

This project was built to demonstrate:
- End-to-end ML pipeline from data to deployment
- Multiple model comparison and selection
- Full-stack ML application architecture
- REST API design for model serving
- Interactive data visualization
- Production-ready code structure

---

# 📜 License

This project is open-source and available for educational and learning purposes.
