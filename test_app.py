import app
import json
import unittest


class TestApp(unittest.TestCase):
    bad_request = '{"some_tag": 0}'

    valid_handshake_json = json.loads('{\
            "token": "Jhj5dZrVaK7ZwHHjRyZWjbDl",\
            "challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P",\
            "type": "url_verification"\
        }')

    valid_message_event_json = json.loads('{\
            "token": "Qw671KoWqDm3iv2ok3leR9Ko",\
            "team_id": "T03G61VPV",\
            "api_app_id": "A69BQ5S2Z",\
            "event": {\
                "type": "message",\
                "user": "USLACKBOT",\
                "text": "I searched for that on our Help Center. Perhaps this article will help: <https://get.slack.help/hc/en-us/articles/216951758-Customize-your-team-s-call-settings|Customize your team call settings>",\
                "ts": "1500183396.097119",\
                "channel": "D03GALK0C",\
                "event_ts": "1500183396.097119"\
            },\
            "type": "event_callback",\
            "authed_users": [\
                "U03GALK02"\
            ],\
            "event_id": "Ev69GLSSGM",\
            "event_time": 1500183396\
        }')

    def test_handshake_req_parsing(self):
        response = app.process_handshake_request(self.valid_handshake_json)

        self.assertIsNotNone(response)
        self.assertTrue(app.FIELD_CHALLENGE in response)

    def test_message_req_parsing(self):
        response = app.process_event_request(self.valid_message_event_json)

        self.assertIsNotNone(response)

    def test_malformed_req_parsing(self):
        with app.app.app_context():
            response = app.process_event_api_request(self.bad_request)

        self.assertEquals(response.status_code, 500)


if __name__ == "__main__":
    unittest.main()
