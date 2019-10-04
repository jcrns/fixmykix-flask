import pyrebase, json, requests

# Importing os for enviroment variables
import os

def firebaseConnect():
	production = os.environ.get('PRODUCTION_CONNECT', None)

	if production == 'False':
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
	else:
		# OFFICIAL DB #
		# Configuring connection to database
		config = {
			'apiKey': "AIzaSyAd59kgeeImaBUmuDvQAnHygW6zVmPbEmU",
			'authDomain': "fixmykix-production.firebaseapp.com",
			'databaseURL': "https://fixmykix-production.firebaseio.com",
			'projectId': "fixmykix-production",
			'storageBucket': "fixmykix-production.appspot.com",
			'messagingSenderId': "28170604507",
			'appId': "1:28170604507:web:c58507746478cbf71aa1fe"
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