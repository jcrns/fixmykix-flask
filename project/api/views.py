# Importing all needed Flask classes
from flask import Flask, session, redirect, Blueprint, request, jsonify, g, url_for, make_response, Response

# Importing firebase connection
from project.firebase_connection import firebaseConnect

api = Blueprint('api', __name__)

# FIREBASE AUTHENTICATION
databaseConnect = firebaseConnect()

database = databaseConnect['database']

authe = databaseConnect['authe']

@api.route("/signup-api", methods=['GET', 'POST'])
def signUpApi():
	
	# Assigning variables equvilent to posted data
	name = request.json['name']
	username = request.json['username']
	email = request.json['email']
	address = request.json['address']
	city = request.json['city']
	zip_code = request.json['zip_code']
	
	# Variables for providers
	business_name = request.json['business_name']
	password = request.json['password']

	try:
		description = request.json['description']

		# Running create user function
		createdUser = createUserFunc(name, email, username, address, city, zip_code, description, business_name,  password)
	except Exception as e:
		print("user not provider")

		# Running create user function
		createdUser = createUserFunc(name, email, username, address, city, zip_code, 0, 0, password)

	return jsonify(createdUser)

def createUserFunc(name, email, username, address, city, zip_code, description, business_name, password):
	try:
		print(email)
		print(password)
		
		# Creating user in firebase
		user = authe.create_user_with_email_and_password(email,password)

		# Assigning uid which will be used to create paths in database
		uid = user['localId']

		# Assigning json data to variable to return to database
		if description and business_name != 0:
			userAccount = { "name" : name, "email" : email, "username" : username, "address" : address, "city": city , "description" : description, "business_name" : business_name, "provider": { "is_provider": True, "clean_shoes": False, "shoe_artist": False, "background_info": "", "about_brand_or_individual": "" }, "setup_complete": False, "number_of_transactions": 0, "rating": 0 }
		else:
			print("user not provider")
			userAccount = { "name" : name, "email" : email, "username" : username, "address" : address, "city": city , "description" : "", "business_name" : "", "provider": { "is_provider": False, "clean_shoes": False, "shoe_artist": False, "background_info": "", "about_brand_or_individual": "" }, "setup_complete": True, "number_of_transactions": 0, "rating": 0 }

		# Saving data to firebase
		database.child("users").child(uid).child("account").set(userAccount)
		database.child("users").child(uid).child("account").set("interest").set("['null']")
		database.child("users").child(uid).child("account").set("history").set("['null']")
		message = "success"
	except Exception as e:
		print(e)
		message = "failed"

	return message

@api.route("/signin-api", methods=['GET', 'POST'])
def signInApi():

	# Assigning variables equvilent to posted data
	name = request.json['name']
	password = request.json['password']

	# Running signin function
	signIn = signInFunc(name, password)

	return jsonify(signIn)

def signInFunc(email, password):
	# Creating empty dictionary
	userData = dict()
	try:
		print('aaaaaa')
		# Signing into firebase
		user = authe.sign_in_with_email_and_password(email,password)

		# Assigning uid which will be used to create paths in database
		uid = user['localId']

		# Getting data from firebase
		account = dict(database.child("users").child(uid).child("account").get().val())

		# Saving data in dictionary
		userData['user'] = user
		userData['account'] = account
		userData['message'] = "success"
	except Exception as e:
		userData['message'] = "failed"
		print(e)

	return userData

def updateSetup():
	print('setup')

