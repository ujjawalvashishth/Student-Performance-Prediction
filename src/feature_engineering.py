import pandas as pd
import numpy as np

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Creates derived features and performance categories from raw features."""
    df = df.copy()
    
    # Combined academic score feature
    df["total_academic_score"] = (
        df["assignment_score"] + df["internal_assessment"] + df["midterm_marks"]
    ) / 3.0
    
    # Study efficiency index
    df["study_efficiency"] = df["study_hours"] * (df["attendance_pct"] / 100.0)
    
    # Performance Category classification based on final_score (or predicted score)
    if "final_score" in df.columns:
        conditions = [
            (df["final_score"] >= 85),
            (df["final_score"] >= 70) & (df["final_score"] < 85),
            (df["final_score"] >= 50) & (df["final_score"] < 70),
            (df["final_score"] < 50)
        ]
        choices = ["Excellent", "Good", "Average", "At Risk"]
        df["performance_category"] = np.select(conditions, choices, default="Average")
        
        # Risk score calculation (inverse relation with score and attendance)
        df["risk_score"] = (100 - df["final_score"]) * 0.6 + (100 - df["attendance_pct"]) * 0.4
        df["risk_score"] = df["risk_score"].clip(0, 100).round(1)
        
    return df