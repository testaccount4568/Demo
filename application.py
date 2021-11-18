from website import create_app

application = create_app()
# This calls __init__.py and runs create application which creates a new Flask class object that gets configured in init.py and then returns it to
# this class so that if this class so that the next few lines can be run. These next lines will make sure that if the file is imported and
# therfore not the main class, then the application will not run

if __name__ == '__main__': # if the __name__ of this file equals the "__main__" file, then run the imported create_app() file
    #, but if this is being imported then don't run the application
    application.run(debug=True) # Debug = true means that anytime there is a saved change made to any of these files then the server will automatically rerun