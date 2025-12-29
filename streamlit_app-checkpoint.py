import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==================================================
# PAGE CONFIG (MUST BE FIRST)
# ==================================================
st.set_page_config(
    page_title="Airline Disruption Analytics",
    layout="wide"
)

# ==================================================
# REMOVE STREAMLIT HEADER & FOOTER
# ==================================================
st.markdown("""
<style>
header {visibility: hidden;}
footer {visibility: hidden;}
.block-container {
    padding-top: 0.5rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# GLOBAL THEME (AIRLINE / POWER BI STYLE)
# ==================================================
st.markdown("""
<style>
.stApp {
    background-color: #ffffff;
    color: #0f172a;
    font-family: "Segoe UI", sans-serif;
}

.hero {
    background: linear-gradient(180deg, #f8fbff, #eef5ff);
    border-radius: 18px;
    padding: 26px;
    margin-bottom: 20px;
}

.title {
    font-size: 30px;
    font-weight: 700;
    text-align: center;
}

.subtitle {
    font-size: 14px;
    color: #64748b;
    text-align: center;
    margin-top: 4px;
}

.kpi-box {
    background: #ffffff;
    border-radius: 14px;
    padding: 16px;
    text-align: center;
    border: 1px solid #e5e7eb;
    box-shadow: 0 6px 18px rgba(0,0,0,0.04);
}

.kpi-value {
    font-size: 26px;
    font-weight: 700;
    color: #2563eb;
}

.kpi-label {
    font-size: 13px;
    color: #64748b;
}

.card {
    background: #ffffff;
    border-radius: 16px;
    padding: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 8px 22px rgba(0,0,0,0.04);
}

.section {
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================
df = pd.read_csv("../data/flight_operations_data_cleaned.csv")

# ==================================================
# HERO HEADER (CENTERED LOGO + TITLE)
# ==================================================
st.markdown('<div class="hero">', unsafe_allow_html=True)

# Centered logo
st.image("../assets/indigo_logo.png", width=90)

# Centered two-color title
st.markdown("""
<div class="title">
<span style="color:#0f172a;">Airline Disruption Impact & </span>
<span style="color:#2563eb;">Recovery Analytics</span>
</div>
<div class="subtitle">
Product & Operations Intelligence Dashboard (Academic Case Study)
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# KPI CALCULATIONS
# ==================================================
total_flights = len(df)
delay_rate = round((df["flight_status"] == "Delayed").mean() * 100, 1)
cancel_rate = round((df["flight_status"] == "Cancelled").mean() * 100, 1)
avg_delay = round(df["departure_delay_min"].mean(), 1)
passengers = int(df["passenger_impact"].sum())

# ==================================================
# KPI ROW
# ==================================================
k1, k2, k3, k4, k5 = st.columns(5)

def kpi(col, value, label):
    col.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

kpi(k1, total_flights, "Total Flights")
kpi(k2, f"{delay_rate}%", "Delay Rate")
kpi(k3, f"{cancel_rate}%", "Cancellation Rate")
kpi(k4, f"{avg_delay} min", "Avg Delay")
kpi(k5, passengers, "Passengers Impacted")

# ==================================================
# ANALYTICS GRID (POWER BI STYLE)
# ==================================================
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section">Disruption Severity Trend</div>', unsafe_allow_html=True)

    dsi = df.groupby("flight_date")["disruption_score"].sum()
    fig, ax = plt.subplots(figsize=(6, 2.2))
    dsi.plot(ax=ax, linewidth=2.8, color="#2563eb")

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.grid(axis="y", linestyle="--", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    st.pyplot(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section">Flight Status Mix</div>', unsafe_allow_html=True)

    status = df["flight_status"].value_counts()
    fig2, ax2 = plt.subplots(figsize=(4, 2.2))
    ax2.bar(status.index, status.values, color="#60a5fa")

    ax2.grid(axis="y", linestyle="--", alpha=0.25)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    st.pyplot(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# SECOND ROW
# ==================================================
c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section">Most Impacted Airports</div>', unsafe_allow_html=True)

    airport = (
        df.groupby("origin_airport")["disruption_score"]
        .sum()
        .sort_values(ascending=False)
    )

    fig3, ax3 = plt.subplots(figsize=(4, 2.1))
    ax3.barh(airport.index, airport.values, color="#93c5fd")
    ax3.invert_yaxis()
    ax3.grid(axis="x", linestyle="--", alpha=0.25)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)

    st.pyplot(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section">Delay Severity Distribution</div>', unsafe_allow_html=True)

    delay_dist = df["delay_category"].value_counts()
    fig4, ax4 = plt.subplots(figsize=(4, 2.1))
    ax4.bar(delay_dist.index, delay_dist.values, color="#bfdbfe")

    ax4.grid(axis="y", linestyle="--", alpha=0.25)
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)

    st.pyplot(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
