"""
Web-app
"""

import json
import pymongo
from bson.objectid import ObjectId
from bson import json_util
from flask import Flask, render_template, jsonify, session
from dotenv import dotenv_values
from nested_collections import NestedCollection
from setup_mg import end_mgd, start_mgd
from transcription import Transcription
from prompt import Prompt

config = dotenv_values(".env")


def create_app():
    """
    returns a flask app
    """
        # Make flask app
    app = Flask(__name__)
    app.secret_key = config["WEBAPP_FLASK_SECRET_KEY"]

    mongo_uri = (
        f'mongodb://{config["MONGODB_USER"]}:'
        f'{config["MONGODB_PASSWORD"]}@{config["MONGODB_HOST"]}:'
        f'{config["MONGODB_PORT"]}?authSource={config["MONGODB_AUTHSOURCE"]}'
    )

    print("not done")

    # Make a connection to the database server
    connection = pymongo.MongoClient(mongo_uri)

    print("Done")

    print(connection)

    # Select a specific database on the server
    db = connection[config["MONGODB_NAME"]]

    if not db.nested_collections.find_one({"name": "SE_Project4"}):
        db.nested_collections.insert({"name": "SE_Project4", "children": []})
    se4_db = NestedCollection("SE_Project4", db)

    end_mgd(db, se4_db)
    start_mgd(se4_db)

    try:
        # verify the connection works by pinging the database
        connection.admin.command(
            "ping"
        )  # The ping command is cheap and does not require auth.
        print(" *", "Connected to MongoDB!")  # if we get here, the connection worked!
    except pymongo.errors.OperationFailure as e:
        # the ping command failed, so the connection is not available.
        print(" * MongoDB connection error:", e)  # debug

    @app.route("/")
    def home():
        """
        shows home page
        """

        if not session.get("associated_id"):
            session["associated_id"] = json.loads(json_util.dumps(ObjectId()))
            print(session["associated_id"])
            print("Generating new session id")

        return render_template("home.html", home=True)

    @app.route("/scores")
    def score():
        """
        shows the score associated with this session
        """

        # Area where we get the scores associated with this ID
        scores = []
        scorings = Transcription.transcriptions.find({'scoring.cookie': session['associated_id']}, {'_id': None, 'inputed': 1, 'scoring.score': 1})
        for each_score in scorings:
            scores.append({'key': each_score['inputted'], 'value': each_score['scoring.score']})

        scores = [
            {"key": "This is a sentence", "value": "5/7"},
            {"key": "This is a another sentence", "value": "5/6"},
            {"key": "This is a yet another sentence", "value": "4/4"},
            {"key": "One more", "value": "1/1"},
        ]

        return render_template(
            "scores.html", home=False, foundAny=len(scores) > 0, scores=scores
        )

    @app.route("/api/cards")
    def cards():
        prompts = []
        sentences = list(Prompt.prompts.find({}, {'_id': None, 'prompt': 1}).sort({'$natural':1}).limit(2))
        for each_prompt in sentences:
            prompts.append(each_prompt['prompt'])
        resp = jsonify({"cards": prompts})
        resp.headers.add("Access-Control-Allow-Origin", "*")
        return resp

    @app.route("/api/store-scores")
    def store():
        """
        storing the recorded scores in mongodb
        """

        # find smthn that matches session["associated_id"]

        return jsonify({"message": "successfully saved"})

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(port=config["WEBAPP_FLASK_PORT"])
