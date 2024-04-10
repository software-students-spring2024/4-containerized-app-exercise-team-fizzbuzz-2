"""
Web-app
"""

from flask import Flask, render_template
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

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(port=config["WEBAPP_FLASK_PORT"])
