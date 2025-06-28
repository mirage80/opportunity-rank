import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO

# --- Title and Introduction ---
st.set_page_config(page_title="Opportunity Rank", layout="centered")
st.title("🌍 Life Opportunity Rank Estimator")
st.markdown("""
Estimate your position in the global line of opportunity out of 8.2 billion people. 

This tool reflects the **structural conditions you were born into**—not your effort or achievements.
""")

# --- Load full HDI dataset from public source ---
HDI_CSV_URL = "https://raw.githubusercontent.com/datasets/human-development-index/master/data/hdi.csv"
response = requests.get(HDI_CSV_URL)
df_hdi_full = pd.read_csv(StringIO(response.text))

# Keep latest year per country
df_hdi_full = df_hdi_full.sort_values(by=["Country", "Year"], ascending=[True, False]).drop_duplicates(subset="Country")
df_hdi_full = df_hdi_full[df_hdi_full["HDI"].notnull()]

countries = sorted(df_hdi_full["Country"].unique())

# --- User Inputs ---
st.subheader("🧬 Background")
country = st.selectbox("Country of Birth", options=countries)
age = st.slider("Your Age", 0, 100, 30)

st.subheader("💧 Early-Life Access (0 = None, 10 = Full Access)")
edu = st.slider("Access to Education", 0, 10, 7)
health = st.slider("Access to Healthcare", 0, 10, 7)
water = st.slider("Clean Drinking Water", 0, 10, 8)
sewage = st.slider("Sewage & Sanitation", 0, 10, 6)
safety = st.slider("Personal Safety", 0, 10, 7)
freedom = st.slider("Freedom & Rights", 0, 10, 7)

# --- Calculate Opportunity Score ---
if st.button("📊 Estimate My Rank"):
    hdi_row = df_hdi_full[df_hdi_full["Country"] == country]
    hdi = float(hdi_row["HDI"].values[0]) if not hdi_row.empty else 0.6

    personal_score = (edu + health + water + sewage + safety + freedom) / 60  # scaled 0–1
    total_score = 0.7 * hdi + 0.3 * personal_score
    estimated_rank = int((1 - total_score) * 8_200_000_000)

    st.markdown(f"""
    ### 🧭 Your Estimated Opportunity Rank:
    **{estimated_rank:,}** out of 8.2 billion
    """)

    st.success("This reflects your starting point in life—the opportunities you were given, not what you’ve done with them.")

    # Optional bar chart of component scores
    st.subheader("📊 Breakdown of Your Inputs")
    data = pd.DataFrame({
        'Category': ['HDI (Country)', 'Education', 'Healthcare', 'Water', 'Sanitation', 'Safety', 'Freedom'],
        'Score': [hdi * 10, edu, health, water, sewage, safety, freedom]
    })
    fig, ax = plt.subplots()
    ax.bar(data['Category'], data['Score'], color='skyblue')
    ax.set_ylim(0, 10)
    ax.set_ylabel('Access Level (0-10)')
    ax.set_title('Your Early-Life Opportunity Profile')
    st.pyplot(fig)

    st.markdown("""
---

### 🪞 Reflect:
- Did you have to fight for what others were simply given?
- How many people globally are still denied clean water or education?
- What would your life look like if you had been born somewhere else?

_Use this number not as judgment—but as perspective._
""")
