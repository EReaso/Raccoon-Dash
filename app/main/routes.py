import json
import os
import socket

import simple_websocket
from flask import render_template, request, redirect

from app.extensions import sock
from app.main import bp


@bp.route('/', methods=["GET", "POST"])
def admin():
	if request.method == "GET":
		with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'config.json')) as f:
			config = json.load(f)

		# Pagination
		page = request.args.get('page', 1, type=int)
		per_page = 24  # 6x4 grid

		# Get all photos
		all_photos = ["/photo/" + name + "/" for name in os.listdir(config['upload'])]
		total_photos = len(all_photos)

		# Calculate total pages
		total_pages = (total_photos + per_page - 1) // per_page

		# Ensure page is within bounds
		page = min(max(1, page), total_pages) if total_pages > 0 else 1

		# Get photos for current page
		start_idx = (page - 1) * per_page
		end_idx = start_idx + per_page
		photos = all_photos[start_idx:end_idx]
		return render_template("admin/admin.html",
		                       config=config,
		                       photos=photos,
		                       page=page,
		                       total_pages=total_pages)
	else:
		# Handle POST request
		with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'config.json')) as f:
			config = json.load(f)

		# Update config with form data
		config['calendar'] = request.form.get('calendar', config['calendar'])
		config['upload'] = request.form.get('upload_folder', config['upload'])
		config['weather_loc'] = request.form.get('zip_code', config['weather_loc'])
		config['screensaver_delay'] = int(request.form.get('screensaver_delay', config['screensaver_delay']))
		config['screensaver_rotate_delay'] = int(
			request.form.get('screensaver_rotate_delay', config['screensaver_rotate_delay']))

		# Handle image upload if present
		if "photo" in request.files:
			photo = request.files["photo"]
			if photo.filename:
				upload_path = os.path.join(config["upload"], photo.filename)
				photo.save(upload_path)

		# Save updated config
		with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'config.json'), 'w') as f:
			json.dump(config, f, indent=4)

		return redirect('/')


@bp.route('/display/')
def index():
	with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'config.json')) as f:
		config = json.load(f)
	q_string = config["calendar"]
	weather_api_key = config["weather_api_key"]
	weather_loc = config["weather_loc"]
	hostname = socket.gethostname()
	return render_template('display.html',
	                       calendar_q_string=q_string,
	                       weather_api_key=weather_api_key,
	                       weather_loc=weather_loc,
	                       screensaver_delay=config['screensaver_delay'],
	                       hostname=hostname)


socks = []


@sock.route('/reload/')
def reload_socket(ws):
	socks.append(ws)
	while True:
		message = ws.receive()
		if message == "reload":
			# Broadcast reload command to all connected clients
			ws.send("reload")
	socks.remove(ws)


@bp.route('/trigger-reload/', methods=['GET', 'POST'])
def trigger_reload():
	for sock in socks:
		try:
			sock.send('reload')
		except simple_websocket.errors.ConnectionClosed:
			socks.remove(sock)
			continue
	return 'Reload triggered', 200
