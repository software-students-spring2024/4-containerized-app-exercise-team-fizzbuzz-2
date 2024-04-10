"""
Webapp for providing API for communicating with machine learning client
"""

import pymongo
from dotenv import dotenv_values
from flask import Flask, jsonify, request
import librosa
from ffmpeg import FFmpeg
import inference
from nested_collections import NestedCollection

# from Transcription import *
# from Prompt import *
from setup_mg import end_mgd, start_mgd

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
    except pymongo.errors.OperationFailure as err:
        # the ping command failed, so the connection is not available.
        print(" * MongoDB connection error:", err)  # debug

    @app.route("/api/transcribe", methods=["POST"])
    def upload_audio():
        """
        handles audio file upload
        """

        # audio_file = request.files.get('audio')
        # print(audio_file)
        # file_type = request.form.get("type", "wav")
        # print(file_type)

        audio_file = request.files.get("audio")

        print(audio_file)

        # print(audio_file.filename)

        if audio_file and audio_file.filename != "":
            # Save the file on the server.
            audio_file.stream.seek(0)
            audio_file.save("test.raw")

            print("Managed")

            saved = False

            while not saved:
                try:
                    with open("test.raw", encoding="utf-8") as _:
                        saved = True
                except OSError:
                    saved = False

            ffmpeg = (
                FFmpeg()
                .option("y")
                .input("test.raw")
                .output(
                    "test.mp3",
                    {"codec:v": "libx264"},
                    vf="scale=1280:-1",
                    preset="veryslow",
                    crf=24,
                )
            )

            print("To")

            ffmpeg.execute()

            # data, samplerate = sf.read('test.mp3')
            yee, see = librosa.load("test.mp3", sr=16000)
            print(yee, see)

            transcription = inference.speech2textpipeline(yee, see)
            print(transcription)

            resp = jsonify({"message": transcription})
            resp.headers.add("Access-Control-Allow-Origin", "*")
            return resp

        return jsonify({"Error": "Smthn went wrong"})

    return app


if __name__ == "__main__":
    # use the PORT environment variable
    inference.test()

    flask_app = create_app()

    print(config["ML_FLASK_PORT"])

    flask_app.run(port=config["ML_FLASK_PORT"])
