import time
from datetime import datetime
from datetime import timedelta
from threading import Thread

import slack_utils
from hi_detector import HiDetector
from message_event import MessageEvent, EventSubtype
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
        self._worker = None  # just a declaration

    def start_processing(self):
        self._worker = ProcessingThread(self, self._queue_manager)
        self._worker.setDaemon(True)
        self._worker.start()

    def process_incoming_event(self, event_json):
        """:param event_json: json representing slack message.im event"""
        if not MessageEvent.is_message_event(event_json):
            print("Got hidden event")
            return

        event = MessageEvent(event_json)
        ticket = Ticket.of_event(event)
        existing_event = self._queue_manager.get_item(ticket)
        if MessageProcessor._should_void_old_event(existing_event, event):
            print("Got message that voids existing one")
            self._queue_manager.void(ticket)
        elif MessageProcessor._should_add_new_event(event):
            print("Got HI message :", event.text)
            self._queue_manager.add(ticket, event)
        else:
            print("Got standard message :", event.text)

    @staticmethod
    def _should_void_old_event(existing_event, event):
        if not existing_event:  # nothing to void
            return False

        # any answer to HI message should void the ticket
        if existing_event.sender != event.sender:
            return True
        # any following non HI message from same user should void ticket as well
        if event.subtype == EventSubtype.MESSAGE \
                and not HiDetector.is_greeting(event.text):
            return True
        # if user changed message from Hi to normal one we should void ticket
        if event.subtype == EventSubtype.MESSAGE_CHANGED \
                and not HiDetector.is_greeting(event.text) \
                and HiDetector.is_greeting(event.previous_text):
            return True
        # if user deleted hi message we should void ticket
        if event.subtype == EventSubtype.MESSAGE_DELETED \
                and HiDetector.is_greeting(event.previous_text):
            return True

        return False

    @staticmethod
    def _should_add_new_event(event):
        # only add new incoming messages
        return event.subtype == EventSubtype.MESSAGE and HiDetector.is_greeting(event.text)

    def process_ticket(self, ticket):
        """Process ticket related to handled Hi message, if it's not voided sender should receive his punishment"""
        event = self._queue_manager.pop_item(ticket)
        if event:
            self._send_punishment_for_message(event)

    @staticmethod
    def _send_punishment_for_message(event):
        print("Send warning to %s for message'%s" % (event.text, str(event.time)))
        slack_utils.send_message(event.sender, "Hi! How do you like <http://www.nohello.com|that>?")
