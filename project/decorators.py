# Importing all needed Flask classes
from flask import Flask, session, flash, redirect, url_for

# Importing wraps
from functools import wraps


# Creating logged in required function
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'account' in session:
            return f(*args, **kwargs)
        else:
            # Displaying flash function
            flash("You need to login first")

            # Redirecting User
            return redirect(url_for('users.login'))
    return wrap