# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, Blueprint, request

# Importing firebase connection
from project.firebase_connection import firebaseConnect

# Import time
from time import *

# FIREBASE AUTHENTICATION
databaseConnect = firebaseConnect()

database = databaseConnect['database']

# Defining Blueprint var
explore = Blueprint('explore', __name__, template_folder='templates', static_folder='static', static_url_path='/static/explore')

@explore.route("/explore", methods=['GET', 'POST'])
def home():
	try:
		# Trying to get data
		getPost = database.child("posts").get().val()
		getUsers = dict(database.child("users").get().val())
	except Exception as e:
		print(e)
		print('failed to get data for pyrebase')

	timeList = []
	finalNewPost = []
	# Recent Post
	try:
		for post in getPost:
			createdTime = post['posted_at']
			timeNow = time()
			timeDiff = timeNow - createdTime
			print(timeDiff)
			if timeDiff > 864000:
				continue
			print('a')
			timeList.append(createdTime)
		timeList.sort()
		for number in timeList:
			for post in getPost:
				if post['posted_at'] == number:
					finalNewPost.append(post)
	except Exception as e:
		print(e)
		print('no post')

	print(finalNewPost)
	print('finalNewPost')
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
			if userData['account']['provider']['is_provider'] == True:
				rating = int(getUsers[user]['account']['rating'])
				sortRatingProvider.append(rating)
				counter += 1

		sortRatingProvider.sort()
		for number in sortRatingProvider:
			print(number)
			# Looping again to find high ratings
			for user in getUsers:
				if getUsers[user]['account']['provider']['is_provider'] == True:
					if getUsers[user]['account']['rating'] == number:
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
			if userData['account']['provider']['is_provider'] == True:
				creation = userData['account']['created_at']
				timeNow = time()
				timeDiff = timeNow - creation # In Seconds
				if timeDiff > 864000:
					continue
				print('aa')
				timeList.append(creation)
		timeList.sort()
		for number in timeList:
			print(number)
			for user in getUsers:
				if getUsers[user]['account']['created_at'] == number:
					print('ppp')
					finalRecentProviders.append(getUsers[user])

	except Exception as e:
		print(e)
		print('no recent providers')

	getPostList = []
	# Getting clean shoes posts
	counter = 0
	try:
		for post in getPost:
			if counter == 9:
				break
			if post['clean_shoes'] == 'true' or post['clean_shoes'] == True:
				getPostList.append(post)
				counter += 1
	except Exception as e:
		print(e)
		print('no post yet')
	return render_template('explore/explore.html', clean_shoes_posts=getPostList, final_top_provider=finalTopProvider, final_recent_provider=finalRecentProviders, final_new_post=finalNewPost)