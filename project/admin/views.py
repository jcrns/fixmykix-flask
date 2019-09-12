# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, Blueprint, request

# Importing firebase connection
from project.firebase_connection import firebaseConnect

# Importing forms
from project.admin.forms import SignUpForProviderEarly, AdminLoginForm

# Importing auth functions
from project.api.views import createUserFunc, signInFunc

# Importing login_required function
from project.decorators import login_required_early

# Defining Blueprint var
admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static', static_url_path='/static/admin')

# Importing os for enviroment variables
import os

# FIREBASE AUTHENTICATION
databaseConnect = firebaseConnect()

database = databaseConnect['database']

# Post function
@admin.route("/get-ready", methods=['GET', 'POST'])
def early():
	Launched = os.environ.get('LAUNCHED', None)
	print(Launched)
	if Launched == 'True':
		return redirect(url_for('explore.homepage'))
	form = SignUpForProviderEarly()

	# Checking if form is valid
	if form.validate_on_submit():
		# Running auth function
		results = createUserFunc(form.name.data, form.email.data, form.username.data, form.address.data, form.city.data, form.zip_code.data, form.business_name.data, form.password.data, form.background_info.data, form.write_bio.data, form.clean_shoes.data, form.shoe_artist.data, form.examples_of_services_1.data, form.previous_work_1.data, form.examples_of_services_2.data, form.previous_work_2.data, form.examples_of_services_3.data, form.previous_work_3.data, form.questions_for_customers.data, form.describe_services.data)
		if results != 'success':
			flash(results)
			return redirect(url_for('about.early')) 
		flash(f'Your Application was Submited! Be Sure to Check your Email!', 'success')
		return redirect(url_for('about.home')) 
	return render_template('admin/early.html', form=form)

@admin.route("/admin", methods=['GET', 'POST'])
@login_required_early
def control():
	# Getting User Applications
	applicationList = []
	acceptedList = []

	usersData = dict(database.child("users").get().val())
	for uid in usersData:
		user = usersData[uid]
		if user['account']['provider']['is_provider'] == True and user['account']['provider']['accepted'] == True:
			acceptedList.append(user)
		if user['account']['provider']['is_provider'] == True and user['account']['provider']['accepted'] != True:
			applicationList.append(user)
	return render_template('admin/admin.html', application_list=applicationList, accepted_list=acceptedList)

@admin.route("/admin-login", methods=['GET', 'POST'])
def login():
	form = AdminLoginForm()
	if form.validate_on_submit():
		# Signing user in
		finalizedData = signInFunc(form.email.data, form.password.data)
		if finalizedData['account']['is_admin'] == True:	
			session['account'] = finalizedData['account']
			session['user'] = finalizedData['user']
			return redirect(url_for('admin.control')) 
		else:
			flash(f'Your not an admin')
			return redirect(url_for('admin.early'))
	return render_template('admin/admin-login.html', form=form)



