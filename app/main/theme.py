import os
from pathlib import Path

import sass
from flask import Blueprint, request, current_app, redirect, url_for, flash, abort

from app.main.routes import trigger_reload

theme_bp = Blueprint('theme', __name__)


@theme_bp.route('/font_url/', methods=['GET'])
def get_current_font_url():
	"""Extract the font URL from the generated variables.scss file, if it exists."""
	variables_file = initialize_theme_dir() / "variables.scss"
	if not variables_file.exists():
		return abort(404)
	with open(variables_file, "r") as f:
		for line in f:
			if line.strip().startswith("@import url("):
				start = line.find('"') + 1
				end = line.rfind('"')
				return line[start:end]
	return abort(404)


def initialize_theme_dir():
	"""Ensure theme_dir exists within the app context."""
	theme_dir = Path(current_app.root_path) / "dynamic_assets"
	theme_dir.mkdir(parents=True, exist_ok=True)
	return theme_dir


def get_static_path(filename):
	"""Get absolute path to static files to avoid path issues."""
	return os.path.join(current_app.root_path, "static", filename)


def update_variables(color_map, font_url=None):
	"""Update variables.scss with new theme colors and optional Google Font import."""
	variables_file = initialize_theme_dir() / "variables.scss"

	font_family = None
	if font_url and font_url.startswith("https://fonts.googleapis.com"):
		# Extract font family from URL
		import re
		from urllib.parse import unquote
		match = re.search(r'family=([^:&]+)', font_url)
		if match:
			font_family = unquote(match.group(1)).replace('+', ' ')

	with open(variables_file, "w") as f:
		if font_family:
			# Inject @import and font-family override
			f.write(f'@import url("{font_url}");\n')
			f.write(f'$font-family-base: "{font_family}", sans-serif;\n\n')

		f.write("$custom-theme-colors: (\n")
		for index, (key, value) in enumerate(color_map.items()):
			comma = "," if index < len(color_map) - 1 else ""
			f.write(f'  "{key}": {value}{comma}\n')
		f.write(");\n")


def compile_sass():
	try:
		main_scss = get_static_path("scss/main.scss")
		compiled_css = sass.compile(filename=main_scss, output_style='compressed')
		css_file = initialize_theme_dir() / "compiled.css"
		with open(css_file, "w") as f:
			f.write(compiled_css)
	except Exception as e:
		return e
	else:
		return compiled_css


@theme_bp.route("/update-theme/", methods=["POST"])
def update_theme():
	"""Handle theme updates from the settings form."""
	try:
		theme_colors = {key[6:]: value for key, value in request.form.items() if key.startswith("color_")}
		font_url = request.form.get("font_family", None)

		update_variables(theme_colors, font_url)
		compile_sass()
	except Exception as e:
		flash(str(e))
	else:
		flash("Success!")
		trigger_reload()
	finally:
		return redirect(url_for("main.admin"))


@theme_bp.route("/style/", methods=["GET"])
def get_compiled_css():
	"""Serve the compiled CSS file with the correct MIME type."""
	css_file = initialize_theme_dir() / "compiled.css"
	if css_file.exists():
		with open(css_file, "r") as f:
			return f.read(), 200, {"Content-Type": "text/css"}
	else:
		return abort(404)
