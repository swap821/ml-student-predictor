"""
preprocess.py — Data Preprocessing Pipeline

This module handles all data preprocessing steps for the Student Performance Predictor:
1. Loading data from CSV files
2. Handling missing values
3. Encoding categorical variables (Label Encoding)
4. Scaling numerical features (Standard Scaling)
5. Saving/loading preprocessors for reuse

Understanding these concepts:
- Label Encoding: Converts text categories (Low, Medium, High) into numbers (0, 1, 2)
  so ML models can process them.
- Standard Scaling: Normalizes numerical values to have mean=0 and std=1,
  which helps ML models converge faster and perform better.
- Train/Test Split: Splits data into training (80%) and testing (20%) sets
  to evaluate model performance on unseen data.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os


def load_data(filepath):
    """
    Load the student performance dataset from a CSV file.
    
    Args:
        filepath (str): Path to the CSV file
        
    Returns:
        pandas.DataFrame: The loaded dataset
    """
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    return df


def handle_missing_values(df):
    """
    Handle missing values in the dataset.
    
    Strategy:
    - Numerical columns: Fill with median (robust to outliers)
    - Categorical columns: Fill with mode (most frequent value)
    
    Args:
        df (pandas.DataFrame): Input dataframe
        
    Returns:
        pandas.DataFrame: Dataframe with missing values handled
    """
    # Make a copy to avoid modifying the original
    df = df.copy()
    
    # Handle numerical missing values with median
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    for col in numerical_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            print(f"Filled {col} missing values with median: {median_val}")
    
    # Handle categorical missing values with mode
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            mode_val = df[col].mode()[0]
            df[col].fillna(mode_val, inplace=True)
            print(f"Filled {col} missing values with mode: {mode_val}")
    
    return df


def preprocess_features(df, target_column='Exam_Score'):
    """
    Preprocess all features for machine learning.
    
    Steps:
    1. Separate features (X) from target (y)
    2. Encode categorical variables using LabelEncoder
    3. Scale numerical features using StandardScaler
    4. Return processed X, y, and the preprocessors for later use
    
    Args:
        df (pandas.DataFrame): Raw dataset
        target_column (str): Name of the target column to predict
        
    Returns:
        tuple: (X_scaled, y, scaler, encoders, feature_names)
            - X_scaled: Preprocessed feature matrix
            - y: Target values
            - scaler: Fitted StandardScaler (save this!)
            - encoders: Dictionary of fitted LabelEncoders (save these!)
            - feature_names: List of feature column names
    """
    # Separate features and target
    X = df.drop(columns=[target_column])
    y = df[target_column].values
    
    # Store encoders and scaler
    encoders = {}
    scaler = StandardScaler()
    
    # Identify categorical and numerical columns
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    
    print(f"\nCategorical columns: {categorical_cols}")
    print(f"Numerical columns: {numerical_cols}")
    
    # Encode categorical variables
    # LabelEncoder converts text to numbers (e.g., "Low" -> 0, "Medium" -> 1, "High" -> 2)
    for col in categorical_cols:
        encoder = LabelEncoder()
        X[col] = encoder.fit_transform(X[col].astype(str))
        encoders[col] = encoder
        print(f"Encoded {col}: {list(encoder.classes_)}")
    
    # Scale numerical features
    # StandardScaler transforms values to have mean=0 and standard deviation=1
    # This is important because ML models perform better when features are on similar scales
    if numerical_cols:
        X[numerical_cols] = scaler.fit_transform(X[numerical_cols])
    
    feature_names = X.columns.tolist()
    X_scaled = X.values
    
    print(f"\nFinal feature matrix shape: {X_scaled.shape}")
    print(f"Target shape: {y.shape}")
    
    return X_scaled, y, scaler, encoders, feature_names


def split_data(X, y, test_size=0.2, random_state=42):
    """
    Split data into training and testing sets.
    
    Why 80/20 split?
    - 80% for training: Model needs enough data to learn patterns
    - 20% for testing: We need unseen data to evaluate how well the model generalizes
    
    Args:
        X (numpy.ndarray): Feature matrix
        y (numpy.ndarray): Target values
        test_size (float): Fraction of data to use for testing (default 0.2 = 20%)
        random_state (int): Seed for reproducibility (same split every time)
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    print(f"\nTrain set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    return X_train, X_test, y_train, y_test


def save_preprocessors(scaler, encoders, feature_names, filepath):
    """
    Save the fitted preprocessors to disk so we can reuse them later.
    
    IMPORTANT: We must save the SAME preprocessors used during training
    and apply them to new data during prediction. If we fit new preprocessors
    on prediction data, the encodings won't match!
    
    Args:
        scaler (StandardScaler): Fitted scaler
        encoders (dict): Dictionary of fitted LabelEncoders
        feature_names (list): List of feature column names
        filepath (str): Where to save the preprocessors
    """
    preprocessors = {
        'scaler': scaler,
        'encoders': encoders,
        'feature_names': feature_names
    }
    joblib.dump(preprocessors, filepath)
    print(f"Saved preprocessors to {filepath}")


def load_preprocessors(filepath):
    """
    Load previously saved preprocessors.
    
    Args:
        filepath (str): Path to saved preprocessors
        
    Returns:
        tuple: (scaler, encoders, feature_names)
    """
    preprocessors = joblib.load(filepath)
    return preprocessors['scaler'], preprocessors['encoders'], preprocessors['feature_names']


if __name__ == "__main__":
    # Test the preprocessing pipeline
    data_path = 'data/StudentPerformanceFactors.csv'
    
    if not os.path.exists(data_path):
        print(f"Error: Dataset not found at {data_path}")
        print("Please download the dataset from Kaggle and place it in the data/ folder")
    else:
        # Load and preprocess
        df = load_data(data_path)
        df = handle_missing_values(df)
        X, y, scaler, encoders, features = preprocess_features(df)
        X_train, X_test, y_train, y_test = split_data(X, y)
        
        # Save preprocessors
        os.makedirs('models', exist_ok=True)
        save_preprocessors(scaler, encoders, features, 'models/preprocessors.pkl')
        print("\nPreprocessing complete!")