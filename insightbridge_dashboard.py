import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Inject Google Analytics tracking
GA_MEASUREMENT_ID = "G-578HGNZ4F5"

st.markdown(f"""
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_MEASUREMENT_ID}');
</script>
""", unsafe_allow_html=True)

# Sidebar for Functions Overview
st.sidebar.title("🧠 Functions Overview")
st.sidebar.markdown("""
- `load_data()`: Load and preprocess the dataset
- `initialize_dashboard()`: Run app logic and render visuals
- `render_footer()`: Display project information and personal branding
""")

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

def initialize_dashboard():
    try:
        df = load_data()
        if df is None or df.empty:
            st.error("❌ Dataset loaded but is empty after filtering. Please check your CSV content or cleaning rules.")
            st.stop()
    except Exception as e:
        st.error(f"❌ Data loading failed: {e}")
        st.stop()


def render_footer():
    st.markdown('''
---

### 👤 Dr. **Lebede Ngartera**  
**Independent Researcher, Upper Darby, United States**  
**Founder, [TeraSystemAI](https://www.terasystems.ai)**  
🧠 *AI & Data Strategist | Ph.D. in Mathematics*  
🔍 *NLP, ML & LLMs Expert | Turning Data into Insight & Automation* 

💡 *This project is free and publicly available to empower better understanding of community health challenges.*  
🙏 *Your support—whether through collaboration, partnership, funding, or sharing—is invaluable to our mission.*

**📬 Connect With Me:**  
- [🔗 LinkedIn](https://www.linkedin.com/in/lebede-ngartera-82429343/)  
- [🔬 ResearchGate](https://www.researchgate.net/profile/L-Ngartera?ev=hdr_xprf)  
- [💻 GitHub](https://github.com/Teraces12/skills-introduction-to-github)

📩 *Open to collaborations, consulting, funding, academic exchange, or job opportunities.*

---

### 🫅 Touch a Heart, Fuel a Mission

This project exists to illuminate health disparities, serve communities, and inspire equity.  
Your contribution—no matter the amount—directly supports continued research, platform improvement, and actionable insight.

**Your generosity turns data into change. Thank you for making a difference.** 🙏

---

### 📊 InsightBridge: Health & Poverty Analytics

A public dashboard for exploring health disparities across demographics in Pennsylvania and beyond.  
Built by **Dr. Lebede Ngartera**, Founder of [TeraSystemAI](https://www.terasystems.ai)

---

## 🚀 Live Demo

🔗 [Launch the Dashboard](https://share.streamlit.io/your-streamlit-app-link-here)

## 🎯 Purpose

This tool is designed to:

- Explore **health inequities** through accessible visualizations.
- Provide **data-driven insights** to communities, policymakers, and researchers.
- Support public awareness and inspire **targeted action** toward equity.

---

## 🛠 Features

- 📈 Interactive trend and group comparison charts
- 🧑‍🤝‍🧑 Filters by sex and race/ethnicity
- 📦 Metrics like:
  - Age-adjusted diabetes hospitalization rate
  - Asthma-related ED visits
  - Preventable hypertension and heart failure data
  - Age distribution, poverty, unemployment

---

## 📎 How to Use

1. Clone the repo:
   ```bash
   git clone https://github.com/Teraces12/insightbridge-dashboard.git
   cd insightbridge-dashboard
   ```

---

## 📜 Functions Used in This App

```python
@st.cache_data(show_spinner=False)
def load_data():
    # Loads and filters the dataset
    pass

def initialize_dashboard():
    # Load data and handle UI
    pass

def render_footer():
    # Footer with links and project info
    pass
```
''')

    st.markdown('''
<div style="text-align: center; margin-top: 1em;">
    <a href="https://buy.stripe.com/3cI9AS11N67I3W66IH04801" target="_blank">
        <button style="padding:10px 25px;font-size:16px;background:#6772E5;color:white;border:none;border-radius:5px;">
            💖 Support This Project via Stripe
        </button>
    </a>
</div>
''', unsafe_allow_html=True)

    st.markdown('[💖 Click here to support this project via Stripe](https://buy.stripe.com/3cI9AS11N67I3W66IH04801)', unsafe_allow_html=True)

# Execute the dashboard logic
initialize_dashboard()
render_footer()
