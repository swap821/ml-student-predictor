"""
utils.py — Utility Functions

Helper functions used across the application:
- Logging setup
- Feature importance extraction
- Prediction response formatting
- Model evaluation metrics
"""

import logging
import numpy as np


def setup_logging():
    """
    Configure logging for the Flask application.
    Logs are written to both console and a file for debugging.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Print to console
            logging.FileHandler('app.log')  # Save to file
        ]
    )
    return logging.getLogger(__name__)


def get_feature_importance(model, feature_names):
    """
    Extract feature importance from a trained tree-based model.
    
    Tree-based models (Random Forest, XGBoost) can tell us which features
    were most important for making predictions. This helps us understand
    what drives student performance.
    
    Args:
        model: Trained model with feature_importances_ attribute
        feature_names (list): Names of features
        
    Returns:
        list: Tuples of (feature_name, importance_score) sorted by importance
    """
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        feature_importance = list(zip(feature_names, importances))
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        return feature_importance
    else:
        return []


def create_prediction_json(features, prediction, model_name):
    """
    Format a prediction result as JSON.
    
    Args:
        features (dict): Input features used for prediction
        prediction (float): Predicted exam score
        model_name (str): Name of the model used
        
    Returns:
        dict: Formatted response
    """
    # Round prediction to 1 decimal place
    rounded_prediction = round(float(prediction), 1)
    
    return {
        'prediction': rounded_prediction,
        'model_used': model_name,
        'input_features': features,
        'status': 'success'
    }


def evaluate_model(y_true, y_pred, model_name):
    """
    Calculate regression evaluation metrics.
    
    Metrics explained:
    - MAE (Mean Absolute Error): Average difference between predicted and actual values.
      Lower is better. Easy to interpret (in same units as target).
    - MSE (Mean Squared Error): Squares the errors, penalizing large mistakes more.
      Lower is better.
    - RMSE (Root Mean Squared Error): Square root of MSE. In same units as target.
      Lower is better. Most commonly used metric for regression.
    - R² Score: Percentage of variance in target explained by the model.
      Range: 0 to 1 (higher is better). 1.0 = perfect predictions.
    
    Args:
        y_true (array): Actual values
        y_pred (array): Predicted values
        model_name (str): Name of the model
        
    Returns:
        dict: Evaluation metrics
    """
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    
    metrics = {
        'model': model_name,
        'mae': round(mae, 2),
        'mse': round(mse, 2),
        'rmse': round(rmse, 2),
        'r2_score': round(r2, 4)
    }
    
    return metrics


def format_error_response(error_message, status_code=400):
    """
    Format an error response.
    
    Args:
        error_message (str): Error description
        status_code (int): HTTP status code
        
    Returns:
        dict: Formatted error response
    """
    return {
        'status': 'error',
        'message': error_message,
        'status_code': status_code
    }