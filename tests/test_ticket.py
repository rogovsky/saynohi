import unittest

from message_event import MessageEvent
from message_queue.ticket import Ticket
from tests import data


class TestTicekt(unittest.TestCase):
    def test_can_parse_message_event(self):
        ticket = Ticket.of_event(MessageEvent(data.standard_message_in_another_channel_event_json))

        self.assertIsNotNone(ticket)
