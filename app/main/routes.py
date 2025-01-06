import json
import os
import socket

from flask import render_template, request, redirect

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

		return render_template("admin.html",
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
		config['screensaver_rotate_delay'] = int(request.form.get('screensaver_rotate_delay', config['screensaver_rotate_delay']))
		
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
	local_ip = socket.gethostbyname(hostname)
	return render_template('display.html',
	                      calendar_q_string=q_string,
	                      weather_api_key=weather_api_key,
	                      weather_loc=weather_loc,
	                      local_ip=local_ip,
	                      screensaver_delay=config['screensaver_delay'])
