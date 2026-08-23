import os
import joblib
import pandas as pd
import numpy as np
from src.config import MODEL_PATH, SCALER_PATH
from src.feature_engineering import engineer_features

def load_artifacts():
    """Loads the trained model and scaler from disk."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        raise FileNotFoundError("Trained model or scaler not found. Please run src/train_model.py first.")
    
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler

def predict_student_performance(input_data: dict) -> dict:
    """Takes input features, processes them, runs prediction, and returns results with explanations."""
    model, scaler = load_artifacts()
    
    # Convert input dict to DataFrame
    input_df = pd.DataFrame([input_data])
    
    # Apply feature engineering to match training features
    input_engineered = engineer_features(input_df)
    
    # Feature columns expected by the model
    feature_columns = [
        "age", "study_hours", "attendance_pct", "previous_marks",
        "assignment_score", "internal_assessment", "midterm_marks",
        "sleep_hours", "total_academic_score", "study_efficiency"
    ]
    
    X_input = input_engineered[feature_columns]
    
    # Scale input data
    X_scaled = scaler.transform(X_input)
    
    # Make prediction
    predicted_score = float(model.predict(X_scaled)[0])
    predicted_score = round(min(max(predicted_score, 0.0), 100.0), 1)
    
    # Determine performance category
    if predicted_score >= 85:
        category = "Excellent"
        risk_level = "Low"
    elif predicted_score >= 70:
        category = "Good"
        risk_level = "Low"
    elif predicted_score >= 50:
        category = "Average"
        risk_level = "Medium"
    else:
        category = "At Risk"
        risk_level = "High"
        
    # Calculate composite risk score
    attendance = input_data.get("attendance_pct", 75)
    risk_score = round((100 - predicted_score) * 0.6 + (100 - attendance) * 0.4, 1)
    
    # Feature importance explanation (if model supports feature_importances_)
    explanation = {}
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        for col, imp in zip(feature_columns, importances):
            explanation[col] = round(float(imp), 4)
        # Sort by highest importance
        explanation = dict(sorted(explanation.items(), key=lambda item: item[1], reverse=True))

    result = {
        "predicted_score": predicted_score,
        "performance_category": category,
        "risk_level": risk_level,
        "risk_score": risk_score,
        "feature_importances": explanation
    }
    
    return result