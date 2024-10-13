from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from app.models import User, Category
from wtforms.validators import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class UpdatePreferencesForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(UpdatePreferencesForm, self).__init__(*args, **kwargs)
        self.preferences.choices = [(c.name, c.name) for c in Category.query.all()]

    preferences = SelectMultipleField('Categories')
    submit = SubmitField('Update Preferences')

class SubscriptionForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    preferences = SelectMultipleField('Categories', choices=[
        ('AI', 'Artificial Intelligence'),
        ('IoT', 'Internet of Things'),
        'CS': ['cyberbezpieczeństwo', 'bezpieczeństwo cyfrowe', 'hacking', 'ochrona danych', 'kryptografia'],
    'RA': ['robotyka', 'automatyzacja', 'robot', 'coboty', 'RPA'],
    'TC': ['chmura', 'cloud computing', 'edge computing', 'fog computing', 'centrum danych'],
    'TM': ['5G', '6G', 'smartfon', 'aplikacje mobilne', 'technologie mobilne'],
    'BT': ['biotechnologia', 'inżynieria genetyczna', 'CRISPR', 'terapia genowa', 'bioczujniki'],
    'NT': ['nanotechnologia', 'nanomateriały', 'nanoroboty', 'nanostruktury'],
    'EO': ['energia odnawialna', 'fotowoltaika', 'energia wiatrowa', 'magazynowanie energii'],
    'TK': ['komputer kwantowy', 'kryptografia kwantowa', 'czujniki kwantowe', 'internet kwantowy']

    ])
    submit = SubmitField('Subscribe to Newsletter')