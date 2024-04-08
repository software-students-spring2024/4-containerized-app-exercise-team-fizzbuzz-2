"""
Webapp for providing API for communicating with machine learning client
"""

import pymongo
from dotenv import dotenv_values
from flask import Flask, redirect, url_for, json
from datasets import load_dataset
import inference

# Loading development configurations
config = dotenv_values(".env")


def create_app():
    """
    returns a flask app
    """
    # Make flask app
    app = Flask(__name__)
    app.secret_key = config["ML_FLASK_SECRET_KEY"]

    mongo_uri = (
        f'mongodb://{config["MONGODB_USER"]}:'
        f'{config["MONGODB_PASSWORD"]}@{config["MONGODB_HOST"]}:'
        f'{config["MONGODB_PORT"]}?authSource={config["MONGODB_AUTHSOURCE"]}'
    )

    # Make a connection to the database server
    connection = pymongo.MongoClient(mongo_uri)

    # Select a specific database on the server
    # db = connection[config["MONGODB_NAME"]]

    @app.route("/")
    def show():
        """
        redirects to /home
        """
        return redirect(url_for("test"))

    @app.route("/test", methods=["GET", "POST"])
    def test():
        """
        renders the home page
        """
        ds = load_dataset(
            "patrickvonplaten/librispeech_asr_dummy", "clean", split="validation"
        )

        res = {"transcription": inference.speech2textpipeline(ds[0]["audio"]["array"])}

        print(res["transcription"])

        return json.dumps(res)

    try:
        # verify the connection works by pinging the database
        connection.admin.command(
            "ping"
        )  # The ping command is cheap and does not require auth.
        print(" *", "Connected to MongoDB!")  # if we get here, the connection worked!
    except pymongo.errors.OperationFailure as e:
        # the ping command failed, so the connection is not available.
        print(" * MongoDB connection error:", e)  # debug

    return app


if __name__ == "__main__":
    # use the PORT environment variable
    flask_app = create_app()

    print(config["ML_FLASK_PORT"])

    flask_app.run(port=config["ML_FLASK_PORT"])
