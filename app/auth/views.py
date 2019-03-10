from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..email import send_email
from ..models import Users
from .forms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])  # 登陆路由
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


@auth.route('/logout')  # 登出路由
def logout():
    logout_user()
    flash('你已成功退出。')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['POST', 'GET'])  # 注册路由
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '注册确认邮件', 'auth/email/confirm', user=user, token=token)
        flash('确认邮件已发送至你的邮箱。')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')  # 邮箱确认路由
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('用户注册成功！')
    else:
        flash('确认链接有误，请重试。')
    return redirect(url_for('main.index'))
