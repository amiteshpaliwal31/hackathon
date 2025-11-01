import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import random
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Smart Traffic Controller", layout="wide")

# --- AUTO REFRESH ---
st_autorefresh(interval=3000, key="refresh")

# --- CUSTOM CSS (modern UI theme) ---
st.markdown("""
    <style>
    body {
        background: radial-gradient(circle at top left, #111, #1c1c1c);
        color: white;
        font-family: 'Poppins', sans-serif;
    }
    h1, h2, h3 {
        color: #00E6FF;
        text-align: center;
        letter-spacing: 0.5px;
    }
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        color: #00E6FF;
        text-shadow: 0px 0px 15px #00E6FF;
        margin-bottom: 1rem;
    }
    .sub-title {
        text-align: center;
        color: #bdbdbd;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        color: #00FFB3;
    }
    div[data-testid="stMetricLabel"] {
        color: #ccc;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 class='main-title'>🚦 AI-Powered Smart Traffic Controller</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Real-time Intelligent Traffic Optimization Dashboard</p>", unsafe_allow_html=True)

# --- API CALL ---
api_url = "http://127.0.0.1:5000/traffic"  # Replace with your actual API endpoint
try:
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()
    vehicle_counts = {
        d: data.get(d, {}).get("vehicles", random.randint(5, 40))
        for d in ["North", "South", "East", "West"]
    }
    timestamp = data.get("timestamp", "Unknown")
except Exception as e:
    st.warning(f"⚠️ API offline or unreachable: {e}")
    vehicle_counts = {r: random.randint(5, 40) for r in ["North", "South", "East", "West"]}
    timestamp = "Offline Mode"

# --- AI LOGIC ---
base_time = 15
adjustment_factor = 30
total = sum(vehicle_counts.values())
green_times = {r: int(base_time + (vehicle_counts[r]/total)*adjustment_factor) for r in vehicle_counts}
active_road = max(green_times, key=green_times.get)

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.header("🧠 Control Panel")
mode = st.sidebar.radio("Mode:", ["AI Decision", "Manual Override"])
if mode == "Manual Override":
    active_road = st.sidebar.selectbox("Select Green Light Lane:", list(vehicle_counts.keys()))

# --- AI STATUS CARD ---
if mode == "AI Decision":
    st.info(f"🤖 AI Optimized Signal: Prioritizing **{active_road}** lane based on live congestion.")
else:
    st.success(f"🕹️ Manual Override Active — Green light set to **{active_road}** lane.")

# --- LIVE METRICS ---
cols = st.columns(4)
for i, r in enumerate(vehicle_counts):
    delta_color = "inverse" if r == active_road else "normal"
    cols[i].metric(f"{r} Lane", f"{vehicle_counts[r]} cars", f"{green_times[r]}s", delta_color=delta_color)
style_metric_cards(border_color="#00E6FF", border_left_color="#00FF99")

# --- BAR CHART ---
st.markdown("### 📊 Traffic Load Analysis")
fig = go.Figure()
fig.add_trace(go.Bar(
    x=list(vehicle_counts.keys()),
    y=list(vehicle_counts.values()),
    marker_color=["#2ECC71" if r == active_road else "#E74C3C" for r in vehicle_counts],
    text=[f"{green_times[r]}s green" for r in vehicle_counts],
    textposition='outside'
))
fig.update_layout(
    template="plotly_dark",
    title="Real-Time Vehicle Density",
    xaxis_title="Direction",
    yaxis_title="Vehicle Count",
    height=450,
    font=dict(color='white')
)
st.plotly_chart(fig, use_container_width=True)

# --- INTERSECTION VISUAL ---
st.markdown("### 🛣️ Intersection View")
cols2 = st.columns(4)
for i, r in enumerate(vehicle_counts):
    if r == active_road:
        light = "<span style='font-size:40px;'>🟢</span>"
    else:
        light = "<span style='font-size:40px;'>🔴</span>"
    cols2[i].markdown(f"<h4 style='text-align:center'>{r}<br>{light}</h4>", unsafe_allow_html=True)

# --- PERFORMANCE STATS ---
total_wait = sum([vehicle_counts[r]*green_times[r] for r in vehicle_counts])
st.metric("⏱️ Estimated Total Waiting Units", total_wait)
st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')} | API timestamp: {timestamp}")

# --- FOOTER ---
st.markdown("""
---
<div style="text-align:center; color:#aaa;">
✅ Powered by AI-based adaptive control system <br>
💡 Hackathon Project 2025 | Urban Infrastructure Track
</div>
""", unsafe_allow_html=True)
