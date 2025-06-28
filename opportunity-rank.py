import streamlit as st

# --- Title and Introduction ---
st.set_page_config(page_title="Opportunity Rank", layout="centered")
st.title("🌍 Life Opportunity Rank Estimator")
st.markdown("""
Estimate your position in the global line of opportunity out of 8.2 billion people. 

This tool reflects the **structural conditions you were born into**—not your effort or achievements.
""")

# --- Country and HDI Mapping ---
hdi_map = {
    "Norway": 0.961,
    "Switzerland": 0.955,
    "Ireland": 0.945,
    "United States": 0.921,
    "Mexico": 0.758,
    "India": 0.633,
    "Ethiopia": 0.498,
    "Somalia": 0.398
}

countries = list(hdi_map.keys())

# --- User Inputs ---
st.subheader("🧬 Background")
country = st.selectbox("Country of Birth", options=countries)
age = st.slider("Your Age", 0, 100, 30)

st.subheader("💧 Early-Life Access (0 = None, 10 = Full Access)")
edu = st.slider("Education", 0, 10, 7)
health = st.slider("Healthcare", 0, 10, 7)
water = st.slider("Clean Drinking Water", 0, 10, 8)
sewage = st.slider("Sewage / Sanitation", 0, 10, 6)
safety = st.slider("Personal Safety", 0, 10, 7)
freedom = st.slider("Freedom & Rights", 0, 10, 7)

# --- Calculation ---
if st.button("📊 Estimate My Rank"):
    hdi = hdi_map.get(country, 0.6)  # default HDI if not found
    personal_score = (edu + health + water + sewage + safety + freedom) / 60  # max = 1
    total_score = 0.7 * hdi + 0.3 * personal_score
    estimated_rank = int((1 - total_score) * 8_200_000_000)

    st.markdown(f"### 🧭 Your estimated opportunity rank: **{estimated_rank:,}** out of 8.2 billion")
    st.info("This reflects your starting point in life—the opportunities you were given, not what you’ve done with them.")

    st.markdown("""
---

### 🪞 Reflect:
- Did you have to fight for what others were simply given?
- How many people globally are still denied clean water or education?
- What would your life look like if you had been born somewhere else?

_Use this number not as judgment—but as perspective._
""")
