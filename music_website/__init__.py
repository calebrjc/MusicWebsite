"""This package contains the glue logic that MusicWebsite needs to run."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from music_website.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "login"

__all__ = ["app", "db"]

from music_website import routes, models  # noqa: F401, E402
