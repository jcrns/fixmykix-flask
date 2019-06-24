# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, Blueprint, request

# Importing forms
from project.users.forms import SignUpForProvider, SignUpForConsumer, LoginForm

# Importing auth functions
from project.api.views import createUserFunc

# Defining Blueprint var
users = Blueprint('users', __name__, template_folder='templates')

@users.route("/signup-provider", methods=['GET', 'POST'])
def signupProvider():

	# Defining the form
	form = SignUpForProvider()

	# Checking if form is valid
	if form.validate_on_submit():

		# Running auth function
		finalizedData = createUserFunc(form.name.data, form.email.data, form.username.data, form.address.data, form.description.data, form.business_name.data, form.password.data)
		if finalizedData == 'success':
			flash(f'Application submited! Be sure to check email!')
			return redirect(url_for('homepage.home')) 
		else:
			flash(f'Application Failed')
	return render_template('users/signupProvider.html', form=form)

@users.route("/signup", methods=['GET', 'POST'])
def signupConsumer():

	# Defining the form
	form = SignUpForConsumer()

	# Checking if form is valid
	if form.validate_on_submit():

		# Running auth function
		finalizedData = createUserFunc(form.name.data, form.email.data, form.username.data, form.address.data, 0, 0, form.password.data)
		if finalizedData == 'success':
			flash(f'Account created! Sign in!')
			return redirect(url_for('users.login')) 
		else:
			flash(f'Sign Up Failed')
	return render_template('users/signupConsumer.html', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():

	# Defining the form
	form = LoginForm()

	# Different view for user if provider or consumer
	return render_template('users/login.html', form=form)
