# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, session

# Importing os to encode session variable
import os

# Importing homepage
from project.homepage.views import homepage

# Importing users
from project.users.views import users

# Importing profile
from project.profile.views import profile

# Importing explore
from project.explore.views import explore

# Importing api
from project.api.views import api

# Importing ssl
import ssl

# Importing Time
from datetime import timedelta

ssl._create_default_https_context = ssl._create_unverified_context

# Defing app which is nessisary for flask to run
app = Flask(__name__)

# Registering Blueprints
app.register_blueprint(homepage)

app.register_blueprint(users)

app.register_blueprint(profile)

app.register_blueprint(explore)

app.register_blueprint(api)


# Config
app.config.from_pyfile('app_config.cfg')

@app.route('/')
def root():
	return redirect(url_for(homepage.home))