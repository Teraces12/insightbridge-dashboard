import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset
@st.cache_data(show_spinner=False)
def load_data():
    file_path = "https://raw.githubusercontent.com/YourUsername/insightbridge-dashboard/main/health_of_the_city.csv"

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error("❌ Dataset not found. Please ensure 'health_of_the_city.csv' is in the same directory.")
        st.stop()

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

# Load cleaned data
df = load_data()

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

# Filters
sex = st.selectbox("Select Sex:", sorted(df['sex'].unique()))
race = st.selectbox("Select Race/Ethnicity:", sorted(df['race_ethnicity'].unique()))

# Filtered data
filtered = df[(df['metric_name'] == metric)]

# Check if there's more than one year of data across all groups
trend = filtered.groupby('year')['metric_value'].mean().reset_index()
trend = trend[(trend['metric_value'] > 0) & (trend['metric_value'] < 100000)]

if trend.empty:
    st.warning("⚠️ No data available for this metric across any group. Please try another metric.")
elif len(trend) == 1:
    st.info("ℹ️ Only one year of data available. Try selecting broader filters or check back for updates.")
else:
    # Further narrow filter if desired
    detailed_filtered = filtered[(filtered['sex'] == sex) & (filtered['race_ethnicity'] == race)]
    detailed_trend = detailed_filtered.groupby('year')['metric_value'].mean().reset_index()
    detailed_trend = detailed_trend[(detailed_trend['metric_value'] > 0) & (detailed_trend['metric_value'] < 100000)]

    # Plot
    fig, ax = plt.subplots()
    ax.plot(detailed_trend['year'], detailed_trend['metric_value'], marker='o', color='blue')
    ax.set_title(f"{metric.replace('_', ' ').title()} - {race}, {sex}")
    ax.set_xlabel("Year")
    ax.set_ylabel("Metric Value")
    ax.grid(True)
    st.pyplot(fig)

    if len(detailed_trend) > 1:
        change = ((detailed_trend['metric_value'].iloc[-1] - detailed_trend['metric_value'].iloc[0]) /
                  detailed_trend['metric_value'].iloc[0]) * 100
        st.success(f"📈 Insight: From {detailed_trend['year'].iloc[0]} to {detailed_trend['year'].iloc[-1]}, "
                   f"{metric.replace('_', ' ')} for {race}, {sex} changed by {change:.1f}%.")
    else:
        st.info("ℹ️ Only one year of data available for this demographic.")
