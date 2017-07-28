import time
from datetime import datetime
from datetime import timedelta
from threading import Thread

import slack_utils
from hi_detector import HiDetector
from message_event import MessageEvent
from message_queue.queue_manager import QueueManager
from message_queue.ticket import Ticket

TOLERANCE_PERIOD = timedelta(seconds=30)


class ProcessingThread(Thread):
    """Takes tickets from queue and waits to execute at right time.
    Takes items one by one and sleeps if it's not yet the time to proceed the ticket and then let MessageProcessor
    do the rest."""
    def __init__(self, processor, queue_manager):
        super().__init__()
        self._processor = processor
        self._queue_manager = queue_manager

    def run(self):
        while True:
            ticket = self._queue_manager.get_next_ticket()
            self._sleep_till_time_to_proceed(ticket)
            self._processor.process_ticket(ticket)

    @staticmethod
    def _sleep_till_time_to_proceed(ticket):
        time_since_event = datetime.now() - ticket.event_time
        if time_since_event < TOLERANCE_PERIOD:
            delay = TOLERANCE_PERIOD - time_since_event
            time.sleep(delay.seconds)


class MessageProcessor:
    """Process incoming message events and schedule response if required"""

    def __init__(self):
        self._queue_manager = QueueManager()
        self._processor = None  # just a declaration

    def start_processing(self):
        self._processor = ProcessingThread(self, self._queue_manager)
        self._processor.start()

    def process_incoming_event(self, event_json):
        """:param event_json: json representing slack message.im event"""
        if not MessageEvent.is_message_event(event_json):
            print("Got hidden event")
            return

        event = MessageEvent(event_json)
        ticket = Ticket.of_event(event)
        existing_event = self._queue_manager.get_item(ticket)
        if existing_event and \
                (existing_event.sender != event.sender or not HiDetector.is_greeting(event.text)):
            print("Got message that voids existing one")
            # Any answer to HI message should void the ticket
            # any following non HI message from same user should void ticket as well
            self._queue_manager.void(ticket)
        elif HiDetector.is_greeting(event.text):
            print("Got HI message :", event.text)
            self._queue_manager.add(ticket, event)
        else:
            print("Got standard message :", event.text)

    def process_ticket(self, ticket):
        """Process ticket related to handled Hi message, if it's not voided sender should receive his punishment"""
        event = self._queue_manager.pop_item(ticket)
        if event:
            self._send_punishment_for_message(event)

    @staticmethod
    def _send_punishment_for_message(event):
        print("Send warning to %s for message'%s" % (event.text, str(event.time)))
        slack_utils.send_message(event.sender, "Hi! How do you like <http://www.nohello.com|that>?")
