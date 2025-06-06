import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset
@st.cache_data
def load_data():
    file_path = "health_of_the_city.csv"
    df = pd.read_csv(file_path)
    essential_columns = [
        'year', 'sex', 'race_ethnicity', 'age_category',
        'metric_name', 'metric_value', 'lower_bound', 'upper_bound',
        'source', 'category'
    ]
    df = df[essential_columns].dropna()
    df['year'] = df['year'].astype(str).str.extract(r'(\d{4})')
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df = df.dropna(subset=['year'])
    df['year'] = df['year'].astype(int)
    return df

df = load_data()

# --- Branding and Landing Section ---
st.markdown("""
    <div style="text-align: center; padding: 1em;">
        <h1 style="font-size: 3em; color: #4CAF50;">📊 InsightBridge: Health & Poverty Analytics</h1>
        <p style="font-size: 1.2em;">
            A public dashboard for exploring health disparities across demographics.
        </p>
        <p style="font-size: 1.1em; color: #666;">
            Built by <strong>Lebede Ngartera</strong> – Founder of <strong>TeraSystemAI</strong>
        </p>
    </div>
""", unsafe_allow_html=True)

# --- Hire Me / Contact Section ---
st.markdown("""
    <div style="text-align: center; margin-top: 1.5em;">
        <a href="mailto:lebede.ngartera@example.com" target="_blank">
            <button style="padding:10px 25px;font-size:16px;background:#0072C6;color:white;border:none;border-radius:5px;">
                📬 Contact Me
            </button>
        </a>
        <a href="https://www.linkedin.com/in/lebede-ngartera" target="_blank">
            <button style="padding:10px 25px;font-size:16px;background:#0A66C2;color:white;border:none;border-radius:5px; margin-left:10px;">
                💼 Hire Me on LinkedIn
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)

# Dashboard Title
st.title("📊 InsightBridge: Health Trends Dashboard")

# Metric selection
metric = st.selectbox("Select a Metric:", sorted(df['metric_name'].unique()))

# Filters
sex = st.selectbox("Select Sex:", sorted(df['sex'].unique()))
race = st.selectbox("Select Race/Ethnicity:", sorted(df['race_ethnicity'].unique()))

# Filtered data
filtered = df[
    (df['metric_name'] == metric) &
    (df['sex'] == sex) &
    (df['race_ethnicity'] == race)
]

if filtered.empty:
    st.warning("No data available for this selection.")
else:
    trend = filtered.groupby('year')['metric_value'].mean().reset_index()
    trend = trend[(trend['metric_value'] > 0) & (trend['metric_value'] < 100000)]

    # Plot
    fig, ax = plt.subplots()
    ax.plot(trend['year'], trend['metric_value'], marker='o', color='blue')
    ax.set_title(f"{metric.replace('_', ' ').title()} - {race}, {sex}")
    ax.set_xlabel("Year")
    ax.set_ylabel("Metric Value")
    ax.grid(True)
    st.pyplot(fig)

    # Insight
    if len(trend) > 1:
        change = ((trend['metric_value'].iloc[-1] - trend['metric_value'].iloc[0]) /
                  trend['metric_value'].iloc[0]) * 100
        st.success(f"📈 Insight: From {trend['year'].iloc[0]} to {trend['year'].iloc[-1]}, "
                   f"{metric.replace('_', ' ')} for {race}, {sex} changed by {change:.1f}%.")
    else:
        st.info("Only one year of data available.")
