import pandas as pd
import numpy as np
from src.config import BASE_DIR
import os

def generate_synthetic_data(num_samples: int = 1000) -> pd.DataFrame:
    """Generates realistic synthetic student performance data for development & testing."""
    np.random.seed(42)
    
    data = {
        "student_id": [f"STU{str(i).zfill(4)}" for i in range(1, num_samples + 1)],
        "age": np.random.randint(17, 23, size=num_samples),
        "gender": np.random.choice(["Male", "Female"], size=num_samples),
        "study_hours": np.random.uniform(1.0, 10.0, size=num_samples).round(1),
        "attendance_pct": np.random.uniform(50.0, 100.0, size=num_samples).round(1),
        "previous_marks": np.random.uniform(40.0, 95.0, size=num_samples).round(1),
        "assignment_score": np.random.uniform(45.0, 100.0, size=num_samples).round(1),
        "internal_assessment": np.random.uniform(40.0, 100.0, size=num_samples).round(1),
        "midterm_marks": np.random.uniform(35.0, 95.0, size=num_samples).round(1),
        "sleep_hours": np.random.uniform(5.0, 9.0, size=num_samples).round(1),
    }
    
    df = pd.DataFrame(data)
    
    # Target generation: Final score depends on weighted combination + noise
    df["final_score"] = (
        0.25 * df["previous_marks"] +
        0.20 * df["assignment_score"] +
        0.25 * df["internal_assessment"] +
        0.20 * df["midterm_marks"] +
        0.05 * df["study_hours"] * 3 +
        np.random.normal(0, 3, size=num_samples)
    ).clip(0, 100).round(1)
    
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans the dataset by handling missing values, duplicates, and outliers."""
    # Remove duplicate student IDs if any
    df = df.drop_duplicates(subset=["student_id"], keep="first")
    
    # Handle missing values for numerical columns (fill with median)
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())
        
    # Handle missing values for categorical columns (fill with mode)
    cat_cols = df.select_dtypes(include=["object"]).columns
    for col in cat_cols:
        if col != "student_id":
            df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown")
            
    # Outlier capping using IQR for attendance and study hours
    for col in ["attendance_pct", "study_hours"]:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
        
    return df

def load_or_create_dataset() -> pd.DataFrame:
    """Loads raw dataset if available, otherwise generates synthetic dataset and saves it."""
    raw_path = os.path.join(BASE_DIR, "data", "raw", "student_data.csv")
    
    if os.path.exists(raw_path):
        df = pd.read_csv(raw_path)
    else:
        df = generate_synthetic_data(1200)
        os.makedirs(os.path.dirname(raw_path), exist_ok=True)
        df.to_csv(raw_path, index=False)
        
    return clean_data(df)