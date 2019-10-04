# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, session, request

# Adding socketio for realtime messaging
from flask_socketio import SocketIO, send, emit

# Importing os to encode session variable
import os

# Importing homepage
from project.about.views import about

# Importing admin
from project.admin.views import admin

# Importing users
from project.users.views import users

# Importing profile
from project.profile.views import profile

# Importing explore
from project.explore.views import explore

# Importing post
from project.posts.views import posts

# Importing api
from project.api.views import api

# Importing ssl
import ssl

# Importing Time
from datetime import timedelta

ssl._create_default_https_context = ssl._create_unverified_context

Launched = False

# Defing app which is nessisary for flask to run
app = Flask(__name__)

# Registering Blueprints
app.register_blueprint(about)

app.register_blueprint(users)

app.register_blueprint(profile)

app.register_blueprint(explore)

app.register_blueprint(api)

app.register_blueprint(posts)

app.register_blueprint(admin)

socketio = SocketIO(app)

# Config
SESSION_TYPE = 'filesystem'

app.config.from_pyfile('app_config.cfg')

users = {}

# SocketIO functions
@socketio.on('username', namespace='/messages')
def handleUsername(username):
	print("username")
	print(username)
	if username == session['account']['username']:
		users[username] = request.sid
	print(users)

@socketio.on('private_message', namespace='/messages')
def handleMessage(msg):
	print('aaaaa')
	usernameSessionId = users[msg['username']]
	message = msg['message']
	messageDict = { "message": message, "username" : session['account']['username'] }
	emit('new_message', messageDict, room=usernameSessionId)


@socketio.on('service_request', namespace='/messages')
def serviceRequestSocket(obj):
	print('\n\n\n')
	usernameSessionId = users[obj['username']]




@app.route('/')
def root():
	return redirect(url_for(homepage.home))