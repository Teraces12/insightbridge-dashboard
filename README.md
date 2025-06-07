# --- Personal Branding Footer ---
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
''')

# --- Stripe Support Button (Fallback Included) ---
st.markdown('''
<div style="text-align: center; margin-top: 1em;">
    <a href="https://buy.stripe.com/3cI9AS11N67I3W66IH04801" target="_blank">
        <button style="padding:10px 25px;font-size:16px;background:#6772E5;color:white;border:none;border-radius:5px;">
            💖 Support This Project via Stripe
        </button>
    </a>
</div>
''', unsafe_allow_html=True)

# Optional plain text fallback for environments that don't support HTML buttons
st.markdown('[💖 Click here to support this project via Stripe](https://buy.stripe.com/3cI9AS11N67I3W66IH04801)', unsafe_allow_html=True)
