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
	getPost = database.child("posts").get().val()
	print('getPost')
	print('getPost')
	for post in getPost:
		print(post[''])
	return render_template('explore/explore.html')