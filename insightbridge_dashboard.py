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
  background: linear-gradient(270deg, #42a5f5, #66bb6a, #ffa726, #42a5f5);
  background-size: 800% 800%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: animateGradient 6s ease infinite;
  font-weight: bold;
  font-size: 3em;
  display: inline-block;
}
.marquee-text {
  overflow: hidden;
  white-space: nowrap;
  box-sizing: border-box;
  animation: marquee 15s linear infinite;
  font-size: 1.2em;
  color: #333;
  margin-top: 1em;
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
''', unsafe_allow_html=True)

st.markdown('''
<div style="text-align: center; padding: 1em;">
    <h1 class="gradient-text">📊 InsightBridge: Health & Poverty Analytics</h1>
    <p style="font-size: 1.2em;">
        A public dashboard for exploring health disparities across demographics.
    </p>
    <p style="font-size: 1.1em; color: #666;">
        Built by <strong>Lebede Ngartera</strong> – Founder of <strong>TeraSystemAI</strong>
    </p>
    <div class="marquee-text">
        💡 Empowering communities with data. Advancing equity through insight. Fueling change with your support. 💖
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('''
<div style="text-align: center; margin-top: 1.5em;">
    <a href="mailto:lebede.ngartera@example.com" target="_blank">
        <button style="padding:10px 25px;font-size:16px;background:#0072C6;color:white;border:none;border-radius:5px;">
            📬 Contact Me
        </button>
    </a>
    <a href="https://www.linkedin.com/in/lebede-ngartera-82429343/" target="_blank">
        <button style="padding:10px 25px;font-size:16px;background:#0A66C2;color:white;border:none;border-radius:5px; margin-left:10px;">
            💼 Hire Me on LinkedIn
        </button>
    </a>
    <a href="https://buy.stripe.com/3cI9AS11N67I3W66IH04801" target="_blank">
        <button style="padding:10px 25px;font-size:16px;background:#e91e63;color:white;border:none;border-radius:5px; margin-left:10px;">
            💖 Support via Stripe
        </button>
    </a>
</div>
''', unsafe_allow_html=True)

st.title("📊 InsightBridge: Health Trends Dashboard")

metric_options = sorted(df['metric_name'].dropna().unique())
metric = st.selectbox("Select a Metric:", metric_options)

year_range = df[df['metric_name'] == metric]['year'].dropna().unique()
st.caption(f"🗓️ Available Years: {', '.join(map(str, sorted(year_range)))}")

sex_options = sorted(df['sex'].dropna().unique())
sex = st.selectbox("Select Sex:", sex_options if sex_options else ["All"])

race_options = sorted(df['race_ethnicity'].dropna().unique())
race = st.selectbox("Select Race/Ethnicity:", race_options if race_options else ["All"])

filtered = df[df['metric_name'] == metric]
filtered = filtered[filtered['metric_value'].notna() & (filtered['metric_value'] > 0)]

trend = filtered.groupby('year')['metric_value'].mean().reset_index()

st.write("📊 Trend Preview:", trend)

year_window = sorted([int(year) for year in trend['year'].dropna().unique() if 2019 <= year <= 2022])

if year_window:
    if len(year_window) > 1:
        st.info(f"📊 Showing group comparisons for {metric.replace('_', ' ')} from {min(year_window)} to {max(year_window)}.")
    else:
        st.info(f"ℹ️ Showing group comparisons for {metric.replace('_', ' ')} in {year_window[0]} only (no additional years from 2019–2022).")

    for year in year_window:
        yearly_data = filtered[filtered['year'] == year]
        comparison_data = yearly_data.groupby(['sex', 'race_ethnicity'])['metric_value'].mean().reset_index()
        comparison_data['Group'] = comparison_data['sex'] + " | " + comparison_data['race_ethnicity']
        comparison_data = comparison_data.sort_values(by='metric_value')

        st.subheader(f"📊 Group Comparison - {year}")
        fig, ax = plt.subplots(figsize=(9, len(comparison_data) * 0.4))
        bars = ax.barh(comparison_data['Group'], comparison_data['metric_value'], color='steelblue')
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.5, bar.get_y() + bar.get_height() / 2, f'{width:.1f}', va='center')
        ax.set_xlabel("Metric Value")
        ax.set_ylabel("Demographic Group")
        ax.set_title(f"{metric.replace('_', ' ').title()} in {year}")
        st.pyplot(fig)

        csv = comparison_data.to_csv(index=False).encode('utf-8')
        st.download_button(f"⬇️ Download Comparison {year}", data=csv, file_name=f"group_comparison_{year}.csv", mime="text/csv")
else:
    st.subheader("📈 Yearly Trend (Bar Chart)")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(trend['year'].astype(str), trend['metric_value'], color='mediumseagreen')
    ax.set_xlabel("Metric Value")
    ax.set_ylabel("Year")
    ax.set_title(f"{metric.replace('_', ' ').title()} - Yearly Averages")
    ax.invert_yaxis()
    st.pyplot(fig)

    csv = trend.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Trend Data as CSV", data=csv, file_name="trend_data.csv", mime="text/csv")
