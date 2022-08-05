"""Plugins module."""

# Flask
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Local application
from .config import Config
from .views import tasks_urls


def create_app(config_class):
    """Create and return a Flask instance."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    return app


def create_database(flask_app):
    """Create and return a database instance."""
    db = SQLAlchemy(flask_app)
    db.init_app(flask_app)
    db.create_all()
    return db


def create_login_manager(flask_app):
    """Create and return a login manager instance."""
    login_manager = LoginManager()
    login_manager.login_view = 'tasks.sign_in'
    login_manager.init_app(flask_app)

    @login_manager.user_loader
    def load_user(user_id):
        """Define a function required for Flask-Login."""
        from .models import User  # noqa
        return User.query.get(int(user_id))

    return login_manager


def register_blueprints(flask_app, blueprints):
    """Register the blueprints in the application."""
    for url_prefix, blueprint in blueprints.items():
        flask_app.register_blueprint(blueprint, url_prefix=url_prefix)


def set_cors():
    """Set CORS in the application."""
    pass


def setup(class_config):
    """Run the setup for the application."""
    app = create_app(class_config)
    db = create_database(app)
    create_login_manager(app)
    register_blueprints(app, urls)
    return app, db


urls = {
    '/app/': tasks_urls,
}

app, db = setup(Config)
