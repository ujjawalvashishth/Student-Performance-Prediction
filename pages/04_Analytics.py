import streamlit as st
import plotly.express as px
from src.database import fetch_all_predictions

st.title("📊 Deep Dive Analytics")
st.markdown("Explore deep correlational patterns across study hours, attendance, and scores.")

df = fetch_all_predictions()
if df.empty:
    st.warning("Not enough data available for analytics yet.")
else:
    fig = px.box(df, x="performance_category", y="study_hours", color="performance_category", title="Study Hours Distribution per Category")
    st.plotly_chart(fig, use_container_width=True)