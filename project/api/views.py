# Importing all needed Flask classes
from flask import Flask, session, redirect, Blueprint, request, jsonify, g, url_for, make_response, Response, flash

# Importing firebase connection
from project.firebase_connection import firebaseConnect

# Importing random
import random

# Importing string
import string

# Importing time and datetime
from time import *
import datetime


api = Blueprint('api', __name__)

# FIREBASE AUTHENTICATION
databaseConnect = firebaseConnect()

database = databaseConnect['database']

authe = databaseConnect['authe']

storage = databaseConnect['storage']

# Random id genorator
def randomString(stringLength=16):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

# Mainly ajax functions
@api.route("/get-services", methods=['GET', 'POST'])
def getServices():

	# Assigning variables equvilent to posted data
	party = request.form['party']
	print(party)
	posts = database.child("posts").get().val()
	userServices = []
	for post in posts:
		if post['username'] == party:
			userServices.append(post)
	print(userServices)
	return jsonify(userServices)

@api.route("/application-accepted", methods=['GET', 'POST'])
def applicationAccepted():

	# Assigning variables equvilent to posted data
	username = request.form['username']
	try:
		usersData = database.child("users").get().val()
		for uid in usersData:
			user = usersData[uid]
			if username == user['account']['username']:
				database.child("users").child(uid).child("account").child("provider").child("accepted").set(True)
		return jsonify('success')
	except Exception as e:
		print(e)
		return jsonify('failed')

@api.route("/admin-accepted", methods=['GET', 'POST'])
def adminAccepted():

	# Assigning variables equvilent to posted data
	username = request.form['username']
	try:
		usersData = database.child("users").get().val()
		for uid in usersData:
			user = usersData[uid]
			if username == user['account']['username']:
				database.child("users").child(uid).child("account").child("is_admin").set(True)
		return jsonify('success')
	except Exception as e:
		print(e)
		return jsonify('failed')


@api.route("/scope-of-work-post-api", methods=['GET', 'POST'])
def scopeOfWorkPostApi():
	try:
		print(request.form)

		# Assigning variables equvilent to posted data
		servicesDescription = request.form['services_description']

		print('fgtgwrg')
		postId = request.form['post_id']
		print('fgtgwrg')

		username = request.form['party']
		sender = session['account']['username']
		print('fgtgwrg')
		post = scopeOfWorkPost(postId, username, sender, servicesDescription)

		print(postId)
		return post
	except Exception as e:
		print(e)
		return 'failed'

def scopeOfWorkPost(postId, username, sender, servicesDescription):
	print("trying")
	try:
		users = dict(database.child("users").get().val())
		scopeOfWorkId = randomString(24)

		# Getting time
		timeNow = datetime.datetime.now()
		formatedDateNow = timeNow.strftime("%b-%d-%Y")
		formatedTimeNow = timeNow.strftime("%I:%M:%S %p")
		
		value = 'failed'

		# Creating title for service request
		posts = database.child("posts").get().val()
		for post in posts:
			if post['post_id'] == postId:
				shoeName = post['shoe_name']
				shoeDescription = post['shoe_description']
				shoeCost = post['cost']
				title = shoeName + " - " + shoeDescription + " - $" + str(shoeCost)

		# Storing data in users history
		for user in users:
			if users[user]['account']['username'] == username:
				if users[user]['account']['setup_complete'] == True:
					print(username)
					print(sender)
					scopeOfWork = { "sender": sender , "reciever": username, "post_id": postId, "date": formatedDateNow, "time" : formatedTimeNow, "title" : title, "services_description" : servicesDescription }


					value = 'sent!'
					if users[user]['history']['scope_of_work'][0] == "null":
						database.child("users").child(user).child("history").child("scope_of_work").child(0).set(scopeOfWorkId)
					else:
						count = 0
						for messageCount in users[user]['history']['scope_of_work']:
							count += 1
						database.child("users").child(user).child("history").child("scope_of_work").child(count).set(scopeOfWorkId)
		print(value)
		# Storing data in recievers history
		for user in users:
			if users[user]['account']['username'] == sender:
				if users[user]['account']['setup_complete'] == True:
					scopeOfWork = { "sender": sender , "reciever": username, "post_id": postId, "date": formatedDateNow, "time" : formatedTimeNow, "title" : title, "services_description" : servicesDescription }
					value = 'sent!'
					if users[user]['history']['scope_of_work'][0] == "null":
						database.child("users").child(user).child("history").child("scope_of_work").child(0).set(scopeOfWorkId)
					else:
						count = 0
						for messageCount in users[user]['history']['scope_of_work']:
							count += 1
						database.child("users").child(user).child("history").child("scope_of_work").child(count).set(scopeOfWorkId)

		scopeOfWork = { "sender": sender , "reciever": username, "post_id": postId, "date": formatedDateNow, "time" : formatedTimeNow, "title" : title, "services_description" : servicesDescription }
		database.child("scope_of_work").child(scopeOfWorkId).set(scopeOfWork)
		print("\n\n\n\n\n\n")
		print(value)
		return value
	except Exception as e:
		print("e")
		print(e)
		return 'failed'


