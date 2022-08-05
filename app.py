"""App module."""

# Local application
from app.plugins import app

if __name__ == '__main__':
    app.run(debug=True)
