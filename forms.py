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
        if kwargs['stop_name']:
            self.stop_name = kwargs['stop_name']
        else:
            self.stop_name = "glargh"

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    ip = '127.0.0.1'

    stop_id = HiddenField('stop_id', default='asd')
    stop_name = HiddenField('stop_name', default='A SD')
    timestamp = HiddenField('stop_id', default=st)
    ip = HiddenField('stop_id', default=ip)
    freeway_ramps = BooleanField('Freeway Ramps', default=False)
    sidewalk_poor = BooleanField('Poor sidewalk', default=False)
    no_crosswalks = BooleanField('No crosswalks', default=False)
    no_shade = BooleanField('No shade', default=False)
    poor_signage = BooleanField('Poor signage', default=False)
