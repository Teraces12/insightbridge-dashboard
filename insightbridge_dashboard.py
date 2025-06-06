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

    # Minimal columns check
    expected_cols = [
        'year', 'sex', 'race_ethnicity', 'age_category',
        'metric_name', 'metric_value', 'lower_bound', 'upper_bound',
        'source', 'category'
    ]
    available_cols = [col for col in expected_cols if col in df.columns]
    if not available_cols:
        raise ValueError("CSV is missing all required columns.")

    df = df[available_cols]

    # Clean year field
    df['year'] = df['year'].astype(str).str.extract(r'(\d{4})')
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df = df.dropna(subset=['year'])
    df['year'] = df['year'].astype(int)

    # Clean metric values
    df = df[df['metric_value'].notna()]
    df = df[df['metric_value'] >= 0]

    return df

# --- Safe Data Initialization ---
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
<div style="text-align: center; padding: 1em;">
    <h1 style="font-size: 3em; color: #4CAF50;">📊 InsightBridge: Health & Poverty Analytics</h1>
    <p style="font-size: 1.2em;">
        A public dashboard for exploring health disparities across demographics.
    </p>
    <p style="font-size: 1.1em; color: #666;">
        Built by <strong>Lebede Ngartera</strong> – Founder of <strong>TeraSystemAI</strong>
    </p>
</div>
''', unsafe_allow_html=True)

# --- Hire Me / Contact Section ---
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
</div>
''', unsafe_allow_html=True)

# --- Personal Branding Footer ---
st.markdown('''
---

### 👤 Dr. **Lebede Ngartera**  
**Founder, [TeraSystemAI](https://www.terasystems.ai)**  
🧠 *AI & Data Strategist | Ph.D. in Mathematics*  
🔍 *NLP, ML & LLMs Expert | Turning Data into Insight & Automation*  

**📬 Connect With Me:**  
- [🔗 LinkedIn](https://www.linkedin.com/in/lebede-ngartera-82429343/)  
- [🔬 ResearchGate](https://www.researchgate.net/profile/L-Ngartera?ev=hdr_xprf)  
- [💻 GitHub](https://github.com/Teraces12/skills-introduction-to-github)

📩 *Open to collaborations, consulting, research, or new opportunities.*

---
''', unsafe_allow_html=True)

# Dashboard Title
st.title("📊 InsightBridge: Health Trends Dashboard")

# Metric selection
metric_options = sorted(df['metric_name'].dropna().unique())
metric = st.selectbox("Select a Metric:", metric_options)

# Show available years for user awareness
year_range = df[df['metric_name'] == metric]['year'].dropna().unique()
st.caption(f"🗓️ Available Years: {', '.join(map(str, sorted(year_range)))}")

# Safely populate sex options
sex_options = sorted(df['sex'].dropna().unique())
sex = st.selectbox("Select Sex:", sex_options if sex_options else ["All"])

# Safely populate race options
race_options = sorted(df['race_ethnicity'].dropna().unique())
race = st.selectbox("Select Race/Ethnicity:", race_options if race_options else ["All"])

# Filter by metric
filtered = df[df['metric_name'] == metric]
filtered = filtered[filtered['metric_value'].notna() & (filtered['metric_value'] > 0)]

# Get overall yearly trend
trend = filtered.groupby('year')['metric_value'].mean().reset_index()

# Show the trend table
st.write("📊 Trend Preview:", trend)

# Extract years between 2019–2022 with data
year_window = [int(year) for year in trend['year'].unique() if 2019 <= year <= 2022]

if year_window:
    st.info(f"📊 Showing group comparisons for {metric.replace('_', ' ')} from {min(year_window)} to {max(year_window)}.")

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

        # Download for each year
        csv = comparison_data.to_csv(index=False).encode('utf-8')
        st.download_button(f"⬇️ Download Comparison {year}", data=csv, file_name=f"group_comparison_{year}.csv", mime="text/csv")

else:
    # Fall back if no data from 2019 to 2022
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