@api.route("/service-request-post-api", methods=['GET', 'POST'])
def serviceRequestPostApi():
	try:
		# Assigning variables equvilent to posted data
		postId = request.form['post_id']
		posts = database.child("posts").get().val()
		for post in posts:
			if post['post_id'] == postId:
				username = post['username']

		sender = session['account']['username']
		print('fgtgwrg')
		post = serviceRequestPost(postId, username, sender)

		print(postId)
		return post
	except Exception as e:
		print(e)
		return 'failed'

def serviceRequestPost(postId, username, sender):
	print("trying")
	try:
		users = dict(database.child("users").get().val())
		serviceRequestId = randomString(24)

		# Getting time
		timeNow = datetime.datetime.now()
		formatedDateNow = timeNow.strftime("%b-%d-%Y")
		formatedTimeNow = timeNow.strftime("%I:%M:%S %p")
		
		value = 'failed'

		print(value)

		# Creating title for service request
		posts = database.child("posts").get().val()
		for post in posts:
			if post['post_id'] == postId:
				shoeName = post['shoe_name']
				shoeDescription = post['shoe_description']
				shoeCost = post['cost']
				title = shoeName + " - " + shoeDescription + " - $" + str(shoeCost)
		print(value)

		# Storing data in users history
		for user in users:
			if users[user]['account']['username'] == username:
				if users[user]['account']['setup_complete'] == True:
					print(username)
					print(sender)
					serviceRequestDict = { "sender": sender, "reciever": username, "post_id": postId, "date": formatedDateNow, "time" : formatedTimeNow, "title": title }
					print(users[user]['history'])
					print(users[user]['account'])
					print("??gwrtg")

					value = 'sent!'
					if users[user]['history']['service_request'][0] == "null":
						print("??gwrtg")

						database.child("users").child(user).child("history").child("service_request").child(0).set(serviceRequestId)
					else:
						count = 0
						for messageCount in users[user]['history']['service_request']:
							count += 1
						database.child("users").child(user).child("history").child("service_request").child(count).set(serviceRequestId)
		print(value)
		# Storing data in recievers history
		for user in users:
			if users[user]['account']['username'] == sender:
				if users[user]['account']['setup_complete'] == True:
					serviceRequestDict = { "sender": sender, "reciever": username, "post_id": postId, "date": formatedDateNow, "time" : formatedTimeNow, "title" : title }
					value = 'sent!'
					if users[user]['history']['service_request'][0] == "null":
						database.child("users").child(user).child("history").child("service_request").child(0).set(serviceRequestId)
					else:
						count = 0
						for messageCount in users[user]['history']['service_request']:
							count += 1
						database.child("users").child(user).child("history").child("service_request").child(count).set(serviceRequestId)

		serviceRequestDict = { "sender": sender , "reciever": username, "post_id": postId, "date": formatedDateNow, "time" : formatedTimeNow, "title" : title }
		database.child("service_request").child(serviceRequestId).set(serviceRequestDict)
		print("\n\n\n\n\n\n")
		print(value)
		return value
	except Exception as e:
		print("e")
		print(e)
		return 'failed'






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
	password = request.json['password']

	# Service Providers
	try:
		business_name = request.json['business_name']
	except Exception as e:
		print(e)
		business_name = 0
	try:
		background_info = request.json['background_info']
	except Exception as e:
		print(e)
		background_info = 0

	try:
		about_brand_or_individual = request.json['about_brand_or_individual']
	except Exception as e:
		print(e)
		about_brand_or_individual = 0
	try:
		description = request.json['description']
	except Exception as e:
		print(e)
		description = 0
	try:
		clean_shoes = request.json['clean_shoes']
	except Exception as e:
		print(e)
		clean_shoes = 0
	try:
		about_brand_or_individual = request.json['about_brand_or_individual']
	except Exception as e:
		print(e)
		about_brand_or_individual = 0

	try:
		about_brand_or_individual = request.json['about_brand_or_individual']
	except Exception as e:
		print(e)
		about_brand_or_individual = 0
	
	# Running create user function
	createdUser = createUserFunc(name, email, username, address, city, zip_code, business_name, password, background_info, about_brand_or_individual, clean_shoes, shoe_artist, describe_services, examples_of_services, previous_work, questions_for_customers, examples_of_services)

	return jsonify(createdUser)

