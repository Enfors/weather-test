#!/usr/bin/env python3

from yahoo_weather.weather import YahooWeather
from yahoo_weather.config.units import Unit


def read_private_data(filename: str):
    with open(f"private/{filename}", "r") as f:
        return f.readline().strip()

app_id = read_private_data("app_id")
api_key = read_private_data("client_id")
api_secret = read_private_data("client_secret")


data = YahooWeather(APP_ID=app_id,
                    api_key=api_key,
                    api_secret=api_secret)

data.get_yahoo_weather_by_city("Stockholm", Unit.celsius)

print(data.condition.text)
print(data.condition.temperature)
