"""
Web-app file
"""

from dotenv import dotenv_values
from flask import Flask, render_template, redirect, url_for

# Loading development configurations
config = dotenv_values(".env")

def create_app():
    '''
        returns a flask app
    '''
    # Make flask app
    app = Flask(__name__)
    app.secret_key = config["FLASK_SECRET_KEY"]

    # # Make a connection to the database server
    # connection = pymongo.MongoClient("class-mongodb.cims.nyu.edu", 27017,
    #                                 username = config["USERNAME"],
    #                                 password = config["PASSWORD"],
    #                                 authSource = config["AUTHSOURCE"])

    # # Select a specific database on the server
    # db = connection[config["MONGO_DBNAME"]]

    # try:
    #     # verify the connection works by pinging the database
    #     connection.admin.command("ping")  # The ping command is cheap and does not require auth.
    #     print(" *", "Connected to MongoDB!")  # if we get here, the connection worked!
    # except Exception as e:
    #     # the ping command failed, so the connection is not available.
    #     print(" * MongoDB connection error:", e)  # debug

    # Main Pages

    @app.route('/')
    def show():
        '''
            redirects to /home
        '''
        return redirect(url_for('home'))

    @app.route('/home', methods=["GET", "POST"])
    def home():
        '''
            renders the home page
        '''
        return render_template("home.html")

    return app


if __name__ == '__main__':
    # use the PORT environment variable
    flask_app = create_app()

    flask_app.run(port=config["FLASK_PORT"])
