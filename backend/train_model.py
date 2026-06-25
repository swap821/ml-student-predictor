"""
train_model.py — ML Model Training Pipeline

This script trains and compares 3 different ML models:
1. Linear Regression — Simple baseline model
2. Random Forest — Ensemble of decision trees (usually best for tabular data)
3. XGBoost — Gradient boosted trees (often wins Kaggle competitions)

After training, we compare their performance and save the best model.

Understanding the models:
- Linear Regression: Draws a straight line (or hyperplane) through the data.
  Simple but can't capture complex patterns.
- Random Forest: Builds many decision trees and averages their predictions.
  Great for tabular data, handles non-linear relationships well.
- XGBoost: Builds trees sequentially, where each new tree corrects errors
  from previous trees. Often the most accurate for structured data.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server environments
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# Scikit-learn models
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# Try to import XGBoost, fall back to GradientBoosting if not available
try:
    from xgboost import XGBRegressor
    HAS_XGBOOST = True
    print("Using XGBoost")
except ImportError:
    from sklearn.ensemble import GradientBoostingRegressor
    HAS_XGBOOST = False
    print("XGBoost not available, using GradientBoostingRegressor instead")

# Import our preprocessing module
from preprocess import (
    load_data, handle_missing_values, preprocess_features,
    split_data, save_preprocessors
)
from utils import evaluate_model, get_feature_importance


def train_linear_regression(X_train, y_train):
    """
    Train a Linear Regression model.
    
    Linear Regression assumes a linear relationship between features and target.
    It finds the best-fitting straight line (or hyperplane in higher dimensions).
    
    Pros: Fast, interpretable
    Cons: Can't capture complex non-linear relationships
    
    Args:
        X_train: Training features
        y_train: Training targets
        
    Returns:
        Trained LinearRegression model
    """
    print("\n" + "="*50)
    print("Training Linear Regression...")
    print("="*50)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    print("Linear Regression training complete!")
    return model


def train_random_forest(X_train, y_train):
    """
    Train a Random Forest model.
    
    Random Forest builds 100 decision trees, each trained on a random subset
    of data and features. The final prediction is the average of all trees.
    
    Why it works well:
    - Each tree sees different data, reducing overfitting
    - Averaging many trees smooths out individual tree errors
    - Can capture complex feature interactions
    
    Args:
        X_train: Training features
        y_train: Training targets
        
    Returns:
        Trained RandomForestRegressor model
    """
    print("\n" + "="*50)
    print("Training Random Forest...")
    print("="*50)
    
    model = RandomForestRegressor(
        n_estimators=100,      # Number of trees in the forest
        max_depth=15,          # Maximum depth of each tree
        min_samples_split=5,   # Minimum samples required to split a node
        min_samples_leaf=2,    # Minimum samples required at a leaf node
        random_state=42,       # For reproducibility
        n_jobs=-1              # Use all CPU cores
    )
    model.fit(X_train, y_train)
    print(f"Random Forest training complete! (100 trees)")
    return model


def train_xgboost_model(X_train, y_train):
    """
    Train an XGBoost (or GradientBoosting) model.
    
    Gradient Boosting builds trees sequentially:
    - Tree 1 makes predictions
    - Tree 2 learns to correct Tree 1's errors
    - Tree 3 learns to correct remaining errors
    - And so on...
    
    This sequential correction often leads to better accuracy than Random Forest.
    
    Args:
        X_train: Training features
        y_train: Training targets
        
    Returns:
        Trained XGBRegressor or GradientBoostingRegressor model
    """
    print("\n" + "="*50)
    if HAS_XGBOOST:
        print("Training XGBoost...")
    else:
        print("Training Gradient Boosting...")
    print("="*50)
    
    if HAS_XGBOOST:
        model = XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1
        )
    else:
        model = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
    
    model.fit(X_train, y_train)
    print("Training complete!")
    return model


def compare_models(models, X_test, y_test, feature_names):
    """
    Evaluate and compare all trained models.
    
    We use 4 metrics:
    - R² Score: How well the model explains variance (1.0 = perfect)
    - MAE: Average prediction error in exam score points
    - RMSE: Square root of average squared errors (punishes large errors)
    
    Args:
        models (dict): Dictionary of {model_name: trained_model}
        X_test: Test features
        y_test: Test targets
        feature_names: List of feature names
        
    Returns:
        dict: Evaluation results for each model
    """
    print("\n" + "="*60)
    print("MODEL COMPARISON")
    print("="*60)
    
    results = {}
    predictions = {}
    
    for name, model in models.items():
        # Make predictions on test set
        y_pred = model.predict(X_test)
        predictions[name] = y_pred
        
        # Evaluate
        metrics = evaluate_model(y_test, y_pred, name)
        results[name] = metrics
        
        print(f"\n{name}:")
        print(f"  R² Score: {metrics['r2_score']:.4f}")
        print(f"  MAE: {metrics['mae']:.2f}")
        print(f"  RMSE: {metrics['rmse']:.2f}")
    
    # Determine the best model (highest R² score)
    best_model_name = max(results, key=lambda x: results[x]['r2_score'])
    print(f"\n{'='*60}")
    print(f"BEST MODEL: {best_model_name}")
    print(f"R² Score: {results[best_model_name]['r2_score']:.4f}")
    print(f"{'='*60}")
    
    return results, predictions, best_model_name


def plot_model_comparison(results, output_path='models/comparison.png'):
    """
    Create a bar chart comparing all models.
    
    Args:
        results (dict): Evaluation results for each model
        output_path (str): Where to save the plot
    """
    os.makedirs('models', exist_ok=True)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    model_names = list(results.keys())
    r2_scores = [results[m]['r2_score'] for m in model_names]
    maes = [results[m]['mae'] for m in model_names]
    rmses = [results[m]['rmse'] for m in model_names]
    
    # R² Score (higher is better)
    colors_r2 = ['#10b981' if m == max(model_names, key=lambda x: results[x]['r2_score']) 
                 else '#3b82f6' for m in model_names]
    axes[0].bar(model_names, r2_scores, color=colors_r2)
    axes[0].set_title('R² Score (higher = better)')
    axes[0].set_ylabel('R² Score')
    axes[0].set_ylim(0, 1)
    for i, v in enumerate(r2_scores):
        axes[0].text(i, v + 0.02, f'{v:.3f}', ha='center')
    
    # MAE (lower is better)
    colors_mae = ['#10b981' if m == min(model_names, key=lambda x: results[x]['mae']) 
                  else '#3b82f6' for m in model_names]
    axes[1].bar(model_names, maes, color=colors_mae)
    axes[1].set_title('MAE (lower = better)')
    axes[1].set_ylabel('Mean Absolute Error')
    for i, v in enumerate(maes):
        axes[1].text(i, v + 0.1, f'{v:.2f}', ha='center')
    
    # RMSE (lower is better)
    colors_rmse = ['#10b981' if m == min(model_names, key=lambda x: results[x]['rmse']) 
                   else '#3b82f6' for m in model_names]
    axes[2].bar(model_names, rmses, color=colors_rmse)
    axes[2].set_title('RMSE (lower = better)')
    axes[2].set_ylabel('Root Mean Squared Error')
    for i, v in enumerate(rmses):
        axes[2].text(i, v + 0.1, f'{v:.2f}', ha='center')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nComparison plot saved to {output_path}")
    plt.close()


def plot_feature_importance(model, feature_names, output_path='models/feature_importance.png'):
    """
    Plot the top 10 most important features.
    
    This tells us which factors are most influential in predicting exam scores.
    
    Args:
        model: Trained tree-based model
        feature_names: List of feature names
        output_path: Where to save the plot
    """
    importance = get_feature_importance(model, feature_names)
    
    if not importance:
        print("Feature importance not available for this model type")
        return
    
    # Plot top 10
    top_features = importance[:10]
    names = [f[0] for f in top_features]
    values = [f[1] for f in top_features]
    
    plt.figure(figsize=(10, 6))
    plt.barh(names[::-1], values[::-1], color='#4d7dff')
    plt.xlabel('Importance')
    plt.title('Top 10 Most Important Features')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Feature importance plot saved to {output_path}")
    plt.close()


def save_best_model(model, model_name, filepath='models/best_model.pkl'):
    """
    Save the best performing model to disk.
    
    We use joblib (better for sklearn models than pickle) to serialize
    the model so we can load it later in the Flask API.
    
    Args:
        model: Trained model to save
        model_name (str): Name of the model
        filepath (str): Where to save
    """
    os.makedirs('models', exist_ok=True)
    model_data = {
        'model': model,
        'name': model_name
    }
    joblib.dump(model_data, filepath)
    print(f"Saved best model ({model_name}) to {filepath}")


def main():
    """
    Main training pipeline.
    
    Steps:
    1. Load and preprocess data
    2. Train 3 models
    3. Compare performance
    4. Save best model and plots
    """
    print("="*60)
    print("STUDENT PERFORMANCE PREDICTOR — MODEL TRAINING")
    print("="*60)
    
    # Step 1: Load and preprocess data
    data_path = 'data/StudentPerformanceFactors.csv'
    if not os.path.exists(data_path):
        print(f"\nERROR: Dataset not found at {data_path}")
        print("Please download from Kaggle and place in backend/data/")
        sys.exit(1)
    
    df = load_data(data_path)
    df = handle_missing_values(df)
    X, y, scaler, encoders, feature_names = preprocess_features(df)
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # Step 2: Train all 3 models
    models = {}
    models['Linear Regression'] = train_linear_regression(X_train, y_train)
    models['Random Forest'] = train_random_forest(X_train, y_train)
    models['XGBoost' if HAS_XGBOOST else 'Gradient Boosting'] = train_xgboost_model(X_train, y_train)
    
    # Step 3: Compare models
    results, predictions, best_name = compare_models(models, X_test, y_test, feature_names)
    
    # Step 4: Create visualizations
    plot_model_comparison(results)
    plot_feature_importance(models[best_name], feature_names)
    
    # Step 5: Save best model and preprocessors
    save_best_model(models[best_name], best_name)
    save_preprocessors(scaler, encoders, feature_names, 'models/preprocessors.pkl')
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print(f"Best Model: {best_name}")
    print(f"Models and preprocessors saved in models/ directory")
    print(f"API ready to start: python app.py")


if __name__ == "__main__":
    main()