def createUserFunc(name, email, username, address, city, zip_code, business_name, password, background_info, about_brand_or_individual, clean_shoes, shoe_artist, describe_services_1, previous_work_1, describe_services_2, previous_work_2, describe_services_3, previous_work_3, questions_for_customers, examples_of_services):
	try:
		print("email")
		print("password")

		# Assigning json data to variable to return to database
		if about_brand_or_individual != 0 and business_name != 0:
			if not clean_shoes:
				clean_shoes = False
			else:
				clean_shoes = True

			if not shoe_artist:
				shoe_artist = False
			else:
				shoe_artist = True
			if clean_shoes == False and shoe_artist == False:
				return 'failed'

			image_urls_1 = []
			
			print('gerg')
			print(previous_work_1)
			print(previous_work_2)
			print(previous_work_3)
			
			# Importing previous work
			if previous_work_1[0] != '':
				for pic in previous_work_1:	
					picId = randomString(24)
					putImg = storage.child("images").child("previous_work_1").child(picId).put(pic, picId)
					image_url = storage.child("images").child("previous_work_1").child(picId).get_url(picId)
					image_urls_1.append(image_url)
			else:
				return 'Add photos of previous work'

			image_urls_2 = []
			if previous_work_2[0] != '':
				for pic in previous_work_2:	
					picId = randomString(24)
					putImg = storage.child("images").child("previous_work_2").child(picId).put(pic, picId)
					image_url = storage.child("images").child("previous_work_2").child(picId).get_url(picId)
					image_urls_2.append(image_url)
			else:
				return 'Add photos of previous work'
			
			image_urls_3 = []
			if previous_work_3[0] != '':
				for pic in previous_work_3:	
					picId = randomString(24)
					putImg = storage.child("images").child("previous_work_3").child(picId).put(pic, picId)
					image_url = storage.child("images").child("previous_work_3").child(picId).get_url(picId)
					image_urls_3.append(image_url)
			else:
				return 'Add photos of previous work'
			
			# Creating user in firebase
			user = authe.create_user_with_email_and_password(email,password)


			# Assigning uid which will be used to create paths in database
			uid = user['localId']

			userAccount = { "name" : name, "email" : email, "username" : username, "address" : address, "city": city , "business_name" : business_name, "provider": { "is_provider": True, "clean_shoes": clean_shoes, "shoe_artist": shoe_artist, "background_info": background_info, "about_brand_or_individual": about_brand_or_individual, "accepted": False, "describe_services_1" : describe_services_1, "describe_services_2" : describe_services_2, "describe_services_3" : describe_services_3, "previous_work_1" : image_urls_1, "previous_work_2" : image_urls_2, "previous_work_3" : image_urls_3, "questions_for_customers" : questions_for_customers, "examples_of_services" : examples_of_services }, "setup_complete": False, "number_of_transactions": 0, "rating": 0, "created_at": time(), "profile_pic_url": "null", "is_admin": False }
		else:
			print("user not provider")
			userAccount = { "name" : name, "email" : email, "username" : username, "address" : address, "city": city , "business_name" : "null", "provider": { "is_provider": False, "clean_shoes": False, "shoe_artist": False, "background_info": "null", "about_brand_or_individual": "null", "accepted": "null" }, "setup_complete": True, "number_of_transactions": 0, "rating": 0, "created_at": time(), "profile_pic_url": "null", "is_admin": False  }

		# transactionHistoryDict = { "title": "null", "description": "null", "date": "null", "cost_paid": "null", "status" : "null", "client" : "null", "provider" : "null", "id" : "null" }

		# Saving data to firebase
		database.child("users").child(uid).child("account").set(userAccount)
		database.child("users").child(uid).child("account").child("interest").child(0).set("null")
		database.child("users").child(uid).child("history").child("messages").child(0).set("null")
		database.child("users").child(uid).child("history").child("service_request").child(0).set("null")
		database.child("users").child(uid).child("history").child("scope_of_work").child(0).set("null")
		database.child("users").child(uid).child("history").child("posts").child(0).set("null")
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

