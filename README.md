# 🌤️ Live Weather App

A professional Python application that fetches real-time weather data using the OpenWeatherMap API and displays it in a user-friendly Tkinter GUI.

## 🎯 Features

- **Real-time Weather Data**: Get current weather information for any city worldwide
- **User-friendly GUI**: Clean and intuitive interface built with Tkinter
- **Error Handling**: Robust error handling for network issues and invalid inputs
- **Responsive Design**: Professional UI with proper layout and styling
- **Threading**: Non-blocking API calls for smooth user experience

## 📋 Requirements

- Python 3.6 or higher
- Internet connection for API calls
- OpenWeatherMap API key

## 🚀 Installation

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd weather-app

# Or simply download the weather_app.py file
```

### 2. Install Required Dependencies

```bash
pip install requests
```

### 3. Get OpenWeatherMap API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/)
2. Sign up for a free account
3. Go to your profile and navigate to "API keys"
4. Copy your API key
5. Replace `YOUR_API_KEY_HERE` in the `weather_app.py` file with your actual API key

```python
# In weather_app.py, line 25
self.api_key = "YOUR_ACTUAL_API_KEY_HERE"
```

## 🎮 Usage

### Running the Application

```bash
python weather_app.py
```

### How to Use

1. **Launch the App**: Run the Python script
2. **Enter City Name**: Type the name of any city in the input field
3. **Get Weather**: Click the "Get Weather" button or press Enter
4. **View Results**: The app will display:
   - Temperature in Celsius
   - Weather description
   - Humidity percentage
   - Wind speed in meters per second

### Example Usage

```
City: London
Result:
Temperature: 18°C
Weather: Partly Cloudy
Humidity: 65%
Wind Speed: 3.2 m/s
```

## 🛠️ Technical Details

### Architecture

- **GUI Framework**: Tkinter (Python's standard GUI library)
- **API Integration**: OpenWeatherMap REST API
- **HTTP Requests**: Python requests library
- **Threading**: Separate thread for API calls to prevent GUI freezing

### API Endpoint

The app uses the OpenWeatherMap Current Weather API:
```
GET http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric
```

### Error Handling

The application handles various error scenarios:
- Invalid city names
- Network connectivity issues
- API service errors
- Invalid API responses

## 🎨 UI Components

- **Window Size**: 400x300 pixels
- **Font**: Arial, 14pt for main elements
- **Color Scheme**: Professional blue and gray theme
- **Layout**: Responsive grid-based design

## 🔧 Customization

### Changing API Key

Edit line 25 in `weather_app.py`:
```python
self.api_key = "YOUR_NEW_API_KEY"
```

### Modifying Window Size

Edit line 23 in `weather_app.py`:
```python
self.root.geometry("500x400")  # Change to desired size
```

### Adding New Weather Data

To display additional weather information, modify the `_update_weather_display` method in the `WeatherApp` class.

## 🌟 Future Enhancements

### Planned Features

1. **Weather Icons**: Display weather condition icons
2. **5-Day Forecast**: Extended weather forecast functionality
3. **Unit Conversion**: Toggle between Celsius and Fahrenheit
4. **Location Services**: Automatic location detection
5. **Weather Alerts**: Severe weather notifications

### Web Application Version

The app can be converted to a Flask web application for deployment:
- Replace Tkinter with Flask web framework
- Create HTML templates for the frontend
- Deploy to cloud platforms like Heroku or AWS

## 🐛 Troubleshooting

### Common Issues

1. **"City not found" Error**
   - Check spelling of city name
   - Try using the full city name (e.g., "New York" instead of "NYC")

2. **Network Error**
   - Verify internet connection
   - Check firewall settings
   - Ensure API key is valid

3. **Import Error**
   - Install requests module: `pip install requests`
   - Ensure Python 3.6+ is installed

### API Key Issues

- **Invalid API Key**: Generate a new key from OpenWeatherMap
- **API Limit Exceeded**: Free tier allows 60 calls/minute
- **Key Not Activated**: New keys may take a few hours to activate

## 📝 Code Structure

```
weather_app.py
├── WeatherApp Class
│   ├── __init__() - Initialize application
│   ├── setup_ui() - Create GUI components
│   ├── get_weather() - Main weather fetching method
│   ├── _fetch_weather_data() - API call in separate thread
│   ├── _update_weather_display() - Update UI with weather data
│   ├── _show_error() - Display error messages
│   └── _reset_ui_state() - Reset UI to default state
└── main() - Application entry point
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for providing the weather API
- Python community for excellent documentation and libraries
- Tkinter for the GUI framework

## 📞 Support

For issues, questions, or suggestions:
- Create an issue in the repository
- Contact the development team
- Check the troubleshooting section above

---

**Happy Weather Tracking! 🌤️** 