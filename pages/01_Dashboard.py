import streamlit as st
import pandas as pd
import plotly.express as px
from src.database import fetch_all_predictions

st.setHeader = st.title("📈 Executive Dashboard")
st.markdown("Overview of student predictions, risk ratios, and academic analytics.")

df = fetch_all_predictions()

if df.empty:
    st.warning("No prediction records found in the database yet. Go to the **Prediction** page to evaluate students!")
else:
    # KPI Metrics Cards
    total_students = len(df)
    avg_score = round(df["predicted_score"].mean(), 1)
    at_risk_count = len(df[df["performance_category"] == "At Risk"])
    avg_attendance = round(df["attendance_pct"].mean(), 1)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Predictions", value=total_students)
    with col2:
        st.metric(label="Avg Predicted Score", value=f"{avg_score} / 100")
    with col3:
        st.metric(label="Students At Risk", value=at_risk_count, delta=f"-{at_risk_count}", delta_color="inverse")
    with col4:
        st.metric(label="Avg Attendance Rate", value=f"{avg_attendance}%")

    st.markdown("---")

    # Visualizations
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Performance Category Distribution")
        cat_counts = df["performance_category"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Count"]
        fig_pie = px.pie(cat_counts, names="Category", values="Count", hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        st.subheader("Attendance vs Predicted Score")
        fig_scatter = px.scatter(df, x="attendance_pct", y="predicted_score", color="performance_category",
                                 hover_data=["student_id", "study_hours"],
                                 color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_scatter, use_container_width=True)