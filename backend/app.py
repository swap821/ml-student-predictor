"""
app.py — Flask REST API for Student Performance Prediction

This API serves the trained ML model and provides endpoints for:
- Making predictions from student data
- Getting model information and comparison metrics
- Health checks

The API follows REST conventions and returns JSON responses.
"""

import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

from utils import setup_logging, format_error_response, create_prediction_json

# Initialize Flask app
app = Flask(__name__)

# Enable CORS so the React frontend can make requests to this API
# from a different domain (e.g., localhost:5173 → localhost:5000)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173", "http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Set up logging
logger = setup_logging()

# Global variables for model and preprocessors
MODEL = None
MODEL_NAME = None
PREPROCESSORS = None
FEATURE_NAMES = None


def load_model_and_preprocessors():
    """
    Load the trained model and preprocessors on startup.
    
    This runs when the Flask app starts, NOT on every request.
    Loading once at startup makes predictions much faster.
    """
    global MODEL, MODEL_NAME, PREPROCESSORS, FEATURE_NAMES
    
    try:
        # Load the trained model
        model_data = joblib.load('models/best_model.pkl')
        MODEL = model_data['model']
        MODEL_NAME = model_data['name']
        logger.info(f"Loaded model: {MODEL_NAME}")
        
        # Load preprocessors (scaler, encoders, feature names)
        PREPROCESSORS = joblib.load('models/preprocessors.pkl')
        FEATURE_NAMES = PREPROCESSORS['feature_names']
        logger.info(f"Loaded preprocessors for {len(FEATURE_NAMES)} features")
        
    except FileNotFoundError:
        logger.warning("Model files not found. Please run train_model.py first.")
        logger.warning("API will start but predictions will fail.")


# Load model when app starts
load_model_and_preprocessors()


@app.route('/', methods=['GET'])
def home():
    """
    Welcome endpoint.
    
    Returns:
        JSON with API info and available endpoints.
    """
    return jsonify({
        'message': 'Student Performance Predictor API',
        'version': '1.0.0',
        'model_loaded': MODEL is not None,
        'model_name': MODEL_NAME,
        'endpoints': {
            'POST /predict': 'Make a prediction from student data',
            'GET /models': 'Get model information and metrics',
            'GET /health': 'Health check'
        }
    })


@app.route('/predict', methods=['POST'])
def predict():
    """
    Make a prediction from student data.
    
    Expects JSON body with 19 features:
    {
        "Hours_Studied": 5,
        "Attendance": 80,
        "Parental_Involvement": "Medium",
        "Access_to_Resources": "High",
        ... (all 19 features)
    }
    
    Returns:
        JSON with predicted exam score and model info.
    """
    if MODEL is None:
        return jsonify(format_error_response(
            'Model not loaded. Please run train_model.py first.',
            503
        )), 503
    
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify(format_error_response(
                'No data provided. Please send a JSON body.',
                400
            )), 400
        
        # Validate that all required features are present
        missing_features = [f for f in FEATURE_NAMES if f not in data]
        if missing_features:
            return jsonify(format_error_response(
                f'Missing features: {missing_features}',
                400
            )), 400
        
        # Extract features in the correct order
        features_dict = {name: data[name] for name in FEATURE_NAMES}
        
        # Convert to numpy array and reshape for single prediction
        features_array = np.array([list(features_dict.values())])
        
        # Preprocess the features
        features_processed = preprocess_input(features_array)
        
        # Make prediction
        prediction = MODEL.predict(features_processed)[0]
        
        # Ensure prediction is within valid range (0-100)
        prediction = max(0, min(100, prediction))
        
        logger.info(f"Prediction made: {prediction:.1f}")
        
        return jsonify(create_prediction_json(
            features_dict, prediction, MODEL_NAME
        ))
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify(format_error_response(
            f'Prediction failed: {str(e)}',
            500
        )), 500


def preprocess_input(features_array):
    """
    Apply the same preprocessing used during training to new input data.
    
    This is CRITICAL: we must use the SAME scaler and encoders that were
    fitted on the training data, not create new ones.
    
    Args:
        features_array: Raw feature values
        
    Returns:
        Preprocessed features ready for prediction
    """
    # Get preprocessors
    scaler = PREPROCESSORS['scaler']
    encoders = PREPROCESSORS['encoders']
    
    # Create DataFrame with correct column names
    df = pd.DataFrame(features_array, columns=FEATURE_NAMES)
    
    # Apply label encoders to categorical columns
    for col, encoder in encoders.items():
        if col in df.columns:
            # Handle unseen categories
            try:
                df[col] = encoder.transform(df[col].astype(str))
            except ValueError:
                # If category wasn't seen during training, use most frequent
                df[col] = 0
    
    # Apply scaler to numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    if len(numerical_cols) > 0:
        df[numerical_cols] = scaler.transform(df[numerical_cols])
    
    return df.values


@app.route('/models', methods=['GET'])
def get_models_info():
    """
    Get information about the trained models.
    
    Returns:
        JSON with model comparison metrics.
    """
    if MODEL is None:
        return jsonify(format_error_response(
            'Model not loaded. Please run train_model.py first.',
            503
        )), 503
    
    # Return model info
    return jsonify({
        'current_model': MODEL_NAME,
        'features': FEATURE_NAMES,
        'feature_count': len(FEATURE_NAMES),
        'model_params': str(MODEL.get_params()) if hasattr(MODEL, 'get_params') else 'N/A'
    })


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Used by deployment platforms (Render, Heroku) to verify
    the API is running correctly.
    
    Returns:
        JSON with status information.
    """
    return jsonify({
        'status': 'healthy',
        'model_loaded': MODEL is not None,
        'model_name': MODEL_NAME
    })


if __name__ == '__main__':
    # Run in debug mode for development
    # In production, use gunicorn instead
    app.run(debug=True, host='0.0.0.0', port=5000)