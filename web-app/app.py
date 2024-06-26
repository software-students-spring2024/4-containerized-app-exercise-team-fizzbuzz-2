"""
Web-app
"""

import json
import pymongo
from bson.objectid import ObjectId
from bson import json_util
from flask import Flask, render_template, jsonify, session, request
from dotenv import dotenv_values
from nested_collections import NestedCollection
from setup_mg import end_mgd, start_mgd
from transcription import Transcription, Scoring
from prompt import Prompt

config = dotenv_values(".env")


async def connect_to_mongo(app):
    """
    Connects to mongoDB asyncronously
    """

    mongo_uri = ""

    # if config["MODE"] == "test":
    #     mongo_uri = "mongodb://127.0.0.1:27017/?directConnection=true"
    #     print(mongo_uri)
    # else:
    mongo_uri = (
        f'mongodb://{config["MONGODB_USER"]}:'
        f'{config["MONGODB_PASSWORD"]}@{config["MONGODB_HOST"]}:'
        f'{config["MONGODB_PORT"]}?authSource={config["MONGODB_AUTHSOURCE"]}'
    )

    # Make a connection to the database server
    connection = pymongo.MongoClient(mongo_uri)

    try:
        # verify the connection works by pinging the database
        connection.admin.command(
            "ping"
        )  # The ping command is cheap and does not require auth.
        print(" *", "Connected to MongoDB!")  # if we get here, the connection worked!
    except pymongo.errors.OperationFailure as e:
        # the ping command failed, so the connection is not available.
        print(" * MongoDB connection error:", e)  # debug

    # Select a specific database on the server
    db = connection[config["MONGODB_NAME"]]

    print(db.test_collection.find_one({}))

    if not db.nested_collections.find_one({"name": "SE_Project4"}):
        db.nested_collections.insert_one({"name": "SE_Project4", "children": []})
    se4_db = NestedCollection("SE_Project4", db)

    start_mgd(se4_db)
    end_mgd(db, se4_db)
    if not db.nested_collections.find_one({"name": "SE_Project4"}):
        db.nested_collections.insert_one({"name": "SE_Project4", "children": []})
    se4_db = NestedCollection("SE_Project4", db)
    se4_db = NestedCollection("SE_Project4", db)
    start_mgd(se4_db)

    app.connected = True
    app.db = db
    # app.se4_db = se4_db


def create_app():
    """
    returns a flask app
    """
    # Make flask app
    app = Flask(__name__)
    app.secret_key = config["WEBAPP_FLASK_SECRET_KEY"]

    app.connected = False

    app.ensure_sync(connect_to_mongo)(app)

    @app.route("/")
    def home():
        """
        shows home page
        """

        if not session.get("associated_id"):
            session["associated_id"] = json.loads(json_util.dumps(ObjectId()))
            print(session["associated_id"].get("$oid"))
            print("Generating new session id")

        return render_template("home.html", home=True)

    @app.route("/scores")
    def score():
        """
        shows the score associated with this session
        """

        # Area where we get the scores associated with this ID
        for thing in Transcription.transcriptions.find({}):
            print(thing)

        scores = []
        scorings = Transcription.transcriptions.find(
            {"cookie": ObjectId(session["associated_id"].get("$oid"))},
            {"_id": None, "inputed": 1, "score": 1},
        )

        if scorings:
            for each_score in scorings:
                scores.append(
                    {"key": each_score["inputed"], "value": each_score["score"]}
                )

        # scores = [
        #     {"key": "This is a sentence", "value": "5/7"},
        #     {"key": "This is a another sentence", "value": "5/6"},
        #     {"key": "This is a yet another sentence", "value": "4/4"},
        #     {"key": "One more", "value": "1/1"},
        # ]

        return render_template(
            "scores.html", home=False, foundAny=len(scores) > 0, scores=scores
        )

    @app.route("/api/cards")
    def cards():
        prompts = []
        sentences = list(
            Prompt.prompts.find({}, {"_id": None, "prompt": 1})
            .sort({"$natural": 1})
            .limit(2)
        )
        for each_prompt in sentences:
            prompts.append(each_prompt["prompt"])
        resp = jsonify({"cards": prompts})
        resp.headers.add("Access-Control-Allow-Origin", "*")
        return resp

    @app.route("/api/store-score", methods=["POST"])
    def store():
        """
        storing the recorded scores in mongodb
        """

        # find smthn that matches session["associated_id"]

        if request.method == "POST":
            # getting input with name = fname in HTML form
            inputed = request.form.get("inputed")
            # getting input with name = lname in HTML form
            score = request.form.get("score-input")

            Transcription(
                inputed,
                "",
                Scoring(ObjectId(str(session["associated_id"].get("$oid"))), score),
                "",
            )

        return jsonify({"message": "successfully saved"})

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(port=config["WEBAPP_FLASK_PORT"])
