
import streamlit as st
import os
from dotenv import load_dotenv
from utils import get_weather
import pandas as pd

# Optional autorefresh
try:
    from streamlit_autorefresh import st_autorefresh
    HAS_AUTOREFRESH = True
except Exception:
    HAS_AUTOREFRESH = False

# Load environment variables
load_dotenv()
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", "30"))

st.set_page_config(page_title="Weather Dashboard", layout="wide")
st.title("🌤️ WeatherAPI.com Dashboard")

# Sidebar input
col1, col2 = st.columns([2, 1])
with col1:
    city = st.text_input("City (name,country optional)", value="Stockholm")
    refresh = st.button("Refresh now")
    auto_refresh = st.checkbox(
        "Auto-refresh every 30s (requires streamlit-autorefresh)",
        value=False if not HAS_AUTOREFRESH else True
    )

with col2:
    st.markdown("""
        **Instructions**
        - Type a city name (e.g. `London,uk` or `Stockholm,se`).
        - Click Refresh.
        - Toggle auto-refresh if installed.
    """)
    st.markdown("---")
    st.markdown("Powered by WeatherAPI.com")

# Enable auto-refresh if available
if HAS_AUTOREFRESH and auto_refresh:
    st_autorefresh(interval=30_000, limit=None, key="autorefresh")

# Cache API calls
@st.cache_data(ttl=CACHE_TTL)
def fetch(city):
    return get_weather(city)

if not city.strip():
    st.warning("Please enter a city name.")
    st.stop()

# Fetch data
data = fetch(city)

# Display data
if not data:
    st.error("No data returned. Check your API key and network.")
elif "error" in data:
    st.error(f"API error: {data.get('error')} (status: {data.get('status_code')})")
else:
    current = data["current"]
    location = data["location"]

    left, right = st.columns([2,3])

    with left:
        st.subheader(f"{location['name']}, {location['country']}")
        st.metric("Temperature (°C)", current["temp_c"])
        st.write(f"Feels like: {current['feelslike_c']}°C")
        st.write(f"Humidity: {current['humidity']} %")
        st.write(f"Pressure: {current['pressure_mb']} hPa")
        st.write(f"Wind: {current['wind_kph']} kph")

    with right:
        st.subheader("Conditions")
        st.write(f"**{current['condition']['text']}**")
        icon_url = f"http:{current['condition']['icon']}"
        st.image(icon_url, width=100)

    # Show raw JSON
    st.markdown("---")
    with st.expander("Show raw JSON"):
        st.json(data)

    # Display numeric values in a DataFrame
    df = pd.DataFrame({
        "metric": ["temp_c","feelslike_c","humidity","pressure_mb","wind_kph"],
        "value": [current["temp_c"], current["feelslike_c"], current["humidity"], current["pressure_mb"], current["wind_kph"]]
    })
    st.dataframe(df)


