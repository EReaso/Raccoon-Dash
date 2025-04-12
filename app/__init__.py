from flask import Flask

from .config import Config

app = Flask(__name__)

app.config.from_object(Config)

from app.extensions import sock

sock.init_app(app)

from app.main import bp as main_bp
from app.main.theme import theme_bp

app.register_blueprint(main_bp)
app.register_blueprint(theme_bp)

from app.weather import bp as weather_bp

app.register_blueprint(weather_bp)

from app.photos import bp as photos_bp

app.register_blueprint(photos_bp)

from app.my_calendar import bp as calendar_bp

app.register_blueprint(calendar_bp)
