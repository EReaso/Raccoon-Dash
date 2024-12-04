import os

from flask import current_app as app
from flask import request, render_template, send_from_directory, redirect
from werkzeug.utils import secure_filename

from app.photos import bp


@bp.route("/photos/", methods=["GET"])
def photo_gallery():
	photos = ["/photo/" + name + "/" for name in os.listdir(app.config['UPLOAD'])]
	return render_template("gallery.html", photos=photos)


@bp.route("/photos/", methods=["POST"])
def upload_photo():
	current_files = os.listdir(app.config['UPLOAD'])
	files = request.files.getlist('photo')
	for f in files:
		if f.filename == '':
			continue
		if secure_filename(f.filename) in current_files:
			filename = secure_filename(f.filename + os.urandom(5).decode('ascii'))
			f.save(os.path.join(app.config['UPLOAD'], filename))
		else:
			filename = secure_filename(f.filename)
			f.save(os.path.join(app.config['UPLOAD'], filename))
	return redirect("/photos/")


@bp.route("/photo/<path:photo>/", methods=["GET"])
def serve_photo(photo):
	return send_from_directory(app.config['UPLOAD'], photo)


@bp.route("/photo/<path:photo>/", methods=["DELETE"])
def delete_photo(photo):
	os.remove(os.path.join(app.config['UPLOAD'], photo))
	return "204 OK"


@bp.route("/screensaver/", methods=["GET"])
def serve_screensaver():
	global total_images
	total_images = len(request.args.get("path"))
	return render_template("screensaver.html", total_images=total_images)


@bp.route("/screensaver/image/", methods=["GET"])
def screensaver_image():
	num = request.args.get("num", default=0, type=int)
	if int(num) < 0 or int(num) >= total_images:
		num = num % num

	return send_from_directory(app.config['UPLOAD'], f"/photo/{os.listdir(app.config['UPLOAD'])[int(num)]}/")
