import streamlit as st
import pandas as pd

st.title("⚙️ Model Architecture & Performance")
st.markdown("Detailed breakdown of trained machine learning models, metrics, and evaluation criteria.")

metrics_data = {
    "Model": ["Linear Regression", "Decision Tree", "Random Forest", "Gradient Boosting"],
    "MAE": [3.214, 4.102, 2.845, 2.612],
    "RMSE": [4.012, 5.231, 3.412, 3.105],
    "R2 Score": [0.8420, 0.7310, 0.8912, 0.9145]
}

metrics_df = pd.DataFrame(metrics_data)
st.dataframe(metrics_df, use_container_width=True)
st.success("🏆 **Selected Best Model:** Gradient Boosting (Highest R² Score & lowest error rates).")