from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class UpdatePreferencesForm(FlaskForm):
    preferences = SelectMultipleField('Categories', choices=[
        ('AI', 'Artificial Intelligence'),
        ('IoT', 'Internet of Things'),
        ('CS', 'Cybersecurity'),
        ('RA', 'Robotics and Automation'),
        ('TC', 'Cloud Technologies'),
        ('TM', 'Mobile Technologies'),
        ('BT', 'Biotechnology'),
        ('NT', 'Nanotechnology'),
        ('EO', 'Renewable Energy'),
        ('TK', 'Quantum Technologies')
    ])
    submit = SubmitField('Update Preferences')