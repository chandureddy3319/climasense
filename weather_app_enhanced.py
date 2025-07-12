"""
Enhanced Live Weather App
A Python application that fetches real-time weather data using OpenWeatherMap API
and displays it in a user-friendly Tkinter GUI with weather icons and additional features.

Author: Weather App Developer
Version: 2.0
"""

import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json
from datetime import datetime
import threading
import os
import itertools

class EnhancedWeatherApp:
    def __init__(self, root):
        """
        Initialize the Enhanced Weather App with main window and components.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Enhanced Live Weather App")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#eaf6fb")
        
        # API Configuration
        self.api_key = "cZJxNQZNzG9eboACNsqEcg4WBx1z9a5U"  # Tomorrow.io API key
        self.base_url = "https://api.tomorrow.io/v4/weather/forecast"
        
        # Weather icons mapping
        self.weather_icons = {
            '01d': '☀️',  # clear sky day
            '01n': '🌙',  # clear sky night
            '02d': '⛅',  # few clouds day
            '02n': '☁️',  # few clouds night
            '03d': '☁️',  # scattered clouds
            '03n': '☁️',  # scattered clouds
            '04d': '☁️',  # broken clouds
            '04n': '☁️',  # broken clouds
            '09d': '🌧️',  # shower rain
            '09n': '🌧️',  # shower rain
            '10d': '🌦️',  # rain day
            '10n': '🌧️',  # rain night
            '11d': '⛈️',  # thunderstorm
            '11n': '⛈️',  # thunderstorm
            '13d': '🌨️',  # snow
            '13n': '🌨️',  # snow
            '50d': '🌫️',  # mist
            '50n': '🌫️',  # mist
        }
        
        # Create and configure the main frame with card style
        self.main_frame = tk.Frame(root, padx=0, pady=0, bg="#eaf6fb")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        # Add tabbed notebook for dashboard
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=30, pady=(0, 10))
        self.current_tab = tk.Frame(self.notebook, bg="white")
        self.hourly_tab = tk.Frame(self.notebook, bg="white")
        self.alerts_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.current_tab, text="Current")
        self.notebook.add(self.hourly_tab, text="Hourly")
        self.notebook.add(self.alerts_tab, text="Alerts")
        self.setup_ui()
        
        self.icon_frames = None  # For animated GIF frames
        self.icon_anim = None    # Animation job id
        
    def setup_ui(self):
        """Set up the user interface components with a professional look and dashboard tabs."""
        # Title Label with modern font
        title_label = tk.Label(
            self.main_frame,
            text="🌤️ ClimaSense Weather Dashboard",
            font=("Segoe UI", 20, "bold"),
            fg="#1a5276",
            bg="#eaf6fb"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 10))
        # Search Frame
        search_frame = tk.Frame(self.main_frame, bg="#eaf6fb")
        search_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        search_frame.grid_columnconfigure(0, weight=1)
        # City Input Section
        city_label = tk.Label(
            search_frame,
            text="Enter City Name:",
            font=("Segoe UI", 12, "bold"),
            fg="#2471a3",
            bg="#eaf6fb"
        )
        city_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        # Input frame for city entry and button
        input_frame = tk.Frame(search_frame, bg="#eaf6fb")
        input_frame.grid(row=1, column=0, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        self.city_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            relief=tk.GROOVE,
            bd=2,
            width=22
        )
        self.city_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.city_entry.focus()
        # Get Weather Button (modern style)
        self.weather_button = tk.Button(
            input_frame,
            text="Get Weather",
            font=("Segoe UI", 12, "bold"),
            bg="#2980b9",
            fg="white",
            activebackground="#5499c7",
            activeforeground="white",
            relief=tk.FLAT,
            padx=18,
            pady=4,
            bd=0,
            cursor="hand2",
            command=self.get_weather
        )
        self.weather_button.grid(row=0, column=1)
        self.weather_button.bind("<Enter>", lambda e: self.weather_button.config(bg="#5499c7"))
        self.weather_button.bind("<Leave>", lambda e: self.weather_button.config(bg="#2980b9"))
        # Bind Enter key to get weather
        self.city_entry.bind('<Return>', lambda event: self.get_weather())
        # Status Label
        self.status_label = tk.Label(
            self.main_frame,
            text="Enter a city name and click 'Get Weather'",
            font=("Segoe UI", 10),
            fg="#7f8c8d",
            bg="#eaf6fb"
        )
        self.status_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        # --- Current Tab UI ---
        self._setup_current_tab()
        # --- Hourly Tab UI ---
        self._setup_hourly_tab()
        # --- Alerts Tab UI ---
        self._setup_alerts_tab()
        # Progress Bar (hidden by default)
        self.progress = ttk.Progressbar(
            self.main_frame,
            mode='indeterminate'
        )
        
    def _setup_current_tab(self):
        # Weather Card in Current Tab
        self.weather_card = tk.Frame(self.current_tab, bg="white", bd=0, highlightthickness=0)
        self.weather_card.pack(fill="both", expand=True, padx=10, pady=10)
        self.weather_card.grid_columnconfigure(0, weight=1)
        self.weather_card.grid_propagate(False)
        self.weather_card.configure(height=220)
        self.icon_city_frame = tk.Frame(self.weather_card, bg="white")
        self.icon_city_frame.pack(fill="x", padx=10, pady=(18, 0))
        self.weather_icon_label = tk.Label(
            self.icon_city_frame,
            text="🌤️",
            font=("Segoe UI Emoji", 44),
            bg="white"
        )
        self.weather_icon_label.pack(side="left", padx=(0, 15))
        self.city_info_label = tk.Label(
            self.icon_city_frame,
            text="Enter a city name",
            font=("Segoe UI", 14, "bold"),
            fg="#1a5276",
            bg="white"
        )
        self.city_info_label.pack(side="left")
        info_frame = tk.Frame(self.weather_card, bg="white")
        info_frame.pack(fill="x", padx=10, pady=(0, 10))
        self.temp_label = tk.Label(
            info_frame,
            text="--°C",
            font=("Segoe UI", 28, "bold"),
            fg="#e74c3c",
            bg="white"
        )
        self.temp_label.pack(anchor="w", pady=(0, 5))
        self.desc_label = tk.Label(
            info_frame,
            text="Weather: --",
            font=("Segoe UI", 12),
            fg="#34495e",
            bg="white",
            anchor="w"
        )
        self.desc_label.pack(fill="x", pady=2)
        details_frame = tk.Frame(info_frame, bg="white")
        details_frame.pack(fill="x", pady=(10, 0))
        self.humidity_label = tk.Label(
            details_frame,
            text="💧 Humidity: --%",
            font=("Segoe UI", 11),
            fg="#2c3e50",
            bg="white",
            anchor="w"
        )
        self.humidity_label.grid(row=0, column=0, sticky="w", padx=(0, 20))
        self.wind_label = tk.Label(
            details_frame,
            text="💨 Wind: -- m/s",
            font=("Segoe UI", 11),
            fg="#2c3e50",
            bg="white",
            anchor="w"
        )
        self.wind_label.grid(row=0, column=1, sticky="w")
        self.pressure_label = tk.Label(
            details_frame,
            text="🌡️ Pressure: -- hPa",
            font=("Segoe UI", 11),
            fg="#2c3e50",
            bg="white",
            anchor="w"
        )
        self.pressure_label.grid(row=1, column=0, sticky="w", padx=(0, 20), pady=(5, 0))
        self.visibility_label = tk.Label(
            details_frame,
            text="👁️ Visibility: -- km",
            font=("Segoe UI", 11),
            fg="#2c3e50",
            bg="white",
            anchor="w"
        )
        self.visibility_label.grid(row=1, column=1, sticky="w", pady=(5, 0))
    def _setup_hourly_tab(self):
        self.hourly_tree = ttk.Treeview(self.hourly_tab, columns=("Time", "Temp", "Wind", "Humidity"), show="headings", height=8)
        self.hourly_tree.heading("Time", text="Time")
        self.hourly_tree.heading("Temp", text="Temp (°C)")
        self.hourly_tree.heading("Wind", text="Wind (m/s)")
        self.hourly_tree.heading("Humidity", text="Humidity (%)")
        self.hourly_tree.column("Time", width=100)
        self.hourly_tree.column("Temp", width=80)
        self.hourly_tree.column("Wind", width=90)
        self.hourly_tree.column("Humidity", width=100)
        self.hourly_tree.pack(fill="both", expand=True, padx=10, pady=10)
    def _setup_alerts_tab(self):
        self.alerts_text = tk.Text(self.alerts_tab, wrap="word", font=("Segoe UI", 11), bg="white", fg="#c0392b", height=10, state="disabled", bd=0)
        self.alerts_text.pack(fill="both", expand=True, padx=10, pady=10)
        
    def get_weather(self):
        """
        Fetch weather data from Tomorrow.io API using city name (with geocoding).
        This method runs in a separate thread to prevent GUI freezing.
        """
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return
        self.weather_button.config(state=tk.DISABLED, text="Loading...")
        self.status_label.config(text="Fetching weather data...")
        self.progress.grid(row=4, column=0, columnspan=2, pady=(5, 0), sticky="ew")
        self.progress.start()
        thread = threading.Thread(target=self._fetch_weather_data, args=(city,))
        thread.daemon = True
        thread.start()

    def _fetch_weather_data(self, city):
        """
        Geocode city, then fetch weather from Tomorrow.io API.
        """
        try:
            # Step 1: Geocode city name to lat/lon
            geo_url = f"https://nominatim.openstreetmap.org/search"
            geo_params = {"q": city, "format": "json", "limit": 1}
            geo_resp = requests.get(geo_url, params=geo_params, timeout=10, headers={"User-Agent": "climasense-weather-app"})
            geo_resp.raise_for_status()
            geo_data = geo_resp.json()
            if not geo_data:
                self.root.after(0, self._show_error, "City not found. Try again.")
                return
            lat = geo_data[0]["lat"]
            lon = geo_data[0]["lon"]
            display_name = geo_data[0]["display_name"].split(",")[0]
            # Step 2: Fetch weather from Tomorrow.io
            params = {
                "location": f"{lat},{lon}",
                "apikey": self.api_key,
                "units": "metric"
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            weather_data = response.json()
            self.root.after(0, self._update_weather_display, weather_data, display_name)
        except requests.exceptions.RequestException:
            self.root.after(0, self._show_error, "Network error. Please check your internet connection.")
        except Exception as e:
            self.root.after(0, self._show_error, f"An error occurred: {str(e)}")

    def _load_animated_icon(self, icon_code):
        """Load and animate GIF icon for the given weather code."""
        import os
        icon_path = os.path.join('icons', f'{icon_code}.gif')
        if not os.path.exists(icon_path):
            return None  # Fallback to emoji
        try:
            frames = []
            frame_idx = 0
            while True:
                frame = tk.PhotoImage(file=icon_path, format=f'gif -index {frame_idx}')
                frames.append(frame)
                frame_idx += 1
        except Exception:
            pass  # End of frames
        if not frames:
            return None
        return frames

    def _animate_icon(self, frames, idx=0):
        if not frames:
            return
        frame = frames[idx]
        self.weather_icon_label.config(image=frame)
        self.weather_icon_label.image = frame  # type: ignore
        next_idx = (idx + 1) % len(frames)
        self.icon_anim = self.root.after(100, self._animate_icon, frames, next_idx)

    def _stop_icon_animation(self):
        if self.icon_anim:
            self.root.after_cancel(self.icon_anim)
            self.icon_anim = None
        self.weather_icon_label.config(image='')
        self.weather_icon_label.image = None  # type: ignore

    def _update_weather_display(self, weather_data, city_name):
        """
        Update the UI with weather information from Tomorrow.io and fade in the card.
        Also update the Hourly and Alerts tabs.
        """
        try:
            # Parse current weather
            minutely = weather_data.get("timelines", {}).get("minutely", [])
            current = minutely[0].get("values", {}) if minutely else {}
            if not current:
                self._show_error("Weather data unavailable.")
                return
            temp = current.get("temperature", "--")
            wind_speed = current.get("windSpeed", "--")
            humidity = current.get("humidity", "--")
            description = "See details below"
            # Animated icon fallback
            self._stop_icon_animation()
            self.weather_icon_label.config(text="🌤️", image="")
            self.city_info_label.config(text=city_name)
            self.temp_label.config(text=f"{temp}°C")
            self.desc_label.config(text=f"Weather: {description}")
            self.humidity_label.config(text=f"💧 Humidity: {humidity}%")
            self.wind_label.config(text=f"💨 Wind: {wind_speed} m/s")
            self.pressure_label.config(text=f"🌡️ Pressure: -- hPa")
            self.visibility_label.config(text=f"👁️ Visibility: -- km")
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.status_label.config(
                text=f"Last updated: {timestamp} | {city_name}",
                fg="#27ae60"
            )
            # Fade-in animation for weather card
            self._fade_in(self.weather_card)
            # --- Update Hourly Tab ---
            self.hourly_tree.delete(*self.hourly_tree.get_children())
            hourly = weather_data.get("timelines", {}).get("hourly", [])
            for entry in hourly[:12]:
                values = entry.get("values", {})
                t = entry.get("time", "--")[11:16]
                temp = values.get("temperature", "--")
                wind = values.get("windSpeed", "--")
                hum = values.get("humidity", "--")
                self.hourly_tree.insert("", "end", values=(t, temp, wind, hum))
            # --- Update Alerts Tab ---
            self.alerts_text.config(state="normal")
            self.alerts_text.delete("1.0", tk.END)
            alerts = weather_data.get("alerts", [])
            if alerts:
                for alert in alerts:
                    self.alerts_text.insert(tk.END, f"{alert.get('event', 'Alert')}: {alert.get('description', '')}\n\n")
            else:
                self.alerts_text.insert(tk.END, "No weather alerts.")
            self.alerts_text.config(state="disabled")
        except Exception as e:
            self._show_error(f"Error parsing weather data: {str(e)}")
        finally:
            self._reset_ui_state()
            
    def _show_error(self, message):
        """
        Display error message to user.
        
        Args:
            message (str): Error message to display
        """
        self.status_label.config(text=message, fg="#e74c3c")
        self._reset_ui_state()
        
    def _reset_ui_state(self):
        """Reset UI elements to their default state."""
        self.weather_button.config(state=tk.NORMAL, text="Get Weather")
        self.progress.stop()
        self.progress.grid_remove()

    def _fade_in(self, widget, alpha=0):
        """Fade in a widget by gradually increasing its opacity (simulated)."""
        # Tkinter does not support true alpha for widgets, so simulate with bg color
        if alpha > 1:
            return
        bg = self._blend_color("#eaf6fb", "#ffffff", alpha)
        widget.configure(bg=bg)
        for child in widget.winfo_children():
            try:
                child.configure(bg=bg)
            except:
                pass
        self.root.after(20, lambda: self._fade_in(widget, alpha + 0.05))
    def _blend_color(self, c1, c2, alpha):
        """Blend two hex colors by alpha (0-1)."""
        c1 = c1.lstrip('#'); c2 = c2.lstrip('#')
        r1, g1, b1 = int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
        r2, g2, b2 = int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)
        r = int(r1 + (r2 - r1) * alpha)
        g = int(g1 + (g2 - g1) * alpha)
        b = int(b1 + (b2 - b1) * alpha)
        return f'#{r:02x}{g:02x}{b:02x}'

def main():
    """
    Main function to run the Enhanced Weather App.
    """
    # Create the main window
    root = tk.Tk()
    
    # Set window icon (optional)
    try:
        root.iconbitmap('weather_icon.ico')
    except:
        pass  # Icon file not found, continue without it
    
    # Create and run the weather app
    app = EnhancedWeatherApp(root)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main() 