"""
Web-app file
"""

import pymongo
from dotenv import dotenv_values
from flask import Flask, render_template, redirect, url_for

# Loading development configurations
config = dotenv_values(".env")


def create_app():
    """
    returns a flask app
    """
    # Make flask app
    app = Flask(__name__)
    app.secret_key = config["WEBAPP_FLASK_SECRET_KEY"]

    mongo_uri = (f'mongodb://{config["MONGODB_USER"]}:'
                f'{config["MONGODB_PASSWORD"]}@{config["MONGODB_HOST"]}:'
                f'{config["MONGODB_PORT"]}?authSource={config["MONGODB_AUTHSOURCE"]}')

    # Make a connection to the database server
    connection = pymongo.MongoClient(mongo_uri)

    # Select a specific database on the server
    # db = connection[config["MONGODB_NAME"]]

    try:
        # verify the connection works by pinging the database
        connection.admin.command("ping")  # The ping command is cheap and does not require auth.
        print(" *", "Connected to MongoDB!")  # if we get here, the connection worked!
    except pymongo.errors.OperationFailure as e:
        # the ping command failed, so the connection is not available.
        print(" * MongoDB connection error:", e)  # debug

    # Main Pages

    @app.route("/")
    def show():
        """
        redirects to /home
        """
        return redirect(url_for("home"))

    @app.route("/home", methods=["GET", "POST"])
    def home():
        """
        renders the home page
        """
        return render_template("home.html")

    return app


if __name__ == "__main__":
    # use the PORT environment variable
    flask_app = create_app()

    flask_app.run(port=config["WEBAPP_FLASK_PORT"])
