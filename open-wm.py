#!/usr/bin/env python3

import configparser
import requests
import sys
import pprint

base_url = "https://api.openweathermap.org/data/2.5/"


def get_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["openweathermap"]["api"]


def get_weather(api_key, location):
    url = f"{base_url}weather?q={location}&units=metric&appid={api_key}"
    r = requests.get(url)
    return r.json()


def get_forecast(api_key, location):
    url = f"{base_url}forecast?q={location}&units=metric&appid={api_key}"
    r = requests.get(url)
    return r.json()


def format_forecast_item(data):
    disp = ""

    disp += f"{data['dt_txt']}: "
    disp += f"{data['weather'][0]['description'].capitalize()}, "
    disp += f"{int(data['main']['temp'])} C."

    return disp


def main():
    if len(sys.argv) != 2:
        exit(f"Usage: {sys.argv[0]} location")

    location = sys.argv[1].capitalize()
    api_key = get_api_key()

    forecast = get_forecast(api_key, location)

    code = forecast["cod"]
    if code != "200":
        exit(f"Code {code}: {forecast['message']}")

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(forecast)

    for item in forecast["list"]:
        print(format_forecast_item(item))

    current = get_weather(api_key, location)

    print(f"Current conditions in {location}, ", end="")
    print(f"{current['sys']['country']}: ", end="")
    print(f"{current['weather'][0]['description'].capitalize()}, ", end="")
    print(f"{int(current['main']['temp'])} C.")

if __name__ == "__main__":
    main()
