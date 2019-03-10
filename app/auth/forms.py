from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError
from ..models import Users


class LoginForm(FlaskForm):
    email = StringField('你的邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('输入密码', validators=[DataRequired()])
    remember_me = BooleanField('保持登陆')
    submit = SubmitField('登陆')


class RegistrationForm(FlaskForm):
    email = StringField('邮箱地址', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64),
                                              Regexp('[\u4E00-\u9FD5a-zA-Z0-9_.]*$', 0,
                                                     '仅支持常见汉字、英文大小写、数字、点及下划线命名。')])
    password = PasswordField('输入密码', validators=[DataRequired()])
    password2 = PasswordField('再次输入密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已注册！')

    def validate_username(self, field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在！')
