import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.config import MODEL_PATH, SCALER_PATH
from src.data_preprocessing import load_or_create_dataset
from src.feature_engineering import engineer_features

def train_and_evaluate_models():
    """Trains multiple regression models, evaluates performance, and saves the best model."""
    print("Loading and preprocessing data...")
    df = load_or_create_dataset()
    df = engineer_features(df)
    
    # Define features and target variable (Predicting final_score)
    feature_columns = [
        "age", "study_hours", "attendance_pct", "previous_marks",
        "assignment_score", "internal_assessment", "midterm_marks",
        "sleep_hours", "total_academic_score", "study_efficiency"
    ]
    
    X = df[feature_columns]
    y = df["final_score"]
    
    # Train-test split (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Define candidate models
    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42)
    }
    
    best_model_name = None
    best_model = None
    best_r2 = -float("inf")
    
    evaluation_results = []
    
    print("\n--- Model Training & Evaluation Summary ---")
    for name, model in models.items():
        # Train model using scaled features for linear, or unscaled/scaled for trees
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        
        # Calculate evaluation metrics
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        evaluation_results.append({
            "Model": name,
            "MAE": round(mae, 3),
            "MSE": round(mse, 3),
            "RMSE": round(rmse, 3),
            "R2 Score": round(r2, 4)
        })
        
        print(f"Model: {name} | RMSE: {rmse:.3f} | R2 Score: {r2:.4f}")
        
        # Track the best model based on R2 Score
        if r2 > best_r2:
            best_r2 = r2
            best_model = model
            best_model_name = name

    print(f"\nBest Performing Model: {best_model_name} with R2 Score: {best_r2:.4f}")
    
    # Save the best model and scaler
    joblib.dump(best_model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    print(f"Model saved successfully to {MODEL_PATH}")
    print(f"Scaler saved successfully to {SCALER_PATH}")
    
    return pd.DataFrame(evaluation_results)

if __name__ == "__main__":
    train_and_evaluate_models()