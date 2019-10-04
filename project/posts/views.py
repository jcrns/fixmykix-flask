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
posts = Blueprint('posts', __name__, template_folder='templates', static_folder='static', static_url_path='/static/posts')

from project.__init__ import Launched

# Post function
@posts.route("/post/<postId>", methods=['GET', 'POST'])
def home(postId):
	Launched = os.environ.get('LAUNCHED', None)
	if Launched == 'False':
		return redirect(url_for('admin.early'))
	try:
		postsData = database.child("posts").get().val()
		users = database.child("users").get().val()
		for getPost in postsData:
			post = postsData[getPost]
			if post['post_id'] == postId:
				print('found')
				cost = post['cost']
				shoe_name = post['shoe_name']
				shoe_description = post['shoe_description']
				username = post['username']
				clean_shoes = post['clean_shoes']
				shoe_artist = post['shoe_artist']
				post_pic_urls = post['post_pic_urls']
				post_id = post['post_id']
				comments = post['comments']
		print('aaa')
		for user in users:
			print(user)
			if username == users[user]['account']['username']:
				city = users[user]['account']['city']

				# Checking if post was requested
				try:
					print('\n\n\n\n\n\n')
					requested = False
					userInSession = session['user']
					uid = userInSession['localId']
					serviceRequestId = database.child("users").child(uid).child("history").child("service_request").get().val()
					for serviceId in serviceRequestId:
						serviceRequestDict = dict(database.child("service_request").child(serviceId).get().val())
						serviceRequestPostId = serviceRequestDict['post_id']
						if serviceRequestPostId == post_id:
							requested = True
					print('hhhh\n\n\n\n\n\n')

				except Exception as e:
					print("not signed in")
					print(e)
				return render_template('posts/post.html', cost=cost, shoe_name=shoe_name, shoe_description=shoe_description, username=username, clean_shoes=clean_shoes, shoe_artist=shoe_artist, post_pic_urls=post_pic_urls, post_id=post_id, comments=comments, city=city, requested=requested)
	except Exception as e:
		print(e)
		return redirect(url_for('explore.home'))
