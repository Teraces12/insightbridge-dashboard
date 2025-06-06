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
''')

# Dashboard Title
st.title("📊 InsightBridge: Health Trends Dashboard")

# Metric selection
metric = st.selectbox("Select a Metric:", sorted(df['metric_name'].unique()))

# Show available years for user awareness
year_range = df[df['metric_name'] == metric]['year'].unique()
st.caption(f"📅 Available Years: {', '.join(map(str, sorted(year_range)))}")

# Filters
sex = st.selectbox("Select Sex:", sorted(df['sex'].unique()))
race = st.selectbox("Select Race/Ethnicity:", sorted(df['race_ethnicity'].unique()))

# Filtered data
filtered = df[df['metric_name'] == metric]

# Check trend across all groups first
trend = filtered.groupby('year')['metric_value'].mean().reset_index()
trend = trend[(trend['metric_value'] > 0) & (trend['metric_value'] < 100000)]

if trend.empty:
    st.warning("⚠️ No data available for this metric across any group. Please try another metric.")
elif len(trend) == 1:
    one_year = trend['year'].iloc[0]
    st.info(f"ℹ️ Only one year of data available for '{metric.replace('_', ' ')}' in {one_year}. Showing group comparisons instead.")

    # Group comparison chart for the one year
    comparison_data = filtered[filtered['year'] == one_year].groupby(['sex', 'race_ethnicity'])['metric_value'].mean().reset_index()
    comparison_data['Group'] = comparison_data['sex'] + " | " + comparison_data['race_ethnicity']

    st.subheader(f"📊 Group Comparison for {metric.replace('_', ' ').title()} ({one_year})")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(comparison_data['Group'], comparison_data['metric_value'], color='skyblue')
    ax.set_xlabel("Metric Value")
    ax.set_ylabel("Demographic Group")
    ax.set_title(f"{metric.replace('_', ' ').title()} in {one_year}")
    st.pyplot(fig)

    # Optional: download button for this data
    csv = comparison_data.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Group Comparison", data=csv, file_name="group_comparison.csv", mime="text/csv")

else:
    detailed_filtered = filtered[(filtered['sex'] == sex) & (filtered['race_ethnicity'] == race)]
    detailed_trend = detailed_filtered.groupby('year')['metric_value'].mean().reset_index()
    detailed_trend = detailed_trend[(detailed_trend['metric_value'] > 0) & (detailed_trend['metric_value'] < 100000)]

    # Debug info toggle
    if st.checkbox("🔍 Show Debug Info"):
        st.write("🔎 Filtered Years:", detailed_trend['year'].unique())
        st.write("📋 Sample Data:", detailed_trend.head())

    # If not enough data, fallback to general trend
    fallback = False
    if detailed_trend.empty and len(trend) > 1:
        st.warning("ℹ️ Not enough data for the selected sex and race. Showing overall trend instead.")
        detailed_trend = trend
        fallback = True

    # Plot
    fig, ax = plt.subplots()
    title_suffix = "All Groups (Fallback)" if fallback else f"{race}, {sex}"
    ax.plot(detailed_trend['year'], detailed_trend['metric_value'], marker='o', color='blue')
    ax.set_title(f"{metric.replace('_', ' ').title()} - {title_suffix}")
    ax.set_xlabel("Year")
    ax.set_ylabel("Metric Value")
    ax.grid(True)
    st.pyplot(fig)

    if len(detailed_trend) > 1:
        change = ((detailed_trend['metric_value'].iloc[-1] - detailed_trend['metric_value'].iloc[0]) /
                  detailed_trend['metric_value'].iloc[0]) * 100
        st.success(f"📈 Insight: From {detailed_trend['year'].iloc[0]} to {detailed_trend['year'].iloc[-1]}, "
                   f"{metric.replace('_', ' ')} for {title_suffix} changed by {change:.1f}%.")
    else:
        st.info(f"ℹ️ Only one year of data available for {title_suffix}.")

    # Download button
    csv = detailed_trend.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Trend Data as CSV", data=csv, file_name="trend_data.csv", mime="text/csv")
