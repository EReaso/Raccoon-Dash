import datetime
import json
import os

import requests
from flask import render_template

from app.weather import bp


class WeatherFetchError(Exception):
	pass


def get_weather(city, api_key):
	"""Fetches weather data for the next 3 days and formats it."""
	base_url = "https://api.weatherapi.com/v1/forecast.json?days=10&"

	complete_url = base_url + "key=" + api_key + "&q=" + city
	response = requests.get(complete_url)

	if response.status_code == 200:
		data = response.json()

		forecast_data = []
		for i in range(0, len(data["forecast"]["forecastday"])):
			day_data = data["forecast"]["forecastday"][i]["day"]
			temp_max = day_data["maxtemp_f"]
			temp_min = day_data["mintemp_f"]
			condition_text = day_data["condition"]["text"]
			condition_icon_url = day_data["condition"]["icon"]
			date = data["forecast"]["forecastday"][i]["date"]

			forecast_data.append({
				'date': datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%m/%d"),
				'day': ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")[
					datetime.datetime.strptime(date, "%Y-%m-%d").weekday()],
				'high': temp_max,
				'low': temp_min,
				'condition_text': condition_text,
				'condition_icon_url': condition_icon_url
			})

		return forecast_data
	else:
		return WeatherFetchError(response.status_code)


@bp.route("/weather/")
def weather_route():
	with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'config.json')) as f:
		config = json.load(f)
		try:
			forecast_data = get_weather(config["weather_loc"], config["weather_api_key"])
		except WeatherFetchError:
			return render_template("weather_error.html")

	updated_time = datetime.datetime.now().strftime("%H:%M")
	return render_template("weather.html", data=forecast_data, updated_time=updated_time)
