# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, Blueprint, request

# Importing firebase connection
from project.firebase_connection import firebaseConnect

# Import time
from time import *

# Importing os for enviroment variables
import os

# FIREBASE AUTHENTICATION
databaseConnect = firebaseConnect()

database = databaseConnect['database']

# Defining Blueprint var
explore = Blueprint('explore', __name__, template_folder='templates', static_folder='static', static_url_path='/static/explore')


@explore.route("/", methods=['GET', 'POST'])
def homepage():
	Launched = os.environ.get('LAUNCHED', None)
	if Launched == 'False':
		return redirect(url_for('admin.early'))
	try:
		# Trying to get data
		getPosts = database.child("posts").get().val()
		getUsers = dict(database.child("users").get().val())
	except Exception as e:
		print(e)
		print('failed to get data for pyrebase')
	# Top providers
	counter = 0
	sortRatingProvider = []
	finalTopProvider = []
	try:
		for user in getUsers:
			if counter == 9:
				break
			print('user')
			userData = getUsers[user]
			print(userData['account']['username'])
			print(userData['account']['setup_complete'])
			if userData['account']['provider']['is_provider'] == True and userData['account']['setup_complete'] == True:
				print('aaaa')
				rating = int(getUsers[user]['account']['rating'])
				sortRatingProvider.append(rating)
				counter += 1
		print(sortRatingProvider)
		print("sortRatingProvider")
		sortRatingProvider.sort()
		for number in sortRatingProvider:
			print(number)
			# Looping again to find high ratings
			for user in getUsers:
				if getUsers[user]['account']['provider']['is_provider'] == True:
					if getUsers[user]['account']['rating'] == number:
						if getUsers[user] not in finalTopProvider:
							finalTopProvider.append(getUsers[user])
	except Exception as e:
		print(e)
		print('no top providers')

	# Recent providers
	print('recent providers')
	counter = 0
	timeList = []
	finalRecentProviders = []
	try:
		for user in getUsers:
			if counter == 9:
				break
			userData = getUsers[user]
			if userData['account']['provider']['is_provider'] == True and userData['account']['setup_complete'] == True:
				print(userData)
				creation = userData['account']['created_at']
				timeNow = time()
				timeDiff = timeNow - creation # In Seconds
				if timeDiff > 864000:
					continue
				print('aa')
				timeList.append(creation)
		print(timeList)
		timeList.sort()
		for number in timeList:
			print(number)
			for user in getUsers:
				if getUsers[user]['account']['created_at'] == number:
					if getUsers[user] not in finalRecentProviders:
						finalRecentProviders.append(getUsers[user])

	except Exception as e:
		print(e)
		print('no recent providers')
	print(finalTopProvider)
	return render_template('explore/home.html', final_top_provider=finalTopProvider, final_recent_provider=finalRecentProviders)

@explore.route("/users", methods=['GET', 'POST'])
def users():
	Launched = os.environ.get('LAUNCHED', None)
	if Launched == 'False':
		return redirect(url_for('admin.early'))
	try:
		# Trying to get data
		getUsers = dict(database.child("users").get().val())
	except Exception as e:
		print(e)
		print('failed to get data for pyrebase')

	try:
		finalTopProvider = []
		for user in getUsers:
			print('user')
			userData = getUsers[user]
			print(userData['account']['setup_complete'])
			if userData['account']['provider']['is_provider'] == True and userData['account']['setup_complete'] == True:
				if userData not in finalTopProvider:
					finalTopProvider.append(userData)
			print(finalTopProvider)
	except Exception as e:
		print(e)
		print('no top providers')

	return render_template('explore/users.html', users=finalTopProvider)

@explore.route("/new-post", methods=['GET', 'POST'])
def newPost():
	Launched = os.environ.get('LAUNCHED', None)
	if Launched == 'False':
		return redirect(url_for('admin.early'))
	try:
		sessionConfirm = session['account']['username']
		if session['account']['provider']['is_provider'] == True:
			return render_template('explore/new-post.html')
		else:
			return redirect(url_for('explore.home'))
	except Exception as e:
		print(e)
		return redirect(url_for('explore.home'))


@explore.route("/explore", methods=['GET', 'POST'])
def home():
	Launched = os.environ.get('LAUNCHED', None)
	if Launched == 'False':
		return redirect(url_for('admin.early'))
	try:
		# Trying to get data
		getPosts = database.child("posts").get().val()
		getUsers = dict(database.child("users").get().val())
	except Exception as e:
		print(e)
		print('failed to get data for pyrebase')

	# Querying type of service
	service_type = 'all'
	try:
		service_type = request.args['service_type']
		print(service_type)
	except Exception as e:
		print(e)
	timeList = []
	finalNewPost = []

	# Recent Post
	try:
		for newPost in getPosts:
			post = getPosts[newPost]
			createdTime = post['posted_at']
			timeNow = time()
			timeDiff = timeNow - createdTime
			print(timeDiff)
			if timeDiff > 2592000:
				continue
			print('a')
			timeList.append(createdTime)
		timeList.sort()
		print('next')
		for number in timeList:
			for listPost in getPosts:
				post = getPosts[listPost]
				print('aaa')
				if post['clean_shoes'] == 'true' or post['clean_shoes'] == True:
					continue
				if post['posted_at'] == number:
					print('aaaaa')
					brand = None
					try:
						brand = request.args['selected_brand']
					except Exception as e:
						print(e)

					maxPrice = None
					try:
						maxPrice = request.args['max_price']
					except Exception as e:
						print(e)

					if brand != None and maxPrice != None:
						if post['brand'] == brand and post['cost'] > maxPrice:
							finalNewPost.append(post)
					elif brand != None and maxPrice == None:
						if post['brand'] == brand:
							finalNewPost.append(post)
					elif brand == None and maxPrice != None:
						if post['cost'] > maxPrice:
							finalNewPost.append(post)
					elif brand == None and maxPrice == None:
							finalNewPost.append(post)


	except Exception as e:
		print(e)
		print('no post')
	print(finalNewPost)
	print('finalNewPost')

	getPostList = []
	# Getting clean shoes posts
	counter = 0
	try:
		for cleanShoes in getPosts:
			post = getPosts[cleanShoes]
			if counter == 9:
				break
			if post['clean_shoes'] == 'true' or post['clean_shoes'] == True:
				getPostList.append(post)
				counter += 1
	except Exception as e:
		print(e)
		print('no post yet')
	return render_template('explore/explore.html', clean_shoes_posts=getPostList, final_new_post=finalNewPost, service_type=service_type)




