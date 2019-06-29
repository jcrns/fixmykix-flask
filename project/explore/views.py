# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, Blueprint, request

# Importing firebase connection
from project.firebase_connection import firebaseConnect

# FIREBASE AUTHENTICATION
databaseConnect = firebaseConnect()

database = databaseConnect['database']

# Defining Blueprint var
explore = Blueprint('explore', __name__, template_folder='templates', static_folder='static', static_url_path='/static/explore')

@explore.route("/explore", methods=['GET', 'POST'])
def home():
	providersList = []

	# Counter for for loop
	providerCount = 0

	# Getting user data
	usersData = dict(database.child("users").get().val())
	for user in usersData:
		if providerCount == 10:
			break
		# Definning variable
		getProvider = usersData[user]['account']['provider']

		# Looking for provider
		if getProvider == True:

			# Found provider provider count added by 1
			providerCount += 1

			# Definning dict
			providerDict = {}

			# Definning correct variables
			username = usersData[user]['account']['username']
			rating = usersData[user]['account']['username']

	return render_template('explore/explore.html')