from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField('Department Title', validators=[DataRequired()])
    members = StringField("Members")
    email = StringField("Email")
    submit = SubmitField('Submit')
