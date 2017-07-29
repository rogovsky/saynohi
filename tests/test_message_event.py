import unittest
from message_event import MessageEvent, EventSubtype
from tests import data


class TestMessageEvent(unittest.TestCase):
    def test_new_message_detected(self):
        self.assertTrue(MessageEvent.is_message_event(data.standard_message_in_another_channel_event_json))

    def test_message_changed_detected(self):
        self.assertTrue(MessageEvent.is_message_event(data.message_changed_std_to_std_event_json))

    def test_message_deleted_detected(self):
        self.assertTrue(MessageEvent.is_message_event(data.message_deleted_hi_event_json))

    def test_wrong_json_not_detected(self):
        self.assertFalse(MessageEvent.is_message_event(data.valid_handshake_json))
        self.assertFalse(MessageEvent.is_message_event(data.bad_request_json))

    def test_new_message_parsed(self):
        message = MessageEvent(data.standard_message_in_another_channel_event_json)

        self.assertEqual(message.subtype, EventSubtype.MESSAGE)
        self.assertEqual(message.text, data.message_std)
        self.assertEqual(message.sender, data.sender_std)

    def test_message_changed_parsed(self):
        message = MessageEvent(data.message_changed_hi_to_std_event_json)

        self.assertEqual(message.subtype, EventSubtype.MESSAGE_CHANGED)
        self.assertEqual(message.text, data.message_std)
        self.assertEqual(message.previous_text, data.message_hi)
        self.assertEqual(message.sender, data.sender_hi)

    def test_message_deleted_parsed(self):
        message = MessageEvent(data.message_deleted_hi_event_json)

        self.assertEqual(message.subtype, EventSubtype.MESSAGE_DELETED)
        self.assertIsNone(message.text)
        self.assertEqual(message.previous_text, data.message_hi)
        self.assertEqual(message.sender, data.sender_hi)
