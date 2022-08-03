"""App package."""

# Flask
from flask import Flask

# Local application
from .config import Config


def create_app():
    """Create, set and return a Flask instance."""
    app = Flask(__name__)
    app.config.from_object(Config)
    return app
