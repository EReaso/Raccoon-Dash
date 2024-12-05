import json

from flask import render_template

from app.main import bp


@bp.route('/')
def index():
	with open('/config.json') as f:
		config = json.load(f)
	q_string = config["calendar"]
	weather_api_key = config["weather_api_key"]
	weather_loc = config["weather_loc"]
	return render_template('display.html', calendar_q_string=q_string, weather_api_key=weather_api_key,
	                       weather_loc=weather_loc)
