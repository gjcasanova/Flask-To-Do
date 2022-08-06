"""Views module."""

# Flask
from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_user

from app.forms import ListForm, SignInForm, TaskForm
from app.models import User, List, Task
from app.plugins import db

app_routes = Blueprint('tasks', __name__)


# @app_routes.route('/sign_in/', methods=['GET', 'POST'])
# def sign_in():
#     """Authenticate a user and start a session."""
#     sign_in_form = SignInForm()
#     context = {
#         'sign_in_form': sign_in_form,
#     }
#     if sign_in_form.validate_on_submit():
#         data = sign_in_form.data
#         print(data)
#         # user = User.query.filter_by(username=data.get('username'), password=data.get('password')).first()
#         # if user:
#         #     login_user(user, remember=False)
#         #     return redirect(url_for('new_list'))
#         return 'It works!'

#     return render_template('sign_in.html', **context)
#     return 'Sign In'

@app_routes.route('/lists/', methods=['GET'])
def list_lists():
    """List the lists of the current user."""
    lists = List.query.all()
    context = {
        'lists': lists,
    }
    return render_template('lists.html', **context)


@app_routes.route('/lists/new/', methods=['GET', 'POST'])
def create_list():
    """Create a new list."""
    # print(current_user.name)
    list_form = ListForm()
    context = {
        'list_form': ListForm()
    }
    if list_form.validate_on_submit():
        data = list_form.data
        data.pop('csrf_token')
        data.pop('submit')
        user = User.query.first()
        new_list = List(**data, user=user)
        db.session.add(new_list)
        db.session.commit()
        return redirect(url_for('tasks.list_lists'))

    return render_template('list_create.html', **context)


@app_routes.route('/lists/<int:list_id>/destroy/', methods=['POST'])
def destroy_list(list_id):
    """Delete a list from database."""
    list = List.query.get(list_id)
    db.session.delete(list)
    db.session.commit()
    return redirect(url_for('tasks.list_lists'))


@app_routes.route('/lists/<int:list_id>/retrieve/', methods=['GET', 'POST'])
def retrieve_list(list_id):
    """Retrieve and allow update details about a list."""
    list = List.query.get(list_id)
    list_form = ListForm()

    if list_form.validate_on_submit():
        data = list_form.data
        list.name = data['name']
        list.details = data['details']
        db.session.commit()
        return redirect(url_for('tasks.retrieve_list', list_id=list.id))

    context = {
        'list': list,
        'list_form': list_form
    }
    return render_template('list_retrieve.html', **context)


@app_routes.route('/lists/<int:list_id>/tasks/<int:task_id>/destroy/', methods=['POST'])
def destroy_task(list_id, task_id):
    """Delete a task from database."""
    list = List.query.get(list_id)
    task = Task.query.filter_by(list=list, id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks.retrieve_list', list_id=list_id))


@app_routes.route('/lists/<int:list_id>/tasks/new/', methods=['GET', 'POST'])
def create_task(list_id):
    """Create a list in database."""
    list = List.query.get(list_id)
    task_form = TaskForm()

    if task_form.validate_on_submit():
        data = task_form.data
        data.pop('csrf_token')
        data.pop('submit')
        task = Task(**data, list=list)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('tasks.retrieve_list', list_id=list_id))

    # pdb.set_trace()
    context = {
        'list': list,
        'task_form': task_form,
    }
    return render_template('task_create.html', **context)


@app_routes.route('/lists/<int:list_id>/tasks/<int:task_id>/retrieve/', methods=['GET', 'POST'])
def retrieve_task(list_id, task_id):
    """Retrieve and allow update details about a task."""
    list = List.query.get(list_id)
    task = Task.query.filter_by(id=task_id, list=list).first()
    task_form = TaskForm()
    if task_form.validate_on_submit():
        data = task_form.data
        task.name = data['name']
        task.details = data['details']
        task.due_date = data['due_date']
        db.session.commit()
        return redirect(url_for('tasks.retrieve_list', list_id=list_id))
    context = {
        'list': list,
        'task': task,
        'task_form': task_form,
    }
    return render_template('task_retrieve.html', **context)
