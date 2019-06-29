# Importing all forms for user validation
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import validators 

class SignUpForProvider(FlaskForm):
    # Setting login fields
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), validators.length(min=3, max=50)])
    phone_number = IntegerField('Phone')
    address = StringField('Address', validators=[DataRequired()]) 
    city = StringField('City', validators=[DataRequired()]) 
    zip_code = StringField('Zip Code', validators=[DataRequired()]) 
    business_name = StringField('Business Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit as Provider')

class SignUpForConsumer(FlaskForm):
    # Setting login fields
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(),validators.length(min=3, max=50)])
    phone_number = IntegerField('Phone')
    address = StringField('Address', validators=[DataRequired()]) 
    city = StringField('City', validators=[DataRequired()]) 
    zip_code = StringField('Zip Code', validators=[DataRequired()]) 
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    # Setting login fields
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')