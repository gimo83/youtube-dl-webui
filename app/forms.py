from flask.ext.wtf import Form
from flask.ext.wtf.html5 import URLField
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username    = StringField('Username', validators=[DataRequired()])
    password    = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)
    submit      = SubmitField('Submit') 



class DownloadVideoForm(Form):
    videoURL    = URLField('URL', validators=[DataRequired()])
    submit      = SubmitField('Submit')
