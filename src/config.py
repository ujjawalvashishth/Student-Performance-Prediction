import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database Path
DB_PATH = os.path.join(BASE_DIR, "data", "student_performance.db")

# Model & Scaler Paths
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")

# Ensure directories exist safely without throwing FileExistsError on Windows
for path in [
    os.path.join(BASE_DIR, "data", "raw"),
    os.path.join(BASE_DIR, "data", "processed"),
    MODEL_DIR
]:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)