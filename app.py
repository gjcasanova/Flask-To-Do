"""App module."""

# Local application
from app import create_app

app = create_app()


@app.route('/')
def hello_world():
    """Return a message just for testing."""
    return 'Hello world!'


if __name__ == '__main__':
    app.run(debug=True)
