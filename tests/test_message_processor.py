import unittest
from unittest import mock
from unittest.mock import MagicMock

from message_processor import MessageProcessor
from tests import data


class TestMessageProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = MessageProcessor()

    @mock.patch("message_queue.queue_manager.QueueManager.add")
    def test_incoming_message_added_to_processing(self, queue_add_mock):
        self.processor.process_incoming_event(data.thread_hi_message_json)

        queue_add_mock.assert_called_once_with(mock.ANY, mock.ANY)

    def test_second_hi_doesnt_void_old_one(self):
        # add one real message then mock the receiver
        self.processor.process_incoming_event(data.thread_hi_message_json)
        self.processor._queue_manager.add = MagicMock()
        self.processor._queue_manager.void = MagicMock()
        # add the same
        self.processor.process_incoming_event(data.thread_hi_message_json)
        # and see what happens
        self.processor._queue_manager.add.assert_called_once_with(mock.ANY, mock.ANY)
        self.processor._queue_manager.void.assert_not_called()

    def test_standard_answer_to_hi_voids_it(self):
        # add one real message then mock the receiver
        self.processor.process_incoming_event(data.thread_hi_message_json)
        self.processor._queue_manager.add = MagicMock()
        self.processor._queue_manager.void = MagicMock()
        # add answer to it
        self.processor.process_incoming_event(data.thread_answer_message_json)
        # check
        self.processor._queue_manager.add.assert_not_called()
        self.processor._queue_manager.void.assert_called_once_with(mock.ANY)

    def test_new_message_from_same_user_voids_old_one(self):
        # add one real message then mock the receiver
        self.processor.process_incoming_event(data.thread_hi_message_json)
        self.processor._queue_manager.add = MagicMock()
        self.processor._queue_manager.void = MagicMock()
        # add answer to it
        self.processor.process_incoming_event(data.thread_following_message_json)
        # check
        self.processor._queue_manager.add.assert_not_called()
        self.processor._queue_manager.void.assert_called_once_with(mock.ANY)

    def test_hi_answer_to_hi_voids_it(self):
        # add one real message then mock the receiver
        self.processor.process_incoming_event(data.thread_hi_message_json)
        self.processor._queue_manager.add = MagicMock()
        self.processor._queue_manager.void = MagicMock()
        # add answer to it
        self.processor.process_incoming_event(data.thread_answer_hi_message_json)
        # check
        self.processor._queue_manager.add.assert_not_called()
        self.processor._queue_manager.void.assert_called_once_with(mock.ANY)
