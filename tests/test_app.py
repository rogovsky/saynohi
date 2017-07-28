from httplib2 import Response

import unittest
import app
from tests import data


class TestApp(unittest.TestCase):

    def test_handshake_req_parsing(self):
        response = app.process_handshake_request(data.valid_handshake_json)

        self.assertIsNotNone(response)
        self.assertTrue(app.EVENT_API_FIELD_CHALLENGE in response)

    def test_message_req_parsing(self):
        response = app.process_event_request(data.standard_message_event_json)

        self.assertIsNotNone(response)

    def test_malformed_req_parsing(self):
        with app.app.app_context():
            response = app.process_event_api_request(data.bad_request_json)

        self.assertEqual(response.status_code, 400)

    def test_auth_response_parsing(self):
        app.parse_auth_response(Response({"status": 200}), data.valid_auth_response)

if __name__ == "__main__":
    unittest.main()
