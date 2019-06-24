# Importing all needed Flask classes
from flask import Flask, session, redirect, Blueprint, request, jsonify, g, url_for, make_response, Response
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
	password = request.json['password']
	try:
		business_name = request.json['business_name']
		description = request.json['description']
		createdUser = createUserFunc(name, email, username, address, description, business_name,  password)
	except Exception as e:
		print("user not provider")
		createdUser = createUserFunc(name, email, username, address, 0, 0, password)

def createUserFunc(name, email, username, address, description, business_name, password):
	try:
		print(email)
		print(password)
		
		# Creating user in firebase
		user = authe.create_user_with_email_and_password(email,password)

		# Assigning uid which will be used to create paths in database
		uid = user['localId']

		# Assigning json data to variable to return to database
		if description and business_name != 0:
			userAccount = { "name" : name, "email" : email, "username" : username, "address" : address, "description" : description, "business_name" : business_name }
		else:
			print("user not provider")
			userAccount = { "name" : name, "email" : email, "username" : username, "address" : address, "description" : "", "business_name" : ""  }

		# Saving data to firebase
		database.child("users").child(uid).child("account").set(userAccount)
		message = "success"
	except Exception as e:
		print(e)
		message = "failed"

	return message
