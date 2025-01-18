import json
import os
import re
import uuid

from flask import request, render_template, send_file
from werkzeug.utils import secure_filename

from app.photos import bp


@bp.route("/photos/", methods=["POST"])
def upload_photos():
	with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'config.json')) as f:
		config = json.load(f)
	files = request.files.getlist('photo')
	for f in files:
		if f.filename == '':
			continue

		# Get base name and extension separately
		base_name = os.path.splitext(secure_filename(f.filename))[0]
		ext = os.path.splitext(f.filename)[1].lower()  # Lowercase extension

		# Clean the base name further - only allow alphanumeric and underscore
		base_name = re.sub(r'[^a-zA-Z0-9_]', '', base_name)

		# Generate URL-safe unique filename
		unique_suffix = uuid.uuid4().hex[:10]
		filename = f"{base_name}_{unique_suffix}{ext}"

		f.save(os.path.join(config['upload'], filename))
	return "204 OK"


@bp.route("/photo/<path:path>/", methods=["GET"])
def serve_photo(path):
	with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'config.json')) as f:
		config = json.load(f)
	print(path)
	return send_file(os.path.join(config['upload'], path))


@bp.route("/photo/<path:path>/", methods=["DELETE"])
def delete_photo(path):
	with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'config.json')) as f:
		config = json.load(f)
	os.remove(os.path.join(config['upload'], path))
	return "204 OK"


@bp.route("/screensaver/", methods=["GET"])
def screensaver():
	with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'config.json')) as f:
		config = json.load(f)
	images = os.listdir(config["upload"])
	return render_template("screensaver.html", images=images, delay=config["screensaver_rotate_delay"])
