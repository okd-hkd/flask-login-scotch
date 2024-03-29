
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from .models import User
from . import db


# @bp.route(‘/’)は、url_prefix=’/auth’と結合され、 @app.route(‘/users/’)を登録したのと同じことになる。
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login_post():

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # Return the first result of this Query or None
    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page
    
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup', methods=['POST'])

def signup_post():
    email = request.form.get('email')
    name = request.form.get('name') 
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.

    # Hash a password with the given method and salt with a string of the given length.
    # The format of the string returned includes the method that was used so that check_password_hash() can check the hash.

    # return formt of generate_password_hash: method$salt$hash
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/logout')
def logout():
    return 'Logout'