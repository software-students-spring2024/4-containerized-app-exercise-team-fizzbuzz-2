'''
    Tests for functions used in the webapp
'''

import pytest
from app import create_app

class Tests:
    '''
        Class for handling tests
    '''

    @pytest.fixture()
    def app(self):
        '''
            Creates an app
        '''
        app = create_app()
        app.config.update({
            "TESTING": True,
        })

        # other setup can go here

        yield app

        # clean up / reset resources here


    @pytest.fixture()
    def client(self, app):
        '''
            Copied
        '''
        return app.test_client()

    @pytest.fixture()
    def runner(self, app):
        '''
            Copied
        '''
        return app.test_cli_runner()

    def test_test(self):
        '''
            Copied
        '''
        assert True
