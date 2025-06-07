import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset
@st.cache_data(show_spinner=False)
def load_data():
    file_path = "https://raw.githubusercontent.com/Teraces12/insightbridge-dashboard/main/health_of_the_city.csv"
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise RuntimeError(f"Could not read CSV file: {e}")

    expected_cols = [
        'year', 'sex', 'race_ethnicity', 'age_category',
        'metric_name', 'metric_value', 'lower_bound', 'upper_bound',
        'source', 'category'
    ]
    available_cols = [col for col in expected_cols if col in df.columns]
    if not available_cols:
        raise ValueError("CSV is missing all required columns.")

    df = df[available_cols]
    df['year'] = df['year'].astype(str).str.extract(r'(\d{4})')
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df = df.dropna(subset=['year'])
    df['year'] = df['year'].astype(int)
    df = df[df['metric_value'].notna()]
    df = df[df['metric_value'] >= 0]
    return df

# Safe Data Initialization
try:
    df = load_data()
    if df is None or df.empty:
        st.error("❌ Dataset loaded but is empty after filtering. Please check your CSV content or cleaning rules.")
        st.stop()
except Exception as e:
    st.error(f"❌ Data loading failed: {e}")
    st.stop()

# --- Branding and Landing Section ---
st.set_page_config(page_title="InsightBridge: Health & Poverty Analytics", layout="wide")

st.mar
