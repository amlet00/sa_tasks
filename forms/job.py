from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField('Job Title', validators=[DataRequired()])
    work_size = IntegerField("Work Size")
    collaborators = StringField("Collaborators")
    is_finished = BooleanField("Is job finished?")
    submit = SubmitField('Submit')
