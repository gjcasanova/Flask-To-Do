"""Models module."""

# Flask
from flask_login import UserMixin

# Local applications
from .plugins import db


class User(UserMixin, db.Model):
    """
    User.

    User model to authentication and authorization tasks.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)


class List(db.Model):
    """
    List.

    Model to representate a list of tasks. Each list is related with its owner and 
    it can have many tasks.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    details = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('lists', lazy=True))


class Task(db.Model):
    """
    Task.

    Model to representate a task. Each task is related with a list.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    details = db.Column(db.Text)
    is_finished = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
    list = db.relationship('List', backref=db.backref('tasks', lazy=True))
