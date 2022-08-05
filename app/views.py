"""Views module."""

# Flask
from flask import Blueprint, Response, make_response, redirect, render_template, request, url_for
from flask_login import current_user, login_user

from app.forms import ListForm, SignInForm
# from app.models import User


tasks_urls = Blueprint('tasks', __name__)


@tasks_urls.route('/sign_in/', methods=['GET', 'POST'])
def sign_in():
    """Authenticate a user and start a session."""
    sign_in_form = SignInForm()
    context = {
        'sign_in_form': sign_in_form,
    }
    if sign_in_form.validate_on_submit():
        data = sign_in_form.data
        # user = User.query.filter_by(username=data.get('username'), password=data.get('password')).first()
        # if user:
        #     login_user(user, remember=False)
        #     return redirect(url_for('new_list'))
        return 'It works!'

    return render_template('sign_in.html', **context)
    return 'Sign In'


@tasks_urls.route('/lists/new/', methods=['GET', 'POST'])
def new_list():
    """Create a new list."""
    print(current_user.name)
    list_form = ListForm()
    context = {
        'list_form': ListForm()
    }
    if list_form.validate_on_submit():
        return redirect(url_for('tasks.sign_in'))

    return render_template('list_detail.html', **context)
