import pyrebase, json, requests

def firebaseConnect():
	# Configuring connection to database
	config = {
		'apiKey': "AIzaSyCgzNKfA17BLwDaWDfQkwA4hkpKU4f7T44",
		'authDomain': "fixmykix.firebaseapp.com",
		'databaseURL': "https://fixmykix.firebaseio.com",
		'projectId': "fixmykix",
		'storageBucket': "fixmykix.appspot.com",
		'messagingSenderId': "401125909914",
		'appId': "1:401125909914:web:0760eeffc02646a4"
	  }

	returnData = dict()

	# Defining variable equal to database connection
	firebase = pyrebase.initialize_app(config)

	# Test Variables
	database = firebase.database()

	returnData['database'] = database

	# Defing users with
	authe = firebase.auth()

	returnData['authe'] = authe

	storage = firebase.storage()

	returnData['storage'] = storage
	
	return returnData
