# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, Blueprint, request

# Importing os for enviroment variables
import os

# Defining Blueprint var
about = Blueprint('about', __name__, template_folder='templates', static_folder='static', static_url_path='/static/about')

@about.route("/about", methods=['GET', 'POST'])
def home():
	Launched = os.environ.get('LAUNCHED', None)
	print(Launched)
	if Launched == 'True':
		return render_template('about/about.html', launched=Launched)
	return render_template('about/about-early.html',  launched=False)