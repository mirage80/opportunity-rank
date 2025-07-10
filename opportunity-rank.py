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

# --- Load local HDI dataset instead of remote source ---
df_hdi_full = pd.read_csv("hdi.csv")
df_hdi_full.columns = df_hdi_full.columns.str.strip().str.lower()
df_hdi_full = df_hdi_full[df_hdi_full["hdi"].notnull()]
countries = sorted(df_hdi_full["country"].unique())

# --- User Inputs ---
st.subheader("🧬 Background")
country = st.selectbox("Country of Birth", options=countries)
age = st.slider("Your Age", 0, 100, 30)

# --- Calculate Opportunity Score ---
if st.button("📊 Estimate My Rank"):
    hdi_row = df_hdi_full[df_hdi_full["country"] == country]
    hdi = float(hdi_row["hdi"].values[0]) if not hdi_row.empty else 0.6

    total_score = hdi  # Only use HDI now
    estimated_rank = int((1 - total_score) * 8_200_000_000)

    st.markdown(f"""
    ### 🧭 Your Estimated Opportunity Rank:
    **{estimated_rank:,}** out of 8.2 billion
    """)

    st.success("This reflects your starting point in life—the opportunities you were given, not what you’ve done with them.")

    # Visual representation of global line with pointer
st.subheader("📽️ Visualizing Your Place in the Line")

# Simulated zoom effect by plotting multiple scales
zoom_levels = [100_000, 1_000_000, 10_000_000, 100_000_000, 1_000_000_000, 8_200_000_000]

for zoom in zoom_levels:
    fig, ax = plt.subplots(figsize=(10, 1))
    ax.plot([0, zoom], [0, 0], color='lightgray', linewidth=15)
    if estimated_rank < zoom:
        ax.scatter(estimated_rank, 0, color='red', s=100, zorder=5)
        ax.annotate('⬇ You', xy=(estimated_rank, 0), xytext=(estimated_rank, 0.2),
                    textcoords='data', ha='center', fontsize=10,
                    arrowprops=dict(arrowstyle='->', color='red'))
    ax.set_xlim(0, zoom)
    ax.axis('off')
    st.pyplot(fig)
    st.caption(f"Zoom level: 0 to {zoom:,}")



    st.markdown("""
---

### 🪞 Reflect:
- Did you have to fight for what others were simply given?
- How many people globally are still denied clean water or education?
- What would your life look like if you had been born somewhere else?

_Use this number not as judgment—but as perspective._
""")
