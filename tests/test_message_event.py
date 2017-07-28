import unittest
from message_event import MessageEvent
from tests import data


class TestMessageEvent(unittest.TestCase):
    def test_json_detected(self):
        self.assertTrue(MessageEvent.is_message_event(data.standard_message_event_json))

    def test_wrong_json_not_detected(self):
        self.assertFalse(MessageEvent.is_message_event(data.valid_handshake_json))
        self.assertFalse(MessageEvent.is_message_event(data.bad_request_json))

    def test_message_edited_event_not_detected(self):
        self.assertFalse(MessageEvent.is_message_event(data.message_edited_event_json))

    def test_message_parsed(self):
        message = MessageEvent(data.standard_message_event_json)

        self.assertEqual(message.text, data.message_std)
        self.assertEqual(message.sender, data.sender_std)
