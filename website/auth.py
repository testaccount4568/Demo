from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.sql.expression import _Null # You imported:
# - "render_template" so that you can render your html template
# - "request" so that you can access request information sent to the server
# - "flash" so that you can flash a message to a webpage
# - "redirect()" so that you can redirect to a url
# - "url_for" to find the url for a route specified by the name of the file and then the route function
from .models import User # You imported .models so that you could import the user database class
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user # You imported:
# - "login_user" to login user and remember that the device has been logged in
# - "login required" allows you to use a decorator to distinguish which page can be accessed by an anonymous user
# - "current_user" shows the current user (relates to user mixin?)
#This is blueprint "auth" is being registered in under app in website

auth = Blueprint('auth', __name__)# this passes the string 'auth' and the file name '__name__' which will be equal to website.auth, 
# it is recommended that you set blueprint to the file name, this file will be loaded from the blueprints registered in the __init__.py code

@auth.route('/login', methods=['GET', 'POST']) # By default, routes only allow GET requests. If you want to allow other requests, then you
def login(): # have to insert the methods of communication that you wish to allow. In this case you wish to allow GET and Post requests.
    
    if current_user.is_authenticated:# If this current user has already been logged in, ...
        return redirect(url_for('views.home'))# ... then redirect this user to the "/home" route in case they have already been authenticated

    elif request.method == 'POST':
        email = request.form.get('email') # Gets the "email" input field from the login form in the login POST request.
        password = request.form.get('password') # Gets the "password" input field from the login form in the login POST request.
        print(email, password) # prints the submitted email and password
        user = User.query.filter_by(email=email).first()

        print(User.query.filter_by(email=email).all()) # with this you found out that this will print all objects with that email
        print(User.query.filter_by(email=email).first()) # This will print the first object with related to this email
        # When the email is not found it will return an empty list for ".all()" and it will return "None" when using ".first()"
        # https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
        if user: # Because it will return "None" or some value this creates a true or false if statement. "None" is the equivalent to "null".
            if check_password_hash(user.password, password): # This will compare the already stored and hashed password with the password from the form 
                # and it will compare to see if the two values are the same.
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) # This stores a cookie on the user device to remember that the user has been authenticated
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    print(current_user)
    return render_template("login.html", user=current_user) # When send this website route (/login) a get request, the server will render the template
    # "login.html" and then send it to the current user 


@auth.route('/logout')
@login_required # This dissallows any Anonymous Users viewing this page
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    if current_user.is_authenticated:# If this current user has already been logged in, ...
        return redirect(url_for('views.home'))# ... then redirect this user to the "/home" route in case they have already been authenticated

    elif request.method == 'POST':
        email = request.form.get('email') # The variable "email" is being defined as the "email" being sent from a post request coming from the user signup page
        #This above is also true for the variables on the following line
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first() # Sets user equal to the "User" SQL database search (.query) for an email that equals "email" 
        if user:
            flash('Email already exists.', category='error') # flash will flash a an error message to the sign-up webpage if the email 
            # already exists. You can name the category whatever you like as long as you know what it means. In this case, it is an error.
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error') # Passes the category "error" so that the webpage can take these parameters 
            # and display the message as an error
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2: # This is what flashes the error if the passwords do not match
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # If all the above conditions have been met then...
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256')) # Sets new user equal to a format
            # that can be stored by the database. It specifies the database "User",  sets each variable in the model equal to the variables which have been 
            # pulled from the form, and it sets the variable "password" equal to a the hashed password and it uses the sha256 algorithm to do so. The algorith
            db.session.add(new_user) # add the new user to the database
            db.session.commit() # commits the new user to the database
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home')) # "redirect" will redirect you to a specified url, and "urlfor" gets the url for a specific route "views.home"
            # This means that you can enter a url of your choice, but it is easier to map it to a specific route function rather than a url which can be changed.

    return render_template("sign_up.html", user=current_user)

