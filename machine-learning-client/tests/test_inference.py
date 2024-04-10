"""
test_inference.py: test

This module tests the inference module.

Author: Firas Darwish
"""

import json
import pytest
from datasets import load_dataset
from inference import speech2textpipeline
from app import create_app

class Tests:
    """Class defines tests"""

    @pytest.fixture
    def test_fixture(self):
        """
        sample test with pytest.fixture
        """
        print(1)

    def test_inference(self):
        """
        test whether speech2text returns proper string
        """
        ds = load_dataset(
            "hf-internal-testing/librispeech_asr_demo", "clean", split="validation"
        )
        returned = speech2textpipeline(ds[0]["audio"]["array"])
        assert returned == [
            "mister quilter is the apostle of the middle classes and we are glad to welcome his gospel"
        ]

    # test with non input
    def test_none_input(self):
        """
        test when speech2text does not receive proper string
        """
        transcription = speech2textpipeline()
        assert transcription is None

    # Test with None input
    def test_none_input(self):
        """
        test when speech2text does not receive proper string
        """
        transcription = speech2textpipeline()
        assert transcription is None

    # def test_api(self):
    #     """
    #     tests whether api works at creating app
    #     """
    #     flask_a = create_app()

    #     # Create a test client using the Flask application configured for testing
    #     with flask_a.test_client() as test_client:
    #         response = test_client.get("/test")
    #         assert response.status_code == 200

    #         # Check if the response content type is JSON
    #         print(response.content_type)
    #         assert response.content_type == "application/json"
    #         # Check if the response contains the expected key
    #         data = json.loads(response.data.decode("utf-8"))
    #         assert "transcription" in data

