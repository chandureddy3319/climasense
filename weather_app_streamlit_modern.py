import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import json
from typing import Optional
try:
    from streamlit_lottie import st_lottie
except ImportError:
    pass # If streamlit_lottie is not installed, the app will show an ImportError, which is acceptable for now.

# --- CONFIG ---
TOMORROW_API_KEY = "cZJxNQZNzG9eboACNsqEcg4WBx1z9a5U"
TOMORROW_URL = "https://api.tomorrow.io/v4/weather/forecast"
GEOCODE_URL = "https://nominatim.openstreetmap.org/search"

# --- Weather code to description mapping (Tomorrow.io) ---
WEATHER_CODE_MAP = {
    1000: 'clear', 1100: 'mostly clear', 1101: 'partly cloudy', 1102: 'mostly cloudy', 1001: 'cloudy',
    2000: 'fog', 2100: 'light fog', 4000: 'drizzle', 4001: 'rain', 4200: 'light rain', 4201: 'heavy rain',
    5000: 'snow', 5001: 'flurries', 5100: 'light snow', 5101: 'heavy snow', 6000: 'freezing drizzle',
    6001: 'freezing rain', 6200: 'light freezing rain', 6201: 'heavy freezing rain', 7000: 'ice pellets',
    7101: 'heavy ice pellets', 7102: 'light ice pellets', 8000: 'thunderstorm'
}

# --- Lottie Animations URLs for backgrounds ---
# (Lottie animation backgrounds removed as per user request)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- Simple, modern weather app CSS ---
st.markdown("""
    <style>
    body, .main, .stApp {
        background: linear-gradient(120deg, #e0eafc 0%, #cfdef3 100%) !important;
        color: #222 !important;
    }
    .glass-card {
        background: rgba(255,255,255,0.85);
        border-radius: 24px;
        padding: 32px 32px 24px 32px;
        margin: 24px auto 0 auto;
        box-shadow: 0 4px 24px 0 rgba(31,38,135,0.10);
        max-width: 400px;
        width: 100%;
    }
    .city-title {
        font-size:2.2rem; font-weight:700; text-align:center; margin-bottom:0.5em; color: #1976d2;
    }
    .temp-main {
        font-size:4.5rem; font-weight:800; text-align:center; margin-bottom:0.1em; color: #1565c0;
    }
    .weather-desc {
        font-size:1.3rem; text-align:center; color:#607d8b; margin-bottom:0.5em; font-weight:500;
    }
    .highlow {
        font-size:1.1rem; text-align:center; color:#607d8b; margin-bottom:1.2em;
    }
    .hourly-row, .forecast-row {
        display: flex; gap: 12px; justify-content: center; margin-bottom: 1.5em;
    }
    .hourly-card, .forecast-card {
        background: #f5fafd;
        border-radius: 14px;
        padding: 12px 10px;
        text-align: center;
        min-width: 60px;
        box-shadow: 0 1px 4px 0 rgba(31,38,135,0.06);
        scroll-snap-align: start;
        transition: box-shadow 0.2s, transform 0.2s;
        border: 2px solid #bbdefb;
    }
    .hourly-card:hover, .forecast-card:hover {
        box-shadow: 0 4px 16px 0 rgba(30, 136, 229, 0.13);
        transform: translateY(-3px) scale(1.04);
        z-index: 2;
    }
    .divider {
        width: 100%;
        max-width: 420px;
        margin: 1.5em auto 1em auto;
        border-bottom: 1.5px solid #e3eafc;
    }
    .forecast-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
        gap: 14px;
        margin-bottom: 2em;
    }
    .alert-banner {
        background: linear-gradient(90deg, #fffbe6 0%, #ffe0b2 100%);
        color: #b26a00;
        border-radius: 16px;
        padding: 18px 24px;
        margin: 18px auto 0 auto;
        max-width: 440px;
        font-size: 1.08rem;
        font-weight: 600;
        box-shadow: 0 2px 8px 0 rgba(255,193,7,0.10);
        border: 1.5px solid #ffe082;
        display: flex;
        align-items: flex-start;
        gap: 12px;
    }
    .alert-banner .icon { font-size: 1.5em; margin-right: 8px; }
    </style>
""", unsafe_allow_html=True)

