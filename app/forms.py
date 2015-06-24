from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username    = StringField('Username', validators=[DataRequired()])
    password    = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)
    submit      = SubmitField('Submit') 
