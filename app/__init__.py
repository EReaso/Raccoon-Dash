from flask import Flask


def create_app():
	app = Flask(__name__)

	# Initialize Flask extensions here

	# Register blueprints here
	from app.main import bp as main_bp
	app.register_blueprint(main_bp)

	from app.weather import bp as weather_bp
	app.register_blueprint(weather_bp)

	from app.photos import bp as photos_bp
	app.register_blueprint(photos_bp)

	return app
