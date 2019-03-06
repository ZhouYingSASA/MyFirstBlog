from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('<h3><b>君の名甚?</b></h3>', validators=[DataRequired()])
    submit = SubmitField('提交')


class NoForm(FlaskForm):
    pass
