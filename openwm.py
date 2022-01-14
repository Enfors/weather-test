#!/usr/bin/env python3

import configparser
import requests
import sys

import datetime

base_url = "https://api.openweathermap.org/data/2.5/"


def get_api_key():
    config = configparser.ConfigParser()
    config.read("/home/enfors/.weather.conf")
    return config["openweathermap"]["api"]


def get_weather(api_key, location):
    url = f"{base_url}weather?q={location}&units=metric&appid={api_key}"
    r = requests.get(url)
    return r.json()


def get_forecast(api_key, location):
    url = f"{base_url}forecast?q={location}&units=metric&appid={api_key}"
    r = requests.get(url)
    return r.json()


def format_direction(degrees):
    cardinals = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
    return cardinals[int((degrees + 22.5) / 45)]


def format_item(data, timestamp):
    disp = ""

    disp += datetime.datetime.fromtimestamp(timestamp).\
        strftime("%Y-%m-%d %H:%M: ")
    disp += f"{data['weather'][0]['description'].capitalize():16s} "
    disp += f"{int(data['main']['temp']):3d} C   wind "
    wind = data["wind"]
    disp += f"{format_direction(wind['deg'])} at "
    disp += f"{int(wind['speed'] + 0.5)} m/s."

    return disp


def format_item_briefly(data):
    disp = ""

    disp += f"{data['weather'][0]['description'].capitalize()}, "
    disp += f"{int(data['main']['temp'])} C"

    return disp


def get_current_formatted_briefly(location: str):
    api_key = get_api_key()
    data = get_weather(api_key, location)
    return format_item_briefly(data)


def main():
    if len(sys.argv) != 2:
        exit(f"Usage: {sys.argv[0]} location")

    location = sys.argv[1].capitalize()
    api_key = get_api_key()

    forecast = get_forecast(api_key, location)

    code = forecast["cod"]
    if code != "200":
        exit(f"Code {code}: {forecast['message']}")

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(forecast)

    current = get_weather(api_key, location)

    print(f"=== Current conditions in {location}, " +
          f"{current['sys']['country']} ===")

    print(format_item(current, int(current["dt"])))

    print(f"=== Forecast ===")
    for item in forecast["list"]:
        print(format_item(item, int(item["dt"])))

    print(get_current_formatted_briefly("karlstad"))


if __name__ == "__main__":
    main()
