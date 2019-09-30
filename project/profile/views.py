# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, Blueprint, request

# Importing firebase connection
from project.firebase_connection import firebaseConnect

# Importing Login Required
from project.decorators import login_required

# Importing os for enviroment variables
import os

# FIREBASE AUTHENTICATION
databaseConnect = firebaseConnect()

database = databaseConnect['database']

# Creating blueprint for app
profile = Blueprint('profile', __name__, static_folder='static' , template_folder='templates', static_url_path='/static/profile')


# Profile function
@profile.route("/profile/<username>", methods=['GET', 'POST'])
# @login_required
def home(username):
	Launched = os.environ.get('LAUNCHED', None)
	if Launched == 'False':
		return redirect(url_for('admin.early'))

	try:
		# Getting database
		usersData = dict(database.child("users").get().val())

		postsData = dict(database.child("posts").get().val())

	except Exception as e:
		usersData = None
		postsData = None

	# Trying to define variable
	try:
		sessionUsername = session['account']['username']
		userInSession = session['user']
		uid = userInSession['localId']
		userAccount = dict(database.child("users").child(uid).child("account").get().val())
		session['account'] = userAccount
	except Exception as e:
		print('uu')
		print(e)
		sessionUsername = ''

	print(sessionUsername)
	print(username)
	# Logged In User Profile
	if sessionUsername == username:
		print('datasddxbase')
		title = username + " - FixMyKix"
		try:
			messageHistory = database.child("users").child(uid).child("history").child("messages").get().val()
			print(messageHistory)
			# Getting Messages
			frontendMessagseList = []
			messageParty = []
			for message in messageHistory:
				messageDict = dict(database.child("messages").child(message).get().val())
				sender = messageDict['sender']
				if sender not in messageParty:
					if sender != sessionUsername:
						messageParty.append(sender)
				
				reciever = messageDict['reciever']
				if reciever not in messageParty:
					if reciever != sessionUsername:
						messageParty.append(reciever)

			for party in messageParty:
				frontendMessageDict = {}
				frontendMessageDict['party'] = party
				print("aarrf")
				messageList = []
				for message in messageHistory:
					messageDict = dict(database.child("messages").child(message).get().val())
					print(messageDict)
					print('aa')
					if messageDict['sender'] == party or messageDict['reciever'] == party:
						messageList.append(messageDict)

					frontendMessageDict['messages'] = messageList
				frontendMessagseList.append(frontendMessageDict)
			print(messageParty)
			print("messageParty")
			print(frontendMessagseList)
		except Exception as e:
			print("message format failed")
			print(e)
			frontendMessagseList = [{ "messages" : { "sender": "null", "reciever":"null", "message":"null", "date": "null", "time" : "null" }, "party" : "null"}]
		
		try:
			# Getting Service Request
			print('sssssss')
			serviceRequest = database.child("users").child(uid).child("history").child("service_request").get().val()
			serviceRequestList = []
			print('sdfergerg')
			for request in serviceRequest:
				print('sergwergsdfergerg')
				print(request)
				serviceRequestData = dict(database.child("service_request").child(request).get().val())
				print(serviceRequestData)
				serviceRequestList.append(serviceRequestData)
		except Exception as e:
			print("service_request error")
			print(e)
			serviceRequestList = [{ "sender": "null", "reciever":"null", "post_id":"null", "date": "null", "time" : "null", "title" : "null" }]

		try:
			# Getting Scope of Work
			scopeOfWork = database.child("users").child(uid).child("history").child("scope_of_work").get().val()
			scopeOfWorkList = []
			for scope in scopeOfWork:
				scopeOfWorkDict = dict(database.child("scope_of_work").child(scope).get().val())
				scopeOfWorkList.append(scopeOfWorkDict)
		except Exception as e:
			print(e)
			scopeOfWorkList = [{ "sender": "null", "reciever":"null", "post_id":"null", "date": "null", "time" : "null", "title" : "null", "services_description" : "null" }]

		# Handling Parties
		partyList = []
		try:
			for serviceRequest in serviceRequestList:
				print("serviceRequest")
				if serviceRequest['time'] != 'null':		
					if serviceRequest['reciever'] != session['account']['username']:
						if serviceRequest['reciever'] not in partyList:
							partyList.append(serviceRequest['reciever'])
					elif serviceRequest['sender'] != session['account']['username']:
						if serviceRequest['sender'] not in partyList:
							partyList.append(serviceRequest['sender'])
			for message in frontendMessagseList:
				print("message")
				print(message)
				if message['time'] != 'null':
					if message['party'] not in partyList:
						partyList.append(message['party'])
		except Exception as e:
			print(e)
			print('no parties')

		userPostList = []

		try:
			for post in postsData:
				print("efeferfdfpost")
				postDict = postsData[post]
				print(postDict)
				if postDict['username'] == username:
					userPostList.append(postDict)
			print(userPostList)
		except Exception as e:
			print("e")
			print(e)

		print("partyList")
		print(partyList)
		return render_template('profile/profile.html',viewing=False, title=title, messages=frontendMessagseList, parties=partyList, service_request=serviceRequestList, scope_of_work=scopeOfWorkList, posts=userPostList)
	else:
		# Viewing a profile
		print('xbase')

		# Finding matching url username
		for user in usersData:
			# print('xbbase')

			# Getting username
			iteratedUsername = usersData[user]['account']['username']
			print(iteratedUsername)
			print(user)
			# Checking for matching username
			if iteratedUsername == username:
				print("founsdd")
				# Getting Public Data
				email = usersData[user]['account']['email']
				number_of_transactions = usersData[user]['account']['number_of_transactions']
				rating = usersData[user]['account']['rating']
				city = usersData[user]['account']['city']
				setup_complete = usersData[user]['account']['setup_complete']
				profile_pic_url = usersData[user]['account']['profile_pic_url']
				title = username + " - FixMyKix"
				userPostList = []
				try:
					for post in postsData:
						if post['username'] == username:
							userPostList.append(post)
				except Exception as e:
					print(e)
					print('not post')
				if setup_complete == True:
					return render_template("profile/profile.html", viewing=True, title=title, email=email, username=username, number_of_transactions=number_of_transactions, rating=rating, city=city, posts=userPostList, profile_pic_url=profile_pic_url) 
				else:
					print('not setup')
					flash(f'Url not found', 'text-danger')
					return redirect(url_for('explore.home'))
			else:
				print('not found')

		# Redirecting user for unfound url
		# flash('Url not found', 'text-danger')
		return redirect(url_for('homepage.home'))
