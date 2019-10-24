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


def main():
    if len(sys.argv) != 2:
        exit(f"Usage: {sys.argv[0]} location")

    location = sys.argv[1]
    api_key = get_api_key()

    result = get_weather(api_key, location)

    code = result["cod"]
    if code != 200:
        exit(f"Code {code}: {result['message']}")

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(result)

    print(f"Current conditions in {location}, ", end="")
    print(f"{result['sys']['country']}: ", end="")
    print(f"{result['weather'][0]['description'].capitalize()}, ", end="")
    print(f"{result['main']['temp']}C.")

    result = get_forecast(api_key, location)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(result)

if __name__ == "__main__":
    main()