@api.route("/consumer-account-update", methods=['POST'])
def consumerAccountUpdateApi():
	if request.method == "POST":
		print(request.form)
		print(request.files)
		city = request.form['location'] 
		if city == session['account']['city']:
			city = None
		try:
			profile_pic = request.files['profile_pic']
		except Exception as e:
			profile_pic = None
		username = session['account']['username']
		updateDatabase = consumerAccountUpdate(city, profile_pic, username)
		print(updateDatabase)
		return redirect(url_for('profile.home',username=username))

def consumerAccountUpdate(city, profile_pic, username):
	# Getting database
	usersData = dict(database.child("users").get().val())
	# Finding matching url username
	for user in usersData:
		if username == usersData[user]['account']['username']:
			# Checking if city variable is null before interaction with database
			if city != None:
				database.child("users").child(user).child("account").child("city").set(city)
			if profile_pic != None:
				putImg = storage.child("images").child(user).put(profile_pic, user)
				image_url = storage.child("images").child(user).get_url(user)
				database.child("users").child(user).child("account").child("profile_pic_url").set(image_url)
			return 'success'
		else:
			print('not found')
	return 'not found'
# Udpating providers setup
@api.route("/provider-setup-api", methods=['POST'])
def updateSetupApi():
	if request.method == "POST":

		# Website posted
		try:
			username = session['account']['username']

			# Checking if checkbox is empty
			try:
				clean_shoes = request.form.getlist('clean_shoes')
			except Exception as e:
				clean_shoes = 'false'
			try:
				shoe_artist = request.form.getlist('shoe_artist')
			except Exception as e:
				shoe_artist = 'false'


			if clean_shoes == 'false' and shoe_artist == 'false':
				flash('Check what service you provide')
				return redirect(url_for('profile.home',username=username))

			background_info = request.form['background_info']
			write_about_brand = request.form['write_about_brand']

			try:
				profile_pic = request.files['profile_pic']
			except Exception as e:
				flash('Profile Empty')
				return redirect(url_for('profile.home',username=username))

			try:
				describe_services = request.form['describe_services']
			except Exception as e:
				flash('Describe your Services')
				return redirect(url_for('profile.home',username=username))


			try:
				previous_work = request.files.getlist('previous_work')
			except Exception as e:
				flash('Show your previous work')
				return redirect(url_for('profile.home',username=username))

			if background_info == '' or write_about_brand == '':
				flash('Field Empty')
				return redirect(url_for('profile.home',username=username))

			try:
				questions_for_customers = request.form['questions_for_customers']
			except Exception as e:
				flash('Field Empty')
				return redirect(url_for('profile.home',username=username))

			try:
				examples_of_services = request.form['examples_of_services']
			except Exception as e:
				flash('Field Empty')

		except Exception as e:
			print(e)
			print('Not posted from website')
			# Assigning variables equvilent to posted data
			background_info = request.json['background_info']
			clean_shoes = request.json['clean_shoes']
			username = request.json['username']
			shoe_artist = request.json['shoe_artist']
			write_about_brand = request.json['write_about_brand']


		setup = updateSetup(background_info, write_about_brand, clean_shoes, username, shoe_artist, profile_pic, previous_work, describe_services, questions_for_customers, examples_of_services)
		flash(setup)
		return redirect(url_for('profile.home',username=username))
	else:
		return jsonify({'message' : 'failed'})

