"""Forms module."""

# Third party
import wtforms
# Flask
from flask_wtf import FlaskForm


class SignInForm(FlaskForm):
    """
    SignInForm.

    Provide a form to sign in with username and password.
    """

    username = wtforms.StringField('username', validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField('password')
    submit = wtforms.SubmitField('submit')


class ListForm(FlaskForm):
    """
    ListForm.

    Provide a form to create and update a list.
    """

    name = wtforms.StringField('name', validators=[wtforms.validators.DataRequired()])
    details = wtforms.StringField('details')
    submit = wtforms.SubmitField('submit')


class TaskForm(FlaskForm):
    """
    TaskForm.

    Provide a form to create and update a task.
    """

    name = wtforms.StringField('name', validators=[wtforms.validators.DataRequired()])
    details = wtforms.StringField('details')
    due_date = wtforms.DateTimeField('due date', validators=[wtforms.validators.Optional()])
    submit = wtforms.SubmitField('submit')
