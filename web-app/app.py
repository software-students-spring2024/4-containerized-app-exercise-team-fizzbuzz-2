"""
Web-app
"""

from flask import Flask, render_template, jsonify
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

    @app.route("/api/cards")
    def cards():
        sentences = ["test", "words"]
        resp = jsonify({"cards": sentences})
        resp.headers.add("Access-Control-Allow-Origin", "*")
        return resp

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(port=config["WEBAPP_FLASK_PORT"])
