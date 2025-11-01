import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import random
import plotly.graph_objects as go

# --- CONFIG ---
st.set_page_config(page_title="AI Traffic Controller", layout="wide")

# --- STYLES ---
st.markdown("""
    <style>
    body { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); color: white; }
    .stApp { background-color: transparent; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00FF9C; font-weight: bold; }
    div[data-testid="stMetricLabel"] { font-size: 16px; color: #ddd; }
    .css-18e3th9 { background-color: transparent !important; }
    h1, h2, h3, h4, h5, h6 { color: #00E6FF !important; }
    </style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.title("🚦 AI-Powered Smart Traffic Controller (Interactive Dashboard)")
st.caption("Real-Time Intersection Management using Live API Data")

st_autorefresh(interval=3000, key="refresh")

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

# --- METRICS DISPLAY ---
st.markdown("### 🚗 Live Traffic Snapshot")
cols = st.columns(4)
for i, r in enumerate(vehicle_counts):
    delta_color = "normal" if r != active_road else "inverse"
    cols[i].metric(f"{r} Lane", f"{vehicle_counts[r]} cars", f"{green_times[r]}s", delta_color=delta_color)

# --- VISUAL BAR CHART ---
st.markdown("### 📊 Traffic Density Visualization")
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
    title="Traffic Distribution per Lane",
    xaxis_title="Direction",
    yaxis_title="Vehicle Count",
    height=450
)
st.plotly_chart(fig, use_container_width=True)

# --- INTERSECTION SIMULATION ---
st.markdown("### 🛣️ Intersection Simulation")
cols2 = st.columns(4)
for i, r in enumerate(vehicle_counts):
    light_color = "🟢" if r == active_road else "🔴"
    cols2[i].markdown(f"<h3 style='text-align:center'>{r}<br>{light_color}</h3>", unsafe_allow_html=True)

# --- TOTAL WAITING TIME ---
total_wait = sum([vehicle_counts[r]*green_times[r] for r in vehicle_counts])
st.metric("⏱️ Estimated Total Waiting Units", total_wait)
st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')} | API timestamp: {timestamp}")

# --- FOOTER ---
st.markdown("""
---
✅ *Powered by AI-driven optimization logic.*  
💡 *Created for Hackathon 2025 — Urban Development & Infrastructure.*
""")
