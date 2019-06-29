# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, Blueprint, request

# Importing firebase connection
from project.firebase_connection import firebaseConnect

# Importing Login Required
from project.decorators import login_required

# FIREBASE AUTHENTICATION
databaseConnect = firebaseConnect()

database = databaseConnect['database']

# Creating blueprint for app
profile = Blueprint('profile', __name__, static_folder='static' , template_folder='templates', static_url_path='/static/dashboard')


# Profile function
@profile.route("/profile/<username>", methods=['GET', 'POST'])
# @login_required
def home(username):

	# Trying to define variable
	try:
		sessionUsername = session['account']['username']
	except Exception as e:
		print('uu')
		sessionUsername = ''

	print(sessionUsername)
	print(username)
	# Logged In User Profile
	if sessionUsername == username:
		print('datasddxbase')
		title = username + " - FixMyKix"
		return render_template('profile/profile.html',viewing=False, title=title)
	else:
		print('xbase')

		# Getting database
		usersData = dict(database.child("users").get().val())

		# Finding matching url username
		for user in usersData:
			# print('xbbase')

			# Getting username
			iteratedUsername = usersData[user]['account']['username']
			print(iteratedUsername)
			# Checking for matching username
			if iteratedUsername == username:
				print("founsdd")
				# Getting Public Data
				email = usersData[user]['account']['email']
				number_of_transactions = usersData[user]['account']['number_of_transactions']
				rating = usersData[user]['account']['rating']
				city = usersData[user]['account']['city']
				setup_complete = usersData[user]['account']['setup_complete']
				title = username + " - FixMyKix"
				if setup_complete == True:
					return render_template("profile/profile.html", viewing=True, title=title, email=email, username=username, number_of_transactions=number_of_transactions, rating=rating, city=city) 
				else:
					print('not setup')
					flash(f'Url not found', 'text-danger')
					return redirect(url_for('homepage.home'))
			else:
				print('not found')

				# Redirecting user for unfound url
				flash('Url not found', 'text-danger')
				return redirect(url_for('homepage.home'))
