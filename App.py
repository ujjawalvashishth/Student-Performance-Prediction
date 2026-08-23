import streamlit as st
import os
from src.database import init_db

# Page Configuration
st.set_page_config(
    page_title="Student Performance Prediction System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize SQLite Database on Startup
init_db()

# Load Custom SaaS CSS Styles
css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Main Navigation Setup using Streamlit's native multi-page feature
# Streamlit automatically looks into the 'pages/' folder for navigation.

st.sidebar.title("🎓 EduPredict AI")
st.sidebar.markdown("---")
st.sidebar.info(
    "Welcome to the Enterprise Student Performance Analytics & Prediction Platform. "
    "Use the sidebar navigation above to switch between modules."
)

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 EduPredict AI • Production Grade System")

# Home/Landing Overview inside app.py
st.title("🎓 Student Performance Prediction Platform")
st.markdown(
    """
    Welcome to the **Machine Learning-powered Academic Intelligence System**. 
    This application helps educators and administrators monitor academic performance, 
    predict student outcomes, identify at-risk students early, and execute data-driven interventions.
    """
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 📊 Executive Analytics")
    st.markdown("Track overall metrics, attendance trends, and performance distributions in real-time.")
with col2:
    st.markdown("### 🤖 ML Predictions")
    st.markdown("Input student parameters to forecast final marks and risk levels instantly with explainable factors.")
with col3:
    st.markdown("### 🗄️ Student History & SQL")
    st.markdown("Search records, filter students by category, view past history, and export reports seamlessly.")

st.markdown("---")
st.markdown("👉 **Get started by selecting a page from the sidebar menu.**")