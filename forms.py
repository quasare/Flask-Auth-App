from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=50)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30)])



class LoginForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """ Form for adding feedback"""

    title = StringField('Title', validators=[InputRequired(message='Please enter a title'), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])

