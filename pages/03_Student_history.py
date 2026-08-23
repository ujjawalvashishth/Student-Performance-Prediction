import streamlit as st
import pandas as pd
from src.database import fetch_all_predictions

st.title("🗄️ Prediction History & Student Records")
st.markdown("Search, filter, and review historical prediction records stored in the SQLite database.")

df = fetch_all_predictions()

if df.empty:
    st.info("No records found.")
else:
    # Search & Filters
    col1, col2 = st.columns(2)
    with col1:
        search_id = st.text_input("🔍 Search by Student ID").strip()
    with col2:
        selected_category = st.selectbox("Filter by Category", ["All"] + list(df["performance_category"].unique()))
        
    filtered_df = df.copy()
    if search_id:
        filtered_df = filtered_df[filtered_df["student_id"].str.contains(search_id, case=False, na=False)]
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["performance_category"] == selected_category]
        
    st.dataframe(filtered_df, use_container_width=True)
    
    # CSV Export Button
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Records as CSV",
        data=csv_data,
        file_name="student_predictions_export.csv",
        mime="text/csv"
    )