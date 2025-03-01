import json
import os
from itertools import groupby

import requests
import tzlocal
from arrow import Arrow
from flask import render_template
from ics import Calendar, Event

from . import bp


@bp.app_template_filter("zfill")
def zfill_filter(value, width=2):
	"""Zero-fill a number to the specified width."""
	return str(value).zfill(width)


@bp.route('/calendar/agenda/', methods=['GET'])
def agenda():
	with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'config.json')) as f:
		config = json.load(f)
	response = requests.get(url=config['calendar'])
	calendar = Calendar(response.text)

	# Get the correct local timezone
	local_tz = tzlocal.get_localzone()

	# Ensure 'now' is in the local timezone
	now = Arrow.now().to(local_tz)

	# If no events today, add an all-day event
	if not any(event.begin.to(local_tz).date() == now.date() for event in calendar.events):
		ev = Event(name="No Events Today", begin=now.date())  # All-day event
		ev.make_all_day()
		calendar.events.add(ev)

	# Convert events to local timezone and filter
	events = []
	for event in calendar.events:
		event.begin = event.begin.to(local_tz)
		event.end = event.end.to(local_tz)

		if event.end > now.shift(days=-3):  # Using Arrow's shift() instead of timedelta
			events.append(event)

	# Sort events by date (groupby requires sorted data)
	events_sorted = sorted(events, key=lambda event: event.begin.date())

	# Group events by date
	days = ((date, list(group)) for date, group in groupby(events_sorted, key=lambda event: event.begin.date()))

	weekdays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
	months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Dec")

	return render_template("calendar/agenda/agenda.html", days=days, now=now, weekdays=weekdays, months=months)
