# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, Blueprint, request

# Importing forms
from project.users.forms import SignUpForProvider, SignUpForConsumer, LoginForm

# Importing auth functions
from project.api.views import createUserFunc, signInFunc

# Importing login_required function
from project.decorators import login_required


# Defining Blueprint var
users = Blueprint('users', __name__, template_folder='templates')

@users.route("/signup-provider", methods=['GET', 'POST'])
def signupProvider():

	# Defining the form
	form = SignUpForProvider()

	# Checking if form is valid
	if form.validate_on_submit():

		# Running auth function
		finalizedData = createUserFunc(form.name.data, form.email.data, form.username.data, form.address.data, form.city.data, form.zip_code.data, form.description.data, form.business_name.data, form.password.data)
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
		finalizedData = createUserFunc(form.name.data, form.email.data, form.username.data, form.address.data, form.city.data, form.zip_code.data, 0, 0, form.password.data)
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

	# Checking if form is valid
	if form.validate_on_submit():
		finalizedData = signInFunc(form.email.data, form.password.data)
		print(finalizedData)
		try:
			if finalizedData['message'] == 'success':
				session['account'] = finalizedData['account']
				session['user'] = finalizedData['user']
				if finalizedData['account']['provider']['is_provider'] == True:
					print('is provider')
					print('fixed session')
					return redirect(url_for('profile.home',username=session['account']['username']))
				else:
					print('not provider') 
					return redirect(url_for('profile.home',username=session['account']['username']))

			else:
				flash(f'Login failed')
		except Exception as e:
			print(e)
			flash(f'Login failed')
			

	# Different view for user if provider or consumer
	return render_template('users/login.html', form=form)

@users.route("/logout")
@login_required 
def logout():
    session.clear()
    flash("You have been logged out")
    return redirect(url_for('homepage.home'))
