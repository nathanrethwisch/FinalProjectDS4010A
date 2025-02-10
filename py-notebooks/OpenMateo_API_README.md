# Open-Metro Historical Weather API
## Source
- The API can be accessed at: `https://open-meteo.com/en/docs/historical-weather-api`.
- The webpage can also be used to generate code tempaltes for the request that we want.

## Project
- Climate conditions greatly influence the likeliness and severity of wildfires.
- Weather forecasts can be used to predict future threats

## Example call
```
# Coordinates of Iowa State University (as example)
lat = 42.02706
long = -93.65288

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": lat,
    "longitude": long,
    "start_date": "2025-01-25",
    "end_date": "2025-02-08",
    "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation"],
    "temperature_unit": "fahrenheit",
    "wind_speed_unit": "kn",
    "timeformat": "unixtime"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")
```