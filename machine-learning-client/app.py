"""
Webapp for providing API for communicating with machine learning client
"""

import os
from bson.objectid import ObjectId
from dotenv import dotenv_values
from flask import Flask, jsonify, request
import librosa
from ffmpeg import FFmpeg
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

    @app.route("/api/transcribe", methods=["POST"])
    def upload_audio():
        """
        handles audio file upload
        """

        audio_file = request.files.get("audio")

        print(audio_file)

        # print(audio_file.filename)

        if audio_file:
            # Save the file on the server.
            audio_file.stream.seek(0)
            file_name = "audio" + str(ObjectId())
            audio_file.save(file_name + ".raw")

            print("Managed")

            saved = False

            while not saved:
                try:
                    with open(file_name + ".raw", encoding="utf-8") as _:
                        saved = True
                except OSError:
                    saved = False

            ffmpeg = (
                FFmpeg()
                .option("y")
                .input(file_name + ".raw")
                .output(
                    file_name + ".mp3",
                    {"codec:v": "libx264"},
                    vf="scale=1280:-1",
                    preset="veryslow",
                    crf=24,
                )
            )

            print("To")

            ffmpeg.execute()

            # data, samplerate = sf.read('test.mp3')
            data, sampling_rate = librosa.load(file_name + ".mp3", sr=16000)

            os.remove(file_name + ".raw")

            transcription = inference.speech2textpipeline(data, sampling_rate)[0]
            print(transcription)

            resp = jsonify({"transcription": transcription})
            resp.headers.add("Access-Control-Allow-Origin", "*")
            return resp

        return jsonify({"error": "Smthn went wrong"})

    return app


if __name__ == "__main__":
    # use the PORT environment variable
    inference.test()

    flask_app = create_app()

    print(config["ML_FLASK_PORT"])

    flask_app.run(port=config["ML_FLASK_PORT"])
