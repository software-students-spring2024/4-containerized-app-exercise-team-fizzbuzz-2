from flask import Flask, render_template, request, jsonify
import io
import soundfile as sf
from ffmpeg import FFmpeg

from dotenv import dotenv_values

config = dotenv_values(".env")


def create_app():
    """
    returns a flask app
    """
    app = Flask(__name__)

    @app.route("/")
    def show():
        """
        redirects to /home
        """
        return render_template("home.html")
    
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

        if audio_file and audio_file.filename != '': 
            # Save the file on the server.            
            audio_file.stream.seek(0)
            audio_file.save('bob.raw')

            print("Managed")

            saved = False

            while not saved:
                try:
                    open('bob.raw')
                    saved = True
                except:
                    saved = False
            
            open('bob.raw')

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
            # print(data)

            # transcription = inference.speech2textpipeline(data, samplerate)
            # print(transcription)

            resp=jsonify({"message": "Bob"})
            resp.headers.add('Access-Control-Allow-Origin','*')
            return resp
        else:
            print("WEIRD")

        return None

    return app

    # @app.route("/upload-audio", methods=["POST"])
    # def upload_audio():
    #     """
    #     handles audio file upload
    #     """

    #     # audio_file = request.files.get('audio')
    #     # print(audio_file)
    #     # file_type = request.form.get("type", "wav")
    #     # print(file_type)

    #     file = request.files.get("audio")

    #     if file and file.filename != '': 
    #         # Save the file on the server.
    #         file.stream.seek(0)
    #         file.save(file.filename)
    #         data, samplerate = sf.read(file.filename)

    #     resp=jsonify({"message": request.form})
    #     resp.headers.add('Access-Control-Allow-Origin','*')
    #     return resp

    # @app.route("/predict", methods=["POST"])
    # def predict():
    #     """
    #     handles prediction
    #     """
    #     # for testing, just return a success message, until we implement the actual prediction
    #     return jsonify({"message": "Prediction successful!"})

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(port=config["WEBAPP_FLASK_PORT"])