def updateSetup(background_info, about_brand_or_individual, clean_shoes, username, shoe_artist, profile_pic, previous_work, describe_services, questions_for_customers, examples_of_services):
	print('setup\n\n\n\n\n\n\n\n\n\n\n\n')
	print(clean_shoes)
	print(shoe_artist)

	if not clean_shoes:
		clean_shoes = False
	else:
		clean_shoes = True

	if not shoe_artist:
		shoe_artist = False
	else:
		shoe_artist = True

	image_urls = []
	# Getting database
	usersData = dict(database.child("users").get().val())
	# Finding matching url username
	for user in usersData:
		iteratedUsername = usersData[user]['account']['username']
		if username == iteratedUsername:
			if shoe_artist != True and clean_shoes != True:
				return 'Check your service'
			print('found')
			# Saving data
			database.child("users").child(user).child("account").child("provider").child("background_info").set(background_info)
			database.child("users").child(user).child("account").child("provider").child("about_brand_or_individual").set(about_brand_or_individual)
			database.child("users").child(user).child("account").child("provider").child("describe_services").set(describe_services)
			database.child("users").child(user).child("account").child("provider").child("clean_shoes").set(clean_shoes)
			database.child("users").child(user).child("account").child("provider").child("shoe_artist").set(shoe_artist)
			database.child("users").child(user).child("account").child("provider").child("is_provider").set(True)
			database.child("users").child(user).child("account").child("provider").child("questions_for_customers").set(questions_for_customers)
			database.child("users").child(user).child("account").child("provider").child("examples_of_services").set(examples_of_services)
			database.child("users").child(user).child("account").child("email_confirmed").set(False)
			database.child("users").child(user).child("account").child("setup_complete").set(True)
			putImg = storage.child("images").child(user).put(profile_pic, user)
			image_url = storage.child("images").child(user).get_url(user)
			database.child("users").child(user).child("account").child("profile_pic_url").set(image_url)

			# Importing previous work
			for pic in previous_work:	
				picId = randomString(24)
				putImg = storage.child("images").child("previous_work").child(picId).put(pic, picId)
				image_url = storage.child("images").child("previous_work").child(picId).get_url(picId)
				image_urls.append(image_url)

			database.child("users").child(user).child("account").child("provider").child("previous_work").set(image_urls)

			return 'success'
		else:
			print('not found')
	return 'no users found'


# New post 
@api.route("/new-post-api", methods=['POST'])
def newPostApi():
	if request.method == "POST":
		print('aaa')
		print(request.form)
		print(request.files.getlist('post_pic'))
		# Posted data from website
		try:
			print('aasas')

			# Handling type of post
			service_type = request.form.getlist('service_type')[0]

			brand = request.form.getlist('selected_brand')[0]


			if service_type == 'clean-shoes':
				clean_shoes = True
				shoe_artist = False
			elif service_type == 'design-shoes':
				clean_shoes = False
				shoe_artist = True
			
			if service_type == 'design-shoes':
				# Getting profile pic
				try:
					post_pic = request.files.getlist('post_pic')
					print(post_pic)
					shoeName = request.form['new-post-shoe']
					print('shoeName')
					shoeDescription = request.form['new-post-description']
					print('shoeName')

					shoeTags = request.form['new-post-tags']

					cost = request.form['new-post-design-shoes-cost']
					print('shoeName')

					username = session['account']['username']
					print('shoeName')

				except Exception as e:
					flash('Post a picture of the shoes!')
					return redirect(url_for('explore.home'))
			elif service_type == 'clean-shoes':
				print('---')
				post_pic = 0

				shoeName = ''
				shoeDescription = ''
				shoeTags = ''
				cost = request.form['new-post-clean-shoes-cost']
				username = session['account']['username']
		except Exception as e:
			print(e)
			print('Not posted from website')

			# Assigning variables equvilent to posted data
			shoeName = request.json['shoe_name']
			shoeDescription = request.json['shoe_description']
			cost = request.form['cost']
			username = request.json['username']
			selectedTime = request.json['selected_time']
			clean_shoes = request.json['clean_shoes']
			shoe_artist = request.json['shoe_artist']
		print(post_pic)
		postId = randomString(24)
		post = newPost(shoeName, brand, shoeDescription, cost, username, clean_shoes, shoe_artist, shoeTags, postId, post_pic)
		flash(f'Posted!', 'success')
		return redirect(url_for('posts.home', postId=post))
	else:
		return jsonify({'message' : 'failed'})


def newPost(shoeName, brand, shoeDescription, cost, username, clean_shoes, shoe_artist, shoeTags, postId, post_pics):
	print('setup')
	users = dict(database.child("users").get().val())
	image_urls = []

	# Importing pics in database
	if post_pics != 0:
		for post in post_pics:	
			postPicId = randomString(24)
			putImg = storage.child("images").child("post").child(postPicId).put(post, postPicId)
			image_url = storage.child("images").child("post").child(postPicId).get_url(postPicId)
			image_urls.append(image_url)
	else:
		image_url = ""
		image_urls.append(image_url)
	defaultComment = { "username": "", "comment": "", "date": "" }
	postJson = {"shoe_name": shoeName, "brand" : brand, "shoe_description": shoeDescription, "cost": cost, "username": username, "clean_shoes": clean_shoes, "shoe_artist": shoe_artist, "post_id": postId, "posted_at": time(), "post_pic_urls": image_urls, "comments": [defaultComment], "tags" : shoeTags, "transactions" : 0 }
	
	# updating database history
	for user in users:
		if users[user]['account']['username'] == username:
			if users[user]['history']['posts'][0] == "null":
				database.child("users").child(user).child("history").child("posts").child(0).set(postId)
			else:
				count = 0
				for messageCount in users[user]['history']['posts']:
					count += 1
				database.child("users").child(user).child("history").child("posts").child(count).set(postId)

	database.child("posts").child(postId).set(postJson)
	return 'success'

