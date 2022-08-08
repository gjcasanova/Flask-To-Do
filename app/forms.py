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

    username = wtforms.StringField('Username', validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField('Password')
    submit = wtforms.SubmitField('Submit')


class ListForm(FlaskForm):
    """
    ListForm.

    Provide a form to create and update a list.
    """

    name = wtforms.StringField('Name', validators=[wtforms.validators.DataRequired()])
    details = wtforms.StringField('Details')
    submit = wtforms.SubmitField('Submit')


class TaskForm(FlaskForm):
    """
    TaskForm.

    Provide a form to create and update a task.
    """

    name = wtforms.StringField('Name', validators=[wtforms.validators.DataRequired()])
    details = wtforms.StringField('Details')
    due_date = wtforms.DateTimeField('Due date', validators=[wtforms.validators.Optional()])
    is_finished = wtforms.BooleanField('Finished')
    submit = wtforms.SubmitField('Submit')
