"""Config module."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


class Config:
    """
    Config.

    Settings to App package.
    """

    ENV = 'development'
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'eHSgKycMopOvwFRxUzcXckyBo0Gp4C66'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'database.sqlite'}"
