"""
Live Weather App
A Python application that fetches real-time weather data using OpenWeatherMap API
and displays it in a user-friendly Tkinter GUI.

Author: Weather App Developer
Version: 1.0
"""

import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json
from datetime import datetime
import threading

class WeatherApp:
    def __init__(self, root):
        """
        Initialize the Weather App with main window and components.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Live Weather App")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # API Configuration
        self.api_key = "YOUR_API_KEY_HERE"  # Replace with your OpenWeatherMap API key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        # Create and configure the main frame
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights for responsive layout
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface components."""
        
        # Title Label
        title_label = tk.Label(
            self.main_frame,
            text="🌤️ Live Weather App",
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # City Input Section
        city_label = tk.Label(
            self.main_frame,
            text="Enter City Name:",
            font=("Arial", 14),
            fg="#34495e"
        )
        city_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        self.city_entry = tk.Entry(
            self.main_frame,
            font=("Arial", 14),
            width=20,
            relief=tk.SOLID,
            bd=1
        )
        self.city_entry.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        self.city_entry.focus()
        
        # Bind Enter key to get weather
        self.city_entry.bind('<Return>', lambda event: self.get_weather())
        
        # Get Weather Button
        self.weather_button = tk.Button(
            self.main_frame,
            text="Get Weather",
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white",
            relief=tk.FLAT,
            padx=20,
            command=self.get_weather
        )
        self.weather_button.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        
        # Weather Display Frame
        self.weather_frame = tk.Frame(self.main_frame, relief=tk.GROOVE, bd=2)
        self.weather_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Weather Information Labels
        self.temp_label = tk.Label(
            self.weather_frame,
            text="Temperature: --",
            font=("Arial", 14),
            fg="#2c3e50",
            anchor="w"
        )
        self.temp_label.pack(fill="x", padx=10, pady=5)
        
        self.desc_label = tk.Label(
            self.weather_frame,
            text="Weather: --",
            font=("Arial", 14),
            fg="#2c3e50",
            anchor="w"
        )
        self.desc_label.pack(fill="x", padx=10, pady=5)
        
        self.humidity_label = tk.Label(
            self.weather_frame,
            text="Humidity: --",
            font=("Arial", 14),
            fg="#2c3e50",
            anchor="w"
        )
        self.humidity_label.pack(fill="x", padx=10, pady=5)
        
        self.wind_label = tk.Label(
            self.weather_frame,
            text="Wind Speed: --",
            font=("Arial", 14),
            fg="#2c3e50",
            anchor="w"
        )
        self.wind_label.pack(fill="x", padx=10, pady=5)
        
        # Status Label
        self.status_label = tk.Label(
            self.main_frame,
            text="Enter a city name and click 'Get Weather'",
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        self.status_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        # Progress Bar (hidden by default)
        self.progress = ttk.Progressbar(
            self.main_frame,
            mode='indeterminate'
        )
        
    def get_weather(self):
        """
        Fetch weather data from OpenWeatherMap API.
        This method runs in a separate thread to prevent GUI freezing.
        """
        city = self.city_entry.get().strip()
        
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return
            
        # Update UI to show loading state
        self.weather_button.config(state=tk.DISABLED, text="Loading...")
        self.status_label.config(text="Fetching weather data...")
        self.progress.grid(row=6, column=0, columnspan=2, pady=(5, 0), sticky="ew")
        self.progress.start()
        
        # Run API call in separate thread
        thread = threading.Thread(target=self._fetch_weather_data, args=(city,))
        thread.daemon = True
        thread.start()
        
    def _fetch_weather_data(self, city):
        """
        Fetch weather data from API (runs in separate thread).
        
        Args:
            city (str): City name to fetch weather for
        """
        try:
            # Prepare API request parameters
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            # Make API request
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse JSON response
            weather_data = response.json()
            
            # Update UI with weather data (must be done in main thread)
            self.root.after(0, self._update_weather_display, weather_data)
            
        except requests.exceptions.RequestException as e:
            error_msg = "Network error. Please check your internet connection."
            self.root.after(0, self._show_error, error_msg)
        except json.JSONDecodeError:
            error_msg = "Invalid response from weather service."
            self.root.after(0, self._show_error, error_msg)
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            self.root.after(0, self._show_error, error_msg)
            
    def _update_weather_display(self, weather_data):
        """
        Update the UI with weather information.
        
        Args:
            weather_data (dict): Weather data from API
        """
        try:
            # Extract weather information
            temp = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']
            description = weather_data['weather'][0]['description'].title()
            city_name = weather_data['name']
            country = weather_data['sys']['country']
            
            # Update labels with weather data
            self.temp_label.config(text=f"Temperature: {temp}°C")
            self.desc_label.config(text=f"Weather: {description}")
            self.humidity_label.config(text=f"Humidity: {humidity}%")
            self.wind_label.config(text=f"Wind Speed: {wind_speed} m/s")
            
            # Update status
            self.status_label.config(
                text=f"Weather data for {city_name}, {country} - Updated at {datetime.now().strftime('%H:%M:%S')}",
                fg="#27ae60"
            )
            
        except KeyError as e:
            self._show_error("City not found. Try again.")
        except Exception as e:
            self._show_error(f"Error parsing weather data: {str(e)}")
        finally:
            # Reset UI state
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

def main():
    """
    Main function to run the Weather App.
    """
    # Create the main window
    root = tk.Tk()
    
    # Set window icon (optional)
    try:
        root.iconbitmap('weather_icon.ico')
    except:
        pass  # Icon file not found, continue without it
    
    # Create and run the weather app
    app = WeatherApp(root)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main() 