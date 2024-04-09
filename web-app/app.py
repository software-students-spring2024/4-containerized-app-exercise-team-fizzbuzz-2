from flask import Flask, render_template, request, jsonify

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

    @app.route("/upload-audio", methods=["POST"])
    def upload_audio():
        """
        handles audio file upload
        # """
        audio_file = request.files.get("audio")
        # print(request.form)
        # For testing, just return a success message
        
        resp=jsonify({"message": request.form})
        resp.headers.add('Access-Control-Allow-Origin','*')
        return resp

    @app.route("/predict", methods=["POST"])
    def predict():
        """
        handles prediction
        """
        # for testing, just return a success message, until we implement the actual prediction
        return jsonify({"message": "Prediction successful!"})

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(port=config["WEBAPP_FLASK_PORT"])
