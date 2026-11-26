import json
import pandas as pd
import csv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Install ChromeDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Get the World Weather website
driver.get("https://www.timeanddate.com/weather/")

# Find all the weather table rows
weather_rows = driver.find_elements(By.CSS_SELECTOR, ".tad-table__mobile-scroll table tbody tr")

# Create an empty list to store the scraped weather data
results = []

# Loop through each weather table row
for weather in weather_rows:

    # Extract weather conditions, temperature, and wind speed
    try: 

        condition = weather.find_element(By.CSS_SELECTOR, "span.tad-weather-table__conditions-text").get_property("textContent")
        temperature = weather.find_element(By.CSS_SELECTOR, "td.tad-weather-table__temperature-cell").text
        wind = weather.find_element(By.CSS_SELECTOR, "div.tad-weather-table__wind-cell-inner").text

    # Handle missing weather elements and retain the city record when weather measurements are unavailable
    except NoSuchElementException:
        condition = 'Weather data unavailable'
        temperature = None
        wind = None

    # Extract the city, country, and local time
    city = weather.find_element(By.CSS_SELECTOR, "td.tad-weather-table__city-cell")
    country = weather.find_element(By.CSS_SELECTOR, "td.tad-weather-table__country-cell")
    time = weather.find_element(By.CSS_SELECTOR, "span.tad-weather-table__row-time-value")

    # Create Weather Dictionary
    weather_dict = {
        "City": city.text ,
        "Country": country.text,
        "Condition": condition, 
        "Temperature": temperature,
        "Wind": wind,
        "Time": time.text
    }

    # Append each city's weather dictionary to the results list
    results.append(weather_dict)

# Convert weather data into DataFrame
df = pd.DataFrame(results)

# Save raw weather data to CSV
df.to_csv("weather_raw.csv", index=False)

# Close the browser
driver.quit()

