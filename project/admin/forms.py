# Importing all forms for user validation
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, MultipleFileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import validators 

class SignUpForProviderEarly(FlaskForm):
    # Setting login fields
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), validators.length(min=3, max=50)])
    phone_number = IntegerField('Phone')
    address = StringField('Address', validators=[DataRequired()]) 
    city = StringField('City', validators=[DataRequired()]) 
    zip_code = StringField('Zip Code', validators=[DataRequired()]) 
    business_name = StringField('Business Name', validators=[DataRequired()])
    background_info = TextAreaField('Background Info', validators=[DataRequired()])
    write_bio = TextAreaField('WRITE A BIO ABOUT YOURSELF/ BRAND', validators=[DataRequired()])
    clean_shoes = BooleanField("Shoe Restoration")
    shoe_artist = BooleanField("Shoe Art/Customization")
    describe_services = TextAreaField('List services that you provide', validators=[DataRequired()])

    # Examples of Services Fields
    examples_of_services_1 = TextAreaField('Example 1', validators=[DataRequired()])
    previous_work_1 = MultipleFileField('Upload 3 pictures of your previous work')

    examples_of_services_2 = TextAreaField('Example 2', validators=[DataRequired()])
    previous_work_2 = MultipleFileField('Upload 3 pictures of your previous work')

    examples_of_services_3 = TextAreaField('Example 3', validators=[DataRequired()])
    previous_work_3 = MultipleFileField('Upload 3 pictures of your previous work')

    questions_for_customers = TextAreaField('What info do you need from your customers to do your best work?', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit as Provider')

class AdminLoginForm(FlaskForm):
    # Setting login fields
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')