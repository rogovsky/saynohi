import json
import tempfile
import unittest
import configuration
import os

# test data
NOT_EXISTING_CONFIG_FILE = "not existing path to the file:?"
API_KEY = "api_key"
CLIENT_ID = "client_id"
CLIENT_SECRET = "client_secret"
TOKEN = "token"
TEST_CONFIG = {
    configuration.SLACK_PERSONAL_API_KEY: API_KEY,
    configuration.SLACK_CLIENT_ID: CLIENT_ID,
    configuration.SLACK_CLIENT_SECRET: CLIENT_SECRET,
    configuration.SLACK_VERIFICATION_TOKEN: TOKEN
}


class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.clean_env()
        configuration.load(NOT_EXISTING_CONFIG_FILE)

    @staticmethod
    def clean_env():
        try:
            for key in TEST_CONFIG.keys():
                del (os.environ[key])
        except KeyError:
            pass

    @staticmethod
    def put_config_to_env():
        for key, value in TEST_CONFIG.items():
            os.environ[key] = value

    @staticmethod
    def put_config_to_tempfile():
        f = tempfile.NamedTemporaryFile("w", delete=False)
        json.dump(TEST_CONFIG, f)
        f.close()
        return f

    def test_initial_values_are_empty(self):
        self.assertIsNone(configuration.slack_personal_api_key)
        self.assertIsNone(configuration.slack_client_id)
        self.assertIsNone(configuration.slack_client_secret)
        self.assertIsNone(configuration.slack_verification_token)

    def test_loads_from_env(self):
        self.put_config_to_env()

        configuration.load(NOT_EXISTING_CONFIG_FILE)

        self.assert_configuration_correct()

    def test_loads_from_file(self):
        f = self.put_config_to_tempfile()

        configuration.load(f.name)

        self.assert_configuration_correct()
        os.remove(f.name)

    def assert_configuration_correct(self):
        self.assertEqual(configuration.slack_personal_api_key, API_KEY)
        self.assertEqual(configuration.slack_client_id, CLIENT_ID)
        self.assertEqual(configuration.slack_client_secret, CLIENT_SECRET)
        self.assertEqual(configuration.slack_verification_token, TOKEN)
