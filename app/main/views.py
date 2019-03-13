from flask import render_template, session, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from . import main
from .forms import NameForm, PostForm
from .. import db
from ..models import Post


@main.route('/', methods=['GET', 'POST'])
def index():
    user_agent = request.headers.get('user_agent')
    if current_user.is_authenticated:
        form = PostForm()
        if form.validate_on_submit():
            post = Post(cont=form.body.data, author_id=current_user._get_current_object())
            db.session.add(post)
            return redirect(url_for('.index'))
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


@main.route('/register', methods=['GET', 'POST'])
def register():
    pass