# --- Helper: Info chip CSS ---
st.markdown("""
    <style>
    .info-chips-row {
        display: flex;
        gap: 12px;
        justify-content: center;
        margin-bottom: 0.8em;
        flex-wrap: wrap;
    }
    .info-chip {
        background: #e3f0ff;
        color: #1976d2;
        border-radius: 16px;
        padding: 7px 16px 7px 12px;
        font-size: 1.05rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        box-shadow: 0 1px 4px 0 rgba(30, 136, 229, 0.08);
        border: 1px solid #bbdefb;
        margin-bottom: 4px;
    }
    .info-chip .icon { margin-right: 7px; font-size: 1.2em; }
    .sun-row {
        display: flex;
        gap: 24px;
        justify-content: center;
        margin-bottom: 1.2em;
        color: #f9a825;
        font-size: 1.08rem;
        font-weight: 500;
    }
    .sun-row .icon { margin-right: 6px; font-size: 1.2em; }
    </style>
""", unsafe_allow_html=True)

# --- Helper: Weather icon mapping ---
WEATHER_ICON_MAP = {
    'clear': '☀️',
    'mostly clear': '🌤️',
    'partly cloudy': '⛅',
    'mostly cloudy': '🌥️',
    'cloudy': '☁️',
    'fog': '🌫️',
    'light fog': '🌫️',
    'drizzle': '🌦️',
    'rain': '🌧️',
    'light rain': '🌦️',
    'heavy rain': '🌧️',
    'snow': '❄️',
    'flurries': '🌨️',
    'light snow': '🌨️',
    'heavy snow': '❄️',
    'freezing drizzle': '🌧️',
    'freezing rain': '🌧️',
    'light freezing rain': '🌧️',
    'heavy freezing rain': '🌧️',
    'ice pellets': '🧊',
    'heavy ice pellets': '🧊',
    'light ice pellets': '🧊',
    'thunderstorm': '⛈️',
}

# --- Main Content Wrapper ---
st.markdown("<div class='main-content'>", unsafe_allow_html=True)

