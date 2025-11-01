import streamlit as st
import random
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 2 seconds (2000 milliseconds)
#st_autorefresh(interval=2000, key="auto_refresh")

# Page setup
st.set_page_config(page_title="AI Traffic Signal Simulator", layout="wide")
st.title("🚦 AI-Powered Traffic Signal Simulation (Auto Update)")

# Roads and base times
roads = ["North", "South", "East", "West"]
base_time = 15
adjustment_factor = 30

# Generate random vehicle counts for each road
vehicle_counts = {road: random.randint(5, 40) for road in roads}

# Calculate total vehicles and green light durations proportional to traffic
total_vehicles = sum(vehicle_counts.values())
green_times = {
    road: int(base_time + (vehicle_counts[road] / total_vehicles) * adjustment_factor)
    for road in roads
}

# Display metrics for each road in columns
col1, col2, col3, col4 = st.columns(4)
for i, road in enumerate(roads):
    cols = [col1, col2, col3, col4]
    cols[i].metric(
        label=f"{road} Lane 🚗",
        value=f"{vehicle_counts[road]} cars",
        delta=f"{green_times[road]}s green light",
    )

# Traffic intersection animation (simple text-based)
st.subheader("Intersection Simulation")
display = ""
for road in roads:
    light_color = "🟢" if green_times[road] > base_time else "🔴"
    cars = "🚗" * (vehicle_counts[road] // 5)
    display += f"{road} Lane: {light_color} {cars}\n"
st.text(display)

# Summary metric: total waiting units (simplified calculation)
total_waiting_time = sum(
    vehicle_counts[road] * green_times[road] for road in roads
)
st.metric("Estimated Total Waiting Units", total_waiting_time)

# Timestamp of last update
st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
import streamlit as st
import requests

st.title("Live Traffic Data from API")

try:
    response = requests.get("https://mocki.io/v1/82f5efa3-6386-4a08-a11c-b2f6742cceb6")
    response.raise_for_status()
    traffic_data = response.json()
    
    # Example display
    st.write("Available keys:", traffic_data.keys())
    st.write("Traffic on Main Road:", traffic_data.get("main_road_traffic", "Data not available"))


    
    
except requests.exceptions.RequestException as e:
    st.error(f"API request failed: {e}")
