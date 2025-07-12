import streamlit as st
import requests
from datetime import datetime
import pandas as pd
try:
    from streamlit_lottie import st_lottie
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False
    def st_lottie(*args, **kwargs):
        st.warning("Install streamlit-lottie for animated icons: pip install streamlit-lottie")
        return None

# requirements: streamlit-lottie
# pip install streamlit-lottie

# --- CONFIG ---
TOMORROW_API_KEY = "cZJxNQZNzG9eboACNsqEcg4WBx1z9a5U"
TOMORROW_URL = "https://api.tomorrow.io/v4/weather/forecast"
GEOCODE_URL = "https://nominatim.openstreetmap.org/search"

# --- Custom CSS for dark mode and card style ---
st.markdown("""
    <style>
    body, .main, .stApp {background-color: #181c24 !important; color: #f5f6fa !important;}
    .stTabs [data-baseweb="tab-list"] {justify-content: center;}
    .stMetric {background: #232733; border-radius: 10px; padding: 8px;}
    .weather-card {background: #232733; border-radius: 18px; padding: 24px 24px 12px 24px; margin-bottom: 16px;}
    .forecast-row {display: flex; gap: 12px; justify-content: center;}
    .forecast-card {background: #232733; border-radius: 12px; padding: 10px 14px; text-align: center; min-width: 80px;}
    </style>
""", unsafe_allow_html=True)

st.title("🌤️ ClimaSense Weather Dashboard")

# --- Lottie Animations URLs ---
LOTTIE_URLS = {
    "clear_day": "https://assets2.lottiefiles.com/packages/lf20_jzv1zqtk.json",
    "clear_night": "https://assets2.lottiefiles.com/packages/lf20_2glqweqs.json",
    "clouds": "https://assets2.lottiefiles.com/packages/lf20_Stdaec.json",
    "rain": "https://assets2.lottiefiles.com/packages/lf20_Stdaec.json",
    "thunder": "https://assets2.lottiefiles.com/packages/lf20_Stdaec.json",
    "snow": "https://assets2.lottiefiles.com/packages/lf20_Stdaec.json",
    "mist": "https://assets2.lottiefiles.com/packages/lf20_Stdaec.json"
}

# --- Lottie Animations URLs for backgrounds ---
LOTTIE_BG_URLS = {
    'clear': 'https://assets2.lottiefiles.com/packages/lf20_jzv1zqtk.json',  # Sun
    'cloudy': 'https://assets2.lottiefiles.com/packages/lf20_Stdaec.json',   # Clouds
    'rain': 'https://assets2.lottiefiles.com/packages/lf20_rpC1Rd.json',     # Rain
    'snow': 'https://assets2.lottiefiles.com/packages/lf20_JUr2Xt.json',     # Snow
    'thunderstorm': 'https://assets2.lottiefiles.com/packages/lf20_8gdcgjqj.json', # Thunder
    'fog': 'https://assets2.lottiefiles.com/packages/lf20_8gdcgjqj.json',    # Fog (reuse thunder for demo)
}

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def pick_lottie_icon(weather, is_night):
    weather = weather.lower()
    if "clear" in weather:
        return LOTTIE_URLS["clear_night"] if is_night else LOTTIE_URLS["clear_day"]
    if "cloud" in weather:
        return LOTTIE_URLS["clouds"]
    if "rain" in weather or "drizzle" in weather:
        return LOTTIE_URLS["rain"]
    if "thunder" in weather:
        return LOTTIE_URLS["thunder"]
    if "snow" in weather:
        return LOTTIE_URLS["snow"]
    if "mist" in weather or "fog" in weather:
        return LOTTIE_URLS["mist"]
    return LOTTIE_URLS["clear_day"]

def pick_lottie_bg(weather):
    weather = weather.lower()
    if 'thunder' in weather:
        return LOTTIE_BG_URLS['thunderstorm']
    if 'snow' in weather:
        return LOTTIE_BG_URLS['snow']
    if 'rain' in weather or 'drizzle' in weather:
        return LOTTIE_BG_URLS['rain']
    if 'cloud' in weather:
        return LOTTIE_BG_URLS['cloudy']
    if 'mist' in weather or 'fog' in weather:
        return LOTTIE_BG_URLS['fog']
    return LOTTIE_BG_URLS['clear']

# --- Weather code to description mapping (Tomorrow.io) ---
WEATHER_CODE_MAP = {
    1000: 'clear',
    1100: 'mostly clear',
    1101: 'partly cloudy',
    1102: 'mostly cloudy',
    1001: 'cloudy',
    2000: 'fog',
    2100: 'light fog',
    4000: 'drizzle',
    4001: 'rain',
    4200: 'light rain',
    4201: 'heavy rain',
    5000: 'snow',
    5001: 'flurries',
    5100: 'light snow',
    5101: 'heavy snow',
    6000: 'freezing drizzle',
    6001: 'freezing rain',
    6200: 'light freezing rain',
    6201: 'heavy freezing rain',
    7000: 'ice pellets',
    7101: 'heavy ice pellets',
    7102: 'light ice pellets',
    8000: 'thunderstorm'
}

