from flask import Flask, render_template, request, jsonify

def create_app():
    """
    returns a flask app
    """
    app = Flask(__name__)
    # app.secret_key = "your_secret_key"  # Set a secret key for session management

    # Main Pages
    @app.route("/")
    def show():
        """
        redirects to /home
        """
        return render_template("home.html")

    @app.route("/home", methods=["GET", "POST"])
    def home():
        """
        renders the home page
        """
        return render_template("home.html")

    @app.route('/upload-audio', methods=['POST'])
    def upload_audio():
        """
        handles audio file upload
        """
        audio_file = request.files['audio']
        # For testing, just return a success message
        return jsonify({"message": "Audio received successfully!"})
    
    @app.route('/predict', methods=['POST'])
    def predict():
        """
        handles prediction
        """
        # for testing, just return a success message, until we implement the actual prediction
        return jsonify({"message": "Prediction successful!"})

    return app
