import sqlite3
import pandas as pd
from src.config import DB_PATH

def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    """Initialize the SQLite database and create the predictions table if not exists."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            study_hours REAL,
            attendance_pct REAL,
            previous_marks REAL,
            assignment_score REAL,
            internal_assessment REAL,
            midterm_marks REAL,
            sleep_hours REAL,
            predicted_score REAL,
            performance_category TEXT,
            risk_score REAL,
            prediction_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def save_prediction(data: dict):
    """Save a single student prediction record into the database securely."""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO predictions (
            student_id, age, gender, study_hours, attendance_pct, 
            previous_marks, assignment_score, internal_assessment, 
            midterm_marks, sleep_hours, predicted_score, 
            performance_category, risk_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    cursor.execute(query, (
        data.get("student_id"),
        data.get("age"),
        data.get("gender"),
        data.get("study_hours"),
        data.get("attendance_pct"),
        data.get("previous_marks"),
        data.get("assignment_score"),
        data.get("internal_assessment"),
        data.get("midterm_marks"),
        data.get("sleep_hours"),
        data.get("predicted_score"),
        data.get("performance_category"),
        data.get("risk_score")
    ))
    
    conn.commit()
    conn.close()

def fetch_all_predictions() -> pd.DataFrame:
    """Fetch all prediction records as a Pandas DataFrame for analytics and history."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM predictions ORDER BY prediction_timestamp DESC", conn)
    conn.close()
    return df