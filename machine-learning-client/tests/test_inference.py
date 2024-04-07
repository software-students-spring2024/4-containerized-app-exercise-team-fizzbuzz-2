"""
test_inference.py: test

This module tests the inference module.

Author: Firas Darwish
"""

import pytest
from inference import test_test


class Tests:
    """Class defines tests"""

    @pytest.fixture
    def test_fixture(self):
        """
        sample test with pytest.fixture
        """
        print(1)

    def test_test_test(self):
        """
        test to test if pytest tests properly
        """
        assert test_test() is True

    def test_to_make_pylint_happy(self):
        """
        pylint wants two public methods here, I oblige
        """
        print(1)