# --- IP Geolocation ---
def detect_location() -> Optional[str]:
    try:
        resp = requests.get("https://ipinfo.io/json", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("city", None)
    except Exception:
        pass
    return None

# --- Unit toggle in sidebar ---
st.sidebar.header("Search City")
unit = st.sidebar.radio("Temperature Unit", ["°C", "°F"], index=0, horizontal=True)
unit_api = "metric" if unit == "°C" else "imperial"
unit_symbol = "°C" if unit == "°C" else "°F"

# --- Theme Toggle ---
st.sidebar.header("Theme")
theme = st.sidebar.radio("Choose theme", ["Light", "Dark"], index=0, horizontal=True)

if theme == "Dark":
    st.markdown("""
        <style>
        body, .main, .stApp {
            background: linear-gradient(120deg, #232526 0%, #414345 100%) !important;
            color: #f5fafd !important;
        }
        .glass-card {
            background: rgba(40,40,50,0.85);
            color: #f5fafd !important;
            box-shadow: 0 4px 24px 0 rgba(31,38,135,0.18);
        }
        .city-title { color: #90caf9; }
        .temp-main { color: #bbdefb; }
        .weather-desc, .highlow { color: #b0bec5; }
        .hourly-card, .forecast-card {
            background: #232b33;
            border: 2px solid #37474f;
            color: #e3f2fd;
        }
        .hourly-card:hover, .forecast-card:hover {
            box-shadow: 0 4px 16px 0 rgba(144,202,249,0.13);
        }
        .divider { border-bottom: 1.5px solid #37474f; }
        .forecast-grid { }
        .alert-banner {
            background: linear-gradient(90deg, #2d2d2d 0%, #424242 100%);
            color: #ffe082;
            border: 1.5px solid #ffe082;
        }
        .info-chip {
            background: #263238;
            color: #90caf9;
            border: 1px solid #37474f;
        }
        .sun-row { color: #ffe082; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body, .main, .stApp {
            background: linear-gradient(120deg, #e0eafc 0%, #cfdef3 100%) !important;
            color: #222 !important;
        }
        .glass-card {
            background: rgba(255,255,255,0.85);
            color: #222 !important;
            box-shadow: 0 4px 24px 0 rgba(31,38,135,0.10);
        }
        .city-title { color: #1976d2; }
        .temp-main { color: #1565c0; }
        .weather-desc, .highlow { color: #607d8b; }
        .hourly-card, .forecast-card {
            background: #f5fafd;
            border: 2px solid #bbdefb;
            color: #1976d2;
        }
        .hourly-card:hover, .forecast-card:hover {
            box-shadow: 0 4px 16px 0 rgba(30, 136, 229, 0.13);
        }
        .divider { border-bottom: 1.5px solid #e3eafc; }
        .forecast-grid { }
        .alert-banner {
            background: linear-gradient(90deg, #fffbe6 0%, #ffe0b2 100%);
            color: #b26a00;
            border: 1.5px solid #ffe082;
        }
        .info-chip {
            background: #e3f0ff;
            color: #1976d2;
            border: 1px solid #bbdefb;
        }
        .sun-row { color: #f9a825; }
        </style>
    """, unsafe_allow_html=True)

# --- Dashboard Options ---
st.sidebar.header("Dashboard Options")
show_hourly = st.sidebar.checkbox("Show Hourly Forecast", value=True)
show_weekly = st.sidebar.checkbox("Show 7-Day Forecast", value=True)
show_chips = st.sidebar.checkbox("Show AQI/UV Info Chips", value=True)
show_sun = st.sidebar.checkbox("Show Sunrise/Sunset", value=True)
show_map = st.sidebar.checkbox("Show Map", value=True)

def convert_temp(temp_c, to_f):
    if temp_c is None or temp_c == '--':
        return temp_c
    try:
        t = float(temp_c)
        return round(t * 9/5 + 32, 1) if to_f else round(t, 1)
    except Exception:
        return temp_c

# --- Favorites/Recent Locations ---
if 'favorites' not in st.session_state:
    st.session_state['favorites'] = []
if 'selected_favorite' not in st.session_state:
    st.session_state['selected_favorite'] = None

st.sidebar.subheader("Favorites")
fav_cities = st.session_state['favorites']
selected_fav = st.sidebar.selectbox(
    "Select a favorite city",
    ["-"] + fav_cities,
    index=0,
    key="favorite_selectbox"
)

# City input logic
city = st.sidebar.text_input("City name", value="", key="city_input")
if selected_fav != "-" and selected_fav:
    city = selected_fav

# Add to favorites button
if city and city not in fav_cities:
    if st.sidebar.button(f"Add '{city}' to favorites"):
        st.session_state['favorites'].append(city)
        st.rerun()

# Remove from favorites button
if selected_fav != "-" and selected_fav:
    if st.sidebar.button(f"Remove '{selected_fav}' from favorites"):
        st.session_state['favorites'].remove(selected_fav)
        st.session_state['selected_favorite'] = None
        st.rerun()

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
def fetch_weather(lat, lon, units="metric"):
    params = {"location": f"{lat},{lon}", "apikey": TOMORROW_API_KEY, "units": units}
    resp = requests.get(TOMORROW_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

# --- Animated weather background (always visible, full-screen, on top of gradient) ---
# (Removed: do not load or display any Lottie animation or overlays)

if city:
    try:
        lat, lon, display_name = geocode_city(city)
        if not lat:
            st.error("City not found. Try again.")
        else:
            weather_data = fetch_weather(lat, lon, units=unit_api)
            # --- Enhanced Weather Alerts Banner ---
            alerts = weather_data.get("alerts", [])
            if alerts:
                st.markdown("<h3 style='text-align:center; color:#d32f2f; margin-bottom:1em;'>⚠️ Weather Alerts</h3>", unsafe_allow_html=True)
                for i, alert in enumerate(alerts):
                    event = alert.get('event', 'Weather Alert')
                    desc = alert.get('description', '')
                    severity = alert.get('severity', 'moderate').lower()
                    
                    # Determine alert styling based on severity
                    if severity in ['severe', 'extreme']:
                        bg_color = "linear-gradient(90deg, #ffebee 0%, #ffcdd2 100%)"
                        text_color = "#c62828"
                        border_color = "#ef5350"
                        icon = "🚨"
                    elif severity in ['moderate', 'minor']:
                        bg_color = "linear-gradient(90deg, #fff3e0 0%, #ffe0b2 100%)"
                        text_color = "#ef6c00"
                        border_color = "#ff9800"
                        icon = "⚠️"
                    else:
                        bg_color = "linear-gradient(90deg, #e8f5e8 0%, #c8e6c9 100%)"
                        text_color = "#2e7d32"
                        border_color = "#4caf50"
                        icon = "ℹ️"
                    
                    # Format alert time if available
                    start_time = alert.get('startTime', '')
                    end_time = alert.get('endTime', '')
                    time_info = ""
                    if start_time and end_time:
                        start_str = start_time[11:16] if 'T' in start_time else start_time
                        end_str = end_time[11:16] if 'T' in end_time else end_time
                        time_info = f"<br><small>Active: {start_str} - {end_str}</small>"
                    
                    st.markdown(f"""
                        <div style='
                            background: {bg_color};
                            color: {text_color};
                            border-radius: 16px;
                            padding: 20px 24px;
                            margin: 12px auto;
                            max-width: 500px;
                            font-size: 1.1rem;
                            font-weight: 600;
                            box-shadow: 0 4px 12px 0 rgba(0,0,0,0.15);
                            border: 2px solid {border_color};
                            display: flex;
                            align-items: flex-start;
                            gap: 15px;
                        '>
                            <span style='font-size: 2em;'>{icon}</span>
                            <div>
                                <div style='font-size: 1.2rem; font-weight: 700; margin-bottom: 8px;'>{event}</div>
                                <div style='font-weight: 500; line-height: 1.4;'>{desc}</div>
                                {time_info}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            minutely = weather_data.get("timelines", {}).get("minutely", [])
            current = minutely[0].get("values", {}) if minutely else {}
            hourly = weather_data.get("timelines", {}).get("hourly", [])
            daily = weather_data.get("timelines", {}).get("daily", [])
            # --- Modern glassmorphism weather card ---
            weather_code = current.get('weatherCode', 1000)
            weather_desc = WEATHER_CODE_MAP.get(weather_code, 'Clear').capitalize()
            weather_icon = WEATHER_ICON_MAP.get(weather_desc.lower(), '❔')
            st.markdown(f"<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:2.5rem; text-align:center; margin-bottom:0.2em;'>{weather_icon}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='city-title'>{display_name}</div>", unsafe_allow_html=True)
            temp_val = current.get('temperature', '--')
            temp_disp = convert_temp(temp_val, unit=="°F") if unit=="°F" else temp_val
            st.markdown(f"<div class='temp-main'>{temp_disp}{unit_symbol}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='weather-desc'>{weather_desc}</div>", unsafe_allow_html=True)
            high = daily[0].get('values', {}).get('temperatureMax', '--')
            low = daily[0].get('values', {}).get('temperatureMin', '--')
            high_disp = convert_temp(high, unit=="°F") if unit=="°F" else high
            low_disp = convert_temp(low, unit=="°F") if unit=="°F" else low
            st.markdown(f"<div class='highlow'>H:{high_disp}{unit_symbol} L:{low_disp}{unit_symbol}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            # --- Info Chips: AQI, UV Index ---
            if show_chips:
                aqi = current.get('epaIndex', None) or current.get('aqi', None)
                uv = current.get('uvIndex', None)
                chips = []
                if aqi is not None:
                    chips.append(f"<div class='info-chip' title='Air Quality Index'><span class='icon'>🌫️</span> AQI: {aqi}</div>")
                if uv is not None:
                    chips.append(f"<div class='info-chip' title='UV Index'><span class='icon'>☀️</span> UV: {uv}</div>")
                if chips:
                    st.markdown(f"<div class='info-chips-row'>{''.join(chips)}</div>", unsafe_allow_html=True)
            # --- Sunrise/Sunset Row ---
            if show_sun:
                sunrise = daily[0].get('values', {}).get('sunriseTime', None)
                sunset = daily[0].get('values', {}).get('sunsetTime', None)
                if sunrise and sunset:
                    sunrise_str = sunrise[11:16] if 'T' in sunrise else sunrise
                    sunset_str = sunset[11:16] if 'T' in sunset else sunset
                    st.markdown(f"<div class='sun-row'><span class='icon'>🌅</span>Sunrise: {sunrise_str} <span class='icon'>🌇</span>Sunset: {sunset_str}</div>", unsafe_allow_html=True)
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            # --- Hourly Forecast Row (scrollable) ---
            if show_hourly:
                st.markdown("<div class='hourly-row'>", unsafe_allow_html=True)
                hourly_times = []
                hourly_temps = []
                for entry in hourly[:12]:
                    t = entry.get("time", "--")[11:16]
                    v = entry.get("values", {})
                    temp = v.get("temperature", "--")
                    temp_disp = convert_temp(temp, unit=="°F") if unit=="°F" else temp
                    hourly_times.append(t)
                    hourly_temps.append(temp_disp)
                    hcode = v.get('weatherCode', 1000)
                    hdesc = WEATHER_CODE_MAP.get(hcode, 'Clear').lower()
                    hicon = WEATHER_ICON_MAP.get(hdesc, '❔')
                    sunset = v.get('sunsetTime', None)
                    if sunset and t == sunset[11:16]:
                        hicon = "🌇"
                    st.markdown(f"<div class='hourly-card'><div class='icon'>{hicon}</div><div class='hour'>{t}</div><div class='temp'>{temp_disp}{unit_symbol}</div></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                # --- Hourly Temperature Chart ---
                st.markdown(f"<h4 style='margin-top:2em; text-align:center;'>Hourly Temperature ({unit_symbol})</h4>", unsafe_allow_html=True)
                st.line_chart(pd.DataFrame({f"Temperature ({unit_symbol})": hourly_temps}, index=pd.Index(hourly_times)))
            # --- 7-Day Forecast Grid ---
            if show_weekly:
                st.markdown("<h4 style='margin-top:2em; text-align:center;'>7-Day Forecast</h4>", unsafe_allow_html=True)
                st.markdown("<div class='forecast-grid'>", unsafe_allow_html=True)
                for day in daily[:7]:
                    d = day.get("time", "--")
                    dt = datetime.strptime(d[:10], "%Y-%m-%d")
                    day_name = dt.strftime("%a")
                    v = day.get("values", {})
                    high = v.get("temperatureMax", "--")
                    low = v.get("temperatureMin", "--")
                    high_disp = convert_temp(high, unit=="°F") if unit=="°F" else high
                    low_disp = convert_temp(low, unit=="°F") if unit=="°F" else low
                    precip = v.get("precipitationIntensityAvg", v.get("precipitationProbabilityAvg", '--'))
                    dcode = v.get('weatherCode', 1000)
                    ddesc = WEATHER_CODE_MAP.get(dcode, 'Clear').lower()
                    dicon = WEATHER_ICON_MAP.get(ddesc, '❔')
                    st.markdown(f"<div class='forecast-card' title='{ddesc.title()}'><div style='font-size:2rem'>{dicon}</div><div style='font-size:1.1rem; font-weight:600'>{day_name}</div><div style='font-size:1.2rem; font-weight:700'>{high_disp}{unit_symbol}/{low_disp}{unit_symbol}</div><div style='font-size:1rem;color:#7ed6df;'>Precip: {precip} mm</div></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)  # Close main-content
            # --- Share Weather Feature ---
            share_url = f"{st.get_option('server.address') or 'http://localhost:8501'}?city={city}"
            st.markdown("<div style='text-align:center; margin-bottom:1em;'>", unsafe_allow_html=True)
            st.code(share_url, language='text')
            st.button("Copy Link", on_click=st.session_state.setdefault, args=("copied", True), key="copy_link_btn")
            if st.session_state.get("copied"):
                st.success("Link copied! (Copy manually if not auto-copied)")
            # Download weather summary as text
            weather_summary = f"Weather for {display_name}\nTemperature: {temp_disp}{unit_symbol}\nCondition: {weather_desc}\nHigh: {high_disp}{unit_symbol}, Low: {low_disp}{unit_symbol}"
            st.download_button("Download Weather Summary", weather_summary, file_name=f"weather_{city}.txt")
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            # --- Map Integration: Show city location ---
            if show_map and lat is not None and lon is not None:
                try:
                    lat_f = float(lat)
                    lon_f = float(lon)
                    st.markdown("<h4 style='text-align:center;'>Location Map</h4>", unsafe_allow_html=True)
                    st.map(pd.DataFrame({"lat": [lat_f], "lon": [lon_f]}))
                except Exception:
                    pass
    except TypeError as e:
        if "unhashable type" in str(e):
            st.error("Internal error: unhashable type used in cache or widget key. Please contact support.")
        else:
            st.error(f"Error: {e}")
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Enter a city name to get started.")
st.markdown("</div>", unsafe_allow_html=True)  # Close main-content 