import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import random

# Auto-refresh every 3 seconds
st_autorefresh(interval=3000, key="auto_refresh")

st.set_page_config(page_title="AI Traffic Controller", layout="wide")
st.title("🚦 AI-Powered Smart Traffic Controller (with Live API)")

# --- Replace this URL with your actual Mocki.io API ---
api_url = "http://127.0.0.1:5000/traffic"

# Fetch traffic data from API
try:
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    # ✅ Correctly extract vehicle data
    vehicle_counts = {
        "North": data.get("North", {}).get("vehicles", random.randint(5, 40)),
        "South": data.get("South", {}).get("vehicles", random.randint(5, 40)),
        "East": data.get("East", {}).get("vehicles", random.randint(5, 40)),
        "West": data.get("West", {}).get("vehicles", random.randint(5, 40)),
    }
    timestamp = data.get("timestamp", "Unknown")

except Exception as e:
    st.error(f"Failed to fetch API data: {e}")
    vehicle_counts = {r: random.randint(5, 40) for r in ["North", "South", "East", "West"]}
    timestamp = "Offline Mode"

# --- Traffic AI Logic ---
base_time = 15
adjustment_factor = 30
total_vehicles = sum(vehicle_counts.values())
green_times = {
    road: int(base_time + (vehicle_counts[road] / total_vehicles) * adjustment_factor)
    for road in vehicle_counts
}

# --- UI Display ---
col1, col2, col3, col4 = st.columns(4)
for i, road in enumerate(vehicle_counts):
    [col1, col2, col3, col4][i].metric(
        label=f"{road} Lane 🚗",
        value=f"{vehicle_counts[road]} cars",
        delta=f"{green_times[road]}s green light"
    )

# Intersection display
st.subheader("🛣️ Intersection Simulation")
display = ""
for road in vehicle_counts:
    light_color = "🟢" if green_times[road] > base_time else "🔴"
    cars = "🚗" * (vehicle_counts[road] // 5)
    display += f"{road} Lane: {light_color} {cars}\n"
st.text(display)

# Total waiting units
total_waiting_time = sum([vehicle_counts[r] * green_times[r] for r in vehicle_counts])
st.metric("Estimated Total Waiting Units", total_waiting_time)

st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')} | API timestamp: {timestamp}")
