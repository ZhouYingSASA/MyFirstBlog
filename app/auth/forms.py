from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    email = StringField('你的邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('输入密码', validators=[DataRequired()])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('登陆')
