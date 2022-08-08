"""App package."""

# Local application
from .config import Config


def create_app(config_class):
    """Create and return a Flask instance."""
    from flask import Flask  # noqa
    app = Flask(__name__)
    app.config.from_object(config_class)
    return app


def register_plugins(flask_app):
    """Register the plugins in the application context."""
    from .plugins import bootstrap, db, login_manager  # noqa

    # Database
    db.init_app(flask_app)
    with flask_app.app_context():
        db.create_all()
    # Login manager
    login_manager.login_view = 'tasks.sign_in'
    login_manager.init_app(flask_app)
    # Bootstrap
    bootstrap.init_app(flask_app)

    @login_manager.user_loader
    def load_user(user_id):
        """Define a function required for Flask-Login."""
        from .models import User  # noqa
        return User.query.get(int(user_id))


def register_blueprints(flask_app):
    """Register the blueprints in the application context."""
    from .views import app_routes  # noqa
    flask_app.register_blueprint(app_routes, url_prefix='/app/')


def set_cors():
    """Set CORS in the application."""
    pass


def setup(class_config):
    """Run the setup for the application."""
    flask_app = create_app(class_config)
    register_blueprints(flask_app)
    register_plugins(flask_app)
    return flask_app


app = setup(Config)
