from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditStationForm(FlaskForm):
    coordinates = StringField('coordinates', validators=[DataRequired()])
    number = StringField('number', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    submit = SubmitField('Update')


class EditGoodsForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    amount = StringField('amount', validators=[DataRequired()])
    currency = StringField('currency', validators=[DataRequired()])
    image_url = StringField('image_url', validators=[DataRequired()])
    submit = SubmitField('Update')


class EditServicesForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    image_url = StringField('image_url', validators=[DataRequired()])
    submit = SubmitField('Update')


#class IndexForm(FlaskForm):
#    submit = SubmitField('Refresh')
