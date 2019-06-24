# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, Blueprint, request

# Defining Blueprint var
homepage = Blueprint('homepage', __name__, template_folder='templates', static_folder='static', static_url_path='/static/homepage')

@homepage.route("/", methods=['GET', 'POST'])
def home():
	return render_template('homepage/homepage.html')