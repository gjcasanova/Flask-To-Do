"""Views module."""

# Flask
from flask import Blueprint, abort, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

# Local application
from app.forms import ListForm, SignInForm, TaskForm
from app.models import List, Task, User
from app.plugins import db

app_routes = Blueprint('tasks', __name__)


@app_routes.route('/sign_in/', methods=['GET', 'POST'])
def sign_in():
    """Authenticate a user and start a session."""
    sign_in_form = SignInForm()
    if sign_in_form.validate_on_submit():
        data = sign_in_form.data
        user = User.query.filter_by(username=data['username'], password=data['password']).first()
        if user:
            login_user(user, remember=False)
            return redirect(url_for('tasks.list_lists'))
    context = {
        'sign_in_form': sign_in_form,
    }
    return render_template('sign_in.html', **context)


@app_routes.route('/sign_out/', methods=['POST'])
@login_required
def sign_out():
    """Finish a session."""
    logout_user()
    return redirect(url_for('tasks.sign_in'))


@app_routes.route('/lists/', methods=['GET'])
@login_required
def list_lists():
    """List the lists of the current user."""
    lists = List.query.filter_by(user=current_user)
    context = {
        'current_user': current_user,
        'lists': lists,
    }
    return render_template('lists.html', **context)


@app_routes.route('/lists/new/', methods=['GET', 'POST'])
@login_required
def create_list():
    """Create a new list."""
    list_form = ListForm()
    if list_form.validate_on_submit():
        data = list_form.data
        data.pop('csrf_token')
        data.pop('submit')
        user = current_user
        new_list = List(**data, user=user)
        db.session.add(new_list)
        db.session.commit()
        return redirect(url_for('tasks.list_lists'))

    context = {
        'current_user': current_user,
        'list_form': ListForm()
    }
    return render_template('list_create.html', **context)


@app_routes.route('/lists/<int:list_id>/destroy/', methods=['POST'])
@login_required
def destroy_list(list_id):
    """Delete a list from database."""
    list = List.query.filter_by(id=list_id, user=current_user).first()
    if not list:
        abort(404)
    db.session.delete(list)
    db.session.commit()
    return redirect(url_for('tasks.list_lists'))


@app_routes.route('/lists/<int:list_id>/retrieve/', methods=['GET', 'POST'])
@login_required
def retrieve_list(list_id):
    """Retrieve and allow update details about a list."""
    list = List.query.filter_by(id=list_id, user=current_user).first()
    if not list:
        abort(404)
    list_form = ListForm()

    if list_form.validate_on_submit():
        data = list_form.data
        list.name = data['name']
        list.details = data['details']
        db.session.commit()
        return redirect(url_for('tasks.retrieve_list', list_id=list.id))

    list_form.name.data = list.name
    list_form.details.data = list.details

    context = {
        'current_user': current_user,
        'list': list,
        'list_form': list_form
    }
    return render_template('list_retrieve.html', **context)


@app_routes.route('/lists/<int:list_id>/tasks/<int:task_id>/destroy/', methods=['POST'])
@login_required
def destroy_task(list_id, task_id):
    """Delete a task from database."""
    list = List.query.filter_by(id=list_id, user=current_user).first()
    task = Task.query.filter_by(list=list, id=task_id).first()
    if not task:
        abort(404)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks.retrieve_list', list_id=list_id))


@app_routes.route('/lists/<int:list_id>/tasks/new/', methods=['GET', 'POST'])
@login_required
def create_task(list_id):
    """Create a list in database."""
    list = List.query.filter_by(id=list_id, user=current_user).first()
    if not list:
        abort(404)
    task_form = TaskForm()

    if task_form.validate_on_submit():
        data = task_form.data
        data.pop('csrf_token')
        data.pop('submit')
        task = Task(**data, list=list)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('tasks.retrieve_list', list_id=list_id))

    context = {
        'current_user': current_user,
        'list': list,
        'task_form': task_form,
    }
    return render_template('task_create.html', **context)


@app_routes.route('/lists/<int:list_id>/tasks/<int:task_id>/retrieve/', methods=['GET', 'POST'])
@login_required
def retrieve_task(list_id, task_id):
    """Retrieve and allow update details about a task."""
    list = List.query.filter_by(id=list_id, user=current_user).first()
    task = Task.query.filter_by(id=task_id, list=list).first()
    if not task:
        abort(404)
    task_form = TaskForm()
    if task_form.validate_on_submit():
        data = task_form.data
        task.name = data['name']
        task.details = data['details']
        task.due_date = data['due_date']
        task.is_finished = data['is_finished']
        db.session.commit()
        return redirect(url_for('tasks.retrieve_list', list_id=list_id))

    task_form.name.data = task.name
    task_form.details.data = task.details
    task_form.due_date.data = task.due_date
    task_form.is_finished.data = task.is_finished

    context = {
        'current_user': current_user,
        'list': list,
        'task': task,
        'task_form': task_form,
    }
    return render_template('task_retrieve.html', **context)
