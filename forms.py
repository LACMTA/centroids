from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Length
import time, datetime

# Set your classes here.


class RegisterForm(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


class LoginForm(Form):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )

class CommentForm(Form):

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.stop_id = kwargs['stop_id']
        self.ip = kwargs['ip']
        self.timestamp = kwargs['timestamp']

        if kwargs['stop_name']:
            self.stop_name = kwargs['stop_name']
        else:
            self.stop_name = "glargh"

    ip = '127.0.0.1'
    stop_id = HiddenField('stop_id', default='asd')
    stop_name = HiddenField('stop_name', default='A SD')
    timestamp = HiddenField('timestamp', default="2015-01-01 01:01:01")
    ip = HiddenField('ip', default=ip)

    # freeway_ramps = BooleanField('Freeway Ramps', default=False)
    # sidewalk_poor = BooleanField('Poor sidewalk conditions or lack of sidewalk', default=False)
    # poor_crosswalks = BooleanField('Poor crosswalks or lack of crosswalks', default=False)
    # not_safe = BooleanField('No safe place to bicycle', default=False)
    # vehicle_speed = BooleanField('Vehicle speed and traffic (due to freeway ramps)', default=False)
    # poor_lighting = BooleanField('Poor lighting', default=False)
    # poor_signage = BooleanField('Poor signage or lack of crosswalks', default=False)
    # no_enforcement = BooleanField('Lack of enforcement of traffic violations', default=False)
    # no_shade = BooleanField('No shade', default=False)
    # personal_safety = BooleanField('Personal safety concerns', default=False)
    # too_far = BooleanField('Destinations are too far away', default=False)
    # bad_drivers = BooleanField('Bad driver behaviors', default=False)
    # no_facilities = BooleanField('Lack of worksite facilities (for example, showers or lockers)', default=False)
    # other = BooleanField('Other challenges not listed above', default=False)
