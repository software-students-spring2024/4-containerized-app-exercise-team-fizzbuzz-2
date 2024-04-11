"""
    Tests for functions used in the webapp
"""

import pytest
from app import create_app, Prompt, Transcription, Scoring, end_mgd


class Tests:
    """
    Class for handling tests
    """

    @pytest.fixture
    def app(self):
        """
        Creates an app
        """

        app = create_app()

        app.config.update(
            {
                "TESTING": True,
            }
        )

        assert app.connected

        # other setup can go here

        yield app

        # clean up / reset resources here
        if not hasattr(app, "db"):
            app.db = None
        if not hasattr(app, "se4_db"):
            app.se4_db = None
        end_mgd(app.db, app.se4_db)

    # @pytest.fixture()
    # def client(self, app):
    #     """
    #     Copied
    #     """
    #     return app.test_client()

    # @pytest.fixture()
    # def runner(self, app):
    #     """
    #     Copied
    #     """
    #     return app.test_cli_runner()

    def test_prompt(self, app):
        """
        Copied
        """

        print(app)

        p = Prompt("ABC", 5, 4)

        found = Prompt.prompts.find_one({"_id": p.idef, "prompt": "ABC"})

        for f in found:
            print(f)

        assert found

    def test_transcript(self, app):
        """
        Copied
        """

        print(app)

        t = Transcription("test", "taste", Scoring("", 0))

        found = Transcription.transcriptions.find_one(
            {"_id": t.idef, "inputed": "test", "score": 0}
        )

        for f in found:
            print(f)

        assert found
