'''
Library imports for the app
'''
import sys
import requests
import pyowm
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from QtPy import QtCore, QtGui, QtWidgets
from geopy.geocoders import Nominatim

class WeatherApp(QWidget):
    """
    Main class for the weather application.
    """

    def __init__(self):
        """
        Initializes the weather app widget.
        """
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setGeometry(300, 300, 300, 200)

        # Labels for weather data
        self.location_label = QLabel("Location:")
        self.min_temp_label = QLabel("Min Temperature:")
        self.max_temp_label = QLabel("Max Temperature:")
        self.uv_index_label = QLabel("UV Index:")
        self.wind_speed_label = QLabel("Wind Speed:")
        self.storm_warnings_label = QLabel("Storm Warnings:")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.location_label)
        layout.addWidget(self.min_temp_label)
        layout.addWidget(self.max_temp_label)
        layout.addWidget(self.uv_index_label)
        layout.addWidget(self.wind_speed_label)
        layout.addWidget(self.storm_warnings_label)

        self.setLayout(layout)

    def update_weather_data(self, location):
        """
        Updates weather data based on the given location.

        Args:
            location (str): The city or region to fetch weather data for.
        """
        api_key = "7d9ef15ae8db3f8c2ab4448cbd2efe8b"  # Replace with your actual API key

        # Create an OpenWeatherMap client
        owm = pyowm.OWM('617074221fda70c92dfe63c06b1ddf6a')

        # Retrieve weather data for the specified location
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(location)
        weather = observation.weather

        # Extract weather data
        location = weather.location_string
        min_temp = weather.temperature('celsius')['temp_min']
        max_temp = weather.temperature('celsius')['temp_max']
        uv_index = weather.uv_index
        wind_speed = weather.wind()['speed']
        storm_warnings = weather.detailed_status if weather.has_storm else "No storm warnings"

        # Update labels with the retrieved data
        self.location_label.setText(f"Location: {location}")
        self.min_temp_label.setText(f"Min Temperature: {min_temp} °C")
        self.max_temp_label.setText(f"Max Temperature: {max_temp} °C")
        self.uv_index_label.setText(f"UV Index: {uv_index}")
        self.wind_speed_label.setText(f"Wind Speed: {wind_speed} m/s")
        self.storm_warnings_label.setText(f"Storm Warnings: {storm_warnings}")

def get_location():
    """
    Retrieves the user's current location using geopy.

    Returns:
        str: The user's location as a string.
    """
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.reverse(geolocator.geocode("my location")).address
    return location

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    location = get_location()
    window.update_weather_data(location)
    window.show()
    sys.exit(app.exec_())