# New Comment
@api.route("/post-comment-api", methods=['POST'])
def postCommentApi():
	if request.method == "POST":
		# Posted on website
		try:
			print(request.form)
			postId = request.form['post_id']
			comment = request.form['post_comment']
			try:
				commenter_username = session['account']['username']
			except Exception as e:
				print(e)
				flash(f'Not Logged In', 'danger')
				return redirect(url_for('users.login'))
			commentFunc = postComment(postId, comment, commenter_username)
		except Exception as e:
			try:
				print(e)
				# Assigning variables equvilent to posted data
				postId = request.json['post_id']
				comment = request.json['post_comment']
				commenter_username = request.json['commenter_username']
			except Exception as e:
				print(e)
				return redirect(url_for('posts.home', postId=postId))
		return redirect(url_for('posts.home', postId=postId))

def postComment(postId, comment, commenter_username):
	print("NExt")
	posts = database.child("posts").get().val()
	counter = 0
	for post in posts:
		print(post)
		foundPostId = post['post_id']

		# Post Found
		if postId == foundPostId:
			print('aaadsdsds')
			
			# Getting time
			timeNow = datetime.datetime.now()
			formatedDateNow = timeNow.strftime("%b-%d-%Y")
			formatedTimeNow = timeNow.strftime("%I:%M:%S %p")
			finalTime = formatedDateNow + " " + formatedTimeNow
			# Importing important info in dict
			comment = { "username": commenter_username, "comment": comment, "date": finalTime }
			
			# Getting data
			postComments = database.child("posts").child(counter).child("comments").get().val()

			# Getting number of comments
			commentCount = 0
			for i in postComments:
				postComments
				commentCount += 1

			# Posting the comment
			database.child("posts").child(counter).child("comments").child(commentCount).set(comment)
			break
		else:
			counter += 1

	return 'success'

@api.route("/new-message-api", methods=['GET', 'POST'])
def newMessageAPI():
	try:
		print("new message api")
		print("new message apie")
		username = request.form['username-input']
		message = request.form['message-input']
		senderName = session['account']['username']

		# Running new message function
		print("username")
		send = newMessage(username, message, senderName)
		return send
	except Exception as e:
		return 'failed'

def newMessage(username, message, sender):
	print("trying")
	try:
		users = database.child("users").get().val()
		print('gerg')

		messageId = randomString(24)
		print('gerg')

		# Getting time
		timeNow = datetime.datetime.now()
		formatedDateNow = timeNow.strftime("%b-%d-%Y")
		formatedTimeNow = timeNow.strftime("%I:%M:%S %p")
		
		value = 'failed'
		print('gerg')
		# Storing data in users history
		for user in users:
			if users[user]['account']['username'] == username:
				if users[user]['account']['setup_complete'] == True:
					print(username)
					print(sender)
					value = 'sent!'
					if users[user]['history']['messages'][0] == "null":
						database.child("users").child(user).child("history").child("messages").child(0).set(messageId)
					else:
						message_count = 0
						for messageCount in users[user]['history']['messages']:
							message_count += 1
						database.child("users").child(user).child("history").child("messages").child(message_count).set(messageId)
		print(value)
		# Storing data in recievers history
		for user in users:
			if users[user]['account']['username'] == sender:
				if users[user]['account']['setup_complete'] == True:
					value = 'sent!'
					if users[user]['history']['messages'][0] == "null":
						database.child("users").child(user).child("history").child("messages").child(0).set(messageId)
					else:
						message_count = 0
						for messageCount in users[user]['history']['messages']:
							message_count += 1
						database.child("users").child(user).child("history").child("messages").child(message_count).set(messageId)

		messageDict = {"date" : formatedDateNow, "time" : formatedTimeNow, "message" : message, "sender" : username, "reciever" : sender, "created_at": time() }
		database.child("messages").child(messageId).set(messageDict)
		print("\n\n\n\n\n\n")
		print(value)
		return value
	except Exception as e:
		print(e)
		return 'failed'
