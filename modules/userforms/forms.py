from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, FileField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileAllowed
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')


class Projectform(FlaskForm):
    projectname = StringField("Projectnaam", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Create Project")


class Scanform(FlaskForm):
    target = StringField("Target", validators=[DataRequired()])
    service = BooleanField("Service scan (-sV)")
    ping = BooleanField("Skip host discovery (-Pn)")
    submit = SubmitField("Run scan")


class Fileform(FlaskForm):
    targetfile = FileField("File with targets", validators=[FileAllowed(['txt']), DataRequired()])
    service = BooleanField("Service scan (-sV)")
    ping = BooleanField("Skip host discovery (-Pn)")
    submit = SubmitField("Run scan")


class Updateform(FlaskForm):
    note = TextAreaField("Update note", validators=[DataRequired()])
    id = StringField("Unique ID of the scan result")
    submit = SubmitField("Update")


class Inviteform(FlaskForm):
    email = StringField("Email")
    submit = SubmitField('Grant access')