# --- City Input ---
st.sidebar.header("Search City")
city = st.sidebar.text_input("Enter city name", "London")

# --- Geocode City ---
def geocode_city(city):
    params = {"q": city, "format": "json", "limit": 1}
    resp = requests.get(GEOCODE_URL, params=params, headers={"User-Agent": "climasense-weather-app"}, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        return None, None, None
    lat, lon = data[0]["lat"], data[0]["lon"]
    display_name = data[0]["display_name"].split(",")[0]
    return lat, lon, display_name

# --- Fetch Weather ---
import requests.exceptions
@st.cache_data(ttl=600)
def fetch_weather(lat, lon):
    params = {"location": f"{lat},{lon}", "apikey": TOMORROW_API_KEY, "units": "metric"}
    resp = requests.get(TOMORROW_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

# --- Main Logic ---
if city:
    try:
        lat, lon, display_name = geocode_city(city)
        if not lat:
            st.error("City not found. Try again.")
        else:
            try:
                weather_data = fetch_weather(lat, lon)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    st.error("API rate limit exceeded. Please wait a few minutes and try again.")
                    st.stop()
                else:
                    st.error(f"Error: {e}")
                    st.stop()
            minutely = weather_data.get("timelines", {}).get("minutely", [])
            current = minutely[0].get("values", {}) if minutely else {}
            hourly = weather_data.get("timelines", {}).get("hourly", [])
            daily = weather_data.get("timelines", {}).get("daily", [])
            # --- Current Weather Card ---
            st.markdown(f"<div class='weather-card'>", unsafe_allow_html=True)
            # Weather icon and temp
            col1, col2 = st.columns([1,2])
            # Weather description (use mapped description)
            weather_code = current.get('weatherCode', 1000)
            weather_desc = WEATHER_CODE_MAP.get(weather_code, 'Clear').capitalize()
            is_night = False
            now_hour = datetime.now().hour
            is_night = now_hour < 6 or now_hour > 18
            lottie_url = pick_lottie_icon(weather_desc, is_night)
            lottie_json = load_lottieurl(lottie_url)
            with col1:
                if lottie_json:
                    st_lottie(lottie_json, height=100, key="weather_anim")
                else:
                    st.markdown("### 🌤️")
            with col2:
                st.markdown(f"<h1 style='font-size:3.5rem; margin-bottom:0;'>{current.get('temperature', '--')}°</h1>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:1.2rem; color:#b2bec3;'>{weather_desc}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:1.1rem; color:#b2bec3;'>{display_name} • {datetime.now().strftime('%A, %b %d, %I:%M %p')}</div>", unsafe_allow_html=True)
            # Metrics row
            mcol1, mcol2, mcol3, mcol4 = st.columns(4)
            mcol1.metric("Humidity", f"{current.get('humidity', '--')}%")
            mcol2.metric("Precipitation", f"{current.get('precipitationIntensity', '--')} mm/h")
            mcol3.metric("Wind", f"{current.get('windSpeed', '--')} km/h")
            mcol4.metric("Visibility", f"{current.get('visibility', '--')} km")
            st.markdown("</div>", unsafe_allow_html=True)
            # --- Animated weather background ---
            bg_lottie_url = pick_lottie_bg(weather_desc)
            bg_lottie_json = load_lottieurl(bg_lottie_url)
            if bg_lottie_json:
                st_lottie(bg_lottie_json, height=350, key="weather_bg_anim")
            # --- Tabbed Line Charts ---
            chart_tabs = st.tabs(["Temperature", "Wind"])
            # Prepare hourly data for charts
            chart_hours = [entry.get("time", "--")[11:16] for entry in hourly[:12]]
            temp_vals = [entry.get("values", {}).get("temperature", None) for entry in hourly[:12]]
            wind_vals = [entry.get("values", {}).get("windSpeed", None) for entry in hourly[:12]]
            with chart_tabs[0]:
                st.line_chart(pd.DataFrame({"Temperature (°C)": temp_vals}, index=chart_hours))
            with chart_tabs[1]:
                st.line_chart(pd.DataFrame({"Wind (km/h)": wind_vals}, index=chart_hours))
            # --- 7-Day Forecast ---
            st.markdown("<h4 style='margin-top:2em;'>7-Day Forecast</h4>", unsafe_allow_html=True)
            st.markdown("<div class='forecast-row'>", unsafe_allow_html=True)
            for day in daily[:7]:
                d = day.get("time", "--")
                dt = datetime.strptime(d[:10], "%Y-%m-%d")
                day_name = dt.strftime("%a")
                v = day.get("values", {})
                high = v.get("temperatureMax", "--")
                low = v.get("temperatureMin", "--")
                precip = v.get("precipitationIntensityAvg", v.get("precipitationProbabilityAvg", '--'))
                # Use emoji as icon placeholder
                icon = "🌤️"
                st.markdown(f"<div class='forecast-card'><div style='font-size:1.5rem'>{icon}</div><div>{day_name}</div><div style='font-size:1.1rem'>{high}°/{low}°</div><div style='font-size:0.95rem;color:#7ed6df;'>Precip: {precip} mm</div></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Enter a city name to get started.") 