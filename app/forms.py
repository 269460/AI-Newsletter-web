from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User, Category

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
    submit = SubmitField('Subscribe to Newsletter')
