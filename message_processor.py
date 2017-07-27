from queue import Full
from queue import Queue

from datetime import datetime
from datetime import timedelta

import time

import slack_utils
from hi_detector import HiDetector
from message_event import MessageEvent
from threading import Timer
from threading import Thread

TOLERANCE_PERIOD = timedelta(seconds=30)


class Ticket:
    def __init__(self, key, time_to_process):
        self.key = key
        self.event_time = time_to_process


class ProcessingThread(Thread):
    def __init__(self, processor):
        super().__init__()
        self._processor = processor

    def run(self):
        while True:
            pass
            ticket = self._processor._tickets.get()
            time_since_event = datetime.now() - ticket.event_time
            if time_since_event < TOLERANCE_PERIOD:
                delay = TOLERANCE_PERIOD - time_since_event
                time.sleep(delay.seconds)

            self._processor.proceed_with_ticket(ticket)

class MessageProcessor:
    """Process incoming message events and schedule response if required"""

    def __init__(self):
        self._tickets = Queue()
        """Queue of channels where hi message was detected"""
        self._events_map = {}
        """Contains all Hi events that need to be processed, events may be voided and removed from this map
         by appropriate message in same channel during the tolerance interval"""
        self._processor = None  # just a declaration

    def start_processing(self):
        self._processor = ProcessingThread(self)
        self._processor.start()

    def process(self, event_json):
        """@:param message_event json representing slack message.im event"""
        if not MessageEvent.is_message_event(event_json):
            return

        event = MessageEvent(event_json)
        if event.is_incoming:
            print("Got incoming message :", event.text)
            if HiDetector.is_greeting(event.text):
                self._add_event_to_queue(event)

    def _add_event_to_queue(self, event):
        try:
            key = self._create_event_key(event)
            self._tickets.put_nowait(Ticket(key, event.time))
            self._events_map[key] = event
            print("Added to processing :", event.text, str(event.time))
        except Full:
            print("Failed to add event. Queue is full")

    def proceed_with_ticket(self, ticket):
        event = self._events_map[ticket.key]
        if event:
            self.send_punishment_for_message(event)

    def send_punishment_for_message(self, event):
        print("Send warning to %s for message'%s" % (event.text, str(event.time)))
        slack_utils.send_message(event.sender, "Hi! How do you like <http://www.nohello.com|that>?")

    @staticmethod
    def _create_event_key(event):
        return event.channel + "_" + event.sender
