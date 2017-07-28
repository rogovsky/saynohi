import unittest

from datetime import datetime
from message_event import MessageEvent
from message_queue.queue_manager import QueueManager
from message_queue.ticket import Ticket
from tests import data


class TestQueueManager(unittest.TestCase):
    def setUp(self):
        self.message_event1 = MessageEvent(data.standard_message_event_json)
        self.message_event2 = MessageEvent(data.hi_message_event_json)
        self.queue_manager = QueueManager()
        self.ticket1 = Ticket.of_event(self.message_event1)
        self.queue_manager.add(self.ticket1, self.message_event1)
        self.ticket2 = Ticket.of_event(self.message_event2)
        self.queue_manager.add(self.ticket2, self.message_event2)

    def test_add_get_ticket_works(self):
        ticket1 = self.queue_manager.get_next_ticket()
        ticket2 = self.queue_manager.get_next_ticket()

        self.assertEqual(ticket1, self.ticket1)
        self.assertEqual(ticket2, self.ticket2)

    def test_fetching_works(self):
        event2 = self.queue_manager.pop_item(self.ticket2)
        event1 = self.queue_manager.pop_item(self.ticket1)

        self.assertEqual(self.message_event1, event1)
        self.assertEqual(self.message_event2, event2)

    def test_fetching_clears_data(self):
        event1 = self.queue_manager.pop_item(self.ticket1)
        no_event = self.queue_manager.pop_item(self.ticket1)

        self.assertIsNotNone(event1)
        self.assertIsNone(no_event)

    def test_voiding_works(self):
        self.queue_manager.void(self.ticket1)
        no_event = self.queue_manager.pop_item(self.ticket1)

        self.assertIsNone(no_event)

    def test_voiding_not_cause_errors(self):
        # void twice
        self.queue_manager.void(self.ticket1)
        self.queue_manager.void(self.ticket1)
        # void something that doesn't exist
        self.queue_manager.void(Ticket("random_key", datetime.fromtimestamp(0)))

    def test_event_with_same_ticket_replaces_old_one(self):
        self.queue_manager.add(self.ticket1, self.message_event2)  # same ticket and new message
        event2 = self.queue_manager.pop_item(self.ticket1)

        self.assertEqual(self.message_event2, event2)

    def test_get_not_cause_error(self):
        self.queue_manager.pop_item(self.ticket1)
        no_event = self.queue_manager.get_item(self.ticket1)

        self.assertIsNone(no_event)
