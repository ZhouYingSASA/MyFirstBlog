from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user
from . import auth
from ..models import Users
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            nex = request.args.get('next')
            if nex is None or not nex.startwith('/'):
                nex = url_for('main.index')
            return redirect(nex)
        flash('用户名或密码无效。')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('你已成功退出。')
    return redirect(url_for('main.index'))
