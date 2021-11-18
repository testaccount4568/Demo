from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path #
from flask_login import LoginManager

db = SQLAlchemy() # Defines Database
DB_NAME = "database.db"

#Why do we call this "__init__.py" ---- Because whenever you put the "__init__.py" file into a folder it becomes a python package


def create_app(): # defines new function create app with no parameters
    app = Flask(__name__) # Would pass "website.__init__.py" which is the folder name and then the file name, but it just passes the folder name
    # because when "__init__.py" is the file name it is left out of __name__.
    print(__name__)
    app.config["SECRET_KEY"] = "This is the MOST secret key" #Configures the secret key used for encryption for this specific app
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # This stores the location of the database in the app
    db.init_app(app) #initialize database

    from .views import views # imports the blueprint (views) from views.py
    from .auth import auth # imports the blueprint (auth) from auth.py

    app.register_blueprint(views, url_prefix='/') # This registers the blueprint "views" imported above from the file "views.py" so that it 
    # will be called when the url ends in slash.
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note # You cannot start a variable with a period, you import the .models file so that you the database classes are defined

    create_database(app) # Calls the create database function below.

    login_manager = LoginManager() #
    login_manager.login_view = 'auth.login' #
    login_manager.init_app(app) #

    @login_manager.user_loader #
    def load_user(id): #
        return User.query.get(int(id)) # When you use the ".get()" command it automatically looks for the primary key 

    return app #returns the specific flask object we just created


def create_database(app): 
    if not path.exists('website/' + DB_NAME): # If the database does not exist yet, then:
        db.create_all(app=app) # This creates a database called "database.db" by default and that is why we made the variable "DB_NAME" that is 
        # set equal to "database.db"
        print('Created Database!')
