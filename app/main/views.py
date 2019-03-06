from flask import render_template, session, redirect, url_for, current_app, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from .. import db
from ..models import Users
from ..email import send_email
from . import main
from .forms import NameForm, NoForm


@main.route('/', methods=['GET', 'POST'])
def index():
    user_agent = request.headers.get('user_agent')
    if current_user.is_authenticated:
        form = NoForm()
    else:
        form = NameForm()
        if form.validate_on_submit():
            old_name = session.get('name')
            if old_name is not None and old_name != form.name.data:
                flash('你改名啦~')
            session['name'] = form.name.data
            return redirect(url_for('main.index'))
    return render_template(
        'index.html', name=session.get('name'), form=form,
        user_agent=user_agent, current_time=datetime.utcnow()
    )


@main.route('/user/<name>')
def user(name):
    user_agent = request.headers.get('user_agent')
    return render_template('index.html', name=name, user_agent=user_agent)


@login_required
@main.route('/secret')
def secret():
    return "Only authenticated users are allowed."


# @main.route('/db', methods=['GET', 'POST'])
# def dbop():
#     dbform = NameForm()
#     if dbform.validate_on_submit():
#         user = User.query.filter_by(username=form.name.data).first()


@main.route('/baidu')
def baidu():
    return redirect('https://www.baidu.com', 302, None)


@main.route('/register', methods=['GET', 'POST'])
def register():
    pass
