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

st.markdown('''
<style>
body {
  background-image: url("https://raw.githubusercontent.com/Teraces12/insightbridge-dashboard/main/background.png");
  background-size: cover;
  background-attachment: fixed;
  margin: 0;
  padding: 0;
}
body::before {
  content: "";
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(255, 255, 255, 0.85);
  z-index: -1;
}
.gradient-text {
  background: linear-gradient(270deg, #42a5f5, #66bb6a, #ffa726, #ab47bc);
  background-size: 800% 800%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: animateGradient 6s ease infinite;
  font-weight: bold;
  font-size: 3em;
  display: block;
  text-align: center;
  width: 100%;
}
.marquee-container {
  width: 100%;
  overflow: hidden;
  white-space: nowrap;
  box-sizing: border-box;
  margin-top: 1em;
  text-align: center;
}
.marquee-text {
  display: inline-block;
  animation: marquee 30s linear infinite;
  font-size: 1.3em;
  color: #ad1457;
  font-weight: bold;
}
@keyframes animateGradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes marquee {
  0% { transform: translateX(100%); }
  100% { transform: translateX(-100%); }
}
</style>
<div class="gradient-text">InsightBridge: Health & Poverty Analytics</div>
<p style="text-align:center; margin-top: 0.5em; font-size: 1.1em;">A public dashboard for exploring health disparities across demographics in Pennsylvania, US.</p>
<p style="text-align:center; font-size: 1em;">Built by <strong>Lebede Ngartera</strong> – Founder of <a href="https://www.terasystems.ai" target="_blank">TeraSystemAI</a></p>
<div class="marquee-container">
  <div class="marquee-text">💡 Empowering communities with data. Advancing equity through insight. Fueling change with your support. 💖</div>
</div>
''', unsafe_allow_html=True)

st.markdown('''
<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-top: 1.5em;">
    <div style="
        padding: 10px 25px;
        font-size: 16px;
        background: #f0f0f0;
        color: #333;
        border: none;
        border-radius: 5px;
        font-family: sans-serif;
        display: flex;
        align-items: center;">
        ✉️ lebede@terasystems.ai
    </div>
    <a href="https://www.linkedin.com/in/lebede-ngartera-82429343/" target="_blank" style="
        padding: 10px 25px;
        font-size: 16px;
        background: #0A66C2;
        color: white;
        border: none;
        border-radius: 5px;
        text-decoration: none;
        font-family: sans-serif;">
        💼 Hire Me on LinkedIn
    </a>
    <a href="https://buy.stripe.com/3cI9AS11N67I3W66IH04801" target="_blank" style="
        padding: 10px 25px;
        font-size: 16px;
        background: #e91e63;
        color: white;
        border: none;
        border-radius: 5px;
        text-decoration: none;
        font-family: sans-serif;">
        💖 Support via Stripe
    </a>
</div>
''', unsafe_allow_html=True)

st.title("📊 InsightBridge: Health Trends Dashboard")

...
