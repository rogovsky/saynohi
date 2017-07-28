import unittest
from unittest import mock

from message_processor import MessageProcessor
from tests import data


class TestMessageProcessor(unittest.TestCase):
    @mock.patch("message_queue.queue_manager.QueueManager.add")
    def test_incoming_message_added_to_processing(self, add_event_mock_method):
        processor = MessageProcessor()
        processor.process_event(data.hi_message_event_json)

        add_event_mock_method.assert_called_once_with(mock.ANY, mock.ANY)
