
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
